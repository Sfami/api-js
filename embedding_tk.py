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
# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("1080x1080")


var = StringVar()
Var1 = StringVar()
Var2 = StringVar()
Var3 = StringVar()
email = StringVar()
password = StringVar()
mav = StringVar()



mva_toggle = ""
mva_value  = 50
def get_data(state):
   label1.config(text= "Moving Average:" + state, font= ('Helvetica 13'))
   global mva_toggle
   global mva_value
   mva_toggle = state
   Var1.set("EMA "+ str(mva_value) + " :" + mva_toggle)

scale = ""
def sel():
   selection = "" + str(var.get())
   label.config(text = selection)
   global scale
   scale = selection




fig = plt.figure()


def plot():
    graph(scale, mva_toggle)


def graph(scale, mva_toggle):
    global fig
    data = pd.read_csv("data/data.csv")
    columns = data.columns
    data["Date"] = pd.to_datetime(data[columns[0]], infer_datetime_format=True) 
    print(data.head())
    print("\n", data.columns)
    
    st = email.get()
    en = password.get()
    av = mva_value
    print(st)
    print(en)
    st_l = st.split("/")

    en_l = en.split("/")
    print(st_l)
    print(en_l)
    # global data

    

    fig.clear()
    data = data[data.Date > datetime(int(st_l[0]),int(st_l[1]),int(st_l[2]))]
    data = data[data.Date < datetime(int(en_l[0]),int(en_l[1]),int(en_l[2]))]

    date = data['Date']
    zar = data['ZAR']

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

    ax1.set_title('Bitcoin Close Price')

    ax2.set_title('Relative Strength Index')
    ax2.plot(rsi, color='orange', linewidth=1)

    ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')

    ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')



    # ax1 = plt.subplot2grid((5,4), (0,0), rowspan = 4, colspan = 4)
    # ax1 = plt.subplot(2,1,1)
    # ax1.plot(date, zar, color='blue', linewidth=0.5)


    # ax1.plot(cs.calc_mva(zar, 50), color='red', linewidth=1.5)
    # plt.ylabel('USD/ZAR Exchange Rate')
    # ax1.grid(True)

    # ax2 = plt.subplot2grid((5,4), (4,0), sharex=ax1, rowspan = 1, colspan = 4)
    # # ax2 = plt.subplot(2,1,2, sharex=ax1)
    # plt.ylabel('RSI')
    # # ax2.plot(cs.calc_rsi(zar))
    # ax2.plot(cs.calc_rsi(zar), color='orange', linewidth=0.5)
    # ax2.axhline(30, linestyle='--', linewidth=1.0, color='green')
    # ax2.axhline(70, linestyle='--', linewidth=1.0, color='red')
    # ax2.axes.yaxis.get_ticklabels([])
    # ax2.grid(True)


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

    canvas = FigureCanvasTkAgg(fig,
                            master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()



# button that displays the plot
plot_button = Button(master = window,
                    command = plot,
                    text = "Plot")

# place the button
# in main window
plot_button.pack()



R1 = Radiobutton(window, text="Lin", variable=var, value="Linear Scale", command=sel)
R1.pack()

R2 = Radiobutton(window, text="Log", variable=var, value="Log Scale", command=sel)
R2.pack()


label = Label(window, text="Select scale")
label.pack()




mva_toggle = ""
mva_vale  = 50
def get_data(state):
   label1.config(text= "Moving Average:" + state, font= ('Helvetica 13'))
   global mva_toggle
   mva_toggle = state
   Var1.set("EMA "+ mva_value + " :" + mva_toggle)


on = Button(window, text="On", command=lambda: get_data("On"))
on.pack()

off = Button(window, text="Off", command=lambda: get_data("Off"))
off.pack()


Var1.set("Toggle SMA On or Of")
label1 = Label(window,text= "Moving Average:",  textvariable = Var1 )
label1.pack()



def val(value):
    global Var1
    global mva_toggle
    global mva_value
    mva_value = value
    Var1.set("EMA "+ value + " :" + mva_toggle)
    # print(value)

Scala2 = Scale(window, from_=50, to=130, length = 200,
               tickinterval = 40, command=val,
               orient=HORIZONTAL, sliderlength = 15)
Scala2.pack()


welcome =  "Welcome\nUse the following date format: "
lbl0 = Label(window, text ="YYYY/MM/DD")
lbl0.pack()

lbl = Label(window, text = "Start Date")
lbl.pack()
start_date = Entry(window, textvariable=email)
start_date.pack()
lbl1 = Label(window, text = "End Date")
lbl1.pack()

end_date = Entry(window, textvariable=password)
end_date.pack()



def _quit():
    window.quit()     # stops mainloop
    window.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = Button(master=window, text="Quit", command=_quit)
button.pack(side=BOTTOM)



# run the gui
window.mainloop()
