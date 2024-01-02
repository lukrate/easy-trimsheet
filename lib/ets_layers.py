import os
from PIL import Image
import numpy as np
from ets_settings import *
from ets_images import EtsImage
import ets_store as store
import customtkinter as ctk

class Layers:
    def __init__(self):
        self.size = IMAGE_SIZE_DEFAULT
        self.background = self.generate_background(self.size)
 
        self.update_canvas = None
        self.images = [] #collections of images

        self.stacked_trim_array = [] #np array of images trimmed
        self.stacked_trim = None #final image
        self.free_space = IMAGE_SIZE_DEFAULT #freespace under existing images

        self.workzone_widgets = None

        self.test_images()



    def generate_background(self, size):
        img = Image.new(mode="RGB", size=(size, size))
        return img
    
    def add_new_image(self, image:object = None, path:str = None):
        if not path == None:
            self.images.append(EtsImage(path))
            self.images[-1].trim_image(0,0, height=350)
            self.construct_image()
            try:
                self.workzone_widgets.layers_view.create_layers()
            except AttributeError:
                pass
        else:
            self.images.append(image)

    def get_free_space(self):
        return IMAGE_SIZE_DEFAULT - self.stacked_trim_array.shape[0]


    def construct_image(self):
        final_img_array = None
        for k,v in enumerate(self.images):
            if k == 0:
                final_img_array = v.trimmed_image
            else:
                final_img_array = np.vstack((final_img_array, v.trimmed_image))
        final_img = self.background.copy()
        final_img.paste(Image.fromarray(final_img_array))
        self.stacked_trim_array = final_img_array
        self.stacked_trim = final_img
        self.free_space = self.get_free_space()

        print(self.workzone_widgets)
        if not self.workzone_widgets == None:
            print("update canvas")
            self.workzone_widgets.update_canvas()
    
    def change_current_layer(self, value):
        print(value)
        value = int(value)
        self.workzone_widgets.current_layer.set(value)
        self.workzone_widgets.current_pos_h.set(self.images[value].current_pos_y)
        self.workzone_widgets.current_trim_h.set(self.images[value].current_height)
        self.workzone_widgets.layers_view.create_layers()
    
    def test_images(self):
        path = os.path.join(os.getcwd(), 'images', 'Brick_wall_006_COLOR.jpg')
        self.add_new_image(path = path)
        path_2 = os.path.join(os.getcwd(), 'images', 'photo_2023-04-23_16-26-56.jpg')
        self.add_new_image(path = path_2)
        self.images[0].trim_image(0,0, height=350)
        self.images[1].trim_image(0,0, height=350)

        self.construct_image()
        #self.stacked_trim.show()    

if __name__ == "__main__":
    content = Layers()
    path = os.path.join(os.getcwd(), 'images', 'Brick_wall_006_COLOR.jpg')
    content.add_new_image(path = path)
    path_2 = os.path.join(os.getcwd(), 'images', 'photo_2023-04-23_16-26-56.jpg')
    content.add_new_image(path = path_2)
    content.images[0].trim_image(0,0, height=350)
    content.images[1].trim_image(0,0, height=350)

    content.construct_image()
    content.stacked_trim.show()