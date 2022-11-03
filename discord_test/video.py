import cv2
import numpy as np
import win32gui
import win32ui
import win32con


def window_init():
    hwnd = win32gui.FindWindow(None, 'Path of Exile')
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, 800, 600)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((-8,-30), (808,630), dcObj, (0,0), win32con.SRCCOPY)
    return hwnd, wDC, dcObj, cDC, dataBitMap

def window_capture(dataBitMap):
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype = 'uint8')
    img.shape = (600, 800, 4)
    img = np.ascontiguousarray(img[...,:3])
    return img

def window_close(hwnd, wDC, dcObj, cDC, dataBitMap):
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

if __name__ == '__main__':
    while True:
        hwnd, wDC, dcObj, cDC, dataBitMap = window_init()
        screenshot = window_capture(dataBitMap)

        '''
        haystack_img = screenshot
        needle_img = cv2.imread('chaos_color_10.png', cv2.IMREAD_UNCHANGED)

        needle_w = needle_img.shape[0]
        needle_h = needle_img.shape[1]

        result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_CCOEFF_NORMED)

        threshold = 0.92
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))


        rectangles = []
        for loc in locations:
            rect = [loc[0], loc[1], needle_w, needle_h]
            rectangles.append(rect)
            rectangles.append(rect)


        rectangles = cv2.groupRectangles(rectangles, 1, 0.5)[0]
        print(rectangles)
        '''


        cv2.imshow('Computer Vision', screenshot)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        window_close(hwnd, wDC, dcObj, cDC, dataBitMap)

