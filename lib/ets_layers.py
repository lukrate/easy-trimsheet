import os
from PIL import Image
import numpy as np
from ets_settings import *
from ets_images import EtsImage
from utils import get_image_dictionnary
from icecream import ic
from copy import copy
from CTkMessagebox import CTkMessagebox
import subprocess

class Layers():
    def __init__(self, size=IMAGE_SIZE_DEFAULT):
        self.size = size
        self.background = self.generate_background(self.size)
 
        self.images = [] #collections of images
        self.available_maps = []

        self.stacked_trim_array = [] #np array of images trimmed
        self.stacked_trim = None #final image
        self.free_space = size #freespace under existing images

        self.workzone_widgets = None
        self.export_widgets = None
        
        #self.test_images()



    def generate_background(self, size):
        img = Image.new(mode="RGB", size=(size, size))
        return img
    
    def add_new_image(self, images_dict:dict = None, height = None, posx = 0, posy = 0):
        height = self.get_free_space() if height == None else height
        if not images_dict == None:
            self.images.append(EtsImage(images_dict, self.size))
            self.get_available_maps()
            self.images[-1].trim_image(posx, posy, height=height, width=self.size)
            self.construct_image(update_layers=True)

    def get_free_space(self):
        try:
            return self.size - self.stacked_trim_array.shape[0]
        except AttributeError:
            return self.size
    
    def get_available_maps(self):
        a_maps = []
        for key, value in FILE_NAME_PATTERNS.items():
            if key != "normal":
                for img in self.images:
                    if img.collection[key] != None:
                        a_maps.append(key)
                        break
        self.available_maps = a_maps
        return self.available_maps

    def construct_image(self, update_layers = False):
        final_img_array = None
        for k,v in enumerate(self.images):
            if k == 0:
                final_img_array = v.trimmed_image
            else:
                final_img_array = np.vstack((final_img_array, v.trimmed_image))
        
        final_img = self.background.copy()
        try:
            final_img.paste(Image.fromarray(final_img_array))
            self.stacked_trim_array = final_img_array
        except AttributeError:
            pass
        
        self.stacked_trim = final_img
        self.free_space = self.get_free_space()
        

        if not self.workzone_widgets == None:
            self.workzone_widgets.update_canvas()
            if update_layers == True and not self.workzone_widgets.layers_view == None:
                self.workzone_widgets.layers_view.create_layers()
                self.export_widgets.set_checkbox_default_values()
    

    def change_current_layer(self, value):
        value = int(value)
        self.workzone_widgets.current_layer.set(value)
        self.workzone_widgets.current_pos_h.set(self.images[value].current_pos_y)
        self.workzone_widgets.current_trim_h.set(self.images[value].current_height)
        self.workzone_widgets.layers_view.create_layers()
    
    def move_layer(self, id, direction):
        self.images[id], self.images[id + direction] = self.images[id + direction], self.images[id]
        self.construct_image(update_layers=True)

    def duplicate_layer(self, id):        
        self.images.insert(id, copy(self.images[id]))
        self.construct_image(update_layers=True)
    
    def remove_layer(self, id): 
        self.images.pop(id)
        self.construct_image(update_layers=True)

    def change_all_material_map(self, map_name):
        for image in self.images:
            image.change_material_map(map_name)
        self.construct_image(update_layers=True)

    def change_image_rotation(self, value, id):
        self.images[id].change_image_rotation(value)
        self.construct_image(update_layers=False)


    def export_final_files(self, selected_files, file_name, destination_folder, format, options):

        i = 0
        for s_file in selected_files:
            self.change_all_material_map(s_file)

            i += 1
            self.export_widgets.progressbar_value.set(i / len(selected_files))

            if s_file in GREYSCALE_MAP:
                self.stacked_trim = self.stacked_trim.convert("L")
            if format == ".jpg":
                self.stacked_trim.save(os.path.join(destination_folder, file_name + "_" + s_file + format),
                    quality=options["quality"],
                    optimize=options["optimize"]
                )
            elif format == ".png":
                self.stacked_trim.save(os.path.join(destination_folder, file_name + "_" + s_file + format),
                    compression=options["compression"],
                    optimize=options["optimize"]
                )
            elif format == ".webp":
                self.stacked_trim.save(os.path.join(destination_folder, file_name + "_" + s_file + format),
                    quality=options["quality"],
                    lossless=options["lossless"]
                )
            else:
                break
        
        self.open_render_complete_box(destination_folder)

    def open_render_complete_box(self, destination_folder):
        box = CTkMessagebox(message="Rendering is complete!",
                  icon="check", option_1="OK", option_2="Open Folder")
        
        resp = box.get()

        if resp == "Open Folder":
            win_dir = os.path.normpath(destination_folder)
            subprocess.Popen('explorer "%s"' %win_dir)
        self.export_widgets.progressbar_value.set(0.0)

    def test_images(self):
        images_dict = get_image_dictionnary(os.path.join(os.getcwd(), 'images', 'RoofingTiles014A', "2k"))
        self.add_new_image(images_dict = images_dict, height=350)
        images_dict_2 = get_image_dictionnary(os.path.join(os.getcwd(), 'images', 'wood_planks', "2k"))
        self.add_new_image(images_dict = images_dict_2, height=850)

        self.construct_image()
        #self.stacked_trim.show()    
