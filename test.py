import mysql.connector
import random
from mysql.connector import Error

try:
    # Database connection parameters
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="dhruvp@70441",
        database="mydata"
    )

    if conn.is_connected():
        print("Connected to MySQL database")

        cursor = conn.cursor()

        # List of tablet names to process
        tabletnames=['Crocin', 'Azithromycin 500mg', 'Digene', 'Paracetamol', 'Allegra', 'Becosules', 'Ibuprofen', 'Cetirizine', 'Rantac', 'Insulin Glargine', 'Neosporin', 'Refresh Tears', 'Aspirin', 'Clarithromycin', 'Pepto-Bismol', 'Tylenol', 'Vitamin D', 'Covid Vaccine', 'Amlodipine', 'Metformin', 'Losartan', 'Epinephrine', 'Hydrocortisone', 'Visine', 'Ibuprofen', 'Paracetamol', 'Mylanta', 'Advil', 'Fish Oil', 'Flu Vaccine', 'Lisinopril', 'Simvastatin', 'Omeprazole', 'Vitamin B12', 'Benadryl', 'Systane', 'Naproxen', 'Amoxicillin', 'Pepto-Bismol', 'Aleve', 'Vitamin C', 'Shingles Vaccine', 'Atenolol']

        for mname in tabletnames:
            # Retrieve dosage and rate for the current tablet name
            cursor.execute("SELECT dosage, price FROM my_pharma WHERE tabletname = %s", (mname,))
            results = cursor.fetchall()
            if results:
                for result in results:
                    dosage, rate = result
                    qt = random.randint(1,15)
                    amnt = int(qt * int(rate))
                    # Update the sales table with the retrieved dosage and rate
                    cursor.execute(
                        "UPDATE sales SET Dose = %s, Rate = %s, Quantity = %s, Amount = %s WHERE tabletname = %s",
                        (dosage, rate,qt, amnt , mname)
                    )
                    conn.commit()  # Commit the transaction

except Error as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
        print("MySQL connection is closed")
