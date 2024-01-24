import os
from PIL import Image
import numpy as np
from lib.ets_settings import *
from lib.ets_images import EtsImage
from lib.utils import get_image_dictionnary
from icecream import ic
from copy import copy
from CTkMessagebox import CTkMessagebox

import threading as th
import subprocess

class Layers():
    def __init__(self, size=IMAGE_SIZE_DEFAULT):
        self.size = size
        self.background = self.generate_background(self.size)
 
        self.images = [] #collections of images
        self.available_maps = []
        self.current_map_type = "color"

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
            self.images.append(EtsImage(images_dict, self.size, self.current_map_type))
            self.get_available_maps()
            self.images[-1].trim_image(posx, posy, height=height, width=self.size)
            try:
                self.construct_image(update_layers=False)
                self.change_current_layer(len(self.images)-1)
            except AttributeError:
                self.construct_image(update_layers=True)
    
    def change_existing_image(self, id, images_dict):
        img = self.images[id]
        img.collection = images_dict
        img.openImage()
        self.get_available_maps()
        img.change_material_map(img.current_map_type)
        #img.trim_image(img.current_pos_x, img.current_pos_y, img.current_width, img.current_height)
        img.change_image_rotation(img.rotation_value)
        img.thumbnails = {}
        self.construct_image(update_layers=True)
                
    def get_free_space(self):
        try:
            return self.free_space
        except AttributeError:
            print("no free space")
    
    def get_available_maps(self):
        a_maps = []
        for key, value in FILE_NAME_PATTERNS.items():
            if key != "normal":
                for img in self.images:
                    try:
                        if img.collection[key] != None:
                            a_maps.append(key)
                            break
                    except KeyError:
                        continue
                    
        self.available_maps = a_maps
        return self.available_maps

    def construct_image(self, update_layers = False):
        final_img_array = None
        
        for k,v in enumerate(self.images):
            if k == 0:
                final_img_array = v.trimmed_image
            else:
                final_img_array = np.vstack((final_img_array, v.trimmed_image))
        
        #final_img = self.background.copy()
        
        try:
            if final_img_array.shape[0] < self.size:
                self.free_space = self.size - final_img_array.shape[0]
                black_part = np.full((self.size - final_img_array.shape[0], self.size, 3), 0, dtype = np.uint8)
                final_img_array = np.vstack((final_img_array, black_part))
            else:
                final_img_array = final_img_array[0 : self.size, 0 : self.size]
        except AttributeError:
            final_img_array = np.full((self.size, self.size, 3), 0, dtype = np.uint8)
            self.free_space = self.size
        
        final_img = Image.fromarray(final_img_array)
        
        self.stacked_trim_array = final_img_array
        self.stacked_trim = final_img

        self.free_space = self.get_free_space()
        
        if not self.workzone_widgets == None:
            self.workzone_widgets.update_canvas()
            self.export_widgets.set_checkbox_default_values()
            if update_layers == True and not self.workzone_widgets.layers_view == None:
                self.workzone_widgets.layers_view.create_layers()

    def change_current_layer(self, value):
        value = int(value)
        self.workzone_widgets.current_layer.set(value)
        self.workzone_widgets.current_pos_h.set(self.images[value].current_pos_y)
        self.workzone_widgets.current_trim_h.set(self.images[value].current_height)
        self.workzone_widgets.set_sliders_max_values()
        self.workzone_widgets.layers_view.create_layers()
        self.workzone_widgets.update_canvas()
    
    def move_layer(self, id, direction):
        self.images[id], self.images[id + direction] = self.images[id + direction], self.images[id]
        self.construct_image(update_layers=True)

    def duplicate_layer(self, id):        
        self.images.insert(id, copy(self.images[id]))
        self.construct_image(update_layers=True)
    
    def remove_layer(self, id): 
        self.images.pop(id)
        self.get_available_maps()
        self.export_widgets.set_checkbox_default_values()
        self.construct_image(update_layers=True)

    def change_all_material_map(self, map_name):
        self.current_map_type = map_name
        for image in self.images:
            image.change_material_map(map_name)
        self.construct_image(update_layers=True)

    def change_image_rotation(self, value, id):
        self.images[id].change_image_rotation(value)
        self.construct_image(update_layers=False)

    def export_final_files(self, selected_files, file_name, destination_folder, format, options, generate_arm, genereate_id, genereate_text_layers_data):
        
        def render_threaded():
            
            ao_map = None
            roughnes_map = None
            metalness_map = None

            first_map_type = copy(self.current_map_type)

            i = 0
            for s_file in selected_files:
                self.change_all_material_map(s_file)

                i += 1
                self.export_widgets.progressbar_value.set(i / len(selected_files))

                if s_file in GREYSCALE_MAP:
                    self.stacked_trim = self.stacked_trim.convert("L")

                self.save_file(self.stacked_trim, format, options, destination_folder, file_name, s_file)
                
                if generate_arm:
                    if s_file == "ao":
                        ao_map = self.stacked_trim
                    if s_file == "roughness":
                        roughnes_map = self.stacked_trim
                    if s_file == "metalness":
                        metalness_map = self.stacked_trim

            if generate_arm:
                self.save_file(self.get_generated_arm_map(ao_map, roughnes_map, metalness_map), 
                               format, options, destination_folder, file_name, "arm")
            
            if genereate_id:
                self.save_file(self.get_generated_id_map(), 
                               format, options, destination_folder, file_name, "ID")
            
            if genereate_text_layers_data:
                self.save_layers_data(destination_folder, file_name)

            self.change_all_material_map(first_map_type)
            self.open_render_complete_box(destination_folder)
        
        render_in_thread = th.Thread(target=render_threaded())
        render_in_thread.start()

    def save_file(self, img, format, options, destination_folder, file_name, map_name):
        if format == ".jpg":
            img.save(os.path.join(destination_folder, file_name + "_" + map_name + format),
                quality=options["quality"],
                optimize=options["optimize"]
            )
        elif format == ".png":
            img.save(os.path.join(destination_folder, file_name + "_" + map_name + format),
                compression=options["compression"],
                optimize=options["optimize"]
            )
        elif format == ".webp":
            img.save(os.path.join(destination_folder, file_name + "_" + map_name + format),
                quality=options["quality"],
                lossless=options["lossless"]
            )

    def get_generated_arm_map(self, ao_map, roughnes_map, metalness_map):
        black_img = self.background.convert("L")
        ao_map = ao_map if ao_map != None else black_img
        roughnes_map = roughnes_map if roughnes_map != None else black_img
        metalness_map = metalness_map if metalness_map != None else black_img
        arm_map = Image.merge("RGB", (ao_map, roughnes_map, metalness_map))
        return arm_map

    def get_generated_id_map(self):
        i = 0
        for img in self.images:
            img.trimmed_image[:,:] = ID_MAP_COLORS[i]
            i += 1
        self.construct_image()
        return self.stacked_trim

    def save_layers_data(self, destination_folder, file_name):
        file_path = os.path.join(destination_folder, f"ets_layers_{file_name}.txt")
        with open(file_path,"w") as file:
            for key, img in enumerate(self.images):
                title = f"Layer {key}\n"
                file.write(title)
                height = f"Height: {img.current_height}\n"
                file.write(height)
                position = f"Position: {img.current_pos_y}\n"
                file.write(position)
                file.write("\n-----------------------\n\n")

    def open_render_complete_box(self, destination_folder):
        box = CTkMessagebox(message="Rendering is complete!", title="Compelete!",
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