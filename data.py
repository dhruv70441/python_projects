import mysql.connector
import random

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="dhruvp@70441",
    database="mydata"
)

# Cursor object to execute SQL queries
cursor = mydb.cursor()

# Step 1: Retrieve all values from the tabletname column of the my_pharma table and store them in a list
cursor.execute("SELECT tabletname FROM my_pharma")
tablet_names = [row[0] for row in cursor.fetchall()]
print(tablet_names)