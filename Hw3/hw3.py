from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

master = Tk()
master.title('DIP Homework3')
master.geometry('1280x960')

# soi is size of image [width, height]

def homomorphic_filter():
    loadin = cv2.imread('Fig0460a.tif')
    img = np.double(cv2.cvtColor(loadin, cv2.COLOR_BGR2GRAY))
    soi = list(img.shape)
    rL, rH, c, D0 = 0.4, 3.0, 5, 20         # parameter
    h_fft = np.fft.fft2(np.log(img+1))
    G, H = np.zeros(soi), np.zeros(soi)
    m, n = np.floor(soi[0]/2), np.floor(soi[1]/2)
    for i in range(soi[0]):
        for j in range(soi[1]):
            G[i,j] = (i-m)**2 + (j-n)**2
            H[i,j] = (rH-rL) * (np.exp(c*(-G[i,j]/(D0**2)))) + rL
    done = np.real(np.exp(np.fft.ifft2(H*h_fft)))
    plt.subplot(1,2,1), plt.imshow(loadin), plt.title('Origin')
    plt.subplot(1,2,2), plt.imshow(done, cmap='gray'), plt.title('Homomorphic')
    plt.show()

def part_two():
    load, soi = None, []
    
    def display():
        nonlocal load, soi

        load = Image.open('Lenna_512_color.tif')
        render = ImageTk.PhotoImage(load)
        soi = list(load.size)
        img = Label(master, image = render, width = soi[0], height = soi[1])
        img.image = render
        img.place(x=150, y=10)

    def rgb_component():
        nonlocal load, soi

        data = load.getdata()
        r_channel = [(d[0], 0, 0) for d in data]
        g_channel = [(0, d[1], 0) for d in data] 
        b_channel = [(0, 0, d[2]) for d in data]
        o_channel = [(d[0],d[1],d[2]) for d in data]    #origin data

        img_r = img_g = img_b = load
        img_r.putdata(r_channel);plt.subplot(1,3,1), plt.imshow(img_r), plt.title('red component')
        img_g.putdata(g_channel);plt.subplot(1,3,2), plt.imshow(img_g), plt.title('green component')
        img_b.putdata(b_channel);plt.subplot(1,3,3), plt.imshow(img_b), plt.title('blue component')
        plt.show()
        load.putdata(o_channel)     # recovery

    def hsi():
        nonlocal load, soi

        rgb = cv2.cvtColor(np.asarray(load), cv2.COLOR_BGR2RGB)
        bgr = np.float32(rgb) / 255.0

        b = bgr[:,:,0]
        g = bgr[:,:,1]
        r = bgr[:,:,2]

        H = np.copy(r)
        for i in range(0,soi[0]):
            for j in range(0,soi[1]):
                x = 0.5 * ( (r[i][j]-g[i][j]) + (r[i][j]-b[i][j]))
                y = math.sqrt( (r[i][j]-g[i][j])**2  + ((r[i][j]-b[i][j])*(g[i][j]-b[i][j])) )
                z = math.acos(x/y)
                if b[i][j] < g[i][j]:
                    H[i][j] = z
                else:
                    H[i][j] = ((360*math.pi)/180.0) - z

        min = np.minimum(np.minimum(r,g),b)
        S = 1 - (3 / (r+g+b+0.001) * min)

        I = np.divide(b+g+r, 3.0)

        plt.subplot(2,3,2),plt.imshow(load),plt.title('Origin')
        plt.subplot(2,3,4),plt.imshow(H,cmap='gray'),plt.title('Hue')
        plt.subplot(2,3,5),plt.imshow(S,cmap='gray'),plt.title('Saturation')
        plt.subplot(2,3,6),plt.imshow(I,cmap='gray'),plt.title('Intensity')
        plt.show()

    def complement():
        nonlocal load, soi

        data = load.getdata()
        rgb_complement = [(255-d[0], 255-d[1], 255-d[2]) for d in data]
        tmp = Image.new('RGBX',soi)
        tmp.putdata(rgb_complement)
        tmp = ImageTk.PhotoImage(tmp)
        img = Label(master, image = tmp, width = soi[0], height = soi[1])
        img.image = tmp
        img.place(x=150 + soi[0] + 10, y = 10)

    def Average_kernal():
        nonlocal load, soi

        smooth = load.filter(ImageFilter.Kernel((5,5),(1/273,4/273,7/273,4/273,1/273,4/273,16/273,26/273,16/273,4/273,7/273,26/273,41/273,26/273,7/273,4/273,16/273,26/273,16/273,4/273,1/273,4/273,7/273,4/273,1/273)))
        render = ImageTk.PhotoImage(smooth)
        img = Label(master, image = render, width = soi[0], height = soi[1])
        img.image = render
        img.place(x=150 + soi[0] + 10, y = 10)

    def Laplacian():
        nonlocal load, soi
        
        sharpen = load.filter(ImageFilter.Kernel((3,3),(1,1,1,1,-9,1,1,1,1)))
        render = ImageTk.PhotoImage(sharpen)
        img = Label(master, image = render, width = soi[0], height = soi[1])
        img.image = render
        img.place(x=150 + soi[0] + 10, y = 10)

    def Segment():
        nonlocal load, soi

        upper_purple = np.array([155,255,255])
        lower_purple = np.array([125,43,46])

        img = cv2.cvtColor(np.asarray(load), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_purple, upper_purple)
        leather = cv2.bitwise_and(img, img, mask=mask)
        leather = cv2.cvtColor(leather, cv2.COLOR_HSV2BGR)
        
        tmp = Image.fromarray(cv2.cvtColor(leather,cv2.COLOR_BGR2RGB))
        render = ImageTk.PhotoImage(tmp)
        l = Label(master, image = render, width = soi[0], height = soi[1])
        l.image = render
        l.place(x=150+soi[0]+10, y=10)
        

    display()
    rgbs_component = Button(master, text = 'RGB component', bg = 'white', command = rgb_component).place(x=0,y=100)
    rgb_to_hsi = Button(master, text = 'RGB to HSI', command = hsi).place(x=0,y=150)            ###########     to-do
    rgb_component = Button(master, text = 'RGB complement', command = complement).place(x=0,y=200)
    smoothing = Button(master, text = 'Smoothing', command = Average_kernal).place(x=0,y=250)
    sharpening = Button(master, text = 'Sharpening', command = Laplacian).place(x=0, y=280)
    segment = Button(master, text = 'Segment', command = Segment).place(x=0,y=330)

homomo = Button(master, text='homomorphic', width = 10, command=homomorphic_filter).place(x=0, y=0)
color = Button(master, text = 'color image',width = 10, command = part_two).place(x=0, y=30)

mainloop()
