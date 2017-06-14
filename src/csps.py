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


#constants for framerates replay duration etc - Ishan
CONST_videoRateMs = 10
CONST_replayDuration = 4
CONST_processingSlack = 0.4
CONST_cacheLimit = 1000/CONST_videoRateMs * CONST_replayDuration * CONST_processingSlack

#flags to check for replay and recordings - Ishan
replay_on = False
record_on = False

#videocache and replay cache and current frame in replay - Ishan
videoCache = []
replayCache = []
replay_frame = 0

class CSPS(tk.Frame):
    def __init__(self, parent):

        global flag
        tk.Frame.__init__(self, parent)

        self.x = [0 for i in range(100)]
        self.y = [0 for i in range(100)]
        self.z = [0 for i in range(100)]

        self.canvas = tk.Canvas(self, background="gray15")
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.grid(sticky="news")

        self.canvas.create_line((0, 0, 0, 0), tag='X', fill='red', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Y', fill='blue', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Z', fill='green', width=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="news")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

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
                print ("true")
                self.tssensor = ts_api.TSBTSensor(self.com_port)
        else:
            flag = 1

    def on_resize(self, event):
        self.replot()

    def bg1(self):
        global button
        button.configure(bg="orange")
        button.after(1000, self.bg2)

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

            #shifts pre impact to replay cache and enables after impact recording - Ishan
            """global record_on
            record_on = True"""
            
            global replayCache
            replayCache = videoCache[:]
            print("shifted")
            global replay_frame
            replay_frame = 0

        self.add(data)
        self.after_idle(self.replot)

    def add(self, data):
        self.x.append(float(data[0]))
        self.x = self.x[-100:]

        self.y.append(float(data[1]))
        self.y = self.y[-100:]

        self.z.append(float(data[2]))
        self.z = self.z[-100:]

        return

    def replot(self):
        w = self.winfo_width()
        h = self.winfo_height()

        max_X = max(self.x) + 1e-5
        max_Y = max(self.y) + 1e-5
        max_Z = max(self.z) + 1e-5

        coordsX, coordsY, coordsZ = [], [], []

        for n in range(0, 100):
            x = (w * n) / 100

            coordsX.append(x)
            coordsX.append(h - ((h * (self.x[n] + 100)) / 200.0))

            coordsY.append(x)
            coordsY.append(h - ((h * (self.y[n] + 100)) / 200.0))

            coordsZ.append(x)
            coordsZ.append(h - ((h * (self.z[n] + 100)) / 200.0))

        self.canvas.coords('X', *coordsX)
        self.canvas.coords('Y', *coordsY)
        self.canvas.coords('Z', *coordsZ)

    

    #Code to replay a impact recording - Ishan
    def replay(self):
        global replay_frame
        if(len(replayCache)  < 1):
            video2.configure(text="No Impact so far")
            global replay_on
            replay_on = False
            return
        
        img = replayCache[replay_frame]
        #print(replay_frame)
        
        
        imgtk = ImageTk.PhotoImage(image=img)
        video2.imgtk = imgtk
        video2.configure(image=imgtk)
        replay_frame += 1

        #once youve replayed the recording stop and reset - Ishan
        if replay_frame == len(replayCache):
            global replay_on
            replay_on = False
            replay_frame = 0

    def video(self):
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)

            

        curWidth = video.winfo_width()
        curHeight = video.winfo_height()
        maxsize = (curWidth, curHeight)
        frame = cv2.resize(frame, maxsize)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)

        #keeps caching for preimpact recording - Ishan
        if record_on == False or True:
            if len(videoCache) > CONST_cacheLimit/2:
                videoCache.pop(0)
                videoCache.append(img)
                #print("limit reached")
            else:
                videoCache.append(img)
        """
        #in the event of an impact triggers postimpact recording into replayCache - Ishan
        global record_on
        if record_on:
            if len(replayCache) < CONST_cacheLimit:
                replayCache.append(img)
            else:
                #turn off recording as replay has been recorded
                record_on = False
        """
    
        imgtk = ImageTk.PhotoImage(image=img)
        video.imgtk = imgtk
        video.configure(image=imgtk)

    
    def show(self):
        global flag, flag2

        if replay_on:
            self.replay()
        
        self.video()

        if flag:
            if flag2:
                flag2 = 0
                sensor.destroy()
                # tkMessageBox.showerror("Error", "No sensor data")
        else:
            self.read_serial()

        self.after(CONST_videoRateMs, self.show)


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
    """subRoot = tk.Tk()
    subRoot.title("Details")

    text = tk.Label(subRoot)
    text.config(text="Testing")
    text.pack()"""
    #replay video from last impact
    print("Turning on replay")
    global replay_on
    replay_on = True

root = tk.Tk()
menu = tk.Menu(root)
flag = 0
flag2 = 1
root.title("CSPS")
# root.iconbitmap(default='CSPS_HR.ico')
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

button = tk.Button(text="Show", bg='green', fg='black', command=call)
button.grid(row=2, column=0, columnspan=3, sticky="news")

video = tk.Label(root)
video.grid(row=0, column=0, sticky="news")
video.configure(width=300, height=300)
capture = cv2.VideoCapture(0)

sensor = tk.Label(root)
sensor.grid(row=0, column=1, sticky="news")
sensor.configure(width=300, height=300)
sensor.grid_rowconfigure(0, weight=1)
sensor.grid_columnconfigure(0, weight=1)

video2 = tk.Label(root)
video2.grid(row=0, column=2, sticky="news")
video2.configure(text="WAITING ON REPLAY")

obj = CSPS(sensor)
obj.show()

root.mainloop()

