from pygameWindow import PYGAME_WINDOW
import random

pygWindow = PYGAME_WINDOW()

x = 500
y = 500

def Perturb_Circle_Position():
    global x, y

    fourSidedDieRoll = random.randint(1,4)

    if fourSidedDieRoll == 1:
        x += -1
    elif(fourSidedDieRoll == 2):
        x += 1
    elif(fourSidedDieRoll == 3):
        y += -1
    elif(fourSidedDieRoll == 4):
        y += 1


while True:
    pygWindow.Prepare()
    Perturb_Circle_Position()
    PYGAME_WINDOW.Draw_Black_Circle(pygWindow, x, y)
    pygWindow.Reveal()