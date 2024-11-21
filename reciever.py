"""
Custom serial library for the Bombug.
Made (mostly) by Carlos ★.

Using pyserial library for access to serial
ports.

Used for recieving data from the arduino
board.
"""

import serial.tools.list_ports # Allows serial communication
import time

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

# Function to select port for serial communication
def selectPort(ports):
    portVar = ""
    portList = []

    # Prints all ports available
    for port in ports:
        portList.append(str(port))
        print(str(port))
    
    val = input("Select port: COM") # Assings port according to user input
    
    for i in range(0, len(portList)):
        if portList[i].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print("Selected: " + portList[i]) # Prints selected port
    return portVar

def serialSetup(serial, ports):
    serial.baudrate = 9600 # Variables for serial set-up
    serial.port = selectPort(ports)
    serial.open()
    return 0

startTime = time.time()
# Function to recieve serial messages
def recieveMessage(flag, d1, d2):
    distances = [d1, d2]
    if serialInst.in_waiting:
        packet = serialInst.readline()
        message = str(packet.decode('utf').rstrip("\n")[:-2])
        """
        The above stated line decodes serial data from
        binary, to unicode and removes unecesary characters.
        """

        # Checks if message has actual data in it
        if message != '':
            number = int(message)
        else:
            number = 0

        # Checks which sensor has sent which piece of data
        if flag == 0:
            distances[0] = number/1000
        if flag == 1:
            distances[1] = number/1000

        currentTime = int((time.time() - startTime) * 1000)
        print(currentTime, distances) # Writes distances to screen
        return distances
