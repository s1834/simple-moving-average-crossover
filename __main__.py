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

def calculateSMA(username, passkey, days):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
        host='localhost',
        user=username,
        password=passkey,
        database='hindalco'
        )

        # Get close and dates
        sql = "SELECT close, datetime FROM financial_data;"
        result = pd.read_sql(sql, conn)
        npResult = result['close'].to_numpy()
        npDates = result['datetime'].to_numpy()
        
        # iterate and get sma and corresponding dates
        ans1 = []
        dates1 = []
        for i in range(0, npResult.size - days[0] + 1, 1):
            sum = 0
            for j in range(i,i + days[0], 1):
                sum += npResult[j]
            ans1.append(sum / days[0])
            dates1.append(npDates[i + days[0] // 2])
        ans1 = np.array(ans1)

        ans2 = []
        dates2 = []
        for i in range(0, npResult.size - days[1] + 1, 1):
            sum = 0
            for j in range(i,i + days[1], 1):
                sum += npResult[j]
            ans2.append(sum / days[1])
            dates2.append(npDates[i + days[0] // 2])

        # convert to numpy array for easy manipulation
        ans2 = np.array(ans2)
        dates1 = np.array(dates1)
        dates2 = np.array(dates2)
        conn.close()
        return dates1, dates2, ans1, ans2, npResult, npDates
    # Handle Errors
    except Exception as e:
        conn.close()
        print(str(e))


# Plot the SMA's
def plot(dates1, dates2, sma1, sma2, close, allDates):
    plt.plot(allDates, close, label="Closing Price")
    plt.plot(dates1, sma1, label='SMA1')
    plt.plot(dates2, sma2, label='SMA2')
    plt.xlabel('Date')
    plt.ylabel('Moving Average')
    plt.legend()
    plt.show()

#__main__
# Get MySql Username, and password
username = input("Enter MySQL username: ")
passkey = input("Enter password for " + username + ": ")
connectSQL(username, passkey)

days = [10, 200]
# Get SMA from user
for i in range(len(days)):
    days[i] = int(input("Enter SMA" + str(i + 1) + ": "))
    
dates1, dates2, sma1, sma2, close, allDates = calculateSMA(username, passkey,days)
plot(dates1, dates2, sma1, sma2, close, allDates)