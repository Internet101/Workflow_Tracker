import sqlite3


# Path to your SQLite database
DB_PATH = 'contractor_tracker.db'

with sqlite3.connect(DB_PATH) as conn:
    conn.execute('PRAGMA journal_mode=WAL;')


# SQL command to create the contracts table
CREATE_CONTRACTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    description TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    location TEXT,
    job_pack_path TEXT
);
"""

# Connect to the database and create the table
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute(CREATE_CONTRACTS_TABLE_SQL)
    conn.commit()

print("Contracts table created successfully!")
