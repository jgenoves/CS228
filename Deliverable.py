import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW

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

        PYGAME_WINDOW.Draw_Black_Line(self.pygameWindow, baseX, baseY, tipX, tipY, drawingWidth)



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
                
        pass

    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = controller.frame()
        if (len(frame.hands) > 0):
            self.Handle_Frame(frame)
        self.pygameWindow.Reveal()


    def Run_Forever(self):
        while True:
            self.Run_Once()

        
