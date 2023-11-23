import numpy as np
import cv2 
from mss import mss

mon = {"top": 0, "left": 0, "width": 2560, "height": 1440} 

sct = mss()

def get_screen():
    return(np.array(sct.grab(mon)))

def get_gray_screen():
    frame_gray = cv2.cvtColor(get_screen(), cv2.COLOR_BGR2GRAY)
    grame_gray = cv2.equalizeHist(frame_gray)
    return frame_gray

def get_width():
    return 2560

def get_height():
    return 1440


# if you have a 1920x 1080 screen change the values to such 