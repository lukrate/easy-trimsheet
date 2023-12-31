import customtkinter as ctk
from tkinter import filedialog
from os import curdir

class OpenImageView(ctk.CTkToplevel):
    def __init__(self, layers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")

        self.layers = layers

        self.path_value = ctk.StringVar(value="Load New Image")

        self.label = ctk.CTkLabel(self, text="Load new image", textvariable=self.path_value)
        self.label.pack(padx=20, pady=20)

        self.button = ctk.CTkButton(self, text="open image", command=self.open_dialog)
        self.button.pack(expand=True)

    def open_dialog(self):
        try:
            self.path_value.set(filedialog.askopenfile(initialdir=f"{curdir}/images").name)
            #self.import_func(path)
            print(self.path_value)
            self.layers.add_new_image(path=self.path_value.get())
            #self.grid_remove()
        except AttributeError:
            path = None
            pass

