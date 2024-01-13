
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
    "bump":["_bump_", "_bump", "bump"]
}

GREYSCALE_MAP = ["roughness", "displacement", "metalness", "ao", "bump"]

FILE_FORMATS = [".jpg", ".png", ".webp"]