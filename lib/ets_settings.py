from PIL import Image
from tkinter import PhotoImage
import customtkinter as ctk
import os

VERSION = "1.2"

IMAGE_SIZE_DEFAULT = 2048
IMAGE_SIZE_OPTIONS = ["256", "512", "1024", "2048", "4096", "8192"]
ROTATE_DEFAULT = 0

ZOOM_DEFAULT = 0
ROTATIONS_OPTIONS = ["0", "90", "180", "270"]
BRIGHTNESS_DEFAULT = 1

BACKGROUND_COLOR = "#2b2b2b"
WHITE = "#FFF"
GREY = "grey"
BLUE = "#1f6aa5"
DARK_GREY = "#242424"
LIGHT_GREY = "#4a4a4a"
CLOSE_RED = "8a0606"

SLIDER_BG = "#64686b"

FILE_NAME_PATTERNS = {
    "color": ["_diff_", "_diffuse","diffuse", "diff", "_col_", "color", "col"],
    "roughness": ["_rough_", "_roughness", "roughness"],
    "displacement": ["_disp_", "_displacement", "_disp", "displacement", "disp"],
    "metalness": ["_metal_", "_metalness", "metalness"],
    "normal": ["_nor_", "_normal", "normal", "nor", "norm"],
    "normal_gl": ["_gl_", "gl", "opengl"],
    "normal_dx": ["_dx_", "dx", "directx"],
    "ao": ["_ao_", "_ambientocclusion", "ambientocclusion", "ambient", "occlusion"],
    "emission": ["_emit_", "_emiss_", "_emission", "emission"],
    "specular": ["_spec_", "_specular", "specular"],
    "bump":["_bump_", "_bump", "bump"]
}

GREYSCALE_MAP = ["roughness", "displacement", "metalness", "ao", "bump", "specular"]

FILE_FORMATS = [".jpg", ".png", ".webp"]


ICON_PLUS_PATH = os.path.join(os.path.curdir, "lib", "icon", "plus.png")
PLUS_BUTTON = ctk.CTkImage(light_image=Image.open(ICON_PLUS_PATH),
                                  dark_image=Image.open(ICON_PLUS_PATH),
                                  size=(16, 16))

ICON_CLOSE_PATH = os.path.join(os.path.curdir, "lib", "icon", "close.png")
CLOSE_BUTTON = ctk.CTkImage(light_image=Image.open(ICON_CLOSE_PATH ),
                                  dark_image=Image.open(ICON_CLOSE_PATH ),
                                  size=(14, 14))

ICON_DUPLICATE_PATH = os.path.join(os.path.curdir, "lib", "icon", "duplicate.png")
DUPLICATE_BUTTON = ctk.CTkImage(light_image=Image.open(ICON_DUPLICATE_PATH ),
                                  dark_image=Image.open(ICON_DUPLICATE_PATH ),
                                  size=(16, 16))

ICON_RECYCLE_PATH = os.path.join(os.path.curdir, "lib", "icon", "recycle.png")
RECYCLE_BUTTON = ctk.CTkImage(light_image=Image.open(ICON_RECYCLE_PATH ),
                                  dark_image=Image.open(ICON_RECYCLE_PATH ),
                                  size=(16, 16))

ICON_LOGO_PATH = os.path.join(os.path.curdir, "lib", "icon", "logo.png")
LOGO_BUTTON = ctk.CTkImage(light_image=Image.open(ICON_LOGO_PATH ),
                                  dark_image=Image.open(ICON_LOGO_PATH ),
                                  size=(200, 120))


ICON_APP_PATH = os.path.join(os.path.curdir, "lib", "icon", "icon.png")