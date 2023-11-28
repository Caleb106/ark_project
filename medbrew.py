import pyautogui
import cv2 
import numpy as np
import time
import screen
import ark 


bed_number = 3 # how many crop plot stations(beds) do you have?
ark.first_run = True
fridge_count = 0
crop = "crop" # the name of your stations bed 


for x in range(5):
    print("time till start", x)
    time.sleep(1)

print("to stop close vscode or get in the terminal and press ctrl + C to raise a keyboard interupt / which will stop the code from running ")
ark.bed_location()
ark.bed_spawn(bed_name="death", bed_count= 0) # Kills at the start this means that food+water will be reset 
time.sleep(15)

while True:
  
    for x in range(bed_number): # amount of beds corralate to the amount of passes we will do 
        
        time.sleep(2)
        ark.bed_spawn(bed_name="fridge", bed_count= fridge_count) # spawns on the fridge bed doing this before harvesting will get rid of any leftovers and will ensure 
        time.sleep(1) #that we have enough narcotics for the run after the spawn 
        ark.fridge_colection() # will collect the medbrews from the fridge
        time.sleep(1)
        ark.click_bed()
        time.sleep(1)
        ark.bed_spawn(bed_name="death", bed_count= 0) # death bed to reset HP food and water 
        time.sleep(15)

        ark.bed_spawn(bed_name= crop, bed_count= ark.bed_count)    # spawns onto the farm bed 
        time.sleep(1)
        ark.harvest_270() # harvest the crop plots 
        time.sleep(1)
        ark.craft_medbrews() # crafts medbrews until none left to craft 
        time.sleep(1)
        ark.click_bed()

        if ark.bed_count < bed_number: # if the bed count is less than the number of beds it will increase by 1
            ark.bed_count = ark.bed_count + 1
            
        else:
            ark.bed_count = 0 # if higher than bed count we will reset the bed count.
            fridge_count = 0    

        if ark.bed_count % 3 == 0: # if bed_count is MOD 3 = 0 so no remanders increment fridge_count as we are at a diffrent section of the farm 
            fridge_count += 1
            