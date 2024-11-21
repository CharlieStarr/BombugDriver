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
from reciever import ports          
from reciever import serialInst

# Pygame Window Setup
pg.init()    # Initializes pygame
HEIGHT = 800 # Constants required for graphics
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

# Function to draw custom objects on screen
def draw(self, center, camera, display):
    """
    Takes as parameters a custom Displayable class 
    (check cengine.py for more info), the center of
    the display, the point of perspective (camera),
    and the screen where the Displayable is
    projected (display). TLDR projects data to screen.
    """
    pointCheck = []
    points = []
    flag = False    # Requiered for checking if objects are behind the camera as to not display them
    # TO DO: Fix perspective issues when object is behind camera

    # Moves object to user issued position and runs projection function
    for node in self.nodes: 
        node.move(center)
        coords = ce.perspective(ce.Displayable(node, camera, display))
        pointCheck.append([(WIDTH/2) + (coords[0]*SIZING), (HEIGHT/2) - (coords[1]*SIZING), coords[2]])

    # Checks if object is behind screen. If it isn't, draws object on screen
    for point in pointCheck:
        flag = flag or point[2] > 0
        points.append([point[0], point[1]])
    #print(points) Debugging only
    #print(flag)
    if flag:
        pg.draw.polygon(displaySurface, ce.colorFromDepth(self.color, center[2]), points)

# Point arrays that define coordinates of to-be-displayed objects. These define a cube
side = TRUESIZE/2 
face1Nodes = [(side, side, 0), (side*-1, side, 0), (side*-1, side*-1, 0), (side, side*-1, 0)]
face2Nodes = [(side, side, side), (side, side, 0), (side, side*-1, 0), (side, side*-1, side)]
face3Nodes = [(side*-1, side, side), (side, side, side), (side, side, 0), (side*-1, side, 0)]
face4Nodes = [(side*-1, side, side), (side*-1, side, 0), (side*-1, side*-1, 0), (side*-1, side*-1, side)]
face5Nodes = [(side*-1, side*-1, side), (side, side*-1, side), (side, side*-1, 0), (side*-1, side*-1, 0)]

# Triangle coordinates for literally no reason
triangleNodes = [(side, side, 0), (side, side*-1, 0), (side*-1, side*-1, 0)] 

# Creates classes that define the faces of to-be-displayed objects
Square1 = ce.Display((255, 0, 0), face1Nodes)
Square2 = ce.Display((255, 0, 255), face2Nodes)
Square3 = ce.Display((0, 255, 0), face3Nodes)
camerax, cameray, cameraz, cameraalpha, camerabeta, cameragamma = 0, 0, 0, 0, 0, 0
cameraCenter = []
Camera = ce.Node((0, 0, 0))
Screen = ce.Node((0, 0, TRUESIZE/2))

d1 = 21 # Distances of meassured object from both sensors
d2 = 21
flag = 0

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
    #print("Distances: ", d1, ", ", d2) Debugging only

    # Variables for object displaying
    displaySurface.fill((0, 0, 0))   # Resets screen
    centerPosition = ce.zCoordinate(d1, d2, SENSORDISTANCE)
    trueCenter = (0, 0, 15, 0, 0, 0) # Defines static center
    Camera.move(cameraCenter)        
    Screen.move((0, 0, 0, 0, 0, 0))

    # Draws object
    draw(Square2, centerPosition, Camera, Screen)
    draw(Square3, centerPosition, Camera, Screen)
    draw(Square1, centerPosition, Camera, Screen)
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
            file.close()
            pg.quit()
            sys.exit()
    framesSec.tick(FPS)
        

