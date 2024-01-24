from lib.ets_settings import *
import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from os import curdir
from lib.utils import get_image_dictionnary
from icecream import ic
from copy import copy

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
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=45)

        self.layers_label = ctk.CTkLabel(master = self, text="Layers")
        self.layers_label.grid(column=0, row=0, padx=0, pady=5)

        self.layers_map_list = ctk.CTkOptionMenu(self, values=self.layers.available_maps, command=lambda value: self.change_current_map(value))
        self.layers_map_list.grid(column=1, row=0, pady=5, sticky="ew")
        self.layers_map_list.grid_forget()

        self.show_outline = ctk.CTkCheckBox(self, text="Show Outline", command=lambda: self.layers.construct_image())
        self.show_outline.grid(column=2,row=0, pady=5, padx=10, sticky="ew")

        self.button_add_picture = ctk.CTkButton(self, text="", image=PLUS_BUTTON, command=self.open_image_view, width=48, height=32)
        self.button_add_picture.grid(column=3, row=0, padx=0, pady=0, sticky="nse")

        self.layer_frame = ctk.CTkScrollableFrame(master=self)
        self.layer_frame.grid(column=0, row=1, padx=2, pady=0, columnspan=4, sticky="nsew")
        self.layer_frame.columnconfigure(0, weight=1)
        self.layer_frame.configure(fg_color=DARK_GREY)

        self.layer_blocks = []
        self.create_layers()

    def create_layers(self):
        self.layer_blocks = []
        for ls_child in self.layer_frame.grid_slaves():
            ls_child.destroy()
        for key, image in enumerate(self.layers.images):
            new_layer = WorkzoneLayer(self.layer_frame, self.layers, key)
            new_layer.rotation_menu.set(image.rotation_value)
            self.layer_blocks.append(new_layer)

        
        if len(self.layer_blocks) > 0:
            self.layers_map_list.grid(column=1, row=0, pady=2, sticky="ew")
            self.layers_map_list.configure(require_redraw=True, values=self.layers.available_maps)
        if self.is_first_generation:
            self.layers_map_list.set("color")
            self.is_first_generation = False

    def open_image_view(self):
        images_path = (filedialog.askopenfile(initialdir=f"{curdir}/images"))
        try:
            images_path = os.path.split(images_path.name)[0]
        except AttributeError:
            print("open path failed")

        try:
            self.layers.change_all_material_map("color")
            self.layers.add_new_image(get_image_dictionnary(images_path))
        except TypeError as e:
            CTkMessagebox(title="Color Map", message="No Color Map found! \n \nYou need a image with '_col_', '_color_' in the name.",
                  icon="warning", option_1="OK")
            pass
    
    def change_current_map(self, map_name):
        self.layers.change_all_material_map(map_name)


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
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.thumbnail = self.get_or_create_thumbnail(id)
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

        self.rotation_menu = ctk.CTkOptionMenu(self, values=ROTATIONS_OPTIONS, command=lambda value: self.layers.change_image_rotation(value, self.id))
        self.rotation_menu.grid(column=1, row=1, padx=5, sticky="w")
        
        # ______________________ BUTTONS
        self.button_frame = ctk.CTkFrame(self, height=30)
        self.button_frame.grid(column=2, row=1, padx=5, sticky="e")

        self.duplicate_button = ctk.CTkButton(self.button_frame, text="", image=DUPLICATE_BUTTON, width=28, command= lambda: self.layers.duplicate_layer(self.id))
        self.duplicate_button.grid(column=0, row=0, padx=5, pady=5, sticky="e")

        self.change_button = ctk.CTkButton(self.button_frame, text="", image=RECYCLE_BUTTON, width=28, command= lambda: self.change_material(self.id))
        self.change_button.grid(column=1, row=0, padx=5, pady=5, sticky="e")

        self.remove_button = ctk.CTkButton(self.button_frame, text="", image=CLOSE_BUTTON, width=28, command= lambda: self.delete_layer(self.id))
        self.remove_button.grid(column=2, row=0, padx=5, pady=5, sticky="e")
        
        #_______________________ END BUTTONS

        if self.id != 0:
            self.move_top_button = ctk.CTkButton(self, text="▲", width=28, command= lambda: self.layers.move_layer(self.id, direction= -1))
            self.move_top_button.grid(column=3, row=0, padx=5, sticky="e")
        
        if self.id != len(self.layers.images) -1:
            self.move_down_button = ctk.CTkButton(self, text="▼", width=28, command= lambda: self.layers.move_layer(self.id, direction= 1))
            self.move_down_button.grid(column=3, row=1, padx=5, sticky="e")

        self.grid(column=0, row=id, sticky="nsew", pady=10)

    def change_material(self, id):
        images_path = (filedialog.askopenfile(initialdir=f"{curdir}/images"))
        try:
            images_path = os.path.split(images_path.name)[0]
        except AttributeError:
            pass
        try:
            self.layers.change_existing_image(id, get_image_dictionnary(images_path))
        except TypeError:
            pass

    def delete_layer(self, id):
        box = CTkMessagebox(title="Delete the layer ?", message="Delete the layer ?",
                  icon="warning", option_1="OK", option_2="Cancel")
        
        resp = box.get()
        if resp == "OK":
            self.layers.remove_layer(id)
        else:
            pass

    def get_or_create_thumbnail(self, id):

        thumb_dict = self.layers.images[id].thumbnails

        if self.layers.current_map_type in thumb_dict:
            return thumb_dict[self.layers.current_map_type]
        else:
            img = ctk.CTkImage(light_image=self.layers.images[id].pil_image, size=(72,72))
            self.layers.images[id].thumbnails[self.layers.current_map_type] = img
            return img