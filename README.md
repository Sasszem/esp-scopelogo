# esp-scopelogo
Draw logos on an XY-mode (analog) oscilloscope using an ESP32

Requirements
- Python3 with pipenv installed
- Ardino IDE with ESP32 core
- ESP32 with internal DAC (**not all versions have this**)

Usage:
- get an SVG file you want to draw
- use a tool ([like inkscape](https://inkscape.org/)) to convert every object in it to PATH
- install dependencies with `pipenv install`
- run the samples generating tool with `pipenv run python3 samples_generator PATH_TO_SVG PATH_TO_OUTPUT.c`
- copy the resulting c file to the *firmware* folder, and remove the original `shape.c`
- compile and upload the code with Arduino
- connect two channels of your o-scope to the DAC pins of your ESP
- switch the scope to XY mode
- use scope controls to adjust image position and size
- you might need to filp the image using scope controls or rotate it by swapping the channels

Used some of the SVG reading code from my [`fourieranim` project](https://github.com/sasszem/fourieranim)