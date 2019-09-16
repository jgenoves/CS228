import sys
import numpy as np

sys.path.insert(0, '..')

import Leap
from pygameWindow_Del03 import PYGAME_WINDOW

controller = Leap.Controller()


class DELIVERABLE:
    
    def __init__(self):
        self.xMin = 1000
        self.xMax = -1000
        self.yMin = 1000
        self.yMax = -1000
        self.x = 0
        self.y = 0
        self.pygameWindow = PYGAME_WINDOW()
        self.prevNumberOfHands = 0
        self.currNumberOfHands = 0
        
    def Scale(self, a, deviceMin, deviceMax, pyMin, pyMax):

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


    def Handle_Vector_From_Leap(self, v):
        
        self.x = int(v[0])
        self.y = int(v[2])

        if(self.x < self.xMin):
            self.xMin = self.x
        if(self.x > self.xMax):
            self.xMax = self.x
        if(self.y < self.yMin):
            self.yMin = self.y
        if(self.y > self.yMax):
            self.yMax = self.y

        self.x = self.Scale(self.x, self.xMin, self.xMax, 0, self.pygameWindow.pygWindowWidth)
        self.y = self.Scale(self.y, self.yMin, self.yMax, 0, self.pygameWindow.pygWindowDepth)

       
        return (self.x, self.y)


    def Handle_Bone(self, bone, drawingWidth):
        base = bone.prev_joint
        tip = bone.next_joint
            
        (baseX, baseY) = self.Handle_Vector_From_Leap(base)
        (tipX, tipY) = self.Handle_Vector_From_Leap(tip)

        r = 0
        g = 255
        b = 0

        if(self.currNumberOfHands == 2):
            r = 255
            g = 0
            b = 0

        PYGAME_WINDOW.Draw_Line(self.pygameWindow, baseX, baseY, tipX, tipY, drawingWidth, r, g, b)



    def Handle_Finger(self, finger):
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
                
            self.Handle_Bone(finger.bone(b), dWidth)
                

    def Handle_Frame(self, frame):

        hand = frame.hands[0]
        fingers = hand.fingers

        for finger in fingers:
            self.Handle_Finger(finger)
                
        if self.Recording_Is_Ending():
            print('recording is ending')
    
    def Recording_Is_Ending(self):
        if(self.currNumberOfHands == 1 and self.prevNumberOfHands == 2):
            return True
            
    
    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = controller.frame()

        if len(frame.hands) == 1:
            self.currNumberOfHands = 1
        elif len(frame.hands) == 2:
             self.currNumberOfHands = 2
        else:
             self.currNumberOfHands = 0
        
        if (len(frame.hands) > 0):
            self.Handle_Frame(frame)
        self.pygameWindow.Reveal()

        
        if len(frame.hands) == 1:
            self.prevNumberOfHands = 1
        elif len(frame.hands) == 2:
             self.prevNumberOfHands = 2
        else:
             self.prevNumberOfHands = 0

    def Run_Forever(self):
        while True:
            self.Run_Once()

        
