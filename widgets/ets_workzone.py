from lib.ets_settings import *
import lib.ets_store as store
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import Canvas

class Workzone(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        print(master)

        self.canvas_height = 0
        self.canvas_width = 0

        self.current_layer = ctk.IntVar(value=0)
        self.current_trim_h = ctk.IntVar(value = 350)
        self.current_pos_h = ctk.IntVar(value = 0)

        #self.current_trim_h.trace_add("write", lambda value: self.update_img(self.current_trim_h.get(), self.current_pos_h.get()))
        #self.current_pos_h.trace_add("write", lambda value: self.update_img(self.current_trim_h.get(), self.current_pos_h.get()))

        self.layers = layers

        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = Canvas(self, background=BACKGROUND_COLOR, bd="0", highlightthickness=0, relief="ridge")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.resize_image)

        self.slider_position = ctk.CTkSlider(
            self, 
            from_=10, to=2048, 
            orientation="vertical", 
            variable=self.current_pos_h,
            command=lambda value: self.update_img(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_position.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        
        self.slider_trim = ctk.CTkSlider(
            self,
            from_=10, to=2048,
            orientation="vertical",
            variable=self.current_trim_h,
            command=lambda value: self.update_img(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_trim.grid(row=0, column=2, padx=10, pady=20, sticky="nsew")
        
        self.image = Image.new(mode="RGB", size=(IMAGE_SIZE_DEFAULT, IMAGE_SIZE_DEFAULT))
        print(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

    def resize_image(self, event):
        print(event)
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

    
    def update_img(self, scale, position):
        self.layers.layers[self.current_layer.get()].trim_image(0, position, 2048, scale)
        self.layers.construct_image()
        self.image = self.layers.stacked_trim
        self.canvas.event_generate("<Configure>")
        #print(trimmed_img)

    def change_current_layer(self, value):
        print(value)
        value = int(value)
        self.current_layer.set(value)
        self.current_pos_h.set(self.layers.layers[value].current_pos_y)
        self.current_trim_h.set(self.layers.layers[value].current_height) 