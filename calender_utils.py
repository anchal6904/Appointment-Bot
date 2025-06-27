import datetime
import sqlite3

DB_PATH = 'calendar.db'
default_slots = [f"{hour:02d}:00" for hour in range(9, 19)]  # 09:00 to 18:00

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_free_slots(date):
    date_str = date.strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time FROM bookings WHERE date = ?", (date_str,))
    booked_times = [row[0] for row in c.fetchall()]
    conn.close()
    available = [t for t in default_slots if t not in booked_times]
    return available

def book_event(date, time, name="Meeting with Anchal"):
    date_str = date.strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO bookings (date, time, name) VALUES (?, ?, ?)", (date_str, time, name))
    conn.commit()
    conn.close()
    return f"Confirmed: {name} at {time} on {date_str}"

def clear_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM bookings")
    conn.commit()
    conn.close()