from __future__ import print_function, division, absolute_import
import threespace_api as ts_api
from PIL import Image, ImageTk
from serial import Serial
import Tkinter as tk
import numpy as np
import time
import sys
import cv2


class Graph(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.npoints = 100
        self.Line1 = [0 for x in range(self.npoints)]
        self.Line2 = [0 for x in range(self.npoints)]
        self.Line3 = [0 for x in range(self.npoints)]
        self.canvas = tk.Canvas(self, background="gray15")
        self.canvas.create_line((0, 0, 0, 0), tag='X', fill='red', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Y', fill='blue', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Z', fill='green', width=1)
        self.canvas.grid(sticky="news")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="news")
        self.tssensor = ts_api.TSBTSensor('COM7')

    def bg(self):
        global button
        button.configure(bg="green")

    def read_serial(self):
        global button
        data = self.tssensor.getCorrectedGyroRate()
        x, y, z = data[0], data[1], data[2]
        
        if x > 5 or x < -5:
            button.configure(bg="red")
            button.after(2000, self.bg)

        if y > 5 or y < -5:
            button.configure(bg="red")
            button.after(2000, self.bg)
        
        if z > 5 or z < -5:
            button.configure(bg="red")
            button.after(2000, self.bg)

        self.append_values(x, y, z)
        self.after_idle(self.replot)
        self.after(10, self.read_serial)

    def append_values(self, x, y, z):
        self.Line1.append(float(x))
        self.Line1 = self.Line1[-1 * self.npoints:]
        self.Line2.append(float(y))
        self.Line2 = self.Line2[-1 * self.npoints:]
        self.Line3.append(float(z))
        self.Line3 = self.Line3[-1 * self.npoints:]
        return

    def replot(self):
        w = self.winfo_width()
        h = self.winfo_height()
        max_X = max(self.Line1) + 1e-5
        max_Y = max(self.Line2) + 1e-5
        max_Z = max(self.Line3) + 1e-5
        max_all = 200.0
        coordsX, coordsY, coordsZ = [], [], []
        for n in range(0, self.npoints):
            x = (w * n) / self.npoints
            coordsX.append(x)
            coordsX.append(h - ((h * (self.Line1[n]+100)) / max_all))
            coordsY.append(x)
            coordsY.append(h - ((h * (self.Line2[n]+100)) / max_all))
            coordsZ.append(x)
            coordsZ.append(h - ((h * (self.Line3[n] + 100)) / max_all))
        self.canvas.coords('X', *coordsX)
        self.canvas.coords('Y', *coordsY)
        self.canvas.coords('Z', *coordsZ)


def hello():
    subRoot = tk.Tk()
    subRoot.title("Welcome")

    text = tk.Label(subRoot)
    text.config(text="Welcome to CSPS")
    text.pack()
    subRoot.after(5000, lambda: subRoot.destroy())

def about():
    subRoot = tk.Tk()
    subRoot.title("About")

    text = tk.Label(subRoot)
    text.config(text="You are using CSPS v1.0")
    text.pack()
    subRoot.after(5000, lambda: subRoot.destroy())

def exit():
    root.destroy()

def call():
    subRoot = tk.Tk()
    subRoot.title("Details")

    text = tk.Label(subRoot)
    text.config(text="Testing")
    text.pack()

def show_video():
    
    _, frame = capture.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    
    video.imgtk = imgtk
    video.configure(image=imgtk)
    video.after(10, show_video)

root = tk.Tk()
menu = tk.Menu(root)

root.title("CSPS")
root.config(menu=menu, background='black')

fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Hello", command=hello)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=exit)

helpMenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="About", command=about)

video = tk.Label(root)
video.grid(row=1, column=0)

sensor = tk.Frame(root)
sensor.grid(row=1, column=1)
graph = Graph(sensor)
graph.read_serial()

button = tk.Button(text="Show", bg='green', fg='black', command=call)
button.grid(row=2, columnspan=2)

capture = cv2.VideoCapture(0)
show_video()
root.mainloop()
