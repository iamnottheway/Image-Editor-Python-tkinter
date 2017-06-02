import os
import random
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from skimage import io,color
from colors import COLORS
from MoveWindow import MovableWindow



BG_COLOR = '#24272b'
SIZE = [800,600]

IMAGE_PATH = "empty"


class ImageOperations():
	# basic image operations	
	def __init__(self,path2img):
		self.path2img = path2img

	# converts an image as an array
	def GetImageAsArray(self):
		self.image = self.path2img
		self.img2ar = []
		try:
			self.img2ar = io.imread(self.image)
		except Exception as e:
			print(e)
		return self.img2ar

	# converts the array to an image and saves
	def SaveArray2Img(self,array,path = '/home/freezer9/Desktop/',imageName='ebab.png'):
		self.array,self.imageName,self.path = array,imageName,path 
		self.path = self.path + self.imageName
		io.imsave(self.path,self.array)
		print("Image saved @ {}".format(self.path))


class ImageEffects():
	def __init__(self):
		pass

	def AddaBox(self,array,row,col,colorAr):
		self.array,self.row,self.col,self.colorAr = array,row,col,colorAr
		self.array[:self.row,:self.col] = self.colorAr
		print('Added a box')
		return self.array

	def ColorGradient(self,array,rainbwRow,rowHeight = 'NONE'):
		# creates a spectrum of random colors
		# rainbwRow is the height of the box, max height depends on the image dimensions
		self.rowHeight = rowHeight
		self.rainbwRow = rainbwRow
		if self.rowHeight == 'MAX':
			self.rainbwRow = max(array.shape)
		self.array = array
		while self.rainbwRow > 0:
			self.array = self.AddaBox(self.array,self.rainbwRow,250,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
			self.rainbwRow -= 2
		return self.array

	def ColorPixelate(self,array):
		# changew the image into random color spots
		self.array = array
		self.maxNum = max(self.array.shape)
		for row in range(0,self.maxNum):
			for col in range(0,self.maxNum):
				# randomly change the color of 1px 
				self.array[row,col] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		return self.array

	def Convert2Gray(self,array):
		# converts to grayscale
		self.array = array
		return color.rgb2gray(self.array)

	def grayscaleFilter1(self,array,TintMagnitude):
		# dim the gray scale or brighten it up
		# gray scale values range from 0 - 1 (sigmoid function to make a number range from 0-1)
		self.array,self.TintMagnitude = array,TintMagnitude
		# convert to gray
		self.array = self.Convert2Gray(self.array)
		self.array = (self.TintMagnitude * self.array)
		return self.array


# EDIT PICTURE 
class PictureEdit(MovableWindow):

	def __init__(self,parent):
		self.parent = parent
		self.PictureEditWin()

	def PictureEditWin(self):
		self.PicEdWin = Toplevel(self.parent)
		self.PicEdWin.title("Picture Effects")
		self.PicEdWin.geometry("300x300+900+150")
		self.PicEdWin.config(bg = BG_COLOR)
		self.PicEdWin.resizable(0,0)
		self.PicEdWin.overrideredirect(1)
		MovableWindow.__init__(self,self.PicEdWin)
		self.grayLab = Label(self.PicEdWin,text = "grayscale",bg=BG_COLOR,fg = "#fff")
		self.grayLab.grid(row = 1,column=1,sticky=W,padx = 10)
		self.grayscaleSlider = Scale(self.PicEdWin, from_=0, to=100,orient=HORIZONTAL,\
			width = 10,bd = 0,bg = "#333",fg = 'white',length = 250,highlightthickness=1)
		self.grayscaleSlider.grid(row = 2,column=1)

		self.okButton = Button(self.PicEdWin,text = "ok",command = self.getGrayScaleValue,bd = 0,bg = BG_COLOR,width = 1,\
			height = 1).grid(row = 3,column=1,\
			ipadx = 1,ipady= 0)

	def getGrayScaleValue(self):
		# return the slider value which ranges btwn 0 - 1
		return self.grayscaleSlider.get()/100

	# find a way to get the image location into this stuff
	def ConvertToGray(self,imPath):
		self.graytintMag = self.getGrayScaleValue()
		self.imPath = imPath
		self.imgOp = ImageOperations(self.imPath)
		self.imAr = self.imgOp.GetImageAsArray()
		self.imEffects = ImageEffects()
		self.imEffects.grayscaleFilter1(self.imAr,self.graytintMag)

# Main Parent window class
class WindowApp(PictureEdit):

	def __init__(self,master):
		self.master = master
		self.master.geometry("800x600+200+100")
		self.master.config(bg = BG_COLOR)
		self.master.title('ImgEd')
		self.master.resizable(0,0)
		# container to hold the tools
		self.ToolBoxFrame = Frame(self.master,width = SIZE[0],height= 50,bg="blue")
		self.ToolBoxFrame.grid(row = 1,column= 1,padx = 10,pady = 5,sticky = W)
		# add icon to open img button
		self.openImgBtn = Button(self.ToolBoxFrame,command = self.open_img,width = 20,height = 20,bd = 0,cursor = "hand2")
		self.FolderOpenIcon = ImageTk.PhotoImage(file="icons/folder-open-resize.png")
		self.openImgBtn.config(image= self.FolderOpenIcon)
		self.openImgBtn.grid(row =  1,column=2,sticky = W)
		# create a button and add an icon 
		self.BrushButton = Button(self.ToolBoxFrame,width = 20,height = 20,text = 'bb',bd = 0,cursor = "hand2",command = self.StartDraw)
		self.BrushIcon = ImageTk.PhotoImage(file="icons/brush-resize.png")
		self.BrushButton.config(image = self.BrushIcon)
		self.BrushButton.grid(row = 1,column = 3)
		# camera edit button
		self.PicEditButton = Button(self.ToolBoxFrame,text = "C",width = 20,height = 20,bd = 0,cursor='hand2',command=self.ShowPicEditor)
		self.PicEditIcon = ImageTk.PhotoImage(file="icons/cam.png")
		self.PicEditButton.config(image = self.PicEditIcon)
		self.PicEditButton.grid(row = 1,column = 4)

	def ShowPicEditor(self):
		super().__init__(self.master)
		

	def openfn(self):
		self.filename = filedialog.askopenfilename(title='open')
		return self.filename

	def open_img(self):
		try:
			self.path = self.openfn()
			self.master.title(self.path)
			self.DrawCanvas = Canvas(self.master,width = SIZE[0],height = SIZE[1],bg = '#333')
			self.DrawCanvas.grid(row = 2,column = 1)
			self.img = Image.open(self.path)
			self.img = self.img.resize((700, 500), Image.ANTIALIAS)
			# image converted to photoimg object
			self.img = ImageTk.PhotoImage(self.img)
			self.DrawCanvas.create_image(SIZE[0]/2,SIZE[1]/2,image=self.img)
			# convert the image into an numpy array for further processing
			self.imgIO = ImageOperations(self.path)
			self.imageAsArray = self.imgIO.GetImageAsArray()
		except:
			# if the open file dialog box is closed without opening any image just ignore the error
			pass

	def GetCurrentPath(self):
		return self.path 

	# function to draw stuff on the canvas
	def StartDraw(self):
		self.BrushWin = EditWindow(self.master)
		self.BrushWin.BrushEffects()
		# callback function to draw the stuff
		self.master.bind('<B1-Motion>',self.Draw)

	def Draw(self,event,thickness = 5):
		try:
			self.event = event
			# gets the current size of the brush
			self.thickness = self.BrushWin.refreshBrushthk()
			self.DrawCanvas.config(cursor="tcross")
			self.x,self.y = self.event.x,self.event.y
			self.point = self.DrawCanvas.create_oval(self.x,self.y,self.x+self.thickness,self.y+self.thickness,fill = COLORS[random.randint(0,len(COLORS)-1)])
			del self.point
		except:
			print("NOTHING TO DRAW ON YOU DUMBFUCK!")


class EditWindow(MovableWindow):

	def __init__(self,parent):
		self.parent = parent
		self.TopLevelXPos = 0
		self.TopLevelYPos = 0
		#self.path = path
		
	def BrushEffects(self):
		self.editWin = Toplevel(self.parent)
		self.editWin.title("Brush Effects")
		self.editWin.geometry("300x300+900+150")
		self.editWin.config(bg = BG_COLOR)
		self.editWin.resizable(0,0)
		self.editWin.overrideredirect(1)
		#  bind the mouse-button to the window, so that when
		# the user holds the window it moves
		# create a canvas to drag the window, so that it doesn't affect oher widgets
		# call the movable window class
		MovableWindow.__init__(self,self.editWin)
		# BRUSH-THICKNESS 
		self.thicknessLabel = Label(self.editWin,text = "Thickness :",bg = BG_COLOR,fg="snow")
		self.thicknessLabel.grid(row = 1,column=1,sticky = W)
		# slider
		self.BrushThickness = Scale(self.editWin, from_=0, to=100,orient=HORIZONTAL,width = 10,bd = 0,bg = "#333",fg = 'white',\
			length = 250)
		self.BrushThickness.grid(row=2,column=1,padx = 5)
		# refresh thickness button
		self.RefreshThicknessBtn = ImageTk.PhotoImage(file="icons/tick.png")
		self.SetBrushThicknessBtn = Button(self.editWin,width=20,height=20,text = 'v',bd = 0,command=self.refreshBrushthk,cursor = "hand2")
		self.SetBrushThicknessBtn.config(image = self.RefreshThicknessBtn)
		self.SetBrushThicknessBtn.grid(row=2,column=2,padx = 5)

		# COLOR PALETTE
		self.ColorPaletteLabel = Label(self.editWin,text = 'Color Palette',fg = 'white',bg = BG_COLOR)
		self.ColorPaletteLabel.grid(row = 3,column = 1,pady = 5,sticky =W)
		self.ColorPaletteCanvas = Canvas(self.editWin,width = 210,height = 100,bg = 'white',cursor = 'tcross')
		self.ColorPaletteCanvas.grid(row = 4,column=1,pady = 2)
		# colors inside the palette
		x_pos = 0
		y_pos = 0
		# final x coord of the canvas is 200
		# and y coord is 100. -20 from them
		for c in COLORS:
			self.colorsInside = self.ColorPaletteCanvas.create_rectangle(x_pos,y_pos,x_pos+10,y_pos+10,fill = c)
			#showing all the colors on the screen
			x_pos += 10
			if x_pos > 200:
				y_pos += 10
				x_pos = 0
		
	def refreshBrushthk(self):
		# store the thickness to use in the label
		self.LabelThickness = self.BrushThickness.get()
		self.thicknessLabel.config(text = "Thickness : {}".format(self.LabelThickness))
		return self.BrushThickness.get()




def Tester(imgPath):
	im = ImageOperations(imgPath)
	effects = ImageEffects()
	bab = im.GetImageAsArray()
	original_image = bab # store a copy of the array
	imageShape = bab.shape 
	imageRow,imageCol = imageShape[0],imageShape[1]
	#bab = effects.AddaBox(bab,startRow,250,[0,0,0])
	#bab = effects.ColorGradient(bab,250,'MAX')
	#bab = effects.ColorPixelate(bab)
	bab = effects.brightORdimGray(bab,[0.5])
	im.SaveArray2Img(bab)
	os.system('gnome-open {}\n\n'.format('ebab.png'))

def TestSigmoid(x):
	return 1.0 / (1.0 + np.exp(-1.0 * x))

def run():
	root = Tk()
	win = WindowApp(root)
	root.mainloop()

#Tester('baboon.png')
run()



