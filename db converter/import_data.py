import pandas as pd
import sqlite3

# Load CSV data
file_path = 'Alexis_christmas_list.csv'
christmas_list_df = pd.read_csv(file_path)

# Drop unnecessary columns (if needed)
christmas_list_df = christmas_list_df.drop(columns=['Unnamed: 0', 'Unnamed: 8'], errors='ignore')

# Connect to SQLite database (or create it if it doesn’t exist)
conn = sqlite3.connect('christmas_list.db')
cursor = conn.cursor()

# Drop the table if it exists (to avoid conflicts with an outdated schema)
cursor.execute("DROP TABLE IF EXISTS items;")

# Create a table for the Christmas list with the correct schema
create_table_query = '''
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    csv_order INTEGER,
    Priority INTEGER,
    Category TEXT,
    Item TEXT,
    Link TEXT,
    Price TEXT,
    Image TEXT
);
'''
cursor.execute(create_table_query)

# Insert data into the database
for _, row in christmas_list_df.iterrows():
    insert_query = '''
    INSERT INTO items (csv_order, Priority, Category, Item, Link, Price, Image)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.execute(insert_query, (
        row['csv_order'],
        row['Priority'],
        row['Category'],
        row['Item'],
        row['Link'],
        row['Price'],
        row['Image']
    ))

# Commit and close the connection
conn.commit()
conn.close()
