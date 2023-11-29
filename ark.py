import pyautogui
import cv2 
import numpy as np
import time
import screen


global bed_number
global first_run

first_run = True


bed_count = 0 # do not change 
look_up_delay = 0.55 # might be a better value to pick 
look_down_delay = 0.49 # might be a better value to pick 
walk_delay = 0.105
delay_90 = 4.37 #2.97 was the previous amount 

crop_type = "tinto" 


def click_bed():
    time.sleep(1)
    pyautogui.press("e")
    time.sleep(1)

def ini():
    f = open("iniFile.txt","r") # This file holds the location of the INI you want to use 
    ini = f.read() 
    f.close()
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.write(ini, interval=0.02) #writing ini to the console 
    pyautogui.press("enter")
    time.sleep(0.3)
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.write("gamma 5 | t.maxfps 10", interval=0.02) # sets gamma at 5 and sets the max fps at 15 
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


def bed_spawn(bed_name, bed_count):


    
    # The bed names for the farm need to set the Bedname in the bot 

    bed_name = bed_name + str(bed_count) # cycling threw the farm 
    count = 0
    bed_screen()
    while (bed_screen() == False): # This is checking to see if the bed has appeared on the map if not the program will retry getting to the bedscreen 
        look_down()
        look_down()
        pyautogui.press("e")
        count += 1
        if (count > 100):
            return False    
        
    
    print("looking to see if your dead")
    if (death_screen()== True): # the death screen search bar is in a differnt place than the alive one 
        time.sleep(1)
        pyautogui.moveTo(300,1300) # The bed search bar while dead 
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
    else:
        time.sleep(1)
        pyautogui.moveTo(500,1300) # The bed search bar while alive
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

    pyautogui.write(bed_name, interval = 0.05) # writes in the bedname we are spawning in 
    time.sleep(1)
    pyautogui.moveTo(bed_location_x,bed_location_y) # Clicks on the bed location of the spawn wanted 
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.moveTo(2200,1300) # This clicks on the spawn button
    time.sleep(0.2)
    pyautogui.click()
    

    white_flash() # detects if the white flash has happened the white flash will take longer on higher ping servers 
    count = 0
    while(white_flash() == False):
        time.sleep(0.1)
        count += 1
        print("no white flash")
        if (count > 100):
            break
    print("white flash")
    time.sleep(10) # This gives time for the respawn animation 


