import sqlite3
from contextlib import contextmanager

DB_FILE = r"C:\Users\thewm\OneDrive\Documents\databases\maintenance.tracker.sqlite"

@contextmanager
def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()