from lib.ets_settings import *
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import Canvas

from ets_workzone_layers import WorkzoneLayers

class Workzone(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        print(master)

        self.canvas_height = 0
        self.canvas_width = 0

        self.current_layer = ctk.IntVar(value=0)
        self.current_trim_h = ctk.IntVar(value = 350)
        self.current_pos_h = ctk.IntVar(value = 0)

        self.layers = layers
        
        #region view
        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=30)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)


        # ------------- CANVAS --------------
        
        self.canvas = Canvas(self, background=BACKGROUND_COLOR, bd="0", highlightthickness=0, relief="ridge")
        self.canvas.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.canvas.bind("<Configure>", self.resize_image)

        # ------------- SLIDER 1 --------------
        self.label_position = ctk.CTkLabel(self, text="Position")
        self.label_position.grid(row=0, column=1, padx=10, pady=0, sticky="ew")

        self.slider_position = ctk.CTkSlider(
            self, 
            from_=10, to=2048, 
            orientation="vertical", 
            variable=self.current_pos_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_position.grid(row=1, column=1, padx=10, pady=20, sticky="ns")
        
        # ------------- SLIDER 2 --------------
        self.label_trim = ctk.CTkLabel(self, text="Height")
        self.label_trim.grid(row=0, column=2, padx=10, pady=0, sticky="ew")
        self.slider_trim = ctk.CTkSlider(
            self,
            from_=10, to=2048,
            orientation="vertical",
            variable=self.current_trim_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_trim.grid(row=1, column=2, padx=10, pady=20, sticky="ns")
        #endregion view

        # ------------- LAYERS --------------

        self.layers_view = WorkzoneLayers(self, self.layers)

        # ------------- DEFAULT IMAGE CREATION --------------

        self.image = Image.new(mode="RGB", size=(IMAGE_SIZE_DEFAULT, IMAGE_SIZE_DEFAULT))
        print(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.layers.workzone_widgets = self


    def resize_image(self, event):
        #current_canvas_ratio
        if not event.width == 0:
            self.canvas_width = event.width
            self.canvas_height = event.height
        canvas_ratio = self.canvas_width / self.canvas_height
        #resize image
        if canvas_ratio > self.image_ratio:
            image_height = self.canvas_height
            image_width = image_height * self.image_ratio
        else:
            image_width = self.canvas_width
            image_height = image_width / self.image_ratio
        #place image
        self.canvas.delete("all")
        resized_image = self.image.resize((int(image_width), int(image_height)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(self.canvas_width/2,self.canvas_height/2, image = self.image_tk)

    
    def sliders_update_current_trim(self, scale, position):
        self.layers.images[self.current_layer.get()].trim_image(0, position, 2048, scale)
        self.layers.construct_image()

    def update_canvas(self):
        self.image = self.layers.stacked_trim
        self.canvas.event_generate("<Configure>") 