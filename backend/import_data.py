import pandas as pd
import sqlite3

# Load your CSV file
csv_file_path = 'Alexis_christmas_list.csv'  # Change this if the file name or path is different

# Read CSV into a DataFrame
data = pd.read_csv(csv_file_path)

# Connect to SQLite database (or create it if it doesn't exist)
db_path = 'christmas_list.db'  # Output database file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for items if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    priority INTEGER,
    category TEXT,
    name TEXT,
    link TEXT,
    price TEXT,
    notes TEXT
)
''')

# Insert each row of data into the database
for _, row in data.iterrows():
    cursor.execute('''
    INSERT INTO items (priority, category, name, link, price, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['Priority'], row['Category'], row['Name'], row['Link'], row['Price'], row.get('Notes', None)))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Database created and data imported successfully.")
