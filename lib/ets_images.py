from ets_settings import *
from PIL import Image
import cv2
import numpy as np
from icecream import ic
import os

class EtsImage:

    def __init__(self, images_dict):
        self.collection = images_dict
        #ic(self.collection)
        self.path = os.path.join(self.collection["path"], self.collection["color"])
        self.width = None
        self.height = None
        self.dtype = None
        self.shape:tuple = None # (w, h, layers)
        self.img_layer:int = None # number of layer in the image

        self.pil_image = None
        self.np_image = None
        self.trimmed_image = None

        self.openImage()

    def openImage(self, generaeted_img = None):
        if generaeted_img == None:
            self.pil_image = Image.open(self.path).convert("RGB")
        else:
            self.pil_image = generaeted_img

        self.np_image = np.array(self.pil_image)
    
        self.dtype = self.np_image.dtype
        self.shape = self.np_image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        #self.layer = self.shape[2]
        self.image_ratio = self.width / self.height

    def trim_image(self, x, y, width=IMAGE_SIZE_DEFAULT, height=IMAGE_SIZE_DEFAULT):
        self.current_pos_x = x
        self.current_pos_y = y
        self.current_height = height
        self.current_width = width
        self.trimmed_image = self.np_image[y:y + height, x:x + width]

    def get_trimmed_image(self):
        return self.trimmed_image
    
    def change_material_map(self, map_name):
        if self.collection[map_name] != None:
            self.path = os.path.join(self.collection["path"], self.collection[map_name])
            self.openImage()
        else:
            self.generate_image(map_name)
        self.trim_image(self.current_pos_x, self.current_pos_y, self.current_width, self.current_height)

    def generate_image(self, map_name):
        if map_name == "normal" or map_name == "normal_dx" or map_name == "normal_gl":
            self.openImage(generaeted_img=Image.new(mode="RGB", size=(self.width, self.height), color=(128,128,255)))
        else:
            self.openImage(generaeted_img=Image.new(mode="RGB", size=(self.width, self.height), color=(0,0,0)))


    def show_image(self, img, name="Show Image"):
        cv2.imshow(name, img)
        cv2.waitKey(0)
        return cv2.destroyAllWindows()

    def __str__(self) -> str:
        return f" path: {self.path}\n w/h: {self.width}/{self.height}\n dtype: {self.dtype}\n layer: {self.layer}"


if __name__ == "__main__":
    img1 = EtsImage("./images/Brick_wall_006_COLOR.jpg")
    #print(img1)
    trimmed_img = img1.trim_image(img1.NP_image, 200, 200, 512, 512)
    img1.show_image(trimmed_img)