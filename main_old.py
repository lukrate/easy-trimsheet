import tkinter as tk
from tkinter import ttk
from lib.ets_images import EtsImage
from PIL import Image, ImageTk
from external.xcanvas import XCanvas
# list of events
# pythontutorial.net/tkinter/tkinter-event-binding

#window
window = tk.Tk()
window.title("Trim")
window.geometry("800x600")


#slider
scale_int = tk.IntVar(value = 600)
pos_int = tk.IntVar(value = 0)
scale = ttk.Scale(window, command=lambda value: update_img(scale_int.get(), pos_int.get()), from_=10, to=2048, length=2048, orient="horizontal", variable=scale_int)
scale.pack()
position = ttk.Scale(window, command=lambda value: update_img(scale_int.get(), pos_int.get()), from_=10, to=2048, length=2048, orient="horizontal", variable=pos_int)
position.pack()

canvas = XCanvas(window, scalewidget=True, x_axis=7, y_axis=7, width=2048, height=2048)


img1 = EtsImage("./images/Brick_wall_006_COLOR.jpg")
#print(img1)



#print(trimmed_img)
def update_img(scale, position):
    trimmed_img = img1.trim_image(img1.NP_image, 0, position, 2048, scale)
    #print(trimmed_img)
    print(trimmed_img.shape)
    print(canvas.width, canvas.height)
    image_layout = ImageTk.PhotoImage(Image.fromarray(trimmed_img))

    canvas.create_image(1, 1, image=image_layout ,anchor=tk.NW)
    canvas.image = image_layout


window.mainloop()