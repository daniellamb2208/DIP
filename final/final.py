from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from scipy.ndimage import filters

master = Tk()
master.title('Final project')
master.geometry('1280x960')

global load, img_gray, img_blur, img_equ, img_sobel

def load_the_origin_picture():
	global load
	master.filename = tkinter.filedialog.askopenfilename(initialdir = "/home/lamb/Desktop/dip/final",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	load = Image.open(master.filename)
	render = ImageTk.PhotoImage(load)
	img = Label(master, image = render, width = load.size[0], height = load.size[1])
	img .image = render
	img.place(x=100, y=10)

def convert_RGB_toL():
	global load, img_gray
	img_gray = load.convert("L")
	render = ImageTk.PhotoImage(img_gray)
	l = Label(master, image = render, width = load.size[0], height = load.size[1])
	l.image = render
	l.place(x=load.size[0]+120,y=10)


def blur():
	global img_gray, img_blur
	
	img_blur = img_gray.filter(ImageFilter.GaussianBlur(radius = 3))#ImageFilter.FIND_EDGES

	tmp = ImageTk.PhotoImage(img_blur)
	l = Label(master, image = tmp, width = load.size[0], height = load.size[1])
	l.image = tmp
	l.place(x=load.size[0]*2+120+20,y=10)

def histogram_equalization():
	global img_blur, img_equ
	img_equ = ImageOps.equalize(img_blur)
	tmp = ImageTk.PhotoImage(img_equ)
	l = Label(master, image = tmp, width = load.size[0], height = load.size[1])
	l.image = tmp
	l.place(x=load.size[0]*3+120+20+20,y=10)

def sobel():
	global img_equ, img_sobel #img_sobel type -> ndarray

	img_data = np.array(img_equ)
	imx = np.zeros(img_data.shape)
	imy = np.zeros(img_data.shape)
	filters.sobel(img_data, 1, imx)
	filters.sobel(img_data, 0, imy)
	mag = np.hypot(imx, imy)

	mag *= 255.0/ np.max(mag)

	mag[mag <= 255.0/2] = 0
	mag[mag > 255.0/2] = 255

	img_sobel = mag

	tmp = Image.fromarray(np.uint8(img_sobel))
	tmp = ImageTk.PhotoImage(tmp)
	l = Label(master, image = tmp, width = load.size[0], height = load.size[1])
	l.image = tmp
	l.place(x=load.size[0]*4+120+20+20+20,y=10)
#	plt.imshow(mag,cmap ="gray")
#	plt.show();

def contours():
	global img_sobel

	img_sobel = np.array(img_sobel, np.uint8)
	contours , hierarchy = cv2.findContours(img_sobel,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


	#img_sobel = Image.fromarray(np.uint8(img_sobel))
	#img_sobel = ImageTk.PhotoImage(img_sobel)
	img_sobel = cv2.cvtColor(img_sobel, cv2.COLOR_GRAY2BGR)

	_contours = []
#	for i in contours:
#		if len(i) == 4:
#			_contours.append(i)
#	print(len(_contours))
	print (len(contours))
	cv2.drawContours(img_sobel ,contours,-1,(0,0,255),len(contours))
	plt.imshow(img_sobel)
	plt.show()

if __name__ == '__main__':
	load_the_origin_picture()
	convert_RGB_toL()
	blur()
	histogram_equalization()
	sobel()
	contours()

mainloop()
