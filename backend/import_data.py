import pandas as pd
import sqlite3

# Load CSV data
file_path = 'Alexis_christmas_list.csv'
christmas_list_df = pd.read_csv(file_path)

# Connect to SQLite database (or create it if it doesn’t exist)
conn = sqlite3.connect('christmas_list.db')
cursor = conn.cursor()

# Create a table for the Christmas list
create_table_query = '''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Priority INTEGER,
    Category TEXT,
    Item TEXT,
    Link TEXT,
    Price TEXT,
    Image TEXT,
    Notes TEXT,
    BlackFridayDeals TEXT
);
'''
cursor.execute(create_table_query)

# Insert data into the database
for _, row in christmas_list_df.iterrows():
    insert_query = '''
    INSERT INTO items (Priority, Category, Item, Link, Price, Image, Notes, BlackFridayDeals)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.execute(insert_query, (
        row['Priority'],
        row['Category'],
        row['Item'],
        row['Link'],
        row['Price'],
        row['Image'],
        row['Notes'],
        row['Black Friday Deals']
    ))

# Commit and close the connection
conn.commit()
conn.close()
