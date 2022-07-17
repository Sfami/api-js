import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)



style.use("ggplot")


# fig = Figure()
fig = plt.figure()

# a = fig.add_subplot(111)


scale = "Linear"
DatCounter = 9000
programName = "linear"
resampleSize = "15Min"
DataPace = "tick"
candleWidth = 0.008

paneCount = 1

topIndicator = "none"
bottomIndicator = "none"
middlepIndicator = "none"
chartLoad = True

EMAs = []
SMAs = []

def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("!")
	label = ttk.Label(popup, text=msg, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
	B1.pack()
	popup.mainloop()


def addTopIndicator(what):
	global topIndicator
	global DatCounter

	# if DataPace == "tick":
	# 	popupmsg("Indicators in Tick Data not available.")

	if what == "none":
		topIndicator = what
		DatCounter = 9000


	elif what == "sma":
		rsiQ = tk.Tk()
		rsiQ.wm_title("Periods?")
		label = ttk.Label(rsiQ, text="Choose how namy periods you want for each RSI calculation.")
		label.pack(side="top", fill="x", pady=10)

		e = ttk.Entry(rsiQ)
		e.insert(0, 14)
		e.pack()
		e.focus_set()

		def callback():
			global topIndicator
			global DatCounter

			periods =(e.get())

			group = []
			group.append("sma")
			group.append(periods)

			topIndicator = group
			DatCounter = 9000
			print("Set top indicator to", group)
			rsiQ.destroy()
		b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
		b.pack()
		tk.mainloop()

	elif what == "ema":
		# global topIndicator
		# global DatCounter
		topIndicator = "ema"
		DatCounter = 9000

def addBottomIndicator(what):
	global bottomIndicator
	global DatCounter

	if DataPace == "tick":
		popupmsg("Indicators in Tick Data not available.")

	elif what == "none":
		bottomIndicator = what
		DatCounter = 9000


	elif what == "sma":
		rsiQ = tk.Tk()
		rsiQ.wm_title("Periods?")
		label = ttk.Label(rsiQ, text="Choose how namy periods you want for each RSI calculation.")
		label.pack(side="top", fill="x", pady=10)

		e = ttk.Entry(rsiQ)
		e.insert(0, 14)
		e.pack()
		e.focus_set()

		def callback():
			global bottomIndicator
			global DatCounter

			periods =(e.get())

			group = []
			group.append("sma")
			group.append(periods)

			bottomIndicator = group
			DatCounter = 9000
			print("Set bottom indicator to", group)
			rsiQ.destroy()
		b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
		b.pack()
		tk.mainloop()

	elif what == "ema":
		# global topIndicator
		# global DatCounter
		bottomIndicator = "ema"
		DatCounter = 9000



def changeTimeFrame(tf):
	global DataPace
	global DatCounter
	if tf == "7d" and resampleSize == "1Min":
		popupmsg("Too much data, choose a smaller time frame or higher OHLC sample size")
	else:
		DataPace = tf
		DatCounter = 9000

def changeSampleSize(size, width):
	global resampleSize
	global DatCounter
	global candleWidth
	if DataPace == "7d" and resampleSize == "1Min":
		popupmsg("Too much data, choose a smaller time frame or higher OHLC sample size")
	elif DataPace == "tick":
		popupmsg("You are currently viewing tick data, not OHLC")

	else:
		resampleSize = size
		DatCounter = 9000
		candleWidth = width


def changeScale(toWhat, progName):
	global scale
	global DatCounter
	global programName

	scale = toWhat
	programName = progName
	DatCounter = 9000

def animate(i):
	global refreshRate
	global DatCounter

	if chartLoad:
		if paneCount == 1:
			if DataPace == "tick":
				try:
					# Load the data into a dataframe
					symbol = yf.Ticker('BTC-USD')
					df_btc = symbol.history(interval="1d",period="max")

					# Filter the data by date
					df_btc = df_btc[df_btc.index > datetime(2020,1,1)]
					df_btc = df_btc[df_btc.index < datetime(2021,9,1)]

					# Delete unnecessary columns
					del df_btc["Dividends"]
					del df_btc["Stock Splits"]

					change = df_btc["Close"].diff()
					change.dropna(inplace=True)

					# Create two copies of the Closing price Series
					change_up = change.copy()
					change_down = change.copy()

					change_up[change_up<0] = 0
					change_down[change_down>0] = 0

					# Verify that we did not make any mistakes
					change.equals(change_up+change_down)

					# Calculate the rolling average of average up and average down
					avg_up = change_up.rolling(14).mean()
					avg_down = change_down.rolling(14).mean().abs()

					rsi = 100 * avg_up / (avg_up + avg_down)

					plt.style.use('fivethirtyeight')

					# Make our resulting figure much bigger
					plt.rcParams['figure.figsize'] = (20, 20)



					# Create two charts on the same figure.
					ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
					ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

					# First chart:
					# Plot the closing price on the first chart
					ax1.plot(df_btc['Close'], linewidth=2)
					ax1.set_title('Bitcoin Close Price')

					# Second chart
					# Plot the RSI
					# ax2.set_title('Relative Strength Index')
					ax2.plot(rsi, color='orange', linewidth=1)
					# Add two horizontal lines, signalling the buy and sell ranges.
					# Oversold
					ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
					# Overbought
					ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')


					# a = plt.subplot2grid((10, 1), (0, 0), rowspan = 4, colspan = 1)
					# a2 = plt.subplot2grid((10, 1), (5, 0), rowspan = 4, colspan = 1, sharex = a)

					# a.clear()


					# a.plot(df_btc.index, df_btc['Close'], label="BTC-USD")
					# a2.plot(df_btc.index, df_btc['Close'], "b",label="RSI")

					# # a.legend()
					# a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
					# 			ncol=1, borderaxespad=0)

					# title = "BTC-USD Prices\nLast Price: " + str(df_btc['Close'].iloc[len(df_btc['Close']) - 1])
					# a.set_title(title)


				except Exception as e:
					print("Failed because of: ", e)
		


def on_key_press(event):
	print("you pressed {}".format(event.key))
	key_press_handler(event, canvas, toolbar)

def _quit():
	app.quit()     # stops mainloop
	app.destroy()  # this is necessary on Windows to prevent
		                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


class FinanceDataApp(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "Finance Data App")

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		menubar = tk.Menu(container)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not suppoerted just yet!"))
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=quit)
		menubar.add_cascade(label="File", menu=filemenu)

		scalemenu = tk.Menu(menubar, tearoff=1)
		scalemenu.add_command(label="Linear", command=lambda: changeScale("Linear", "linear"))
		scalemenu.add_separator()
		scalemenu.add_command(label="Log", command=lambda: changeScale("Log", "log"))
		menubar.add_cascade(label="Scale", menu=scalemenu)

		topIndi = tk.Menu(menubar, tearoff=1)
		topIndi.add_command(label="None", 
			command=lambda: addTopIndicator("none"))
		topIndi.add_command(label="RSI",
		 	command=lambda: addTopIndicator("rsi"))
		topIndi.add_command(label="MACD",
		 	command=lambda: addTopIndicator("macd"))
		menubar.add_cascade(label="Top Indicator", menu=topIndi)


		# dataTF = tk.Menu(menubar, tearoff=1)
		# dataTF.add_command(label="Tick", 
		# 	command=lambda: changeTimeFrame("tick"))
		# dataTF.add_command(label="1 Day",
		#  	command=lambda: changeTimeFrame("1d"))
		# dataTF.add_command(label="3 Day",
		#  	command=lambda: changeTimeFrame("3d"))
		# dataTF.add_command(label="1 Week",
		#  	command=lambda: changeTimeFrame("7d"))
		# menubar.add_cascade(label="Time Frame", menu=dataTF)

		# OHLCI = tk.Menu(menubar, tearoff=1)
		# OHLCI.add_command(label="Tick", 
		# 	command=lambda: changeSampleSize("tick", 0.0005))
		# OHLCI.add_command(label="1 minute",
		#  	command=lambda: changeSampleSize("1Min", 0.0005))
		# OHLCI.add_command(label="5 minute",
		#  	command=lambda: changeSampleSize("5Min", 0.0003))
		# OHLCI.add_command(label="15 minute",
		#  	command=lambda: changeSampleSize("15Min", 0.0008))
		# OHLCI.add_command(label="30 minute",
		#  	command=lambda: changeSampleSize("30Min", 0.0016))
		# OHLCI.add_command(label="1 hour",
		#  	command=lambda: changeSampleSize("1H", 0.0032))
		# OHLCI.add_command(label="3 hour",
		#  	command=lambda: changeSampleSize("3H", 0.0096))
		# menubar.add_cascade(label="OHLC Interval", menu=OHLCI)

		# mainIndi = tk.Menu(menubar, tearoff=1)
		# mainIndi.add_command(label="None", 
		# 	command=lambda: addMiddleIndicator("none"))
		# mainIndi.add_command(label="SMA",
		#  	command=lambda: addMiddleIndicator("sma"))
		# mainIndi.add_command(label="EMA",
		#  	command=lambda: addMiddleIndicator("ema"))
		# menubar.add_cascade(label="Middle Indicator", menu=mainIndi)


		# bottomIndi = tk.Menu(menubar, tearoff=1)
		# bottomIndi.add_command(label="None", 
		# 	command=lambda: addBottomIndicator("none"))
		# bottomIndi.add_command(label="RSI",
		#  	command=lambda: addBottomIndicator("rsi"))
		# bottomIndi.add_command(label="MACD",
		#  	command=lambda: addBottomIndicator("macd"))
		# menubar.add_cascade(label="Bottom Indicator", menu=bottomIndi)

		tk.Tk.config(self, menu=menubar)

		self.frames = {}

		for F in (StartPage, GraphPage):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()



class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="StartPage", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(GraphPage))

		button1.pack()

		button2 = ttk.Button(self, text="Disagree", command=_quit)

		button2.pack()



class GraphPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# start_date_txt = ttk.Label(self, height=1, width=30)
		# start_date_txt.pack()
		# end_date_txt = ttk.Text(self, height=1, width=30)
		# end_date_txt.pack()
		label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back to Home", 
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


app = FinanceDataApp()
app.geometry("1280x720")
ani = animation.FuncAnimation(fig, animate, interval=5000)
app.mainloop()