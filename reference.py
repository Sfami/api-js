from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data into a dataframe
# symbol = yf.Ticker('BTC-USD')
# df_btc = symbol.history(interval="1d",period="max")

# # Filter the data by date
# df_btc = df_btc[df_btc.index > datetime(2020,1,1)]
# df_btc = df_btc[df_btc.index < datetime(2021,9,1)]

# # Print the result
# print(df_btc)

# # Delete unnecessary columns
# del df_btc["Dividends"]
# del df_btc["Stock Splits"]



# Load the data into a dataframe
data = pd.read_csv("data.csv")
print(data.columns)
columns = ["Time Serie", 'NEW ZEALAND - NEW ZELAND DOLLAR/US$']
data = data[columns]

data.dropna(inplace=True)
    
data["Date"] = pd.to_datetime(data[columns[0]], infer_datetime_format=True) 
data["ZAR"] = data[columns[1]]
# data["Price"] = data["Price"].apply(lambda x: 0 if x == "ND",)

data["ZAR"] = data['ZAR'].map(lambda x: float(0) if x =='ND' else float(x))

print(data['ZAR'].head())

print(data['ZAR'].dtype)
data = data.drop(columns, axis=1)
data.set_index("ZAR")

# Filter the data by date
# data = data[data.Date > datetime(1995,1,1)]
# data = data[data.Date < datetime(2005,9,1)]
print(len(data))

# change = df_btc["Close"].diff()
change = data["ZAR"].diff()
change.dropna(inplace=True)


# Create two copies of the Closing price Series
change_up = change.copy()
change_down = change.copy()

# 
change_up[change_up<0] = 0
change_down[change_down>0] = 0

# Verify that we did not make any mistakes
change.equals(change_up+change_down)

# Calculate the rolling average of average up and average down
avg_up = change_up.rolling(14).mean()
avg_down = change_down.rolling(14).mean().abs()



rsi = 100 * avg_up / (avg_up + avg_down)

# Take a look at the 20 oldest datapoints
print(rsi.head(20))

root = Tk()

root.title("Welcome to GeekForGeeks")
root.geometry('200x200')

def graph():
	# Set the theme of our chart
	plt.style.use('fivethirtyeight')

	# Make our resulting figure much bigger
	plt.rcParams['figure.figsize'] = (20, 20)



	# Create two charts on the same figure.
	ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
	ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

	# First chart:
	# Plot the closing price on the first chart
	# ax1.plot(df_btc['Close'], linewidth=2)
	ax1.plot(data['ZAR'], linewidth=2)

	ax1.set_title('Bitcoin Close Price')

	# Second chart
	# Plot the RSI
	ax2.set_title('Relative Strength Index')
	ax2.plot(rsi, color='orange', linewidth=1)
	# Add two horizontal lines, signalling the buy and sell ranges.
	# Oversold
	ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
	# Overbought
	ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

	# Display the charts
	plt.show()

button = Button(root, text="Plot Graph", command=graph)
button.pack()

root.mainloop()