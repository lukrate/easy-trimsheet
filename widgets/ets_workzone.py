from lib.ets_settings import *
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import Canvas, ttk
from icecream import ic

from ets_workzone_layers import WorkzoneLayers

class Workzone(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)

        self.image = Image.new(mode="RGB", size=(IMAGE_SIZE_DEFAULT, IMAGE_SIZE_DEFAULT))
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.canvas_height = 0
        self.canvas_width = 0
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_level = 1

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
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=120)


        # ------------- CANVAS --------------
        
        self.canvas = Canvas(self, background=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, bd="0", highlightthickness=0, relief="ridge")
        self.canvas.grid(row=0, column=0, sticky="nsew", rowspan=3)
        self.canvas.bind("<Configure>", self.resize_image)
        self.canvas.bind('<MouseWheel>', self.zoom_on_mouse_wheel)
        self.canvas.bind('<ButtonPress-1>', self.move_from_click)
        self.canvas.bind('<B1-Motion>', self.move_to_on_click)
        self.canvas.bind('<Button-5>', self.zoom_on_mouse_wheel)  # zoom for Linux, wheel scroll down
        self.canvas.bind('<Button-4>', self.zoom_on_mouse_wheel) # zoom for Linux, wheel scroll up
        self.canvas.bind('r', self.reset_canvas)
        # ------------- SLIDER 1 --------------
        self.label_position = ctk.CTkLabel(self, text="Position")
        self.label_position.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        
        self.input_position = ctk.CTkEntry(
            self, 
            width=50,
            textvariable=self.current_pos_h,
            placeholder_text=0
        )
        self.input_position.bind("<Return>", command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.input_position.grid(row=1, column=1, padx=20, pady=0, sticky="ew")

        self.slider_position = ctk.CTkSlider(
            self, 
            from_=10, to=2048, 
            orientation="vertical", 
            variable=self.current_pos_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_position.grid(row=2, column=1, padx=10, pady=20, sticky="ns")
        
        
        # ------------- SLIDER 2 --------------
        self.label_trim = ctk.CTkLabel(self, text="Height")
        self.label_trim.grid(row=0, column=2, padx=10, pady=0, sticky="ew")
        self.input_trim = ctk.CTkEntry(
            self, 
            width=50,
            textvariable=self.current_trim_h,        
        )
        self.input_trim.bind("<Return>", command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.input_trim.grid(row=1, column=2, padx=20, pady=0, sticky="ew")
        self.slider_trim = ctk.CTkSlider(
            self,
            from_=10, to=2048,
            orientation="vertical",
            variable=self.current_trim_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_trim.grid(row=2, column=2, padx=10, pady=20, sticky="ns")
        #endregion view

        # ------------- LAYERS --------------

        self.layers_view = WorkzoneLayers(self, self.layers)

        # ------------- DEFAULT IMAGE CREATION --------------

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
        try:
            resized_image = self.image.resize((int(image_width * self.zoom_level), int(image_height * self.zoom_level)))
        except AttributeError:
            resized_image = Image.new(mode="RGB", size=(IMAGE_SIZE_DEFAULT, IMAGE_SIZE_DEFAULT)).resize((int(image_width * self.zoom_level), int(image_height * self.zoom_level)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(
            self.canvas_width/2 - self.offset_x ,
            self.canvas_height/2 - self.offset_y , 
            image = self.image_tk
        ) #image_position x,y - img
    
    def zoom_on_mouse_wheel(self, event):
        if event.delta < 0:
            if self.zoom_level > 0.7:
                self.zoom_level -= .25
                
                if self.zoom_level < 1.1:
                    self.offset_x = 0
                    self.offset_y = 0
        else:
            self.zoom_level += .25
            self.offset_x += (event.x - self.canvas_width/2) / 2
            self.offset_y += (event.y - self.canvas_height/2) / 2
        self.canvas.event_generate("<Configure>")
    

    def move_from_click(self, event):
        self.drag_origin_x = event.x
        self.drag_origin_y = event.y
        self.pos_origin_x = self.offset_x
        self.pos_origin_y = self.offset_y

    def move_to_on_click(self, event):
        new_pos_x = round((event.x - self.drag_origin_x))
        new_pos_y = round((event.y - self.drag_origin_y))
        self.offset_x = self.pos_origin_x - new_pos_x
        self.offset_y = self.pos_origin_y - new_pos_y
        self.canvas.event_generate("<Configure>")
    
    def reset_canvas(self, event):
        self.offset_x = 0
        self.offset_y = 0
        self.pos_origin_x = 0
        self.pos_origin_y = 0
        self.zoom_level = 1
        self.canvas.event_generate("<Configure>")

    def sliders_update_current_trim(self, scale, position):
        self.layers.images[self.current_layer.get()].trim_image(0, position, 2048, scale)
        self.layers.construct_image()

    def update_canvas(self):
        self.image = self.layers.stacked_trim
        self.canvas.event_generate("<Configure>") 