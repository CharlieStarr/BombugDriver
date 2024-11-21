# BombugDriver
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

### 2. Installing relevant python modules
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

## Status
Bombug v0.1.1 developed and maintained by Carlos ★
### Features:
- Can **see**
### To Do:
- Add log functionality for storing and sharing visual data
- Add the toy car and program it? (I'm not the one working on that anyway)
- Rework the graphics engine (currently working on this)
- Add sentience



