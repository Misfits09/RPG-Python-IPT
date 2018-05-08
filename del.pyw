from tkinter import *
from tkinter import messagebox
top = Tk()

C = Canvas(top, bg="blue", height=480, width=640)
filename = PhotoImage(file = "C:/Users/nathp/Documents/GitHub/RPG-Python-IPT/tel.png")
background_label = Label(C, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()
bac
C.create_text(240,30,text='RPG - GUI BETA 1.0', font=('Arial',25),anchor=CENTER,)

top.mainloop()