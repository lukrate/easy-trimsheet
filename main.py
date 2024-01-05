import customtkinter as ctk
from lib.ets_images import EtsImage
from lib.ets_layers import Layers
from lib.ets_settings import *
from PIL import Image, ImageTk
from external.xcanvas import XCanvas
from widgets.ets_workzone import Workzone
from widgets.ets_exportzone import Exportzone
# list of events
# pythontutorial.net/tkinter/tkinter-event-binding

#window
class App(ctk.CTk):
    def __init__(self):
        
        #setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1200x800")
        self.title("Easy Trimsheet")
        self.minsize(800, 600)
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.layers = Layers()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        #----------------- TABS INIT
        tabview = ctk.CTkTabview(master=self, anchor="nw")
        tabview.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB WORKSPACE
        tabview.add("Workspace")  # add tab at the end
        tabview.tab("Workspace").grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        tabview.tab("Workspace").rowconfigure(0, weight=1)
        tabview.tab("Workspace").columnconfigure(0, weight=1)

        tab_workzone = Workzone(master = tabview.tab("Workspace"), layers=self.layers)        
        tab_workzone.image=self.layers.stacked_trim
        tab_workzone.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB LAYERS        
        tabview.add("Layers")  # add tab at the end

        #----------------- TAB EXPORT
        tabview.add("Export")  # add tab at the end
        tabview.tab("Export").grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        tabview.tab("Export").rowconfigure(0, weight=1)
        tabview.tab("Export").columnconfigure(0, weight=1)

        tab_workzone = Exportzone(master = tabview.tab("Export"), layers=self.layers)
        tab_workzone.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB SETTTINGS
        tabview.add("Settings")  # add tab at the end
        tabview.set("Export")  # set currently visible tab

        

        #layout
        """ self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(2, weight=2) """
        

        self.mainloop()


if __name__ == "__main__":
    App()