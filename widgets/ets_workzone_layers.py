from lib.ets_settings import *
import customtkinter as ctk
from tkinter import filedialog
from ets_open_image_view import OpenImageView
from PIL import ImageTk
from os import curdir

class WorkzoneLayers(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        print(master)
        
        self.layers = layers
        self.open_image_window = None

        self.grid(row = 0, column = 3, sticky="nsew", rowspan=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=45)


        print("---->", range(0, int(len(self.layers.images))))

        self.layers_label = ctk.CTkLabel(master = self, text="Layers")
        self.layers_label.grid(column=0, row=0, padx=0, pady=10)

        self.button_add_picture = ctk.CTkButton(self, text="+", command=self.open_image_view)
        self.button_add_picture.grid(column=1, row=0, padx=0, pady=0, sticky="nse")

        self.layer_frame = ctk.CTkScrollableFrame(master=self)
        self.layer_frame.grid(column=0, row=1, padx=0, pady=0, columnspan=2, sticky="nsew")
        self.layer_frame.columnconfigure(0, weight=1)

        self.layer_blocks = []
        self.create_layers()

    def create_layers(self):
        self.layer_blocks = []
        for key, layer in enumerate(self.layers.images):
            print(key, layer)
            self.layer_blocks.append(WorkzoneLayer(self.layer_frame, self.layers, key))

    def open_image_view(self):
        self.path_value = (filedialog.askopenfile(initialdir=f"{curdir}/images").name)
            #self.import_func(path)
        print(self.path_value)
        self.layers.add_new_image(path=self.path_value)

        """ if self.open_image_window is None or not self.open_image_window.winfo_exists():
            self.open_image_window = OpenImageView(layers=self.layers)  # create window if its None or destroyed
            self.open_image_window.focus()  # if window exists focus it
        else:
            self.open_image_window.focus()  # if window exists focus it """


class WorkzoneLayer(ctk.CTkFrame):
    def __init__(self, master, layers, id, **kwargs):
        super().__init__(master, **kwargs)

        self.id = id
        try:
            if self.id == layers.workzone_widgets.current_layer.get():
                self.configure(fg_color = DARK_GREY) 
        except AttributeError:
            if self.id == 0:
                self.configure(fg_color = DARK_GREY) 

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
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

        self.grid(column=0, row=id, sticky="nsew", pady=10)