def death_screen():
    roi = screen.get_screen()  # gets the screenshot 

    lower_blue = np.array([0,50,200]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])


    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    death_regions= cv2.imread("icons/death_regions.png", 1) # reads the image of the bed in colour
    hsv = cv2.cvtColor(death_regions, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(death_regions, death_regions, mask=mask)
    death_regions = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, death_regions, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1: # if the min value is less than 0.1 then it will trigger 
        return True
    return False 
    
               
    
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
        return True
    return False

        
def look_up(): # will make the ark charecter look up 
    global look_up_delay 
    pyautogui.keyDown("up")
    time.sleep(look_up_delay)
    pyautogui.keyUp("up")

def walk_forward(): # will make the ark charecter look up 
    global walk_delay 
    pyautogui.keyDown("w")
    time.sleep(walk_delay)
    pyautogui.keyUp("w")

def walk_backwards(): # will make the ark charecter look up 
    pyautogui.keyDown("s")
    time.sleep(walk_delay)
    pyautogui.keyUp("s")

def look_down(): # makes the ark charecter look down 
    global look_down_delay
    pyautogui.keyDown("down")
    time.sleep(look_down_delay)
    pyautogui.keyUp("down")

def turn_right_90(): # turns charecter right by 90* 
    global delay_90
    pyautogui.keyDown("right")
    time.sleep(delay_90)
    pyautogui.keyUp("right")

def turn_left_90(): # turns charecter left by 90* 
    pyautogui.keyDown("left")
    time.sleep(delay_90)
    pyautogui.keyUp("left")

def transfer_all_from(): # transfering all from the tame or strucutre
    pyautogui.moveTo(1875, 265)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

def transfer_all_inventory(): # transfering all from the player inventory 
    pyautogui.moveTo(520,265)
    time.sleep(0.5)
    pyautogui.click()

def check_crop(): # checks if crop plot is open
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    crop_icon = cv2.imread("icons/crop_plot.png", 1) # reads the image of the cropplot in colour
    hsv = cv2.cvtColor(crop_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(crop_icon, crop_icon, mask=mask)
    crop_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crop_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1: # if the min value is less than 0.1 then the part shall trigger 
        global see_crops
        see_crops = True
        return True
    
    see_crops = False
    return None
    
def check_cooker(): # checks if a cooker is open
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    crop_icon = cv2.imread("icons/cooker.png", 1) # reads the image of the cooker in colour
    hsv = cv2.cvtColor(crop_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(crop_icon, crop_icon, mask=mask)
    crop_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crop_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1: 
        return True
    else:
        return False
    
def check_fridge(): # checking if a fridge is open 
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    crop_icon = cv2.imread("icons/fridge.png", 1) # reads the image of the fridge in colour
    hsv = cv2.cvtColor(crop_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(crop_icon, crop_icon, mask=mask)
    crop_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crop_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val < 0.1:
        return True
    else:
        return False
        
    
def check_dedi(): #checking for a dedi is open 
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    dedi_icon = cv2.imread("icons/dedi.png", 1) # reads the image of the dedi in colour
    hsv = cv2.cvtColor(dedi_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(dedi_icon, dedi_icon, mask=mask)
    dedi_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, dedi_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if min_val < 0.1:
        return True
        
    else:  
        return False


def dedi_withdraw(amount):  # hits the withdraw stack button on the dedi 
    time.sleep(0.5)
    pyautogui.moveTo(1290,1111)
    for x in range(amount):
        pyautogui.click()
        time.sleep(0.5)
    
def search_in_object(item): # searches for item in the object your accessing(tame or structure)
    time.sleep(0.2)
    pyautogui.moveTo(1700,275)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.write(item)
    time.sleep(0.2)

def search_in_inventory(item): # searches the the inventory for the item specified
    time.sleep(0.2)
    pyautogui.moveTo(350,275)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.write(item)
    time.sleep(0.2)

def drop_all(): # drops all items on teh floor 
    time.sleep(0.2)
    pyautogui.moveTo(580,275)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(0.4)

def harvest(crop):
    pyautogui.press("f") # to open crop plot 
    time.sleep(2)
    check_crop() # checks to see if crop plots are on the screen 
    if see_crops : #triggers when check_crops = True  
        pyautogui.moveTo(1700, 270)
        time.sleep(0.4)
        pyautogui.click()
        time.sleep(0.4)
        pyautogui.write(crop)
        time.sleep(0.5)
        transfer_all_from()
        time.sleep(0.5)
        pyautogui.press("f") # exiting the crop plots 
        time.sleep(1)
        
    else: #  Crop plots are not on screen will output the date and time of the failure to be logged 
        t = time.localtime() 
        current_time = time.strftime("%H:%M:%S", t)
        print(f"crop{bed_count} failed at {current_time} ")


def harvest_stack(): # harvest the stack of crops verticaly 
    time.sleep(0.2)

    for x in range(4): # for looking to the crop plots from the floor 
        look_up()

    for  x in range(5): # opening up 5 crop plots before moving on 
        harvest(crop=crop_type) #harvesting the crop type set at the top
        time.sleep(1)
        look_up()

    pyautogui.sleep(1)
    pyautogui.press("ctrl") # uncrounching
    time.sleep(0.5)
    look_down() # looking down one to fix the unalienment 
    time.sleep(0.3)
    harvest(crop=crop_type)

    for x in range(1): # harvesting the next 2 stacks ## might be able to change it to 3 in further testing 
        look_up()
        time.sleep(1)
        harvest(crop=crop_type)
        time.sleep(1)

    for x in range(14):
       look_down()  #looks at the floor of the beds 
        


def harvest_270(): #harvest the full 3 stacks of crops 
    time.sleep(1)
    for x in range(7):
        look_down()
    
    pyautogui.press("ctrl")
    time.sleep(0.5)
    walk_forward()
    time.sleep(0.5)
    harvest_stack()
    time.sleep(0.5)
    pyautogui.press("ctrl")
    time.sleep(0.5)
    walk_backwards()
    time.sleep(0.5)
    turn_left_90()
    time.sleep(0.5)
    harvest_stack()
    time.sleep(0.5)
    pyautogui.press("ctrl")
    time.sleep(0.5)
    turn_right_90()
    time.sleep(0.5)
    turn_right_90()
    time.sleep(0.5)
    harvest_stack()
    time.sleep(0.5)


def fridge_colection():
    global first_run
    if(first_run == True): # if this is the first run of the script it will trigger the ini() procedure
        first_run = False
        ini()
    
    time.sleep(0.5)
    walk_forward()
    walk_forward()
    time.sleep(0.5)

    pyautogui.press("f") # opens the cooker 
    time.sleep(1)
    count = 0
    
    while(check_cooker() == False): # if the cooker is not on the screen it will wait (due to server lag)
        time.sleep(0.1)
        count += 1
        
        print("no cooker present")
        if (count > 100):
            break
    print("cooker found")
    time.sleep(1)
    search_in_object(item="medical") # searching in the cooker for medbrews
    transfer_all_from() # transfers all medbrews from cooker into inventory 
    time.sleep(1)

    search_in_object(item="narco") # transfering all narcos from the cooker into the inventory 
    transfer_all_from()
    time.sleep(1)

    pyautogui.press("f") # exiting the cooker
    time.sleep(1)
    look_down()
    look_down()
    look_down()

    pyautogui.press("f") # trying to access the dedi 
    time.sleep(1)

    count = 0
    while(check_dedi() == False): # waiting for the dedi to appear on screen due to lag
        time.sleep(0.2)
        count += 1
        
        if (count > 100):
            break

    time.sleep(1)
    transfer_all_inventory() # transfering all narcos from last run into the dedi 
    time.sleep(0.5)
    dedi_withdraw(amount=7) # withdrawing 7 stacks (700 narcos )
    time.sleep(0.5)
    pyautogui.press("f")
    time.sleep(1)

    look_up() 
    look_up()
    pyautogui.press("f") # accessing the cooker  
    time.sleep(1)
    count = 0
    while(check_cooker() == False):
        time.sleep(0.1)
        count += 1

        print("no cooker present")
        if (count > 100):
            break
    
    time.sleep(1)
    search_in_inventory(item="narco") # searching for only narcos as we will only put narcos in for the next run 
    time.sleep(1)
    transfer_all_inventory() # transfering all narcos into the cooker 
    time.sleep(1)

    pyautogui.press("f") # leaving the cooker 
    time.sleep(1)
    walk_backwards()
    walk_backwards()

    turn_right_90() # turning to face the fridge 
    turn_right_90()


    pyautogui.press("f") # opening fridge 
    time.sleep(1)
    count = 0
    while(check_fridge() == False): # checking to see if the fridge is open (due to lag )
        time.sleep(0.2)
        count += 1
    
        if (count > 100):
            break

    search_in_inventory(item="medical") # adding the medbrews to the fridge 
    time.sleep(1)
    transfer_all_inventory()
    time.sleep(1)
    pyautogui.press("f") # leaving the fridge 
    time.sleep(1)

    for x in range(10):
        look_down() # looking down towards the bed 



def check_medbrews_craftable(): #checking for if medbrews are craftable
    roi = screen.get_screen()

    lower_blue = np.array([0,30,100]) # HSV colour to mask to 
    upper_blue = np.array([255,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # changing the screenshot into HSV 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) # getting rid of anything that isnt between the 2 values 
    masked_template = cv2.bitwise_and(roi, roi, mask= mask) 
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    nomedbrews_icon = cv2.imread("icons/nomedbrew.png", 1) # reads the image of the medbrews not being able to be crafted anymore colour
    hsv = cv2.cvtColor(nomedbrews_icon, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(nomedbrews_icon, nomedbrews_icon, mask=mask)
    nomedbrews_icon = cv2.cvtColor(masked_template,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, nomedbrews_icon, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if min_val < 0.1:
        return True
        
    else: 
        return False
    

def craft_medbrews(): # crafting medbrews 

    for x in range(6):
        look_up() # looking up from the crop bed 
    time.sleep(1)
    turn_right_90() # turning right to face the cooker 
    time.sleep(0.5)
    walk_forward()
    time.sleep(0.5)
    pyautogui.press("f") # openening the cooker 
    time.sleep(2)
    

    while(check_cooker() == False): # checking to see if the cooker has been opened
        time.sleep(1)
        count += 1
        if (check_cooker() == False):
            time.sleep(0.5)
            pyautogui.press("f")

        if (count > 100):
            break
    search_in_inventory(item="seed")
    time.sleep(2)
    drop_all() # dropping all the seeds collected from the cookers 
    time.sleep(2)
    pyautogui.press("f")
    time.sleep(2)
    pyautogui.press("f")
    time.sleep(2)
    transfer_all_inventory() # transfering all the tintos in the inventory into the cooker 

    time.sleep(2)
    search_in_object(item="medical") # searching for the medical brews 
    time.sleep(1)
    while(check_medbrews_craftable() == False): # while medical brews are able to be crafted 
        pyautogui.moveTo(1660,370)
        pyautogui.click()
        pyautogui.press("a") #crafting all(10)- as they have capped it 
        time.sleep(10)
    print("all medbrews crafted") # when medical brews are unable to be crafted (ran out of tintos )
    pyautogui.press("f")
    
    for x in range(14): # look down at the bed 
        look_down()

