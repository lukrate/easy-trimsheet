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
        self.layers.export_widgets = self

        self.file_name = ctk.StringVar(value="")
        self.destination_folder = ctk.StringVar(value="")
        self.progressbar_value = ctk.DoubleVar(value=0.0)
        self.format = ".jpg"
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=180)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=180)

        # --------- EXPORT CHECKBOX -------- #

        self.export_options_frame = ctk.CTkFrame(self)
        self.export_options_frame.grid(column=1, row=1, pady=15, padx=15, rowspan=2, sticky="nsew")
        self.export_options_frame.columnconfigure(0, weight=1)
        self.export_options_frame.columnconfigure(1, weight=1)


        self.create_map_options()
        self.set_checkbox_default_values()

        # ---------------- GENERATE ---------------------- #
        self.generate_options_frame = ctk.CTkFrame(self)
        self.generate_options_frame.grid(column=2, row=1, pady=15, padx=15, rowspan=2, sticky="nsew")
        self.generate_label = ctk.CTkLabel(self.generate_options_frame, text="Generate")
        self.generate_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")

        self.genereate_arm = ctk.CTkCheckBox(self.generate_options_frame, text="ARM map")
        self.genereate_arm.grid(column = 0, row= 1 , padx = 12, pady = 8, sticky="w")

        self.genereate_id = ctk.CTkCheckBox(self.generate_options_frame, text="ID map")
        self.genereate_id.grid(column = 0, row= 2 , padx = 12, pady = 8, sticky="w")



        # ---------------- FILENAME ---------------------- #

        self.export_name_frame = ctk.CTkFrame(self)
        self.export_name_frame.grid(column=3, row=1, padx=15, pady=15, sticky="nsew")
        self.export_name_frame.columnconfigure(0, weight=1)
        self.export_name_label = ctk.CTkLabel(self.export_name_frame, text="File Name")
        self.export_name_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.export_name_input = ctk.CTkEntry(self.export_name_frame, placeholder_text="File Name", textvariable=self.file_name)
        self.export_name_input.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        
        # ---------------- FOLDER ---------------------- #
        self.export_folder_frame = ctk.CTkFrame(self)
        self.export_folder_frame.grid(column=3, row=2, padx=15, pady=15, sticky="nsew")
        self.export_folder_frame.columnconfigure(0, weight=150)
        self.export_folder_frame.columnconfigure(1, weight=1)
        
        self.export_folder_label = ctk.CTkLabel(self.export_folder_frame, text="Folder")
        self.export_folder_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.export_folder_input = ctk.CTkEntry(self.export_folder_frame, placeholder_text="Folder", textvariable=self.destination_folder)
        self.export_folder_input.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.export_open_folder = ctk.CTkButton(self.export_folder_frame, text="open", width=60,
            command= lambda: self.destination_folder.set(filedialog.askdirectory(initialdir=f"{curdir}/images"))
        )
        self.export_open_folder.grid(column=1, row=1, pady=5, padx=10, sticky="ew")
        

        # ---------------- FILE FORMAT ---------------------- #
        self.file_format_frame = ctk.CTkFrame(self)
        self.file_format_frame.grid(column=4, row=1, rowspan=2, padx=15, pady=15, sticky="nsew")
        self.file_format_frame.columnconfigure(0, weight=150)
        self.file_format_frame.rowconfigure(0, weight=1)
        self.file_format_frame.rowconfigure(1, weight=1)
        self.file_format_frame.rowconfigure(2, weight=1)
        self.file_format_frame.rowconfigure(3, weight=1)
        
        self.file_format_label = ctk.CTkLabel(self.file_format_frame, text="Format")
        self.file_format_label.grid(column=0, row=0, padx=10, pady=5, sticky="nw")
        self.file_format_menu = ctk.CTkOptionMenu(self.file_format_frame, values=FILE_FORMATS, command=lambda value: self.change_format_options(value))
        self.file_format_menu.grid(column=0, row=1, padx=5, sticky="nwe")

        self.options_frame = JpegOptions(self.file_format_frame)
        self.options_frame.grid(column=0, row=3, padx=4, pady=4, sticky="nsew")

        self.export_btn = ctk.CTkButton(self, text="Export", height=42,
            command=self.export_files
        )
        self.export_btn.grid(column=1, row=3, columnspan=4, pady=50, sticky="nsew")

        self.progressbar = ctk.CTkProgressBar(self, progress_color="teal", orientation="horizontal", variable=self.progressbar_value)
        self.progressbar.grid(column=1, row=4, columnspan=4, pady=5, sticky="nsew")

    def change_format_options(self, value):
        self.options_frame.grid_forget()
        if value == ".jpg":
            self.format = value
            self.options_frame = JpegOptions(self.file_format_frame)
            self.options_frame.grid(column=0, row=3, padx=4, pady=4, sticky="nsew")
        elif value == ".webp":
            self.format = value
            self.options_frame = WebpOptions(self.file_format_frame)
            self.options_frame.grid(column=0, row=3, padx=4, pady=4, sticky="nsew")
        elif value == ".png":
            self.format = value
            self.options_frame = PngOptions(self.file_format_frame)
            self.options_frame.grid(column=0, row=3, padx=4, pady=4, sticky="nsew")

    def create_map_options(self):
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
                    try:
                        if img.collection[child.cget("text")] != None:
                            child.select()
                            break
                    except KeyError:
                        continue

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
            self.layers.export_final_files(self.get_checkbox_true_values(), self.file_name.get(), self.destination_folder.get(), self.format, self.options_frame.get_values(), self.genereate_arm.get(), self.genereate_id.get())


