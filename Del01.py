import sys

sys.path.insert(0, '..')

import Leap

controller = Leap.Controller()

from pygameWindow import PYGAME_WINDOW
import random

pygWindow = PYGAME_WINDOW()

x = 500
y = 500

xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

# def Perturb_Circle_Position():
#     global x, y

#     fourSidedDieRoll = random.randint(1,4)

#     if fourSidedDieRoll == 1:
#         x += -1
#     elif(fourSidedDieRoll == 2):
#         x += 1
#     elif(fourSidedDieRoll == 3):
#         y += -1
#     elif(fourSidedDieRoll == 4):
#         y += 1

def Scale(a, deviceMin, deviceMax, pyMin, pyMax):

    # This formula is used to scale the dot from the devices coordinates
    # to the pygame window coordinates

    if deviceMin != deviceMax:
        
        deviceLength = abs(deviceMax - deviceMin)
        
        pygLength = abs(pyMax - pyMin)

        device_a_Location = abs(deviceMin - a)


        pyg_a_Location = (pygLength*device_a_Location)/deviceLength

        return pyg_a_Location
    else:

        return abs(pyMax - pyMin)/2
    


def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax

    # Algorithm for retrieving the tip of the index finger's
    # coordinates from the connect LEAP device
    hand = frame.hands[0]
    fingers = hand.fingers
    indexFingerList = fingers.finger_type(1)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(3)
    tip = distalPhalanx.next_joint    
    intX = int(tip[0])
    intY = int(tip[1])  
    x = intX
    y = intY
    
    # Ensures the dot never leaves the screen
    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

    
    



while True:
    pygWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
        x = Scale(x, xMin, xMax, 0, pygWindow.pygWindowWidth)
        y = Scale(y, yMax, yMin, 0, pygWindow.pygWindowDepth)
        print(x,y)
        int(x)
        int(y)

    PYGAME_WINDOW.Draw_Black_Circle(pygWindow, x, y)
    pygWindow.Reveal()
    
