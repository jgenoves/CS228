import sys

sys.path.insert(0, '..')

import Leap

controller = Leap.Controller()

from pygameWindow import PYGAME_WINDOW
import random

pygWindow = PYGAME_WINDOW()

xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

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


def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    
    x = int(v[0])
    y = int(v[2])

    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

    x = Scale(x, xMin, xMax, 0, pygWindow.pygWindowWidth)
    y = Scale(y, yMin, yMax, 0, pygWindow.pygWindowDepth)
   
    return (x,y)


def Handle_Bone(bone, drawingWidth):
    base = bone.prev_joint
    tip = bone.next_joint
        
    (baseX, baseY) = Handle_Vector_From_Leap(base)
    (tipX, tipY) = Handle_Vector_From_Leap(tip)

    PYGAME_WINDOW.Draw_Black_Line(pygWindow, baseX, baseY, tipX, tipY, drawingWidth)



def Handle_Finger(finger):
    for b in range(4):
        
        dWidth = 0
        if(b == 0):
            dWidth = 4
        elif(b == 1):
            dWidth = 3
        elif(b == 2):
            dWidth = 2
        elif(b == 3):
            dWidth = 1
            
        Handle_Bone(finger.bone(b), dWidth)
            

def Handle_Frame(frame):

    hand = frame.hands[0]
    fingers = hand.fingers

    for finger in fingers:
        Handle_Finger(finger)
            
    pass

    
    



while True:
    pygWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
    pygWindow.Reveal()
    
