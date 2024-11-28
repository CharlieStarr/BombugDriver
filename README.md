# BombugDriver
**This is a school project** 

The Bombug Driver is a bundle of C++ and Python code for controlling a Bombug device.

## Technologies
Project made with:
* [Arduino UNO](https://docs.arduino.cc/hardware/uno-rev3/)
* [Python 3.10.5](https://www.python.org/)
* [Pygame 2.1.2](https://www.pygame.org/docs/index.html)
* [Pyserial 3.5](https://pypi.org/project/pyserial/)

## Instalation
Before installing any code make sure you have the following installed on your computer:

* [Arduino IDE 1.8.19 or above](https://www.arduino.cc/en/software)
* [Python 3.10.5 or above](https://www.python.org/downloads/)
* [Pip 24.2 or above](https://pypi.org/project/pip/)

### 1. Setting up the Bombug folder
Clone the github repository to any folder you like. After that you have to upload the `radio_emitter` and `radio_reciever` to your Bombug device and Arduino UNO respectively and make sure they are running. Take note of what port your Arduino is using as it will be important later.
### 2. Adding the RadioHead library
You will have to install the [RadioHead](https://www.airspayce.com/mikem/arduino/RadioHead/) library and manually add it to your libraries in the Arduino IDE to make sure the code works.
### 3. Installing relevant python modules
You will have to install the `pygame` and `pyserial` modules if you do not have them already:
```bash
pip install pygame
```
and 
```bash
pip install pyserial
```
## Usage
Double click on the batch file to start running the program. You will se 2 windows, one is the command prompt and the other is the graphics window. By heading over to the command prompt you will se something like this:
```
Running Bombug python code and dependencies.
pygame 2.1.2 (SDL 2.0.18, Python 3.10.5)
Hello from the pygame community. https://www.pygame.org/contribute.html
COM7 - Arduino Uno (COM7)
COM3 - Arduino Uno (COM3)
Select port: COM_
```
You must then input the serial port the recieving Arduino is using, and after that you will be seing the images captured by the Bombug device on the second window.

## Configuring (VERY optional)
### Modifying display variables
In the ``projector.py`` file you can find various variables written in all-caps. Most of these can be modify to suit whatever needs you have, either with the Bombug device or in general any visual preferences you might have:[^1]
```python
HEIGHT = 800 # Dimentions of the display window
WIDTH = 1200
FPS = 60
```
```python
TRUESIZE = 20       # Defines size of to-be-displayed object (in cm)
MAXSENSOR = 320     # Defines max-distance that the sensor can meassure (in cm)
SIZING = 5          # Defines a constant to convert acual cm meassures to pixels
SENSORDISTANCE = 5  # Defines distance betwen ultrasonic sensors (in cm)
```
[^1]:You _can_ change ``TRUESIZE``, ``MAXSENSOR``, and ``SENSORDISTANCE`` but these are calibrated specifically for the Bombug device. If yours does not match the afforementioned values then you should change them. Personally I would not recommend changing ``FPS`` because it really does not do much to increase fluidity and I do not know your computer's specifications.

### Adding custom displayable shapes
You can find the shapes that the program can read in ``object.py``. To add another shape you must create a 3d array that contains the information of your shape:
```python
cube = [
    [(1, 1, 0), (-1, 1, 0), (-1, -1, 0), (1, -1, 0)],
    [(1, 1, 1), (1, 1, 0), (1, -1, 0), (1, -1, 1)],
    [(-1, 1, 1), (1, 1, 1), (1, 1, 0), (-1, 1, 0)]
]
```
In this case i have arranged them so each line is a face and each touple inside is a point defining the face. You can then add the colours for each face in another array:
```python
cubeColors = [
    [255, 0, 0],
    [255, 255, 0],
    [0, 255, 255]
]
```

To load custom shapes onto the Bombug software you just have to add your arrays to the following line in `projector.py`:
```python
Display = ce.Polyhedra(ob.cube, ob.cubeColors)
```

Note that the last shape writen is the one that will appear on top. This is because the program loads the first ones first and the next on top of them.


## Status
Bombug v0.2.0-alpha developed and maintained by Carlos ★

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Features:
- Can **see**
- Can see multiple different customizable shapes
- Logs data to a text file for future review
### To Do:
- Add the toy car and program it? (I'm not the one working on that anyway)
- Add a way to read logged data
- Add sentience



