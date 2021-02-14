import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame


class PyguguGuiApp:
    def __init__(self, master=None):
        # build ui
        root_frame = ttk.Frame(master)
        scrolledframe_3 = ScrolledFrame(root_frame, scrolltype='both')
        canvas_4 = tk.Canvas(scrolledframe_3.innerframe)
        canvas_4.config(background='#ff8040', height='539', width='1119')
        canvas_4.pack(side='top')
        scrolledframe_3.configure(usemousewheel=False)
        scrolledframe_3.pack(side='top')
        root_frame.config(height='200', width='200')
        root_frame.pack(side='top')

        # Main widget
        self.mainwindow = root_frame


    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = PyguguGuiApp(root)
    app.run()
