import customtkinter as ctk
from tkinter import filedialog, Canvas
from os import curdir
from lib.ets_settings import *
from icecream import ic


class Opening(ctk.CTkFrame):
    def __init__(self, master, init_app_func, **kwargs):
        super().__init__(master, **kwargs)
        
        self.init_app_func = init_app_func

        self.pack(expand=True)

        self.project_size = ctk.StringVar(value="2048")


        self.list_project_size = ctk.CTkOptionMenu(self, variable=self.project_size, values=IMAGE_SIZE_OPTIONS)
        self.list_project_size.pack(pady=12, padx=12)
        
        self.button_start_new = ctk.CTkButton(self, text="New Project", command=self.start_new_project)
        self.button_start_new.pack(pady=12, padx=12)

        self.button_load_project = ctk.CTkButton(self, text="Load Project (coming soon)", command=self.open_dialog, state="disabled")
        self.button_load_project.pack(pady=12, padx=12)

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

    
    def start_new_project(self):
        self.init_app_func(size=int(self.project_size.get()))
        ic(self.project_size.get())