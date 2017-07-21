import serial  # Used for communicating with the Robot
import time  # Used for sleep commands
import cv2  # Image processing library
from grip import GripPipeline  # Class that isolates the cubes as contours

"""SERIAL PORTS"""
# Setup for Communication with the Robotic Arm
ser = serial.Serial()
ser.port = "COM4"
ser.baudrate = 9600
ser.stopbits = 1
ser.parity = "N"
ser.bytesize = 8
ser.open()


def getXY():
    """ Code that determines the x any y values of the cubes in pixels
        No Parameters
        Returns the X coordinate and the Y coordinate
    """
    cap = cv2.VideoCapture(0)  # Connects to the Camera
    pipeline = GripPipeline()
    have_frame, frame = cap.read()  # Sets the frame variable equal to the image the video puts off.
    if have_frame:
        pipeline.process(frame)  # Isolates the Contours
        center_x_positions = []
        center_y_positions = []
        widths = []
        heights = []
        # Find the bounding boxes of the contours to get x, y, width, and height
        for contour in pipeline.filter_contours_output:
            x, y, w, h = cv2.boundingRect(contour)
            center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
            center_y_positions.append(y + h / 2)  # Gets the center of the Box by finding the adding half of the width
            widths.append(w)
            heights.append(h)
            print(center_x_positions[0])
            print(center_y_positions[0])
            return center_x_positions[0], center_y_positions[0]  # Returns the  X and Y Values


def generateStatement():
    # Translates the X and Y coordinates from getXY() to a statement that the robot can use to move to the cube location
    xgen, ygen = getXY()  # Receives Values from getXY()
    xgen = (470 - xgen) * .67  # Finds the value in mm that the robot must move in the x direction
    ygen = (325 - ygen) * .7  # Finds the value in mm that the robot must move in the x direction
    xgen = int(round(xgen))
    ygen = int(round(ygen))
    expression = "DW -" + str(xgen) + "," + str(ygen) + ",0\n"  # Writes Expression
    print("expression is:", expression, "encoded expression is:", expression.encode())  # Print for Debugging
    var = expression.encode()  # Encodes expression in bytes, so the Serial can write it.
    return var


"""ARM CODE"""


# Positions
# Origin: +96.5,+236.5,+72.1,-89.0,+180.0
# PLACE +88.8,+378.2,+122.0,-88.9,+153.9
# Camera: -58.1,+306.1,+111.9,-88.8,+160.7

def GrabAllCubes():
    ser.write(b'Rs\n')
    time.sleep(1)
    ser.write(b'NT\n')
    time.sleep(40)
    """
        Method used to pick up and stack each cube based off of the postitions from the camera
        Takes Picture, Processes, Moves to Origin, Moves to Cube, Picks up Cube, Stacks cube, repeat.
        References the  method generateStatement(), No Parameters or Returns.
        """
    height = 55  # Variable used to determine how much the robot needs to move in the z axis.
    ser.write(b'SP 8\n')  # Sets the speed to 8
    ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')
    # Moves to Image taking position and closes the and so it is able to see everything.
    time.sleep(7)
    ser.write(b'gc\n')
    time.sleep(5)
    for x in range(0, 5):  # Runs 5 times for 5 cubes
        var = generateStatement()  # Generates statement to Find Cube
        time.sleep(1)
        ser.write(b'MP +96.5,+236.5,+72.1,-89.0,+180.0\n')  # Moves to Origin Position
        time.sleep(2)
        ser.write(b'go\n')
        time.sleep(1)
        ser.write(var)  # Moves to Cube position to pick up
        time.sleep(2)
        expression = "DW 0,0,-55\n"
        expression = expression.encode()
        ser.write(expression)  # Picks up Cube
        time.sleep(2)
        ser.write(b'GC\n')
        time.sleep(1)
        expression = "DW 0,0," + str(height) + "\n"
        expression = expression.encode()  # Ascends with Cube
        ser.write(expression)
        time.sleep(2)
        ser.write(b'MP +75.8,+383.2,+137.0,-88.9,+153.9\n')  # Moves to stack position
        time.sleep(2)
        ser.write(b'DW -1,4,0\n')
        time.sleep(2)
        expression = "DW 0,0,-" + str(180 - height) + "\n"  # Places Cube on Stack
        expression = expression.encode()
        ser.write(expression)
        time.sleep(2)
        ser.write(b'GO\n')
        time.sleep(2)
        ser.write(b'DW 0,0,40\n')
        time.sleep(2)
        ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')  # Return  to Camera Position
        time.sleep(2)
        ser.write(b'GC\n')
        height = height + 20  # So it knows to place the cube 20mm higher


def loopR2D2():
    ser.write(b'RS\n')
    time.sleep(1)
    ser.write(b'NT\n')
    time.sleep(40)

    height = 55  # Variable used to determine how much the robot needs to move in the z axis.
    ser.write(b'SP 8\n')  # Sets the speed to 8
    time.sleep(5)
    ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')
    # Moves to Image taking position and closes the and so it is able to see everything.
    time.sleep(5)
    ser.write(b'gc\n')
    while True:  # Runs infinite times
        var = generateStatement()  # Generates statement to Find Cube
        time.sleep(1)
        ser.write(b'MP +96.5,+236.5,+72.1,-89.0,+180.0\n')  # Moves to Origin Position
        time.sleep(2)
        ser.write(b'go\n')
        time.sleep(1)
        ser.write(var)  # Moves to Cube position to pick up
        time.sleep(2)
        expression = "DW 0,0,-55\n"
        expression = expression.encode()
        ser.write(expression)  # Picks up Cube
        time.sleep(2)
        ser.write(b'GC\n')
        time.sleep(1)
        ser.write(b'DW 0,0,55\n')
        time.sleep(2)
        ser.write(b'MP -108.1,+356.1,+211.9,-88.8,+160.7\n')  # Moves to R2 Position
        time.sleep(2)
        ser.write(b'GO\n')
        time.sleep(2)
        ser.write(b'DW 0,0,40\n')
        time.sleep(2)
        ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')  # Return  to Camera Position
        time.sleep(2)
        ser.write(b'GC\n')
        # height = height + 20  # So it knows to place the cube 20mm higher
# ser.write(b'DW 0,0,10\n')
# R2 -118.1,+356.1,+231.9,-88.8,+160.7Gra
# R2 -118.1,+356.1,+231.9,-88.8,+160.7Gra

GrabAllCubes()