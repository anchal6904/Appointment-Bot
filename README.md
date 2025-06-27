# AI Appointment Booking Agent

This project is a conversational AI agent that helps users book appointments via a chat interface. It supports natural language input, flexible date and time parsing, and persistent storage using SQLite.

## Features
- Book appointments using natural language (e.g., "Book a meeting tomorrow at 2pm", "Book a meeting on 2025-07-02 at 9am").
- Handles keywords like "today", "tomorrow", "next week", weekdays, and time ranges (e.g., "between 3pm and 5pm").
- Suggests or books available slots based on your request.
- Stores bookings in a local SQLite database (`calendar.db`).
- Simple admin script to clear all bookings.

## Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite
- **Date Parsing:** dateparser

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## How to Run

### 1. Start the Backend (FastAPI)
```bash
python -m uvicorn main:app --reload
```
The backend will run at `http://localhost:8000`.

### 2. Start the Frontend (Streamlit)
```bash
python -m streamlit run ui.py
```
The chat UI will open in your browser.

## Booking Examples
- `Book a meeting tomorrow at 10am`
- `Book a meeting on 2025-07-02 at 9am`
- `Book a meeting between 3pm and 5pm next week`
- `Do you have any free time this Friday?`
- `Hey, I want to schedule a call for tomorrow afternoon.`

## Clearing All Bookings
To delete all bookings from the database, run:
```bash
python clear_bookings.py
```

## Customizing Available Slots
Edit `default_slots` in `calender_utils.py` to change the available times (default: every hour from 09:00 to 18:00).

## Notes
- The agent uses in-memory and SQLite logic for demonstration. No external calendar integration is included.
- For production, add authentication and more robust error handling.

---
Feel free to extend this project with more features or integrate with real calendar APIs! 