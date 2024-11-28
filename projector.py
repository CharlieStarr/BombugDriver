"""
Radar projection code for the Bombug.
Made (pretty much all) by Carlos ★.

Using pygame library for graphics display and 
multiple custom dependencies for data and
graphics management.

Used for projecting the position of objects 
detected by the ultrasonic sensor.
"""

import pygame as pg  # Allows on-screen drawing
import sys           # Allows execution of system commands
import cengine as ce # Custom graphics library
import math as m

import reciever as re # Custom serial communication library
from reciever import ports, serialInst

import objects as ob  # Object data

# Constants
pg.init()    # Initializes pygame
HEIGHT = 800 # Dimentions of the display window
WIDTH = 1200
FPS = 60

TRUESIZE = 20       # Defines size of the irl object (in cm)
MAXSENSOR = 320     # Defines max-distance that the sensor can meassure (in cm)
SIZING = 22         # Defines a constant to convert acual cm meassures to pixels
SENSORDISTANCE = 5  # Defines distance betwen ultrasonic sensors (in cm)

# Pygame Setup
framesSec = pg.time.Clock()
displaySurface = pg.display.set_mode((WIDTH, HEIGHT)) # Actual function that creates window for displaying
pg.display.set_caption("Ultrasound Sensor")

# Draws objects into the screen
def draw(self, center, camera, screen):
    for i in range(len(self.faces)):
        projection = ce.project(self.faces[i], center, camera, screen, self.colors[i])
        if projection != None:
            points = []
            for node in projection[0]:
                x = (WIDTH/2) + (node[0]*SIZING)
                y = (HEIGHT/2) - (node[1]*SIZING)
                points.append([x,y])
            pg.draw.polygon(displaySurface, projection[1], points)

# Calls the classes necesary for projection and display
Display = ce.Polyhedra(ob.cube, ob.cubeColors)
Camera = ce.Camera()
Screen = ce.Node((0, 0, TRUESIZE/2))

distance1 = 21 # Distances of meassured object from both sensors
distance2 = 21
receiveFlag = 0

#re.serialSetup(serialInst, ports)

while True:

    # Recieves distances from serial
    message = None #re.recieveMessage(receiveFlag, distance1, distance2)
    if message != None:
        distance1 = message[0]
        distance2 = message[1]
        # Changes flag to declare which sensor the data is comming from
        if receiveFlag == 0: 
            receiveFlag = 1
        else:
            receiveFlag = 0

    # Variables for object displaying
    displaySurface.fill((0, 0, 0))   # Resets screen
    objectCenter = ce.zCoordinate(distance1, distance2, SENSORDISTANCE)
    trueCenter = (0, 0, 15) # Defines static center      
    Screen.move((0, 0, 0))

    # Draws object
    draw(Display, objectCenter, Camera, Screen)
    pg.display.flip() # Updates screen

    # User input
    keys = pg.key.get_pressed()
    Camera.alpha += (keys[pg.K_UP] - keys[pg.K_DOWN]) * 0.02
    Camera.beta += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * 0.02
    Camera.y += (keys[pg.K_SPACE] - keys[pg.K_LSHIFT]) * 0.9

    movingLR = (keys[pg.K_d] - keys[pg.K_a])
    movingFB = (keys[pg.K_w] - keys[pg.K_s])

    Camera.x += ((movingLR * m.cos(Camera.beta)) + (movingFB * m.cos(Camera.beta - (m.pi / 2)))) * 0.2 
    Camera.z += ((movingFB * m.cos(Camera.beta)) + (movingLR * m.cos(Camera.beta + (m.pi / 2)))) * 0.2

    for event in pg.event.get():
        if event.type == pg.QUIT: # Quit function
            pg.quit()
            sys.exit()
    framesSec.tick(FPS)
