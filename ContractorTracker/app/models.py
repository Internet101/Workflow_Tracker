# Database setup and models
import sqlite3

# Path to your SQLite database file
DB_PATH = 'contractor_tracker.db'

def init_db():
    """Initialize the database with the required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create Contracts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_description TEXT,
            rate REAL,
            start_date DATE,
            end_date DATE,
            jobs_completed INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Create Revenue table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            contract_id INTEGER,
            amount REAL,
            date DATE,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(contract_id) REFERENCES contracts(id)
        )
    ''')

    conn.commit()
    conn.close()

    print("Database initialized successfully!")

