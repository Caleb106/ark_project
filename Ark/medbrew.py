import pyautogui
import cv2 
import numpy as np
import time
import screen
import ark 


bed_number = 12 # how many crop plot stations do you have?
ark.bed_count = 0
ark.first_run = True

'''
for x in range(5):
    print("time till start", x)
    time.sleep(1)

ark.bed_location()
while True:
    ark.bed_spawn(bed_name="death") # Kills at the start this means that food+water will be reset 
    time.sleep(30)
    for x in range(bed_number):
        ark.bed_spawn(bed_name="crop")
        if ark.bed_spawn <= bed_number:
            ark.bed_spawn + 1
        else:
            ark.bed_spawn = 0
        ark.harvest_270
    
        '''
time.sleep(2)
ark.bed_location()
ark.bed_spawn(bed_name="crop")