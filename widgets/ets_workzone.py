from lib.ets_settings import *
import customtkinter as ctk
from tkinter import Canvas

class Workzone(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print(master)

        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = Canvas(self, background=BACKGROUND_COLOR, bd="0", highlightthickness=0, relief="ridge")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.slider_position = ctk.CTkSlider(self, from_=10, to=2048, orientation="vertical")
        self.slider_position.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        
        self.slider_trim = ctk.CTkSlider(self, from_=10, to=2048, orientation="vertical")
        self.slider_trim.grid(row=0, column=2, padx=10, pady=20, sticky="nsew")        