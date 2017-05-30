from Tkinter import *

root = Tk()
text = Text(root)
text.insert(INSERT, "Hello ")
text.insert(END, "world")
text.pack()

root.mainloop()

# pyinstaller -w python_gui_test.py