"""
Custom graphics library for the Bombug.
Made (completly) by Carlos ★.

Using pygame library for graphics management.

Used for managing projection and graphics 
math and other calculations.
"""

import math as m    # Math
import pygame as pg # Allows graphic management

# Function to calculate color of object according to depth
def colorFromDepth(baseColor, zCoord):
    newColor = []
    for color in baseColor:
        if color != 0 and zCoord !=0:
            value = (color*255)/(m.sqrt(abs(zCoord))*105)
            # TO DO: Fix whatever this mess is
            if value > 255:
                newColor.append(255)
            else:
                newColor.append(value)
        else:
            newColor.append(0)
    return newColor

# Function to calculate position according to distances from ultrasound sensors
def zCoordinate(firstd1, firstd2, a):
    d1 = firstd1
    d2 = firstd2
    x = ((d1**2) - (d2**2))/(4*a)
    z = (m.sqrt(abs((d1)**2-((a+x)**2))))
    return [x, 0, z, 0, 0, 0]

# Node class that represents one point of the displayed object
class Node:
    def __init__(self, shift):
        self.xshift = shift[0] # These are just coordinates
        self.yshift = shift[1]
        self.zshift = shift[2]
        self.x = 0
        self.y = 0
        self.z = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.pos = [0, 0, 0]
    def move(self, center):
        self.alpha = center[3]
        self.beta = center[4]
        self.gamma = center[5]
        self.x = center[0] + self.xshift
        self.y = center[1] + self.yshift
        self.z = center[2] + self.zshift
        self.pos = [self.x, self.y, self.z]

# Displayable class that represents a to-be-displayed object
class Displayable():
    def __init__(self, point, camera, display):
        X = point.x - camera.x # More coordinates
        Y = point.y - camera.y
        Z = point.z - camera.z
        D = (m.sin(camera.gamma)*Y)+(m.cos(camera.gamma)*X)
        E = (m.cos(camera.gamma)*Y)-(m.sin(camera.gamma)*X)
        self.x = (m.cos(camera.beta)*D) - (m.sin(camera.beta)*Z)
        self.y = (m.sin(camera.alpha)*((m.cos(camera.beta)*Z) + (m.sin(camera.beta)*D))) + (m.cos(camera.alpha)*E)
        self.z = (m.cos(camera.alpha)*((m.cos(camera.beta)*Z) + (m.sin(camera.beta)*D))) - (m.sin(camera.alpha)*E)
        """
        The above stated lines are the math for a 'camera transform'.
        Basically it changes the coordinate system of the coordinates
        of the object from the global one, to one in relation to the
        position of the camera. This is required for the calculation
        of the perspective projection. It's just a lot of math really.
        Source: Wikipedia
        """
        self.size = display.z
        # print("Positions: ", self.x, self.y, self.z) Debugging only

# Function to calculate the perspective projection
def perspective(self):
    if self.z != 0:
        x = (self.size*self.x/self.z)
        y = (self.size*self.y/self.z)
        z = self.z
    else:
        x, y, z = 0, 0, self.z
    return (x, y, z)

# Display class that collets projected point for projection as a pygame polygon
class Display(pg.sprite.Sprite):
    def __init__(self, color, nodeList):
        self.color = color
        self.nodes = []
        for node in nodeList:
            self.nodes.append(Node(node))