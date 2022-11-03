import pyautogui as pag
import pywinauto
import pygetwindow as gw
import pyautogui
import numpy as np
import time

win = gw.getWindowsWithTitle('Path of Exile')[0] # 윈도우 타이틀에 Chrome 이 포함된 모든 윈도우 수집, 리스트로 리턴
if win.isActive == False:
    pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
win.activate() #윈도우 활성화p
try:
    while True:
        pyautogui.mouseDown(x=1096, y=658)
        while True:
            rand = np.random.normal(0.06365472727482861,0.012447467353326233)
            if rand <1:
                break
        time.sleep(rand)
        pyautogui.mouseUp(x=1096, y=658)
        while True:
            rand = np.random.normal(0.06365472727482861*1.2,0.012447467353326233*1.2)
            if rand <1:
                break
        time.sleep(rand)
except KeyboardInterrupt:
    print('\n')