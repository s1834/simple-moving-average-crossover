import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt

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

def calculateSMA(days, username, passkey):
    try:
        conn = mysql.connector.connect(
        host='localhost',
        user=username,
        password=passkey,
        database='hindalco'
        )
        sql = "SELECT close FROM financial_data;"
        result = pd.read_sql(sql, conn)
        npResult = result['close'].to_numpy()
        
        ans1 = []
        for i in range(0, npResult.size - days[0] + 1, 1):
            sum = 0
            for j in range(i,i + days[0], 1):
                sum += npResult[j]
            ans1.append(sum / days[0])
        ans1 = np.array(ans1)

        ans2 = []
        for i in range(0, npResult.size - days[1] + 1, 1):
            sum = 0
            for j in range(i,i + days[1], 1):
                sum += npResult[j]
            ans2.append(sum / days[1])
        ans2 = np.array(ans2)
        return ans1, ans2
        conn.close()
    except Exception as e:
        conn.close()
        print(str(e))


# #__main__
# username = input("Enter MySQL username: ")
# passkey = input("Enter password for " + username + ": ")
username = "root"
passkey = "shubh1234"
# connectSQL(username, passkey)
days = [50,100]
sma1, sma2 = calculateSMA(days, username, passkey)
print(sma1, sma2)
