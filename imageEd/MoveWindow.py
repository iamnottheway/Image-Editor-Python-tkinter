
from tkinter import *
from PIL import ImageTk, Image

BG_COLOR = '#24272b'

class MovableWindow():

	'''
		CANVAS WHICH IS MOVABLE WHEN CLICKED AND DRAGGED
	'''

	def __init__(self,parent):
		self.parent = parent
		# create a canvas which is movable
		self.MovableCanvas = Canvas(self.parent,width = 260,height = 25,\
			bg = BG_COLOR)
		self.MovableCanvas.bind('<Button-1>',self.ClickTopLevel)
		self.MovableCanvas.bind('<B1-Motion>',self.DragTopLevel)
		self.MovableCanvas.grid(row = 0,column = 1,sticky = W)

		# CLOSE WINDOW BUTTON
		self.closeXmarker = ImageTk.PhotoImage(file="icons/cc.png")
		self.closeBrushWin = Button(self.parent,width = 15,height=15,bd = 0,bg = BG_COLOR,command=self.parent.withdraw,\
			cursor='hand2',activebackground=BG_COLOR)
		self.closeBrushWin.config(image=self.closeXmarker)
		self.closeBrushWin.grid(row=0,column=2,sticky=E,pady = 5)

	def ClickTopLevel(self,event):
		self.TopLevelXPos,self.TopLevelYPos = event.x,event.y
	
	def DragTopLevel(self,event):
		#print(event)
		self.childWin = self.parent
		x = self.childWin.winfo_pointerx() - self.TopLevelXPos
		y = self.childWin.winfo_pointery() - self.TopLevelYPos
		#self.childWin.config(cursor = 'fleur')
		self.childWin.geometry('+{x}+{y}'.format(x=x,y=y))