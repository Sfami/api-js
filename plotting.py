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
import calculations as cs


root = Tk()
root.title("Ellen's Application")
root.geometry('450x450')

email = StringVar()
password = StringVar()
mav = StringVar()




def plot(scale, mva_toggle):
	st = email.get()
	en = password.get()
	av = moving.get()

	



	print(st)
	print(en)
	st_l = st.split("/")

	en_l = en.split("/")
	print(st_l)
	print(en_l)

	first = datetime(int(st_l[0]),int(st_l[1]),int(st_l[2]))
	second= datetime(int(en_l[0]),int(en_l[1]),int(en_l[2]))

	first= first.strftime("%Y/%m/%d")

	second= second.strftime("%Y/%m/%d")
	data = pd.read_csv("data/data.csv")
	print(data.head())
	print("\n", data.columns)
    data = data[data.Date > first]
    data = data[data.Date < second]


	date = data['Date']
	zar = data['ZAR']

	fig = plt.figure()

	ax1 = plt.subplot2grid((5,4), (0,0), rowspan = 4, colspan = 4)
	ax1.plot(date, zar, color='blue', linewidth=0.5, label="Rate " + str(50))
	ax1.plot(cs.calc_mva(zar, 50), color='red', linewidth=1.5, label="MVA " + str(50))
	plt.ylabel('USD/ZAR Exchange Rate')
	# a.legend()
	ax1.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=2,
				ncol=1, borderaxespad=0)
	ax1.grid(True)

	ax2 = plt.subplot2grid((5,4), (4,0), sharex=ax1, rowspan = 1, colspan = 4)
	# ax2 = plt.subplot(2,1,2, sharex=ax1)
	plt.ylabel('RSI')
	# ax2.plot(cs.calc_rsi(zar))
	ax2.plot(cs.calc_rsi(zar), color='orange', linewidth=0.5)
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

	plt.subplots_adjust(left=.09, bottom=.18, top=.80, right=.94, wspace=.20, hspace=0)
	plt.xlabel('Date')
	plt.suptitle('Daily USD/ZAR Exchange Rate over Time (1992 to 2022)')
	plt.setp(ax1.get_xticklabels(), visible=False)

	plt.show()



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




button = Button(signin, text="Linear Scale", command=lambda: plot("linear", mva_toggle))
button.pack(side=LEFT, fill='both', expand=1)

button1 = Button(signin, text="Log Scale", command=lambda: plot("log", mva_toggle))
button1.pack(side=RIGHT, fill='both', expand=1)



root.mainloop()