from app.helpers.db import connect_db

def init_db():
    with connect_db() as client:
        # Users table
        client.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            
        );
        """)

        # Vehicles table
        client.execute("""
        CREATE TABLE IF NOT EXISTS VEHICLES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
           
            
            
        );
        """)

        # Maintenance info table
        client.execute("""
        CREATE TABLE IF NOT EXISTS INFO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL REFERENCES VEHICLES(id),
            action_taken TEXT,
            details TEXT, NOT NULL
            date INTEGER, NOT NULL          
            odometer_kms INTEGER, NOT NULL
        );
        """)

    print("Database initialized with USERS, VEHICLES, INFO tables.")

if __name__ == "__main__":
    init_db()
