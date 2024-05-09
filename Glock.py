from tkinter import *
from time import *

def upd():
    tstr = strftime("%I:%M:%S %p")
    ltime.config(text=tstr)

    lday.config(text=strftime("%A"))

    dtstr = strftime("%B %d, %Y")
    ldate.config(text=dtstr)
    ltime.after(1000, upd)


window = Tk()
window.config(bg='black')
window.title("Clock")
window.geometry('520x300')
window.resizable(0,1)


ltime = Label(window, font="Adobe 60", text='', fg='green', bg='black')
ltime.pack()
lday = Label(window, font="Adobe 60", text='', fg='green', bg='black')
lday.pack()
ldate = Label(window, font="Adobe 60", text='', fg='green', bg='black')
ldate.pack()

upd()

window.mainloop()