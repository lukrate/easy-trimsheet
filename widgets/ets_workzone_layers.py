from lib.ets_settings import *
import customtkinter as ctk
from ets_open_image_view import OpenImageView

class WorkzoneLayers(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        print(master)
        
        self.layers =  layers
        self.open_image_window = None

        self.grid(row = 0, column = 3, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        print("---->", range(0, int(len(self.layers.layers))))

        layers_label = ctk.CTkLabel(master = self, text="Layers")
        layers_label.grid(column=0, row=0, padx=0, pady=10)

        button_add_picture = ctk.CTkButton(self, text="+", command=self.open_image_view)
        button_add_picture.grid(column=1, row=0, padx=0, pady=0, sticky="nse")

        layer_selection = ctk.CTkOptionMenu(master = self, values=[str(x) for x in range(0, int(len(self.layers.layers)))],
                                         command= lambda value: master.change_current_layer(value))
        layer_selection.grid(column=0, row=1, padx=0, pady=10, columnspan=2, sticky="ew")

    def open_image_view(self):
        if self.open_image_window is None or not self.open_image_window.winfo_exists():
            self.open_image_window = OpenImageView(layers=self.layers)  # create window if its None or destroyed
            self.open_image_window.focus()  # if window exists focus it
        else:
            self.open_image_window.focus()  # if window exists focus it