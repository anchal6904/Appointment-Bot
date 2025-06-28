from fastapi import FastAPI, Request
from agent import agent
from calender_utils import get_free_slots, book_event

# main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("message")
    prompt_lower = prompt.lower()

    # --- Step 1: Natural language to datetime conversion ---
    from dateparser import parse
    import re
    import datetime

    parsed = parse(prompt, settings={'PREFER_DATES_FROM': 'future'})
    if parsed:
        requested_date = parsed.date()
        requested_time = parsed.time()
    else:
        requested_date = None
        requested_time = None
        # Try to extract a date-like substring and parse it
        date_match = re.search(r'\b(\d{4}-\d{2}-\d{2}|\d{1,2} \w+ \d{4}|\w+ \d{1,2}, \d{4})\b', prompt)
        if date_match:
            parsed = parse(date_match.group(0))
            if parsed:
                requested_date = parsed.date()

    # Fallback for common keywords and weekdays if dateparser fails
    if not requested_date:
        today = datetime.date.today()
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        if "today" in prompt_lower:
            requested_date = today
        elif "tomorrow" in prompt_lower:
            requested_date = today + datetime.timedelta(days=1)
        elif "day after tomorrow" in prompt_lower:
            requested_date = today + datetime.timedelta(days=2)
        elif "next week" in prompt_lower:
            requested_date = today + datetime.timedelta(days=7)
        else:
            for i, day in enumerate(weekdays):
                if day in prompt_lower:
                    offset = (i - today.weekday()) % 7
                    requested_date = today + datetime.timedelta(days=offset)
                    break

    # Fallback for time using regex if dateparser fails
    if not requested_time:
        match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', prompt_lower)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            ampm = match.group(3)
            if ampm == 'pm' and hour != 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            # Only create time if hour and minute are valid
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                requested_time = datetime.time(hour, minute)
            else:
                requested_time = None
    # Handle 'afternoon', 'morning', 'evening' keywords
    if not requested_time:
        if "afternoon" in prompt_lower:
            requested_time = datetime.time(15, 0)  # 3pm
        elif "morning" in prompt_lower:
            requested_time = datetime.time(10, 0)  # 10am
        elif "evening" in prompt_lower:
            requested_time = datetime.time(17, 0)  # 5pm

    # Always define free_slots after all date parsing
    if requested_date:
        free_slots = get_free_slots(requested_date)
    else:
        free_slots = []

    print("Prompt:", prompt)
    print("Parsed date:", requested_date)
    print("Parsed time:", requested_time)
    print("Free slots:", free_slots)

    # --- Step 3: Respond accordingly ---
    if not free_slots:
        return {"response": f"No available slots for {requested_date or 'the requested day'}."}

    if requested_time:
        requested_time_str = requested_time.strftime('%H:%M')
        print("Requested time string:", requested_time_str)
        print("Available slots:", free_slots)
        if requested_time_str in free_slots:
            book_event(requested_date, requested_time_str)
            return {"response": f"Confirmed: Meeting with Anchal at {requested_time_str} on {requested_date}"}
        else:
            return {"response": f"Requested time {requested_time_str} not available on {requested_date}"}
    else:
        # Suggest first available slot
        slot = free_slots[0]
        book_event(requested_date, slot)
        return {"response": f"Confirmed: Meeting with Anchal at {slot} on {requested_date}"}
