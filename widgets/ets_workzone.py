from lib.ets_settings import *
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import Canvas, ttk
from icecream import ic
import numpy as np
import cv2
import math

from ets_workzone_layers import WorkzoneLayers

class Workzone(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        
        self.layers = layers

        self.image = np.full((self.layers.size, self.layers.size, 3), 0, dtype = np.uint8)
        self.image_ratio = self.layers.size / self.layers.size

        self.canvas_height = 0
        self.canvas_width = 0
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_level = 1        
        self.move_int = 0


        self.current_layer = ctk.IntVar(value=0)
        self.current_layer.trace_add('write', self.draw_rect)
        self.current_trim_h = ctk.IntVar(value = self.layers.size)
        self.current_pos_h = ctk.IntVar(value = 0)

        self.max_trim_h = ctk.IntVar(value = self.layers.size)
        self.max_pos_h = ctk.IntVar(value = self.layers.size)
        
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
            from_=0, to=self.layers.size, 
            orientation="vertical", 
            variable=self.current_pos_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_position.grid(row=2, column=1, padx=10, pady=20, sticky="ns")
        
        self.slider_position.bind("<MouseWheel>", command=lambda event: self.sliders_update_current_pos_h_on_mousewheel(-5 if event.delta < 0 else 5))
        self.slider_position.bind("<Shift-MouseWheel>", command=lambda event: self.sliders_update_current_pos_h_on_mousewheel(-1 if event.delta < 0 else 1))
        
        
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
            from_=self.layers.size, to=0,
            orientation="vertical",
            variable=self.current_trim_h,
            command=lambda value: self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get()))
        self.slider_trim.grid(row=2, column=2, padx=10, pady=20, sticky="ns")
        self.slider_trim.bind("<MouseWheel>", command=lambda event: self.sliders_update_current_trim_h_on_mousewheel(-5 if event.delta < 0 else 5))
        self.slider_trim.bind("<Shift-MouseWheel>", command=lambda event: self.sliders_update_current_trim_h_on_mousewheel(-1 if event.delta < 0 else 1))

        #endregion view
        
    
        # ------------- LAYERS --------------

        self.layers_view = WorkzoneLayers(self, self.layers)

        self.layers.workzone_widgets = self

        self.update_canvas()
        self.canvas.event_generate("<Configure>") 
        


    def resize_image(self, event):
        #----current_canvas_ratio
        if not event.width == 0:
            self.canvas_width = event.width
            self.canvas_height = event.height
        canvas_ratio = self.canvas_width / self.canvas_height
        #----resize image
        if canvas_ratio > self.image_ratio:
            image_height = self.canvas_height
            image_width = image_height * self.image_ratio
        else:
            image_width = self.canvas_width
            image_height = image_width / self.image_ratio
        #----place image
        self.canvas.delete("all")
        ### draw rect
        
        try:
            #resized_image = self.image.resize((int(image_width * self.zoom_level), int(image_height * self.zoom_level)))
            resized_image = cv2.resize(self.image, (int(image_width * self.zoom_level), int(image_height * self.zoom_level)))
            
            
            
            self.image_tk = ImageTk.PhotoImage(Image.fromarray(resized_image))
        except cv2.error:
            resized_image = Image.new(mode="RGB", size=(self.layers.size, self.layers.size)).resize((int(image_width * self.zoom_level), int(image_height * self.zoom_level)))
            self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(
            self.canvas_width/2 - self.offset_x ,
            self.canvas_height/2 - self.offset_y , 
            image = self.image_tk
        ) #image_position x,y - img
        cur_img = self.layers.images[self.current_layer.get()].current_height
        if self.current_layer.get() != 0:
            pos_offset_y = 0
            for i, image in enumerate(self.layers.images):
                if i < self.current_layer.get():
                    pos_offset_y += math.floor(image.current_height)
                else:
                    break
            pos_offset_y = pos_offset_y * (self.zoom_level/2)
        else: 
            pos_offset_y = 0
        
        ic(pos_offset_y)
        self.canvas.create_rectangle(
                (self.canvas_width/2 - self.offset_x) + (image_width * self.zoom_level)/2, 
                (self.canvas_height/2 - self.offset_y) - (image_height * self.zoom_level)/2 + pos_offset_y, 
                (self.canvas_width/2 - self.offset_x) - (image_width * self.zoom_level)/2, 
                (self.canvas_height/2 - self.offset_y) - (image_height * self.zoom_level)/2 + (cur_img * self.zoom_level)/2 + pos_offset_y, 
                outline='red')

        


    def draw_rect(self, var, index, mode):
        ic(self.current_layer.get())
        
        

    def zoom_on_mouse_wheel(self, event):
        if event.delta < 0:
            if self.zoom_level > 0.7:
                self.zoom_level -= .25
                
                if self.zoom_level < 1.1:
                    self.offset_x = 0
                    self.offset_y = 0
        else:
            if self.zoom_level < 2.5:
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
        if self.move_int == 0:
            new_pos_x = round((event.x - self.drag_origin_x))
            new_pos_y = round((event.y - self.drag_origin_y))
            self.offset_x = self.pos_origin_x - new_pos_x
            self.offset_y = self.pos_origin_y - new_pos_y
            self.move_int += 1
            self.canvas.event_generate("<Configure>")
        if self.move_int >= 4:
            self.move_int = 0
        else:
            self.move_int += 1
    
    def reset_canvas(self, event):
        self.offset_x = 0
        self.offset_y = 0
        self.pos_origin_x = 0
        self.pos_origin_y = 0
        self.zoom_level = 1
        self.canvas.event_generate("<Configure>")

    def sliders_update_current_pos_h_on_mousewheel(self, value):
        self.current_pos_h.set(self.current_pos_h.get() + value)
        self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get())

    def sliders_update_current_trim_h_on_mousewheel(self, value):
        self.current_trim_h.set(self.current_trim_h.get() - value)
        self.sliders_update_current_trim(self.current_trim_h.get(), self.current_pos_h.get())

    def sliders_update_current_trim(self, height, position):
        self.layers.images[self.current_layer.get()].trim_image(0, position, self.layers.size, height)
        self.set_sliders_max_values()
        self.layers.construct_image()

    def set_sliders_max_values(self):
        try:
            self.max_trim_h.set(self.layers.images[self.current_layer.get()].height - self.current_pos_h.get())
            self.slider_trim.configure(from_=self.max_trim_h.get())
            self.slider_trim.set(self.current_trim_h.get())
            if self.max_pos_h != self.layers.images[self.current_layer.get()].height:
                self.max_pos_h.set(self.layers.images[self.current_layer.get()].height)
                self.slider_position.configure(to=self.max_pos_h.get())
                self.slider_position.set(self.current_pos_h.get())
        except ZeroDivisionError:
            pass

    def update_canvas(self):
        self.image = self.layers.stacked_trim_array
        self.canvas.event_generate("<Configure>") 