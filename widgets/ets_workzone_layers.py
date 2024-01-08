from lib.ets_settings import *
import customtkinter as ctk
from tkinter import filedialog
from ets_open_image_view import OpenImageView
from PIL import ImageTk
from os import curdir
from lib.utils import get_image_dictionnary
from icecream import ic

class WorkzoneLayers(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        

        self.layers = layers
        self.open_image_window = None
        self.is_first_generation = True

        self.grid(row = 0, column = 3, sticky="nsew", rowspan=3)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=45)

        self.layers_label = ctk.CTkLabel(master = self, text="Layers")
        self.layers_label.grid(column=0, row=0, padx=0, pady=5)

        self.layers_map_list = ctk.CTkOptionMenu(self, values=self.layers.available_maps, command=lambda value: self.change_current_map(value))
        self.layers_map_list.grid(column=1, row=0, pady=5, sticky="ew")
        self.layers_map_list.grid_forget()

        self.button_add_picture = ctk.CTkButton(self, text="+", command=self.open_image_view, width=48, height=32)
        self.button_add_picture.grid(column=2, row=0, padx=0, pady=0, sticky="nse")

        self.layer_frame = ctk.CTkScrollableFrame(master=self)
        self.layer_frame.grid(column=0, row=1, padx=2, pady=0, columnspan=3, sticky="nsew")
        self.layer_frame.columnconfigure(0, weight=1)
        self.layer_frame.configure(fg_color=DARK_GREY)

        self.layer_blocks = []
        self.create_layers()

    def create_layers(self):
        self.layer_blocks = []
        for ls_child in self.layer_frame.grid_slaves():
            ls_child.destroy()
        for key, layer in enumerate(self.layers.images):
            self.layer_blocks.append(WorkzoneLayer(self.layer_frame, self.layers, key))
        
        if len(self.layer_blocks) > 0:
            self.layers_map_list.grid(column=1, row=0, pady=5, sticky="ew")
            self.layers_map_list.configure(require_redraw=True, values=self.layers.available_maps)
        if self.is_first_generation:
            self.layers_map_list.set("color")
            self.is_first_generation = False

    def open_image_view(self):
        images_path = (filedialog.askdirectory(initialdir=f"{curdir}/images"))
        self.layers.add_new_image(get_image_dictionnary(images_path))
    
    def change_current_map(self, map_name):
        self.layers.change_all_material_map(map_name)
        

        """ if self.open_image_window is None or not self.open_image_window.winfo_exists():
            self.open_image_window = OpenImageView(layers=self.layers)  # create window if its None or destroyed
            self.open_image_window.focus()  # if window exists focus it
        else:
            self.open_image_window.focus()  # if window exists focus it """


class WorkzoneLayer(ctk.CTkFrame):
    def __init__(self, master, layers, id, **kwargs):
        super().__init__(master, **kwargs)
        
        self.layers = layers
        self.id = id
        try:
            if self.id == layers.workzone_widgets.current_layer.get():
                self.configure(fg_color = LIGHT_GREY) 
        except AttributeError:
            if self.id == 0:
                self.configure(fg_color = LIGHT_GREY) 

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.thumbnail = ctk.CTkImage(light_image=layers.images[id].pil_image, size=(72,72))
        self.thumbnail_button = ctk.CTkButton(
            self,
            image=self.thumbnail,
            text="", 
            width=0, height=0, 
            border_spacing=0,
            command= lambda : layers.change_current_layer(self.id)
        )
        self.thumbnail_button.grid(column=0, rowspan=2, sticky="nsw")
        
        self.thumbnail_label = ctk.CTkLabel(self, text=f"Layer {id}")
        self.thumbnail_label.grid(column=1, row=0, sticky="nsw", padx=20)

        self.duplicate_button = ctk.CTkButton(self, text="D", width=28, command= lambda: self.layers.duplicate_layer(self.id))
        self.duplicate_button.grid(column=2, row=1, padx=5, sticky="e")

        self.remove_button = ctk.CTkButton(self, text="X", width=28, command= lambda: self.layers.remove_layer(self.id))
        self.remove_button.grid(column=3, row=1, padx=5, sticky="e")
        
        if self.id != 0:
            self.move_top_button = ctk.CTkButton(self, text="▲", width=28, command= lambda: self.layers.move_layer(self.id, direction= -1))
            self.move_top_button.grid(column=4, row=0, padx=5, sticky="e")
        
        if self.id != len(self.layers.images) -1:
            self.move_down_button = ctk.CTkButton(self, text="▼", width=28, command= lambda: self.layers.move_layer(self.id, direction= 1))
            self.move_down_button.grid(column=4, row=1, padx=5, sticky="e")

        self.grid(column=0, row=id, sticky="nsew", pady=10)