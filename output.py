import tkinter as tk
import pygame
import pyautogui
import time

pyautogui.PAUSE = 0
pygame.init()

DELAY = 0.015 # should be enough

joysticks = []

# This is out of order, it's normal
keys = {0: 'd', 1: 'f', 3: 'j', 2: 'k', 4: 'l'}


class ReadInput:
    def __init__(self, master):
        self.master = master

        # From internet
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            joysticks.append(pygame.joystick.Joystick(i))
            # initialize the appended joystick (-1 means last array item)
            joysticks[-1].init()

    def input(self):
        # for al the connected joysticks
        global held
        global tmax
        # t0 = time.time()
        for event in pygame.event.get():
            dictionary = event.dict
            # Button for fret
            try:
                button = dictionary["button"]
            except:
                button = None
            # Value for strummer
            try:
                value = dictionary["value"]
            except:
                value = None

            try:
                if event.type == 1539:
                    if button == 6:
                        # time.sleep(DELAY + 0.03) # To calibrate properly (worst case scenario)
                        pyautogui.press('space')
                    pressed[button] = True
                elif event.type == 1540:
                    pressed[button] = False
            except:
                pass

            try:
                if value[1] != 0:
                    letters = [keys[i] for i, x in enumerate(held) if x]
                    for letter in letters:
                        pyautogui.keyUp(letter)
                    held = [False] * 8

                    # BUFFER, VERY IMPORTANT
                    time.sleep(DELAY)

                    # Send inputs
                    letters = [keys[i] for i, x in enumerate(pressed) if x]
                    for letter in letters:
                        pyautogui.keyDown(letter)
                    held = pressed.copy()
            except:
                pass

            # if value is not None and type(value) == type(0.1) and axis == 1:
            #     pass  # whammy

        for i, _ in enumerate(held):
            if held[i] and not pressed[i]:
                # Release key
                pyautogui.keyUp(keys[i])
                held[i] = False
        # tmax = (time.time() - t0) if (time.time() - t0) > tmax else tmax
        # print(tmax)
        self.master.after(0, self.input)


if __name__ == "__main__":
    tmax = 0
    pressed = [False] * 8
    held = [False] * 8
    root = tk.Tk()
    root.withdraw() # No need for a window
    app = ReadInput(root)
    app.input()
    root.mainloop()
