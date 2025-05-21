import sqlite3

# Set the path where your database file should be saved
DB_PATH = "fraud_detection.db"


# Connect and create table
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the fraud_data table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fraud_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT NOT NULL,
        type TEXT NOT NULL,  -- 'phone' or 'otp'
        flagged INTEGER DEFAULT 0
    );
''')

conn.commit()
conn.close()

print("Database and table created successfully.")
