from lib.ets_settings import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from os import curdir
from icecream import ic
import math

class Exportzone(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)

        self.layers = layers

        self.file_name = ctk.StringVar(value="")
        self.destination_folder = ctk.StringVar(value="")
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=180)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=180)

        # --------- EXPORT BTN -------- #

        self.export_options_frame = ctk.CTkFrame(self)
        self.export_options_frame.grid(column=1, row=1, padx=5, rowspan=2, pady=30, sticky="ew")
        self.export_options_frame.columnconfigure(0, weight=1)
        self.export_options_frame.columnconfigure(1, weight=1)


        self.create_options()
        self.set_checkbox_default_values()

        
        self.export_name_frame = ctk.CTkFrame(self)
        self.export_name_frame.grid(column=3, row=1, padx=15, pady=15, sticky="sew")
        self.export_name_frame.columnconfigure(0, weight=1)
        self.export_name_label = ctk.CTkLabel(self.export_name_frame, text="File Name")
        self.export_name_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.export_name_input = ctk.CTkEntry(self.export_name_frame, placeholder_text="File Name", textvariable=self.file_name)
        self.export_name_input.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        
        self.export_folder_frame = ctk.CTkFrame(self)
        self.export_folder_frame.grid(column=3, row=2, padx=15, pady=15, sticky="new")
        self.export_folder_frame.columnconfigure(0, weight=150)
        self.export_folder_frame.columnconfigure(1, weight=1)
        
        self.export_folder_label = ctk.CTkLabel(self.export_folder_frame, text="Folder")
        self.export_folder_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.export_folder_input = ctk.CTkEntry(self.export_folder_frame, placeholder_text="Folder", textvariable=self.destination_folder)
        self.export_folder_input.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.export_open_folder = ctk.CTkButton(self.export_folder_frame, text="open", width=60,
            command= lambda: self.destination_folder.set(filedialog.askdirectory(initialdir=f"{curdir}/images"))
        )
        self.export_open_folder.grid(column=1, row=1, pady=5, sticky="ew")
        
        self.export_btn = ctk.CTkButton(self, text="Export", height=42,
            command=self.export_files
        )
        self.export_btn.grid(column=1, row=3, columnspan=3, pady=50, sticky="nsew")

    def create_options(self):
        self.export_options = []
        i = 0
        for key, value in FILE_NAME_PATTERNS.items():
            col = 0 if i % 2 == 0 else 1
            if not key == "normal":
                self.export_option = ctk.CTkCheckBox(self.export_options_frame, text=key)
                self.export_option.grid(column = col, row= math.floor(i / 2) , padx = 8, pady = 8, sticky="w")
                i += 1

    def set_checkbox_default_values(self):
        for key, child in self.export_options_frame.children.items():
            if isinstance(child, ctk.CTkCheckBox):
                for img in self.layers.images:
                    if img.collection[child.cget("text")] != None:
                        child.select()
                        break

    def get_checkbox_true_values(self):
        true_values = []
        for key, child in self.export_options_frame.children.items():
            if isinstance(child, ctk.CTkCheckBox):
                if child.get() == 1:
                    true_values.append(child.cget("text"))
        return true_values

    def export_files(self):
        if len(self.file_name.get()) <= 0:
            CTkMessagebox(message="No FILE NAME has been entered!", title="File Name", icon="warning")
        elif len(self.destination_folder.get()) <= 0:
            CTkMessagebox(message="No FOLDER selected!", title="Folder", icon="warning")
        else:
            self.layers.export_final_files(self.get_checkbox_true_values(), self.file_name.get(), self.destination_folder.get())

