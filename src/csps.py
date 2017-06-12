from __future__ import print_function, division, absolute_import
import threespace_api as ts_api
from PIL import Image, ImageTk
from serial import Serial
import Tkinter as tk
import tkMessageBox
import numpy as np
import time
import sys
import cv2


class Graph(tk.Frame):
    def __init__(self, parent):
        global flag
        tk.Frame.__init__(self, parent)
        self.Line1 = [0 for x in range(100)]
        self.Line2 = [0 for x in range(100)]
        self.Line3 = [0 for x in range(100)]

        self.canvas = tk.Canvas(self, background="gray15")
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.canvas.create_line((0, 0, 0, 0), tag='X', fill='red', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Y', fill='blue', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Z', fill='green', width=1)
        
        self.canvas.grid(sticky="news")
        self.grid(sticky="news")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.com_port = None
        self.device_list = ts_api.getComPorts()
        if len(self.device_list) > 0:
            for self.device in self.device_list:
                self.cp = self.device.com_port
                self.port_info = ts_api.getDeviceInfoFromComPort(self.cp, poll_device=True)
                if self.port_info.dev_type == 'BT-H3' or self.port_info.dev_type == 'BT':
                    self.com_port = self.cp
            if not self.com_port:
                flag = 1
            else:
                self.tssensor = ts_api.TSBTSensor(self.com_port)
        else:
            flag = 1

    def on_resize(self, event):
        self.replot()

    def bg1(self):
        global button
        button.configure(bg="orange")
        button.after(3000, self.bg2)

    def bg2(self):
        global button
        button.configure(bg="green")

    def read_serial(self):
        global button
        data = self.tssensor.getCorrectedGyroRate()
        x, y, z = data[0], data[1], data[2]
        
        if x > 5 or x < -5 or y > 5 or y < -5 or z > 5 or z < -5:
            button.configure(bg="red")
            button.after(5000, self.bg1)

        self.append_values(x, y, z)
        self.after_idle(self.replot)
        self.after(10, self.read_serial)

    def append_values(self, x, y, z):
        self.Line1.append(float(x))
        self.Line1 = self.Line1[-1 * 100:]
        self.Line2.append(float(y))
        self.Line2 = self.Line2[-1 * 100:]
        self.Line3.append(float(z))
        self.Line3 = self.Line3[-1 * 100:]
        return

    def replot(self):
        w = self.winfo_width()
        h = self.winfo_height()
        max_X = max(self.Line1) + 1e-5
        max_Y = max(self.Line2) + 1e-5
        max_Z = max(self.Line3) + 1e-5
        max_all = 200.0
        coordsX, coordsY, coordsZ = [], [], []
        for n in range(0, 100):
            x = (w * n) / 100
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
    
    curWidth = video.winfo_width()
    curHeight = video.winfo_height()
    maxsize = (curWidth, curHeight)
    frame = cv2.resize(frame, maxsize)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video.imgtk = imgtk
    video.configure(image=imgtk)
    video.after(10, show_video)

flag = 0
root = tk.Tk()
menu = tk.Menu(root)

root.title("CSPS")
root.iconbitmap(default='CSPS_HR.ico')
root.config(menu=menu, background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Hello", command=hello)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=exit)

helpMenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="About", command=about)

video = tk.Label(root)
video.grid(row=0, column=0, sticky="news")
video.configure(width=300, height=300)

sensor = tk.Label(root)
sensor.grid(row=0, column=1, sticky="news")
sensor.configure(width=300, height=300)
sensor.grid_rowconfigure(0, weight=1)
sensor.grid_columnconfigure(0, weight=1)
graph = Graph(sensor)

if flag:
    sensor.destroy()
    tkMessageBox.showerror("Error","No sensor data")    
else:
    graph.read_serial()

button = tk.Button(text="Show", bg='green', fg='black', command=call)
button.grid(row=1, column=0, columnspan=2, sticky="news")

capture = cv2.VideoCapture(0)
show_video()
root.mainloop()
