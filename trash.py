import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("student.db")

# Read the data from the student table into a DataFrame
df = pd.read_sql_query('SELECT * FROM student', conn)

# Print the DataFrame
print(df)

# Close the connection
conn.close()
