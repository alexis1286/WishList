import pandas as pd
import sqlite3

# Load the spreadsheet into a DataFrame
file_path = 'D:\My Stuff\X mas List script\Alexis_christmas_list.csv'  # Adjust this path if needed
spreadsheet_data = pd.read_csv(file_path)

# Initialize SQLite database
db_path = 'christmas_list.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table for items if it doesn't exist
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

# Insert data into the database
for _, row in spreadsheet_data.iterrows():
    cursor.execute('''
    INSERT INTO items (priority, category, name, link, price, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['Priority'], row['Category'], row['Name'], row['Link'], row['Price'], row.get('Notes', None)))

# Commit the changes and close the connection
conn.commit()

# Confirm the data was inserted by fetching a few entries
cursor.execute('SELECT * FROM items LIMIT 5')
db_preview = cursor.fetchall()

# Close the database connection
conn.close()

# Print out a preview of the data to confirm
print("Database import complete. Preview of the first 5 entries:")
for row in db_preview:
    print(row)
