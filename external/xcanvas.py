# An extended Python/tkinter Canvas Window with zoom scale and extended bindings
# on which we can draw points, lines, rectangles, etc.
# See the Python tkinter module, Canvas class, for more usage details

import tkinter as tk
from tkinter import ttk

class XCanvas(tk.Canvas):
    def __init__(self, rootwin, **opt):
        width = opt.get("width", 1000)
        height = opt.get("height", 600)
        self.width = width
        self.height = height
        bg = opt.get("bg", "white")
        scrollbars = opt.get("scrollbars", True)
        scalewidget = opt.get("scalewidget", True)
        x_axis = opt.get("x_axis", 7)
        y_axis = opt.get("y_axis", 7)

        self.region = (-50, -50, width, height)
        self.rootwin = rootwin
        self.rootframe = tk.Frame(rootwin, width=width, height=height, bg=bg)
        self.rootframe.pack(expand=True, fill=tk.BOTH)
        tk.Canvas.__init__(self, self.rootframe, width=width, height=height, bg=bg, scrollregion=self.region)
        self.config(highlightthickness=0)

        if scrollbars:
            self.scrollbars()

        self.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
    
        # Scale Widget component
        self.scalewidget = ttk.Scale(self.rootframe, from_=1, to=3000, length=500,
                                    orient=tk.VERTICAL, command=self.resize)
        self.scalewidget.set(100)
        if scalewidget:
            self.scalewidget.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        else:
            # place the scale widget far away so we cannot see it on a normal display (1920x1600)
            self.scalewidget.place(x=100000, y=100000)
        #x1,y1,x2,y2 = self.bbox('all')
        #self.xview_scroll(-x2, "units")
        #self.yview_scroll(-y2, "units")
        self.xview_moveto(0)
        self.yview_moveto(0)
        #self.rootframe.focus_set()
        if x_axis or y_axis:
            self.draw_axis(x_axis, y_axis)
        self.bindings()

    def scrollbars(self):
        self.sbarV = tk.Scrollbar(self.rootframe, orient = tk.VERTICAL)
        self.sbarH = tk.Scrollbar(self.rootframe, orient = tk.HORIZONTAL)
        self.sbarV.config(command = self.yview)
        self.sbarH.config(command = self.xview)
        self.config(yscrollcommand = self.sbarV.set)
        self.config(xscrollcommand = self.sbarH.set)
        self.sbarV.pack(side = tk.RIGHT, fill = tk.Y)
        self.sbarH.pack(side = tk.BOTTOM, fill = tk.X)
    
    def bindings(self):
        self.bind("<Control-MouseWheel>", self.onCtrlMouseWheel)
        self.bind("<Alt-MouseWheel>", self.onAltMouseWheel)
        self.bind("<MouseWheel>", self.onMouseWheel)
        self.bind("<Shift-MouseWheel>", self.onShiftMouseWheel)
        self.bind("f", self.fit_canvas)
        self.bind("<Home>", self.fit_canvas)
        self.bind("<Up>", self.onArrowUp)
        self.bind("<Down>", self.onArrowDown)
        self.bind("<Left>", self.onArrowLeft)
        self.bind("<Right>", self.onArrowRight)
        self.bind("<Prior>", self.onArrowUp)
        self.bind("<Next>", self.onArrowDown)
        self.bind("<Shift-Prior>", self.onPrior)
        self.bind("<Shift-Next>", self.onNext)
        #self.bind("all", self.eventEcho)

    def show(self, force=False):
        if force or not self.winfo_ismapped():
            self.rootwin.iconify()
            self.rootwin.update()
            self.rootwin.deiconify()
            self.rootwin.lift()
            #self.rootwin.mainloop()
            #tk.mainloop()

    def hide(self):
        self.rootwin.iconify()

    def resize(self, percent):
        x1,y1,x2,y2 = self.region
        canvas_breadth = max(x2-x1, y2-y1)
        _region = self.config('scrollregion')[4].split()
        region = tuple(float(x) for x in _region)
        x1,y1,x2,y2 = region
        breadth = max(x2-x1, y2-y1)
        if breadth == 0:
            return
        r = float(percent) / 100
        if r < 0.01 or r > 30:
            return
        s = r / (float(breadth) / canvas_breadth)
        self.scale('all', 0, 0, s, s)
        nregion = tuple(x*r for x in self.region)
        self.config(scrollregion=nregion)
    
    #------------ Key bindings -------------

    def onCtrlMouseWheel(self, event):
        s = self.scalewidget.get()
        if event.delta > 0:
            s += 15
        else:
            s -= 15
        self.scalewidget.set(s)
    
    def onAltMouseWheel(self, event):
        s = self.scalewidget.get()
        if event.delta > 0:
            s += 5
        else:
            s -= 5
        self.scalewidget.set(s)
    
    def onMouseWheel(self, event):
        self.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def onArrowUp(self, event):
        if event.keysym == "Up":
            self.yview_scroll(-1, "units")
        else:
            self.yview_scroll(-1, "pages")
    
    def onArrowDown(self, event):
        if event.keysym == "Down":
            self.yview_scroll(1, "units")
        else:
            self.yview_scroll(1, "pages")
    
    def onArrowLeft(self, event):
        self.xview_scroll(-1, "units")
    
    def onArrowRight(self, event):
        #print(event.keysym)
        self.xview_scroll(1, "units")
    
    def onPrior(self, event):
        self.xview_scroll(1, "pages")
    
    def onNext(self, event):
        #print(event.keysym)
        self.xview_scroll(-1, "pages")
    
    def onShiftMouseWheel(self, event):
        self.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def fit_canvas(self, event):
        print(event.keysym)
        self.scalewidget.set(100)
    
    def draw_axis(self, m, n):
        self.create_line(-40, 0, 100*m, 0, width=1, fill='black', arrow='last')
        self.create_line(0, -40, 0, 100*n, width=1, fill='black', arrow='last')
        for i in range(1,m):
            self.create_line(100*i, -5, 100*i, 0, width=1, fill='black')
            self.create_text(100*i, -5, text=str(100*i), font='Consolas 8', anchor='s')
        for i in range(1,n):
            self.create_line(-5, 100*i, 0, 100*i, width=1, fill='black')
            self.create_text(-7, 100*i, text=str(100*i), font='Consolas 8', anchor='e')

    def eventEcho(self, event):
        print(event.keysym)

#--------------------------------------------------------------------------------------

def xcanvas_test():
    # This is where we create the canvas
    """ rootwin1 = tk.Tk()
    c1 = XCanvas(rootwin1, width=1000, height=800, bg="white")
    c1.create_rectangle(100, 120, 400, 230, width=2, outline='blue', fill='yellow')
    c1.create_rectangle(400, 320, 600, 530, width=2, outline='blue', fill='yellow')
    c1.create_oval(400, 320, 600, 530, width=2, outline='blue', fill='cyan')
    c1.create_line(200, 50, 500, 430, width=3, fill='blue') """

    rootwin2 = tk.Tk()
    c2 = XCanvas(rootwin2, scrollbars=False, scalewidget=True, x_axis=0, y_axis=0, width=1000, height=800, bg="cornsilk")
    c2.create_rectangle(100, 120, 400, 230, width=2, outline='red', fill='yellow')
    c2.create_oval(100, 120, 400, 230, width=2, outline='red', fill='cyan')
    c2.create_rectangle(400, 320, 600, 530, width=2, outline='red', fill='yellow')
    c2.create_line(200, 50, 500, 430, width=3, fill='red')

    #c1.show()
    #c2.show()
    #show_canvas()
    tk.mainloop()

if __name__ == "__main__":
    xcanvas_test()
