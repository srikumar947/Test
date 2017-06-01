from __future__ import print_function
import Tkinter as tki
from PIL import Image, ImageTk
from imutils.video import VideoStream
import time
import threading
import datetime
import imutils
import cv2
import os

class Video:
	def __init__(self, vs):
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None
 
		self.root = tki.Tk()
		self.panel = None
		self.panel2 = None
 
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
 
		self.root.wm_title("CSPS")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=300)

				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
		
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.pack(side="left", padx=10, pady=10)

				else:
					self.panel.configure(image=image)
					self.panel.image = image

				if self.panel2 is None:
					self.panel2 = tki.Label(image=image)
					self.panel2.image = image
					self.panel2.pack(side="right", padx=10, pady=10)

				else:
					self.panel2.configure(image=image)
					self.panel2.image = image
 
		except RuntimeError, e:
			print("RuntimeError")

	def onClose(self):
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()


vs = VideoStream().start()
time.sleep(2.0)

rec = Video(vs)
rec.root.mainloop()
