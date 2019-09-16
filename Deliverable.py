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
        self.gestureData = np.zeros((5,4,6), dtype='f')
        
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


    def Handle_Bone(self, bone, drawingWidth, i, j):
        base = bone.prev_joint
        tip = bone.next_joint
        
        if self.Recording_Is_Ending():           
            self.gestureData[i,j,0] = base[0]
            self.gestureData[i,j,1] = base[1]
            self.gestureData[i,j,2] = base[2]
            
            self.gestureData[i,j,3] = tip[0]
            self.gestureData[i,j,4] = tip[1]
            self.gestureData[i,j,5] = tip[2]
       
            
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



    def Handle_Finger(self, finger, i):
        
        for j in range(4):
            
            dWidth = 0
            if(j == 0):
                dWidth = 4
            elif(j == 1):
                dWidth = 3
            elif(j == 2):
                dWidth = 2
            elif(j == 3):
                dWidth = 1
                
            self.Handle_Bone(finger.bone(j), dWidth, i, j)
                

    def Handle_Frame(self, frame):

        hand = frame.hands[0]
        fingers = hand.fingers

        for i in range(5):
            self.Handle_Finger(fingers[i], i)
                
        if self.Recording_Is_Ending():
            print(self.gestureData)
    
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

        
