import customtkinter as ctk
import json
from tkinter import filedialog
from PIL import Image, ImageTk
from lib.ets_layers import Layers
from lib.ets_settings import *
from lib.utils import get_save_project_data
from widgets.ets_workzone import Workzone
from widgets.ets_exportzone import Exportzone
from widgets.ets_opening import Opening
from icecream import ic
# list of events
# pythontutorial.net/tkinter/tkinter-event-binding

class App(ctk.CTk):
    def __init__(self):        
        #setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        #self.geometry("1200x800")
        self.title(f"Easy Trimsheet - {VERSION}")
        self.state('zoomed')
        self.minsize(1000, 800)
        
        self.bind_all("<Button-1>", lambda event: self.focus_on_view(event))


        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.first_view = Opening(self, self.init_app_func)
        #self.construct_tabs()

        ico = Image.open(ICON_APP_PATH)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconbitmap()
        self.iconphoto(True, photo)
        self.mainloop()

    def init_app_func(self, size=None, path=None):
        self.state('zoomed')
        if path == None:
            self.layers = Layers(size)
        elif path != None:
            with open(path, 'r') as openfile:
                loaded_data = json.load(openfile)
            self.layers = Layers(loaded_data["size"])
            for image in loaded_data["images"]:
                self.layers.add_new_image(images_dict = image["collection"], height=image["current_height"], posx=image["current_pos_x"])
                self.layers.images[-1].is_rotate = image["is_rotate"]
                if image["is_rotate"]:
                    self.layers.images[-1].rotation_value = image["rotation_value"]
                    self.layers.images[-1].change_image_rotation(image["rotation_value"])
                    

        self.first_view.pack_forget()
        self.construct_tabs()
        
        try:
            self.layers.change_current_layer(0)
        except IndexError:
            pass
    
        self.layers.construct_image(update_layers=False)
            
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
        #self.tabview.add("Settings")  # add tab at the end
        self.tabview.set("Workspace")  # set currently visible tab

        # ------------- SAVE BUTTON --------------
        self.save_button = ctk.CTkButton(self, text="Save project", text_color=WHITE, fg_color="transparent", width=40, height=30, command=self.save_project)
        self.save_button.place(relx = 0.18, rely = 0.01, anchor = "nw")

        
    def save_project(self):
        formats = [("Easy Trim Sheet", ".ets")]
        file = filedialog.asksaveasfile(filetypes=formats, defaultextension=formats)
        file_content = json.dumps(get_save_project_data(self.layers))
        file.write(file_content)
        file.close()
        

    def focus_on_view(self, event):
        try:
            event.widget.focus_set()
        except AttributeError:
            pass

if __name__ == "__main__":
    App()