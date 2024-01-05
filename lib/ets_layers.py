import os
from PIL import Image
import numpy as np
from ets_settings import *
from ets_images import EtsImage
from utils import get_image_dictionnary
from icecream import ic

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
        ic(self.get_free_space())



    def generate_background(self, size):
        img = Image.new(mode="RGB", size=(size, size))
        return img
    
    def add_new_image(self, images_dict:dict = None, height = None):
        height = self.get_free_space() if height == None else height
        if not images_dict == None:
            self.images.append(EtsImage(images_dict))
            self.images[-1].trim_image(0,0, height=height)
            self.construct_image(update_layers=True)

    def get_free_space(self):
        return IMAGE_SIZE_DEFAULT - self.stacked_trim_array.shape[0]

    def construct_image(self, update_layers = False):
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

        if not self.workzone_widgets == None:
            self.workzone_widgets.update_canvas()
            if update_layers == True and not self.workzone_widgets.layers_view == None:
                self.workzone_widgets.layers_view.create_layers()
    

    def change_current_layer(self, value):
        value = int(value)
        self.workzone_widgets.current_layer.set(value)
        self.workzone_widgets.current_pos_h.set(self.images[value].current_pos_y)
        self.workzone_widgets.current_trim_h.set(self.images[value].current_height)
        self.workzone_widgets.layers_view.create_layers()
    

    def change_all_material_map(self, map_name):
        for image in self.images:
            image.change_material_map(map_name)
        self.construct_image(update_layers=True)


    def export_final_files(self, selected_files, file_name, destination_folder):
        for s_file in selected_files:
            self.change_all_material_map(s_file)
            self.stacked_trim.save(os.path.join(destination_folder, file_name + "_" + s_file + ".jpg")) 

        ic(selected_files)
        ic(file_name)
        ic(destination_folder)


    def test_images(self):
        images_dict = get_image_dictionnary(os.path.join(os.getcwd(), 'images', 'RoofingTiles014A', "2k"))
        self.add_new_image(images_dict = images_dict, height=350)
        images_dict_2 = get_image_dictionnary(os.path.join(os.getcwd(), 'images', 'wood_planks', "2k"))
        self.add_new_image(images_dict = images_dict_2, height=850)

        self.construct_image()
        #self.stacked_trim.show()    
