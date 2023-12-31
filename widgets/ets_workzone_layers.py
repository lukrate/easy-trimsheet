from lib.ets_settings import *
import customtkinter as ctk

class WorkzoneLayers(ctk.CTkFrame):
    def __init__(self, master, layers, **kwargs):
        super().__init__(master, **kwargs)
        print(master)

        self.grid(row = 0, column = 3, sticky="nsew")
        #self.columnconfigure(0, weight=1)

        self.layers =  layers

        print("---->", range(0, int(len(self.layers.layers))))

        layers_label = ctk.CTkLabel(master = self, text="Layers")
        layers_label.grid(column=0, row=0, padx=0, pady=0)

        layer_selection = ctk.CTkOptionMenu(master = self, values=[str(x) for x in range(0, int(len(self.layers.layers)))],
                                         command= lambda value: master.change_current_layer(value))
        layer_selection.grid(column=0, row=1, padx=0, pady=0)