
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
img = cv2.imread('C:/Python/poe_img/histotest_3.png',cv2.IMREAD_UNCHANGED)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    #plt.plot(histr,color = col)
    #plt.xlim([0,256])
#plt.show()