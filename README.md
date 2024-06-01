# esp-scopelogo
Draw logos on an XY-mode (analog) oscilloscope using an ESP32

Requirements
- Python3 with pipenv installed
- Ardino IDE with ESP32 core
- ESP32 with internal DAC (**not all versions have this**)

Usage:
- get SVG files you want to draw
- use a tool ([like inkscape](https://inkscape.org/)) to convert every object in it to PATH in every image
- install dependencies with `pipenv install`
- run the samples generating tool with `pipenv run python3 samples_generator PATH_TO_SVG --pickle <pickle_file_name>`
- you may pre-view the generated samples using `--export <export_file.png>` (requires pillow to be installed!)
- run `python3 merger.py <pickle_1.pickle> <pickle_2.pickle> ...`
- copy the resulting c file to the *firmware* folder, and remove the original `shape.c`
- compile and upload the code with Arduino
- connect two channels of your o-scope to the DAC pins of your ESP
- switch the scope to XY mode
- use scope controls to adjust image position and size
- you might need to filp the image using scope controls or rotate it by swapping the channels
- you can switch between images via connecting a button between the pin specified in `firmware.ino` (can be changed to any pin featuring pullup, software debouncing is provided)
- after the first upload, the ESP has OTG functionality. Hold down the button while powering up to activate (the builtin LED will also light up). SSID and PW can be set in `firmware.ino`

Used some of the SVG reading code from my [`fourieranim` project](https://github.com/sasszem/fourieranim)

Note: the svg.path library does not handle matrix transforms well, in that case applying the transforms to the coordinates with the [apply transform plugin for inkscape](https://github.com/Klowner/inkscape-applytransforms) does the trick.
