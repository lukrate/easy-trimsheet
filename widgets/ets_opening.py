import customtkinter as ctk
from tkinter import filedialog, Canvas
from os import curdir
from lib.ets_settings import *
from icecream import ic
from CTkMessagebox import CTkMessagebox
import lib.ets_settings


class Opening(ctk.CTkFrame):
    def __init__(self, master, init_app_func, **kwargs):
        super().__init__(master, **kwargs)
        
        self.init_app_func = init_app_func

        self.pack(expand=True)

        self.project_size = ctk.StringVar(value="2048")

        self.logo = ctk.CTkLabel(self, text="", image=LOGO_BUTTON)
        self.logo.pack(pady=64, padx=64)

        self.list_project_size = ctk.CTkOptionMenu(self, variable=self.project_size, values=IMAGE_SIZE_OPTIONS)
        self.list_project_size.pack(pady=12, padx=12)
        
        self.button_start_new = ctk.CTkButton(self, text="New Project", command=self.start_new_project)
        self.button_start_new.pack(pady=12, padx=12)

        self.button_load_project = ctk.CTkButton(self, text="Load Project", command=self.open_dialog)
        self.button_load_project.pack(pady=64, padx=24)

    def open_dialog(self):
        try:
            path = filedialog.askopenfile(initialdir=f"{curdir}/saved_projects").name
            self.init_app_func(path=path)
            
        except (AttributeError, FileNotFoundError) as e:
            path = None
            CTkMessagebox(message=f"{e.args[1]}", title=f"{e.args[1]}", icon="warning")
            pass
    
    def remove_widget(self):
        self.pack_forget()

    
    def start_new_project(self):
        self.init_app_func(size=int(self.project_size.get()))