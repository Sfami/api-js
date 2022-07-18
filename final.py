from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

data = pd.read_csv("data/data.csv")	

data.dropna(inplace=True)

columns = data.columns
data["Date"] = pd.to_datetime(data[columns[0]], infer_datetime_format=True) 
# data["ZAR"] = data[columns[1]]

# data["ZAR"] = data['ZAR'].map(lambda x: float(0) if x =='ND' else float(x))

# print(data['ZAR'].head())

# print(data['ZAR'].dtype)
# data = data.drop(columns, axis=1)
# data.set_index("ZAR")


print(len(data))

change = data["ZAR"].diff()
change.dropna(inplace=True)


change_up = change.copy()
change_down = change.copy()

# 
change_up[change_up<0] = 0
change_down[change_down>0] = 0

change.equals(change_up+change_down)

avg_up = change_up.rolling(14).mean()
avg_down = change_down.rolling(14).mean().abs()



rsi = 100 * avg_up / (avg_up + avg_down)

print(rsi.head(20))

root = Tk()
root.title("Ellen's Application")
root.geometry('450x450')

email = StringVar()
password = StringVar()
mav = StringVar()


def graph(scale, mva_toggle):

	st = email.get()
	en = password.get()
	av = moving.get()
	print(st)
	print(en)
	st_l = st.split("/")

	en_l = en.split("/")
	print(st_l)
	print(en_l)
	global data

	data = data[data.Date > datetime(int(st_l[0]),int(st_l[1]),int(st_l[2]))]
	data = data[data.Date < datetime(int(en_l[0]),int(en_l[1]),int(en_l[2]))]

	print(len(data))

	ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
	ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

	ax1.plot(data['ZAR'], linewidth=2)
	
	mave = data['ZAR'].rolling(int(av)).mean()
	
	print("state", mva_toggle)
	if mva_toggle == "On":
		ax1.plot(mave, linewidth=2)	


	print("scale", scale)
	if scale == "log":
		plt.yscale('log')
	plt.ylabel('RSI')
    # ax2.plot(cs.calc_rsi(zar))
	ax2.plot(rsi, color='orange', linewidth=0.5)
	ax2.axhline(30, linestyle='--', linewidth=1.0, color='green')
	ax2.axhline(70, linestyle='--', linewidth=1.0, color='red')
	ax2.axes.yaxis.get_ticklabels([])
	ax2.grid(True)


	ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

	for label in ax1.xaxis.get_ticklabels():
		label.set_rotation(90)
	for label in ax2.xaxis.get_ticklabels():
		label.set_rotation(45)


   
	plt.xlabel('Date')
	plt.suptitle('Daily USD/ZAR Exchange Rate over Time (1992 to 2022)')
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.subplots_adjust(left=.09, bottom=.18, top=.94, right=.94, wspace=.20, hspace=0)

	plt.show()



	

	# ax2.plot(rsi, color='orange', linewidth=1)

	# ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')

	# ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

	# plt.show()


signin = Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)

lbl0 = Label(signin, text = "Welcome\nUse the following date format: (YYYY/MM/DD)")
lbl0.pack()

lbl = Label(signin, text = "Start Date")
lbl.pack()
start_date = Entry(signin, textvariable=email)
start_date.pack()
lbl1 = Label(signin, text = "End Date")
lbl1.pack()
end_date = Entry(signin, textvariable=password)
end_date.pack()



lbl1 = Label(signin, text = "Moving Average: ", font=('Helvetica 13'))
lbl1.pack()

moving = Entry(signin, textvariable=mav)
moving.pack()

mva_toggle = ""
def get_data(state):
   lbl1.config(text= "Moving Average:" + state, font= ('Helvetica 13'))
   global mva_toggle
   mva_toggle = state

on = Button(signin, text="On", command=lambda: get_data("On"))
on.pack()

off = Button(signin, text="Off", command=lambda: get_data("Off"))
off.pack()




button = Button(signin, text="Linear Scale", command=lambda: graph("linear", mva_toggle))
button.pack(side=LEFT, fill='both', expand=1)

button1 = Button(signin, text="Log Scale", command=lambda: graph("log", mva_toggle))
button1.pack(side=RIGHT, fill='both', expand=1)



root.mainloop()