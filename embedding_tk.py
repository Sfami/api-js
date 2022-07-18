from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
# from matplotlib
# matplotlib.rcParams.update({'font.size': 9})

import numpy as np
import pandas as pd
from datetime import datetime

import calculations as cs

# plot function is created for
# plotting the graph in
# tkinter window
def plot():

    data = pd.read_csv("data/data.csv")
    print(data.head())
    print("\n", data.columns)
    date = data['Date']
    zar = data['ZAR']

    fig = plt.figure()

    ax1 = plt.subplot2grid((5,4), (0,0), rowspan = 4, colspan = 4)
    ax1 = plt.subplot(2,1,1)
    ax1.plot(date, zar, color='blue', linewidth=0.5)
    ax1.plot(cs.calc_mva(zar, 50), color='red', linewidth=1.5)
    plt.ylabel('USD/ZAR Exchange Rate')
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

   
    plt.xlabel('Date')
    plt.suptitle('Daily USD/ZAR Exchange Rate over Time (1992 to 2022)')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=.09, bottom=.18, top=.94, right=.94, wspace=.20, hspace=0)

    canvas = FigureCanvasTkAgg(fig,
                            master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("1080x1080")

# button that displays the plot
plot_button = Button(master = window,
                    command = plot,
                    text = "Plot")

# place the button
# in main window
plot_button.pack()


def _quit():
    window.quit()     # stops mainloop
    window.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = Button(master=window, text="Quit", command=_quit)
button.pack(side=TOP)




# run the gui
window.mainloop()
