"""
Custom graphics library for the Bombug.
Made (completly) by Carlos ★.

Used for managing projection and graphics 
math and other calculations.
"""

import math as m

"""
CLASSES:
Each class represents a specific object 
either pre-projection (3d) or 
after-projection (2d)
"""

# Represents one point of the displayed object
class Node:
    def __init__(self, shift):
        self.xshift = shift[0] # These are just coordinates
        self.yshift = shift[1]
        self.zshift = shift[2]
        self.x = 0
        self.y = 0
        self.z = 0

    # Moves a point to specified coordinates
    def move(self, center): 
        self.x = center[0] + self.xshift
        self.y = center[1] + self.yshift
        self.z = center[2] + self.zshift

class Camera:
    def __init__(self, pos=[0, 0, 0, 0, 0, 0]):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.alpha = pos[3]
        self.beta = pos[4]
        self.gamma = pos[5]

# Collets projected points for displaying them through pygame
class Face:
    def __init__(self, nodeList):
        self.nodes = []
        for node in nodeList:
            self.nodes.append(Node(node))

# Collects faces
class Polyhedra:
    def __init__(self, faceList, colorList):
        self.faces = []
        self.colors = colorList
        for face in faceList:
            self.faces.append(Face(face))

# Represents a node passed through a Camer Transform
class TransformedNode:
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

"""
FUNCTIONS:
These functions are just the bulk of the
math that radar.py needs to project images
"""

# Calculates color of object according to depth
def colorFromDepth(baseColor, zCoord):
    newColor = []
    for color in baseColor:
        if color != 0 and zCoord !=0:
            value = (color*255)/(m.sqrt(abs(zCoord))*105) 
            # TODO: Fix whatever this mess is
            if value > 255:
                newColor.append(255)
            else:
                newColor.append(value)
        else:
            newColor.append(0)
    return newColor

# Calculates position according to distances from ultrasound sensors
def zCoordinate(firstd1, firstd2, a):
    d1 = firstd1
    d2 = firstd2
    x = ((d1**2) - (d2**2))/(4*a)
    z = (m.sqrt(abs((d1)**2-((a+x)**2))))
    return [x, 0, z, 0, 0, 0]
    # TODO: Add a third sensor to detect y values and extra objects

# Calculates the perspective projection
def perspective(self):
    if self.z != 0:
        x = (self.size*self.x/self.z)
        y = (self.size*self.y/self.z)
    else:
        x, y = 0, 0
    return (x, y)

# Projects objects and prepare them for displaying
def project(self, center, camera, screen, color):
    points = []

    # Moves object to user issued position and runs projection function
    for node in self.nodes: 
        node.move(center)
        nodeDisplay = TransformedNode(node, camera, screen)

        # Only adds points that are in front of the camera 
        if nodeDisplay.z > 0: 
            points.append(perspective(nodeDisplay))  

    # Checks if enough points are in front of the camera
    if len(points) < 3:
        return None
    else:
        trueColor = colorFromDepth(color, center[2])
        return (points, trueColor)     
