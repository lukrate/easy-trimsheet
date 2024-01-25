
<img src="https://sepafo.ch/assets/easy-trimsheet/easy_trim_sheet-1706121511.webp" />

> Easy Trimsheet - A tool to quickely create trimsheet with existing PBR textures

## 🚩 Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Releases](#releases)
- [Roadmap](#roadmap)
- [Contact](#contact)
- [License](#license)


## Features

<span id="features"></span>

* Quick and easy editing of different textures with just two sliders, image position and image height.
* Automatic generation of missing maps.
* Automatic image size reduction if too large in relation to the canvas and auto-tilling if too small.
* Automatic import of maps into folder based on name patterns, just need a color map
* Image rotatation
* Organization by layer
* Layer duplication
* ID map genration
* ARM map generation
* *.jpg, *.png, *.webp export
* Save project
* and more...

## Setup
<span id="setup"></span>
#### Clone `master` branch to your local computer. 

```sh
git clone https://github.com/lukrate/easy-trimsheet.git
```

#### Creates a python virtualenv

```sh
python -m venv my-venv
```

#### Activates the virtualenv

linux
```sh
source venv/bin/activate
```
windows - powershell
```sh
.\venv\Scripts\Activate.ps1 (.bat for cmd)
```
windows - cmd
```sh
.\venv\Scripts\Activate.bat
```
#### Install all packages from requirements.txt
```sh
pip install -r requirements.txt
```
#### Start program
```sh
python main.py
```
#### Import your first image
To import your first image, click on the + button in the top right-hand corner of the work area.

Select any image in your folder.

> It is important that your folder contains only images of the material concerned, and that the file names contain the map type as follows:

```python
FILE_NAME_PATTERNS = {
    "color": ["_albedo_", "_albedo","_diff_", "_diffuse","diffuse", "diff", "_col_", "color", "col"],
    "roughness": ["_rough_", "_roughness", "roughness"],
    "displacement": ["_disp_", "_displacement", "_disp", "displacement", "disp"],
    "metalness": ["_metal_", "_metalness", "metalness"],
    "normal": ["_nor_", "_normal", "normal", "nor", "norm"],
    "normal_gl": ["_gl_", "gl", "opengl"],
    "normal_dx": ["_dx_", "dx", "directx"],
    "ao": ["_ao_", "_ambientocclusion", "ambientocclusion", "ambient", "occlusion"],
    "emission": ["_emit_", "_emiss_", "_emission", "emission"],
    "opacity": ["_opacity_", "_opacity", "_transparent", "transparent"],
    "specular": ["_spec_", "_specular", "specular"],
    "bump":["_bump_", "_bump", "bump"]
}
```



## Releases
<span id="releases"></span>
**Future packaged releases will be available on itch.io and gumroad.com**

**PC**: Coming Soon

**Linux**: Coming Soon

**Mac**: Coming Soon

## Roadmap
<span id="roadmap"></span>
Coming Soon

## Contact
<span id="contact"></span>
Coming Soon


## License
<span id="license"></span>
This software is free, open-source and licensed under the [MIT](https://github.com/nhn/tui.editor/blob/master/LICENSE)
