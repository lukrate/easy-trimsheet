import customtkinter as ctk
from lib.ets_layers import Layers
from lib.ets_settings import *
from widgets.ets_workzone import Workzone
from widgets.ets_exportzone import Exportzone
from widgets.ets_opening import Opening
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
        self.bind_all("<Button-1>", lambda event: self.focus_on_view(event))

        self.layers = Layers()


        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #first_view = Opening(self, self.construct_tabs)
        self.construct_tabs()
        

        self.mainloop()


    def construct_tabs(self):
        #----------------- TABS INIT
        self.tabview = ctk.CTkTabview(master=self, anchor="nw")
        self.tabview.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB WORKSPACE
        self.tabview.add("Workspace")  # add tab at the end
        self.tabview.tab("Workspace").grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        self.tabview.tab("Workspace").rowconfigure(0, weight=1)
        self.tabview.tab("Workspace").columnconfigure(0, weight=1)

        tab_workzone = Workzone(master = self.tabview.tab("Workspace"), layers=self.layers)        
        tab_workzone.image=self.layers.stacked_trim
        tab_workzone.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB LAYERS        
        #self.tabview.add("Layers")  # add tab at the end

        #----------------- TAB EXPORT
        self.tabview.add("Export")  # add tab at the end
        self.tabview.tab("Export").grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        self.tabview.tab("Export").rowconfigure(0, weight=1)
        self.tabview.tab("Export").columnconfigure(0, weight=1)

        tab_workzone = Exportzone(master = self.tabview.tab("Export"), layers=self.layers)
        tab_workzone.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        #----------------- TAB SETTTINGS
        self.tabview.add("Settings")  # add tab at the end
        self.tabview.set("Workspace")  # set currently visible tab
        

        

    def focus_on_view(self, event):
        try:
            event.widget.focus_set()
        except AttributeError:
            pass

if __name__ == "__main__":
    App()