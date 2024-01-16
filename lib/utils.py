from os import listdir
from os.path import isfile, join
from ets_settings import FILE_NAME_PATTERNS
from icecream import ic

img_path = "D:\Python\easytrimsheet\images\wood_planks\\2k"
img_path_2 = "D:\Python\easytrimsheet\images\RoofingTiles014A\\2k"
img_path_3 = "D:\Python\easytrimsheet\images\OfficeCeiling005\\2k"


def get_files_in_folder(path):
    try:
        return [f for f in listdir(path) if isfile(join(path, f))]
    except FileNotFoundError:
        pass


def get_image_dictionnary(path):
    organized_images = {
        "path": path
    }
    
    images = get_files_in_folder(path)

    def check_normal_format(img, KEY):
        for normal_format in FILE_NAME_PATTERNS["normal_dx"]:
            if normal_format in img.lower():
                organized_images[KEY + "_dx"] = img
                break
        for normal_format in FILE_NAME_PATTERNS["normal_gl"]:
            if normal_format in img.lower():
                organized_images[KEY + "_gl"] = img
                break

    for KEY, FORMATS in FILE_NAME_PATTERNS.items():
        is_found = False
        for img in images:
            if not is_found:
                for format in FORMATS:
                    if format in img.lower():
                        is_found = True
                        if is_found and KEY == "normal":
                            check_normal_format(img, KEY)
                        elif is_found: 
                            organized_images[KEY] = img
                            break
                        break
        if not is_found:
            organized_images[KEY] = None            

    return organized_images


def get_save_project_data(layers):
    data = {}
    data["size"] = layers.size
    data["images"] = []
    for key, image in enumerate(layers.images):
        layer_name = "layer_" + str(key)
        layer = {}
        layer["collection"] = image.collection
        layer["current_pos_x"] = image.current_pos_x
        layer["current_pos_y"] = image.current_pos_y
        layer["current_height"] = image.current_height
        layer["current_width"] = image.current_width
        layer["is_rotate"] = image.is_rotate
        layer["rotation_value"] = image.rotation_value
        
        data["images"].append(layer)

    return data
    

