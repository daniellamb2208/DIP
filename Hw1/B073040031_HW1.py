from tkinter import *
import tkinter.filedialog as f
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as mp

#1
master = Tk()
master.title('DIP homework 1')
master.geometry('1024x768')

#2
def openfile():			#do everything
	master.filename = f.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	load = Image.open(master.filename)
	render = ImageTk.PhotoImage(load)
	soi = list(load.size)		#soi = size of input pic
	if soi[1] > 500:
		soi[1] = 500
	img = Label(master, image = render, width = soi[0], height = soi[1])
	img.image = render
	img.place(x=100, y=10)

	#3		
	variable = StringVar(master)
	variable.set('method')
	method = OptionMenu(master, variable, 'linear', 'exponentially', 'logarithmically')
	method.place(x=0, y = soi[1]+120)
	go = Label(master, text = 'choose method and check to adjust', bg = 'white').place(x=0, y = soi[1]+100)
	both = Label(master, text = 'a and b must be reset by user, even if the value is equal to default').place(x = 50,y = soi[1]+80)
	reminder = Label(master, text = 'if the pic is cut, click resize and the origin ratio size will appear on the right-hand side').place(x = 0, y = soi[1]+30)

	aa = 0.0
	bb = 0
	data_array = load	
	def ok():
		if variable.get() == 'linear':				
			def brightness(beta):
				global bb				
				bb = beta

			def contrast(alpha):
				global aa
				aa = alpha

			def go():
				global aa,bb
				global data_array
				data_array = np.array(load)
				data_array = data_array * float(aa)
				data_array = np.round(data_array)
				data_array = data_array + float(bb)
				data_array[data_array > 255] = 255
				data_array[data_array < 0] = 0
				data_array = np.round(data_array)
				data_array = Image.fromarray(np.uint8(data_array))
				tmp = ImageTk.PhotoImage(data_array)
				x = Label(master, image = tmp, width = soi[0], height = soi[1])
				x.image = tmp
				x.place(x = soi[0]+120, y = 10)
			a = Scale(master, from_ = 0, to = 10, orient = HORIZONTAL, length = 500, tickinterval=2.00, resolution = 0.01, command = contrast)
			b = Scale(master, from_ = -255, to = 255, orient = HORIZONTAL, length = 500, tickinterval=50, command = brightness)
			c = Button(master, text = 'adjust', command = go)
			
			a.place(x=150, y = soi[1]+100)
			b.place(x=150, y = soi[1]+150)
			c.place(x=0, y = soi[1]+180)
			
			a = Label(master, text = 'a')
			b = Label(master, text = 'b')
			a.place(x = 150, y = soi[1]+90)
			b.place(x = 150, y = soi[1]+140)
			

		elif variable.get() == 'exponentially':

			def brightness(beta):
				global bb				
				bb = beta

			def contrast(alpha):
				global aa
				aa = alpha
			def go():
				global aa,bb
				global data_array
				data_array = np.array(load)					
				data_array = data_array * float(aa)
				data_array = data_array + float(bb)
				data_array = np.exp(data_array)
				data_array = np.round(data_array)
				data_array[data_array > 255] = 255
				data_array[data_array < 0] = 0
				data_array = np.round(data_array)
				data_array = Image.fromarray(np.uint8(data_array))
				tmp = ImageTk.PhotoImage(data_array)
				x = Label(master, image = tmp, width = soi[0], height = soi[1])
				x.image = tmp
				x.place(x = soi[0]+120, y = 10)
			a = Scale(master, from_ = 0, to = 5, orient = HORIZONTAL, length = 500, resolution = 0.001, command = contrast)
			b = Scale(master, from_ = -255, to = 255, orient = HORIZONTAL, length = 500, tickinterval=50, command = brightness)
			c = Button(master, text = 'adjust', command = go)
			a.place(x=150, y = soi[1]+100)
			b.place(x=150, y = soi[1]+150)
			c.place(x=0, y = soi[1]+180)
			
			a = Label(master, text = 'a')
			b = Label(master, text = 'b')
			a.place(x = 150, y = soi[1]+90)
			b.place(x = 150, y = soi[1]+140)


		elif variable.get() == 'logarithmically':
			def brightness(beta):
				global bb				
				bb = beta

			def contrast(alpha):
				global aa
				aa = alpha
			def go():
				global aa,bb
				global data_array
				data_array = np.array(load)					
				data_array = data_array * float(aa)
				data_array = data_array + float(bb)
				data_array = np.log(data_array)
				data_array = np.round(data_array)
				data_array[data_array > 255] = 255
				data_array[data_array < 0] = 0
				data_array = np.round(data_array)
				data_array = Image.fromarray(np.uint8(data_array))
				tmp = ImageTk.PhotoImage(data_array)
				x = Label(master, image = tmp, width = soi[0], height = soi[1])
				x.image = tmp
				x.place(x = soi[0]+120, y = 10)
			a = Scale(master, from_ = 0, to = 1<<63 -1, orient = HORIZONTAL, length = 500, resolution = 0.001, command = contrast)
			b = Scale(master, from_ = 1, to = 1<<63 -1, orient = HORIZONTAL, length = 500, command = brightness)
			c = Button(master, text = 'adjust', command = go)
			a.place(x=150, y = soi[1]+100)
			b.place(x=150, y = soi[1]+150)
			c.place(x=0, y = soi[1]+180)
			
			a = Label(master, text = 'a')
			b = Label(master, text = 'b')
			a.place(x = 150, y = soi[1]+90)
			b.place(x = 150, y = soi[1]+140)


	b = Button(master, text = 'method check', command = ok)
	b.place(x=0, y=soi[1]+150)

	#4
	new = data_array
	def resize(s):
		global data_array
		global new		
		r = float(s) / 100
		o = load.size
		width = int(o[0] * r)
		height = int(o[1] * r)
		new = data_array.resize( (width, height), Image.BILINEAR)
		tmp = ImageTk.PhotoImage(new)
		x = Label(master, image = tmp, width = soi[0], height = soi[1])
		x.image = tmp
		x.place(x=soi[0]+120, y=10)

	def savefile():
		global new
		master.filename = f.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
		new.save(master.filename)
	
	percent = Label(master, text = 'size(%)', font=('Arial', 12)).place(x = 0, y=soi[1]+220)
	size = Scale(master, from_ = 1, to = 300, orient = HORIZONTAL, length = 500, command = resize)
	size.place(x = 150, y = soi[1]+200)
	s = Button(master, text = 'save', command = savefile)
	s.place(x=0, y=50)

	#5
	def qq():
		im2 = ImageOps.equalize(load, mask = None)		
		def show():
			im2.show()	
		ouput = Button(master, text = 'show', command = show).place(x=0,y = soi[1]+280)
		n,bins,patches = mp.hist(im2)
		mp.title('H')
		mp.grid(True)
		mp.show()
		

	eq = Button(master, text = 'histogram equalization', command = qq).place(x = 0, y = soi[1]+250)

man = Label(master, text = 'click to start', font=('Arial', 12)).place(x = 0, y = 30)	
o = Button(master, text = 'open', command = openfile)#1
o.place(x=0, y=0)


mainloop()

