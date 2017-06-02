# @HarowitzBlack -> author
# A MOVABLE TOP AND A SEXY CLOSE BUTTON FOR THE NAKED BITCH!!!
# @candiedpussy :p -> awesome name, isn't it? NEVER USE IT! I'll sue you for intellectual 
# property theft!!! lol :o, (.)(.)


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
		self.Holder = Frame(self.parent,width = 260,height=20,bg = BG_COLOR)
		self.Holder.grid(row = 0,column = 1,ipady=2)
		self.MovableCanvas = Canvas(self.Holder,width = 260,height = 25,\
			bg = BG_COLOR,highlightthickness=0)
		self.MovableCanvas.bind('<Button-1>',self.ClickTopLevel)
		self.MovableCanvas.bind('<B1-Motion>',self.DragTopLevel)
		self.MovableCanvas.grid(row = 0,column = 1,sticky = W)

		# CLOSE WINDOW BUTTON
		self.closeXmarker = ImageTk.PhotoImage(file="icons/cc.png")
		self.closeBrushWin = Button(self.Holder,width = 20,height=20,bd = 0,bg = BG_COLOR,command=self.parent.withdraw,\
			cursor='hand2',activebackground=BG_COLOR,highlightthickness=0)
		self.closeBrushWin.config(image=self.closeXmarker)
		self.closeBrushWin.grid(row=0,column=2,sticky=E,padx = 7)

	def ClickTopLevel(self,event):
		self.TopLevelXPos,self.TopLevelYPos = event.x,event.y
	
	def DragTopLevel(self,event):
		#print(event)
		self.childWin = self.parent
		x = self.childWin.winfo_pointerx() - self.TopLevelXPos
		y = self.childWin.winfo_pointery() - self.TopLevelYPos
		#self.childWin.config(cursor = 'fleur')
		self.childWin.geometry('+{x}+{y}'.format(x=x,y=y))