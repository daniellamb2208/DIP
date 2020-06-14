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

global load, img_gray, img_blur, img_equ, img_sobel, img_plate

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

def closing():
	global img_sobel, img_close, load

	kernel = np.ones((5,5),np.uint8)
	img_close = cv2.morphologyEx(img_sobel, cv2.MORPH_CLOSE, kernel)

	tmp = Image.fromarray(np.uint8(img_close))
	tmp = ImageTk.PhotoImage(tmp)
	l = Label(master, image = tmp, width = load.size[0], height = load.size[1])
	l.image = tmp
	l.place(x=load.size[0]*5+120+20+20+20+20,y=10)

def contours():
	global load, img_sobel, img_plate

	img_sobel = np.array(img_sobel, np.uint8)
	contours , hierarchy = cv2.findContours(img_sobel,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#img_sobel = Image.fromarray(np.uint8(img_sobel))
	#img_sobel = ImageTk.PhotoImage(img_sobel)
	img_sobel = cv2.cvtColor(img_sobel, cv2.COLOR_GRAY2BGR)

#	for i in contours:
#		x,y,w,h = cv2.boundingRect(i)
#		cv2.rectangle(img_sobel, (x,y), (x+w, y+h), (0,255,0),2)

	for i in contours:
		if len(i) == 115:#119
			maxx = minx = i[0][0][0]
			maxy = miny = i[0][0][1]
			maxxy = maxyx = minxy = minyx = 0
			for j in i:
				if j[0][0] >= maxx:	#😝️
					maxx = j[0][0]
					maxxy = j[0][1]
				if j[0][1] >= maxy:
					maxy = j[0][1]
					maxyx = j[0][0]
				if j[0][0] <= minx:
					minx = j[0][0]
					minxy = j[0][1]
				if j[0][1] <= miny:
					miny = j[0][1]
					minyx = j[0][0]
			#print((maxx,maxxy), (maxyx,maxy), (minx,minxy), (minyx,miny))
			rect = cv2.minAreaRect(i)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			cv2.drawContours(img_sobel, [box], 0,(0,0,255),3)
			break
	#print(miny,maxy,minx,maxx)
	img = cv2.cvtColor(np.asarray(load),cv2.COLOR_RGB2BGR)
	img_plate = img[miny:maxy,minx:maxx]

	plt.title('plate')
	plt.imshow(img_plate)
	plt.show()
#	cv2.drawContours(img_sobel ,contours,-1,(0,0,255),20)

if __name__ == '__main__':
	load_the_origin_picture()
	convert_RGB_toL()
	blur()
	histogram_equalization()
	sobel()
	closing()
	contours()

mainloop()
