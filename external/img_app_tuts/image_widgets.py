import customtkinter as ctk
from tkinter import filedialog, Canvas
from os import curdir
from settings import *


class ImageImportWidget(ctk.CTkFrame):
    def __init__(self, master, import_func, **kwargs):
        super().__init__(master, **kwargs)
        
        self.import_func = import_func

        self.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

        self.button = ctk.CTkButton(self, text="open image", command=self.open_dialog)
        self.button.pack(expand=True)

    def open_dialog(self):
        try:
            path = filedialog.askopenfile(initialdir=f"{curdir}/images").name
            self.import_func(path)
            #self.grid_remove()
        except AttributeError:
            path = None
            pass
    
    def remove_widget(self):
        self.grid_remove()

class ImageCanvas(Canvas):
    def __init__(self, master, resize_image):
        super().__init__(master, background=BACKGROUND_COLOR, bd="0", highlightthickness=0, relief="ridge")
        self.grid(row=0, column=1, sticky="nsew")
        self.bind("<Configure>", resize_image)

class CloseButton(ctk.CTkButton):
    def __init__(self, master, close_func):
        super().__init__(master, text="x", text_color=WHITE, fg_color="transparent", width=40, height=40, hover_color=CLOSE_RED, command=close_func)
        self.place(relx = 0.99, rely = 0.01, anchor = "ne")