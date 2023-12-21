from PIL import Image
import cv2
import numpy as np

class easyImage:

    def __init__(self, path):
        self.path = path
        self.width = None
        self.height = None
        self.dtype = None
        self.shape = None
        self.img_layer = None

        self.values = {
            "PIL_image": None,
            "NP_image": None
        }

        self.openImage(path)

    def openImage(self, path):
        self.values["PIL_image"] = cv2.imread(self.path)
        self.values["NP_image"] = np.array(self.values["PIL_image"])
        im = self.values["NP_image"]
        self.dtype = im.dtype
        self.shape = im.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.layer = self.shape[2]

    def trim_image(self, array, x, y, width, height):
        return array[y:y + height, x:x+width]

    def show_image(self, img, name="Show Image"):
        cv2.imshow(name, img)
        cv2.waitKey(0)
        return cv2.destroyAllWindows()

    def __str__(self) -> str:
        return f" path: {self.path}\n w/h: {self.width}/{self.height}\n dtype: {self.dtype}\n layer: {self.layer}"


if __name__ == "__main__":
    img1 = easyImage("./images/Brick_wall_006_COLOR.jpg")
    print(img1)
    trimmed_img = img1.trim_image(img1.values["NP_image"], 200, 200, 512, 512)
    img1.show_image(trimmed_img)