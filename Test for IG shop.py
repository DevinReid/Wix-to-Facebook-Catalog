import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\Dreid\Downloads\catalog_products.csv")

# Create a connection to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect(r"C:\Users\Dreid\Downloads\catalog_products.db")

# Save the DataFrame to the SQLite database
df.to_sql('products', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Data saved to catalog_products.db")