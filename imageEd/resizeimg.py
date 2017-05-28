from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import random

def openfn():
	filename = filedialog.askopenfilename(title='open')
	return filename

def resizeImage():
	path = openfn()
	image = Image.open(path)
	image = image.resize((20,20),Image.ANTIALIAS)
	image.save('{}.png'.format(random.randint(12345,21322)))
	print('resized and Saved!')

root = Tk()
root.resizable(0,0)
root.geometry("200x200")
btn = Button(root,text='resize image',command=resizeImage).pack()
root.mainloop()


