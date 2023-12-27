import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        
        #setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1200x800")
        self.title("Photo Editor")
        self.minsize(800, 600)

        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        self.image_import_widget = ImageImportWidget(self, self.import_image)
        
        #widgets
        # import button (frame and button)

        #run
        self.mainloop()

    def import_image(self, path):
        self.image = Image.open(path)
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_canvas = ImageCanvas(self, self.resize_image)
        self.image_import_widget.grid_forget()
        self.close_button = CloseButton(self, self.close_image)

    def close_image(self):
        self.image_canvas.grid_forget()
        self.close_button.place_forget()
        self.image_import_widget = ImageImportWidget(self, self.import_image)

    def resize_image(self, event):
        print(event)
        #current_canvas_ratio
        canvas_ratio = event.width / event.height
        #resize image
        if canvas_ratio > self.image_ratio:
            image_height = event.height
            image_width = image_height * self.image_ratio
        else:
            image_width = event.width
            image_height = image_width / self.image_ratio
        #place image
        self.image_canvas.delete("all")
        resized_image = self.image.resize((int(image_width), int(image_height)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_canvas.create_image(event.width/2,event.height/2, image = self.image_tk)

App()