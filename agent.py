import datetime

from calender_utils import get_free_slots, book_event

class BookingAgent:
    def extract_date(self, message):
        if "tomorrow" in message:
            return datetime.date.today() + datetime.timedelta(days=1)
        elif "next week" in message:
            return datetime.date.today() + datetime.timedelta(days=7)
        elif "friday" in message:
            today = datetime.date.today()
            offset = (4 - today.weekday()) % 7
            return today + datetime.timedelta(days=offset)
        return datetime.date.today()

    def handle(self, message):
        date = self.extract_date(message)
        slots = get_free_slots(date)

        if not slots:
            return f"No available slots for {date.strftime('%Y-%m-%d')}."

        time = slots[0]  # pick first slot
        confirmation = book_event(date, time)
        return confirmation

agent = BookingAgent()
