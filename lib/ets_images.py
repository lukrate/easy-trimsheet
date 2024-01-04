from ets_settings import *
from PIL import Image
import cv2
import numpy as np
from icecream import ic
import os

class EtsImage:

    def __init__(self, images_dict):
        self.collection = images_dict
        ic(self.collection)
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

    def openImage(self):
        self.pil_image = Image.open(self.path)
        self.np_image = np.array(self.pil_image)
    
        self.dtype = self.np_image.dtype
        self.shape = self.np_image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.layer = self.shape[2]
        self.image_ratio = self.width / self.height

    def trim_image(self, x, y, width=IMAGE_SIZE_DEFAULT, height=IMAGE_SIZE_DEFAULT):
        self.current_pos_x = x
        self.current_pos_y = y
        self.current_height = height
        self.current_width = width
        self.trimmed_image = self.np_image[y:y + height, x:x + width]

    def get_trimmed_image(self):
        return self.trimmed_image

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