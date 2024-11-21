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

import reciever as re           # Custom serial communication library
from reciever import ports, serialInst

import objects as ob

# Pygame Window Setup
pg.init()    # Initializes pygame
HEIGHT = 800 # Dimentions of the display window
WIDTH = 1200
FPS = 60

framesSec = pg.time.Clock()
displaySurface = pg.display.set_mode((WIDTH, HEIGHT)) # Actual function that creates window for displaying
pg.display.set_caption("Ultrasound Sensor")

# Sensor Graphics
TRUESIZE = 20       # Defines size of to-be-displayed object (in cm)
MAXSENSOR = 320     # Defines max-distance that the sensor can meassure
SIZING = 5          # Defines a constant to convert acual cm meassures to pixels
SENSORDISTANCE = 5  # Defines distance betwen ultrasonic sensors (in cm)
COLOR = (255, 0, 0) # Color object in RGB (can be customized)

# Draw function
def draw(self, center, camera, screen):
    displayable = ce.project(self, center, camera, screen)
    if displayable != None:
        points = []
        for point in displayable[0]:
            x = (WIDTH/2) + (point[0]*SIZING)
            y = (HEIGHT/2) - (point[1]*SIZING)
            points.append([x,y])
        pg.draw.polygon(displaySurface, displayable[1], points)

# Loads faces and colors to create the to-be-displayed object (check objects.py for more info)
faceList = [ob.face3Nodes, ob.face2Nodes, ob.face1Nodes]
colorList = [(0, 255, 0), (255, 0, 255), (255, 0, 0)]
Object = []

for i in range(len(faceList)):
    face = []
    for node in faceList[i]:
        point = []
        for coord in node:
            point.append(coord*TRUESIZE/2)
        face.append(point)
    Object.append(ce.Face(colorList[i], faceList[i])) # Creates the object

# Initializes variables required for projection of objects to screen
camerax, cameray, cameraz, cameraalpha, camerabeta, cameragamma = 0, 0, 0, 0, 0, 0
cameraCenter = []
Camera = ce.Node((0, 0, 0))
Screen = ce.Node((0, 0, TRUESIZE/2))

d1 = 21 # Distances of meassured object from both sensors
d2 = 21
flag = 0

# Starts comunication with front-end
re.serialSetup(serialInst, ports)

# Game Loop
while True:
    # Moves camera according to user input
    cameraCenter = []
    for value in (camerax, cameray, cameraz, cameraalpha, camerabeta, cameragamma):
        cameraCenter.append(value)
    # print("CameraCenter: ", cameraCenter) Debugging only

    # Recieves distances from serial (check reciever.py for more info)
    message = re.recieveMessage(flag, d1, d2)
    if message != None:
        d1 = message[0]
        d2 = message[1]
        # Changes flag to declare which sensor the data is comming from
        if flag == 0: 
            flag = 1
        else:
            flag = 0
    # print("Distances: ", d1, ", ", d2) Debugging only

    # Variables for object displaying
    displaySurface.fill((0, 0, 0))   # Resets screen
    centerPosition = ce.zCoordinate(d1, d2, SENSORDISTANCE)
    trueCenter = (0, 0, 15, 0, 0, 0) # Defines static center
    Camera.move(cameraCenter)        
    Screen.move((0, 0, 0, 0, 0, 0))

    # Draws object
    for face in Object:
        draw(face, centerPosition, Camera, Screen)
    pg.display.flip() # Updates screen

    # User input for controling camera
    keys = pg.key.get_pressed()
    camerax += (keys[pg.K_d] - keys[pg.K_a])
    cameray += (keys[pg.K_SPACE] - keys[pg.K_LSHIFT])
    cameraz += (keys[pg.K_w] - keys[pg.K_s])
    cameraalpha += (keys[pg.K_UP] - keys[pg.K_DOWN]) * 0.05
    camerabeta += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * 0.05

    for event in pg.event.get():
        if event.type == pg.QUIT: # Quit function
            pg.quit()
            sys.exit()
    framesSec.tick(FPS)
