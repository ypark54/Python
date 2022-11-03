# Code to check if left or right mouse buttons were pressed
import win32api
import time
import numpy as np


state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
down_interval = []
up_interval = []
while True:
    a = win32api.GetKeyState(0x01)

    if a != state_left:  # Button state changed
        state_left = a
        if a < 0:
            click_start = time.time()
            
            try:
                #print(click_start-click_end)
                down_interval.append(click_start-click_end)
            except:
                pass
        else:
            click_end = time.time()
            
            try:
                #print(click_end-click_start)
                up_interval.append(click_end-click_start)
            except:
                pass
    if len(down_interval) > 100:


        break
    

#down interval = duration between click
ave = np.average(down_interval)
sd = np.std(down_interval)
print(f'average: {ave} standard deviatio: {sd}')

#up intever = click duration
ave = np.average(up_interval)
sd = np.std(up_interval)
print(f'average: {ave} standard deviatio: {sd}')