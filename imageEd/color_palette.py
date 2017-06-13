from tkinter import *
from colors import COLORS
import random

def get_color(*args):
	current_color = ColorPaletteCanvas.itemcget("current","tags")
	print(current_color)

root = Tk()
root.geometry("300x300+300+200")
root.config(bg="#333")
root.resizable(0,0)
root.title("color pallette")

ColorPaletteCanvas = Canvas(root,width = 210,height = 220,bg = 'white',cursor = 'tcross')
ColorPaletteCanvas.grid(row = 0,column=1,padx = 10,pady = 10)
		# colors inside the palette
x_pos = 0
y_pos = 0
		# final x coord of the canvas is 200
		# and y coord is 100. -20 from them
for c in COLORS:
	colorsInside = ColorPaletteCanvas.create_rectangle(x_pos,y_pos,x_pos+10,y_pos+10,fill = c,tags=("{0}".format(c)))
	#showing all the colors on the screen
	x_pos += 10
	if x_pos > 200:
		y_pos += 10
		x_pos = 0

# current is a keyword. It points to the current object. Alternative: CURRENT
# gets the current clicked color from the palette
ColorPaletteCanvas.tag_bind("current",'<Button-1>',get_color)
#print(ColorPaletteCanvas.find_withtag(CURRENT[0])
# prints what typeof item it is
#print(ColorPaletteCanvas.type(colorsInside))
#print(tags)
root.mainloop()