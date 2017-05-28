from tkinter import *
from colors import COLORS
import random

root = Tk()
root.resizable(0,0)

def Draw(event):
  x,y = event.x,event.y
  point = Sheet.create_oval(x,y,x+50,y+50,fill = COLORS[random.randint(0,len(COLORS)-1)])
  del point

def clearscrn():
  Sheet.delete("all")

Sheet = Canvas(root,bg = "white",width = 400,height = 400)
Sheet.pack()

btn = Button(root,text="clear all",command=clearscrn)
btn.pack()

root.bind('<B1-Motion>',Draw)
root.mainloop()