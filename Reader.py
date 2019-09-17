import os
import pickle


class READER:
    def __init__(self):
        self.numGestures = 0
        self.Number_Of_Gestures()

    
    def Number_Of_Gestures(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)
        print(self.numGestures)

    def Print_Gestures(self):

        for i in range(self.numGestures):
            
            filename = os.getcwd() + "\\userData\\gesture" + str(i) + ".p"
            print(filename)
            f_in = open(filename, "r")
            data = pickle.load(f_in)
            print(data)
            
        
