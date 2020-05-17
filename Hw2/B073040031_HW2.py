from tkinter import *
import tkinter.filedialog  
from PIL import Image, ImageTk, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2

master = Tk()
master.title('DIP Homework2')
master.geometry('1280x960')

global load, data, soi
# load is image_data from Image.open()
# data is raw first and processed afterward, datatype is np_array ,(for output and save image
# soi is size of image [width, height]

def open():
	global load, soi
	master.filename = tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	load = Image.open(master.filename)
	render = ImageTk.PhotoImage(load)
	soi = list(load.size)		#size of image
	img = Label(master, image = render, width = soi[0], height = soi[1])
	img.image = render
	img.place(x=100, y=10)
#######################################################################################################
def gray():
	global load, data, soi
	data = np.array(load)

	var = StringVar(master)
	var.set('hightlight only in range')
	method = OptionMenu(master, var, 'hightlight only in range', 'preserve other intensities')
	method.place(x = 100, y = soi[1]+10)

	minimum, maximum = 0, 255
	def s(v):
		nonlocal minimum
		minimum = v
	def b(v):
		nonlocal maximum
		maximum = v
	a = Scale(master, from_ = 0, to = 255, orient = HORIZONTAL, length = 500, command = s).place(x = 100, y = soi[1]+50)
	b = Scale(master, from_ = 0, to = 255, orient = HORIZONTAL, length = 500, command = b).place(x = 100, y = soi[1]+100)
	a = Label(master, text = 'min').place(x=40,y=soi[1]+50)
	b = Label(master, text = 'max').place(x=40,y=soi[1]+100)
	def go():			#really processing
		global data, soi
		nonlocal minimum, maximum
		slicing = np.array(data,copy = True)
		if var.get()[0] == 'h':
			slicing[slicing < int(minimum)] = 0
			slicing[slicing > int(maximum)] = 0
			slicing[slicing != 0] = 255
		else:
			slicing.resize(1,soi[0]*soi[1])
			tmp = slicing.tolist()
			for i in range(soi[0]*soi[1]):
				if (tmp[0][i] > int(minimum) and tmp[0][i] < int(maximum)):
					tmp[0][i] = 255
			slicing = np.asarray(tmp)
			slicing.resize(soi[1],soi[0])		#error detected and revised
			
		data = slicing		#exit
		data = Image.fromarray(np.uint8(data))
		show = ImageTk.PhotoImage(data)
		b = Label(master, image = show, width = soi[0], height = soi[1])
		b.image = show
		b.place(x=soi[0]+120,y=10)
		
	c = Button(master,text='gray-level slicing', command = go).place(x=100,y=soi[1]+150)
	d = Button(master,text='reload the image',command = gray).place(x=250,y=soi[1]+150)
#######################################################################################################
def bit():

	var = StringVar(master)
	var.set('0')
	method = OptionMenu(master, var, '1','2','3','4','5','6','7','8')
	method.place(x = 100, y = soi[1]+30)

	def do():
		global load, data, soi
		data = np.array(load)
		tmp = data.tolist()
		container = [0,0,0,0,0,0,0,0]
		for i in range(soi[1]):
			for j in range(soi[0]):
				container = [0,0,0,0,0,0,0,0]
				for k in range(8):
					container[k] = tmp[i][j] % 2
					tmp[i][j] = tmp[i][j] // 2
				tmp[i][j] = container[int(var.get()) - 1]
		data = np.asarray(tmp)
		data[data>0] = 255
		data = Image.fromarray(np.uint8(data))
		show = ImageTk.PhotoImage(data)
		b = Label(master, image = show, width = soi[0], height = soi[1])
		b.image = show
		b.place(x=soi[0]+120,y=10)
		
	a = Button(master, text = 'bit-plane', command = do).place(x=150,y=soi[1]+30)
	b = Label(master, text = '[0,0,0,0,0,0,0,0] <- [8,7,6,5,4,3,2,1](order)').place(x = 150, y=soi[1]+60)
#######################################################################################################
def smoothing():
	def g(v):
		global load, soi
		tmp = load.filter(ImageFilter.GaussianBlur(radius = int(v)))
		tmp = ImageTk.PhotoImage(tmp)
		b = Label(master, image = tmp, width = soi[0], height = soi[1])
		b.image = tmp
		b.place(x=soi[0]+120,y=10)

	def m(v):
		global load, soi
		tmp = load.filter(ImageFilter.MedianFilter(size = int(v)*2+1))
		tmp = ImageTk.PhotoImage(tmp)
		b = Label(master, image = tmp, width = soi[0], height = soi[1])
		b.image = tmp
		b.place(x=2*soi[0]+120+20,y=10)
	def mi(v):
		global load, soi
		tmp = load.filter(ImageFilter.MinFilter(size = int(v)*2+1))
		tmp = ImageTk.PhotoImage(tmp)
		b = Label(master, image = tmp, width = soi[0], height = soi[1])
		b.image = tmp
		b.place(x=3*soi[0]+120+40,y=10)

	a = Scale(master, from_ = 0, to = 25, orient = HORIZONTAL, length = 250, tickinterval=5, command = g).place(x = 100, y = soi[1]+50)
	a = Label(master, text = 'gaussian').place(x=75, y=soi[1]+50)
	c = Scale(master, from_ = 0, to = 15, orient = HORIZONTAL, length = 250, tickinterval=2, command = m).place(x = 100, y = soi[1]+100)
	c = Label(master, text = 'median').place(x=75, y=soi[1]+100)
	d = Scale(master, from_ = 0, to = 15, orient = HORIZONTAL, length = 250, tickinterval=3, command = mi).place(x = 100, y = soi[1]+150)
	d = Label(master, text = 'minfilter').place(x=75, y=soi[1]+150)
	e = Label(master, text = 'This function does not provide save feature').place(x=100,y=soi[1]+10)

