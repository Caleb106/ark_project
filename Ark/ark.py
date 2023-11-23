import pyautogui
import cv2 
import numpy as np
import time
import screen


global bed_number

first_run = True

bed_number = 0

look_up_delay = 0.5 
look_down_delay = 0.3
delay_90 = 2.97 

crop_type = "rock" 




def ini():
    f = open("iniFile.txt","r") # This file holds the location of the INI you want to use 
    ini = f.read() 
    f.close()
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.write(ini, interval=0.02)
    pyautogui.press("enter")
    time.sleep(0.3)
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.write("gamma 5 | t.maxfps 15", interval=0.02) # sets gamma at 5 and sets the max fps at 15 
    pyautogui.press("enter")

def bed_location():
    global bed_location_x
    global bed_location_y
    f = open("bedlocation.txt","r") # Location for your beds first row is X second row is Y 
    x = f.readline()
    y = f.readline()
    f.close()
    bed_location_x = int(x) # The pixel cordinant of your beds that are used for your farm 
    bed_location_y = int(y)
    


def white_flash(): #This function checks to see if the screen becomes white(when you spawn in )
    roi = screen.get_screen()[700:900,0:2560]
    res1 = np.all([roi == 255]) # checks to see if the numpy array has all white pixels
    return res1 # returns True if there is a white screen 


def bed_spawn(bed_name):

    global first_run

    # The bed names for the farm need to set the Bedname in the bot 
    bed_name = bed_name + str(bed_number) # cycling threw the farm 
    
    time.sleep(1)
    pyautogui.moveTo(100,100) # Moves to the place to enter Bedname
    pyautogui.write(bed_name, interval = 0.05)
    time.sleep(0.5)
    pyautogui.moveTo(bed_location_x,bed_location_y) # Clicks on the bed location of the spawn wanted 
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)
    

    count = 0
    bed_screen()
    while (bed_screen() == False): # This is checking to see if the bed has appeared on the map if not the program will retry getting to the bedscreen 
        pyautogui.moveTo(bed_location_x,bed_location_y)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1.0)
        count += 1
        if (count > 100):
            return False
    
    pyautogui.moveTo() # This clicks on the spawn button
    time.sleep(0.2)
    pyautogui.click()

    white_flash() # detects if the white flash has happened the white flash will take longer on higher ping servers 
    count = 0
    while(white_flash() == False):
        time.sleep(0.1)
        count += 1
        if (count > 100):
            break

        time.sleep(10) # This gives time for the respawn animation 

        if (FirstRun == True): # if this is the first run of the script it will trigger the ini() procedure 
            FirstRun = False
            ini()
        return True
    
def bed_screen():
    roi = screen.get_screen()  # gets the screenshot 

    lower_blue = np.array([70,100,200]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])


    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    bed_icon = cv2.imread("icons/bed_icon.png", 1) # reads the image of the bed in colour
    hsv = cv2.cvtColor(bed_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(bed_icon, bed_icon, mask=mask)
    bed_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, bed_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1: # if the min value is less than 0.1 then it will trigger 
        return (min_loc[0] + 14, min_loc[1] + 14)
    return None
        
def look_up():
    global look_up_delay
    pyautogui.keyDown("up")
    time.sleep(look_up_delay)
    pyautogui.keyUp("up")

def look_down():
    global look_down_delay
    pyautogui.keyDown("down")
    time.sleep(look_down_delay)
    pyautogui.keyUp("down")

def turn_right_90():
    global delay_90
    pyautogui.keyDown("right")
    time.sleep(delay_90)
    pyautogui.keyUp("right")

def turn_left_90():
    pyautogui.keyDown("left")
    time.sleep(delay_90)
    pyautogui.keyUp("left")

def transfer_all_from():
    pyautogui.moveTo(1875, 265)
    time.sleep(0.5)
    pyautogui.click()

def check_crop():
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    crop_icon = cv2.imread("icons/crop_plot.png", 1) # reads the image of the bed in colour
    hsv = cv2.cvtColor(crop_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(crop_icon, crop_icon, mask=mask)
    crop_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crop_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1: # if the min value is less than 0.1 then the part shall trigger 
        global see_crops
        see_crops = True
        return (min_loc[0] + 14, min_loc[1] + 14)
    
    see_crops = False
    return None
    

    


def harvest(crop):
    pyautogui.press("f") # to open crop plot 
    time.sleep(1)
    check_crop() # checks to see if crop plots are on the screen 
    if see_crops : #triggers when check_crops = True  
        pyautogui.moveTo(1700, 270)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.write(crop)
        time.sleep(0.5)
        transfer_all_from()
        time.sleep(0.5)
        pyautogui.press("esc")
        time.sleep(1)
        
    else: #  Crop plots are not on screen will output the date and time of the failure to be logged 
        t = time.localtime() 
        current_time = time.strftime("%H:%M:%S", t)
        print(f"crop{bed_number} failed at {current_time} ")



def harvest_stack(): # harvest the stack of crops verticaly 
    time.sleep(0.2)
    look_up()
    look_up()
    for  x in range(4): 
        look_up()
        time.sleep(1)
        harvest(crop=crop_type)

    pyautogui.sleep(1)
    pyautogui.press("ctrl")
    time.sleep(0.5)
    look_down()
    time.sleep(0.3)
    harvest(crop=crop_type)

    for x in range(2):
        look_up()
        time.sleep(1)
        harvest(crop=crop_type)
        time.sleep(1)

    for x in range(11):
        look_down()


def harvest_270(): #harvest the full 3 stacks of crops 
    pyautogui.press("ctrl")
    turn_left_90()
    harvest_stack()
    pyautogui.press("ctrl")
    turn_right_90()
    harvest_stack()
    pyautogui.press("ctrl")
    turn_right_90()
    harvest_stack()



time.sleep(2)


