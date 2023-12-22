import tkinter as tk
from tkinter import ttk, scrolledtext
from easyImages import easyImage
from PIL import Image
# list of events
# pythontutorial.net/tkinter/tkinter-event-binding

#window
window = tk.Tk()
window.title("Sliders")
window.geometry("800x600")


#slider
scale_int = tk.IntVar(value = 600)
scale = ttk.Scale(window, command=lambda value: print(scale_int.get()), from_=0, to=600, length=600, orient="vertical", variable=scale_int)
scale.pack()


img1 = easyImage("./images/Brick_wall_006_COLOR.jpg")
print(img1)
trimmed_img = img1.trim_image(img1.values["NP_image"], 0, 800, 0, scale_int.get())

image_layout = tk.Image(Image.fromarray(trimmed_img).crop(0,0,255,255))
image_layout.pack()



window.mainloop()