from app.helpers.db import connect_db

def init_db():
    with connect_db() as client:
        client.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL
        );
        """)

 
        client.execute("""
        CREATE TABLE IF NOT EXISTS VEHICLES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_of_vehicle TEXT NOT NULL,
            year_of_vehicle INTEGER NOT NULL,
            MAKE TEXT NOT NULL
        );
        """)

       
        client.execute("""
        CREATE TABLE IF NOT EXISTS INFO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL REFERENCES VEHICLES(id),
            action_taken TEXT,
            details TEXT NOT NULL,
            date INTEGER NOT NULL,
            odometer_kms INTEGER NOT NULL
        );
        """)

        

    print("Database initialized. USERS, VEHICLES, INFO tables are ready.")

if __name__ == "__main__":
    init_db()
