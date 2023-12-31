import os
from PIL import Image
import numpy as np
from ets_settings import *
from ets_images import EtsImage
import ets_store as store

class Layers:
    def __init__(self):
        self.size = IMAGE_SIZE_DEFAULT
        self.background = self.generate_background(self.size)
        
        self.layers = []
        self.stacked_trim = None

        self.test_images()

    def generate_background(self, size):
        img = Image.new(mode="RGB", size=(size, size))
        return img
    
    def add_new_image(self, image:object = None, path:str = None):
        if not path == None:
            self.layers.append(EtsImage(path))
            self.layers[-1].trim_image(0,0, height=350)
            self.construct_image()
        else:
            self.layers.append(image)

    def construct_image(self):
        final_img_array = None
        for k,v in enumerate(self.layers):
            if k == 0:
                final_img_array = v.trimmed_image
            else:
                final_img_array = np.vstack((final_img_array, v.trimmed_image))
        final_img = self.background.copy()
        final_img.paste(Image.fromarray(final_img_array))
        print(final_img)
        self.stacked_trim = final_img
    
    
    def test_images(self):
        path = os.path.join(os.getcwd(), 'images', 'Brick_wall_006_COLOR.jpg')
        self.add_new_image(path = path)
        path_2 = os.path.join(os.getcwd(), 'images', 'photo_2023-04-23_16-26-56.jpg')
        self.add_new_image(path = path_2)
        self.layers[0].trim_image(0,0, height=350)
        self.layers[1].trim_image(0,0, height=350)

        self.construct_image()
        #self.stacked_trim.show()    

if __name__ == "__main__":
    content = Layers()
    path = os.path.join(os.getcwd(), 'images', 'Brick_wall_006_COLOR.jpg')
    content.add_new_image(path = path)
    path_2 = os.path.join(os.getcwd(), 'images', 'photo_2023-04-23_16-26-56.jpg')
    content.add_new_image(path = path_2)
    content.layers[0].trim_image(0,0, height=350)
    content.layers[1].trim_image(0,0, height=350)

    content.construct_image()
    content.stacked_trim.show()