def sharpening():
	var = StringVar(master)
	var.set('choose the kernel')
	method = OptionMenu(master, var, '1.3x3 (0,-1,0,-1,5,-1,0,-1,0)', '2.3x3 (-1,-1,-1,-1,9,-1,-1,-1,-1)','3.5x5 (25 in mid,others are -1)','4. 5x5 Unsharp masking')
	method.place(x = 100, y = soi[1]+30)

	def sh():
		global load
		if var.get()[0] == '1':
			tmp = load.filter(ImageFilter.Kernel(size = (3,3), kernel = (0,-1,0,-1,5,-1,0,-1,0)))
		elif var.get()[0] == '2':
			tmp = load.filter(ImageFilter.Kernel(size = (3,3), kernel = (-1,-1,-1,-1,9,-1,-1,-1,-1)))
		elif var.get()[0] == '3':
			tmp = load.filter(ImageFilter.Kernel(size = (5,5), kernel = (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,25,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)))
		elif var.get()[0] == '4':
			kn = 	(-1/256,-4/256,-6/256,-4/256,-1/256,-4/256,-16/256,-24/256,-16/256,-4/256,-6/256,-24/256,476/256,-24/256,-6/256,-4/256,-16/256,-24/256,-16/256,-4/256,-1/256,-4/256,-6/256,-4/256,-1/256)
			tmp = load.filter(ImageFilter.Kernel(size = (5,5), kernel = kn))
		tmp = ImageTk.PhotoImage(tmp)
		b = Label(master, image = tmp, width = soi[0], height = soi[1])
		b.image = tmp
		b.place(x=soi[0]+120,y=10)
	a = Button(master, text = 'go sharpening', command = sh).place(x=100,y=soi[1]+100)
	e = Label(master, text = 'This function does not provide save feature').place(x=100,y=soi[1]+10)
#######################################################################################################		
def fp():
	global load
	img = cv2.cvtColor(np.asarray(load),cv2.COLOR_RGB2BGR)
	img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = np.log(np.abs(fshift))

	plt.imshow(magnitude_spectrum, cmap = 'gray')
	plt.title('magnitude spectrum'), plt.xticks([]), plt.yticks([])
	plt.show()
#######################################################################################################
def fp2():
	global load
	img = cv2.cvtColor(np.asarray(load),cv2.COLOR_RGB2BGR)
	img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	f = np.fft.fft2(img)		#fft
	fshift = np.fft.fftshift(f)	#fft_shift

	amp_fs = np.abs(np.log(fshift))

	f1shift = np.fft.ifftshift(np.abs(fshift))
	amp = np.real(np.fft.ifft2(f1shift))
	amp = np.log(amp)
	
	plt.subplot(221),plt.imshow(amp_fs, cmap = 'gray')
	plt.title('abs'), plt.xticks([]), plt.yticks([])
	plt.subplot(222),plt.imshow(amp, cmap = 'gray')
	plt.title('amplitude only'), plt.xticks([]), plt.yticks([])

	ph_fs = np.angle(fshift)

	f2shift = np.exp(1j * np.angle(f))
	ang = np.abs(np.fft.ifft2(f2shift))
	
	plt.subplot(223),plt.imshow(ph_fs, cmap = 'gray')
	plt.title('phase spectrum'), plt.xticks([]), plt.yticks([])	
	plt.subplot(224),plt.imshow(ang, cmap = 'gray')
	plt.title('phase only'), plt.xticks([]), plt.yticks([])
	plt.show()


start = Button(master, text = 'open', command = open).place(x=0,y=0)
first = Button(master, text='gray', command = gray).place(x=0,y=40)
second = Button(master, text='bit', command = bit).place(x=0,y=70)
third = Button(master, text = 'smoothing', command = smoothing).place(x=0,y=100)
third_ = Button(master, text = 'sharpening', command = sharpening).place(x=0,y=130)
fourth = Button(master, text = 'FFT', command = fp).place(x=0,y=160)
fifth = Button(master, text = '2D-FFT',command = fp2).place(x=0,y=190)

def save():
	global data 
	tmp = Image.fromarray(np.uint8(data))
	master.filename = tkinter.filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	tmp.save(master.filename)
f = Button(master, text = 'finish', command = save).place(x=0,y=250)

mainloop()
