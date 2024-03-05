import pandas as pd
import mysql.connector

def connectSQL(username, passkey):
    # Read data
    data = pd.read_csv('hindalco.csv')

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user=username,
        password=passkey,
        database='hindalco'
    )

    # Create a cursor to perform operations
    cursor = conn.cursor()

    # Insert data into database
    for index, row in data.iterrows():
        sql = "INSERT INTO financial_data (datetime, instrument, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (row['datetime'], row['instrument'], row['open'], row['high'], row['low'], row['close'], row['volume'])

        cursor.execute(sql, val)

    # Commit changes
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


#__main__
username = input("Enter MySQL username: ")
passkey = input("Enter password for " + username + ": ")
connectSQL(username, passkey);