class JpegOptions(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.quality = ctk.IntVar(value=100)
        self.optimize = ctk.BooleanVar(value=True)
        
        self.columnconfigure(0, weight=30)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        
        self.quality_label = ctk.CTkLabel(self, text="JPEG Quality")
        self.quality_label.grid(column=0, row=0, padx=10, pady=5, columnspan=2, sticky="nw")
        self.quality_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=20, variable=self.quality)
        self.quality_slider.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.quality_input = ctk.CTkEntry(self, textvariable=self.quality)
        self.quality_input.grid(column=1, row=1, padx=10, pady=5, sticky="ew")
        self.opitimize_label = ctk.CTkCheckBox(self, text="Optimize", variable=self.optimize)
        self.opitimize_label.grid(column=0, row=2, padx=10, pady=5, sticky="nw")
        
    def get_values(self):
        return {"quality": self.quality.get(), "optimize": self.optimize.get()}

class WebpOptions(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.quality = ctk.IntVar(value=100)
        self.lossless = ctk.BooleanVar(value=True)
        
        self.columnconfigure(0, weight=30)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        
        self.quality_label = ctk.CTkLabel(self, text="WEBP Quality")
        self.quality_label.grid(column=0, row=0, padx=10, pady=5, columnspan=2, sticky="nw")
        self.quality_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=20, variable=self.quality)
        self.quality_slider.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.quality_input = ctk.CTkEntry(self, textvariable=self.quality)
        self.quality_input.grid(column=1, row=1, padx=10, pady=5, sticky="ew")
        self.opitimize_label = ctk.CTkCheckBox(self, text="Lossless", variable=self.lossless)
        self.opitimize_label.grid(column=0, row=2, padx=10, pady=5, sticky="nw")

    def get_values(self):
        return {"quality": self.quality.get(), "lossless": self.lossless.get()}

class PngOptions(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.compression = ctk.IntVar(value=0)
        self.optimize = ctk.BooleanVar(value=True)
        
        self.columnconfigure(0, weight=30)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        
        self.quality_label = ctk.CTkLabel(self, text="PNG Compression (0:Off, 1:Speed, 9:Best)")
        self.quality_label.grid(column=0, row=0, padx=10, pady=5, columnspan=2, sticky="nw")
        self.quality_slider = ctk.CTkSlider(self, from_=0, to=9, variable=self.compression)
        self.quality_slider.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.quality_input = ctk.CTkEntry(self, textvariable=self.compression)
        self.quality_input.grid(column=1, row=1, padx=10, pady=5, sticky="ew")
        self.opitimize_label = ctk.CTkCheckBox(self, text="Optimize", variable=self.optimize)
        self.opitimize_label.grid(column=0, row=2, padx=10, pady=5, sticky="nw")

    def get_values(self):
        return {"compression": self.compression.get(), "optimize": self.optimize.get()}