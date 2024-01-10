import customtkinter as ctk
from tkinter import filedialog, Canvas
from os import curdir
from lib.ets_settings import *


class Opening(ctk.CTkFrame):
    def __init__(self, master, init_app_func, **kwargs):
        super().__init__(master, **kwargs)
        
        self.init_app_func = init_app_func

        self.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

        self.button_start = ctk.CTkButton(self, text="New Project", command=self.open_dialog)
        self.button_start.pack(expand=True)

        self.button_load = ctk.CTkButton(self, text="New Project", command=self.open_dialog)
        self.button_load.pack(expand=True)

    def open_dialog(self):
        try:
            path = filedialog.askopenfile(initialdir=f"{curdir}/images").name
            self.init_app_func(path)
            #self.grid_remove()
        except AttributeError:
            path = None
            pass
    
    def remove_widget(self):
        self.grid_remove()