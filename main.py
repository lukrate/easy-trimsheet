import customtkinter as ctk
from lib.ets_images import EtsImage
from lib.ets_layers import Layers
from lib.ets_settings import *
from PIL import Image, ImageTk
from external.xcanvas import XCanvas
from widgets.ets_workzone import Workzone
# list of events
# pythontutorial.net/tkinter/tkinter-event-binding

#window
class App(ctk.CTk):
    def __init__(self):
        
        #setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1200x800")
        self.title("Photo Editor")
        self.minsize(800, 600)

        self.layers = Layers()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        #tabs
        tabview = ctk.CTkTabview(master=self)
        tabview.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        tabview.add("Workspace")  # add tab at the end
        tabview.tab("Workspace").configure()
        tabview.tab("Workspace").grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        tabview.tab("Workspace").rowconfigure(0, weight=1)
        tabview.tab("Workspace").columnconfigure(0, weight=1)

        tab_workzone = Workzone(master = tabview.tab("Workspace"), layers=self.layers)        
        tab_workzone.image=self.layers.stacked_trim
        tab_workzone.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

                
        tabview.add("Layers")  # add tab at the end
        tabview.add("Settings")  # add tab at the end
        tabview.set("Workspace")  # set currently visible tab

        

        #layout
        """ self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(2, weight=2) """
        

        self.mainloop()


if __name__ == "__main__":
    App()