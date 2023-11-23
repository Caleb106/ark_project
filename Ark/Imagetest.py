import numpy as np
import cv2 as cv

img  = cv.imread('icons/test1.png', 0)
template = cv.imread('icons/yesmedbrew.png', 0)
h, w = template.shape

methods = cv.TM_SQDIFF_NORMED , cv.TM_CCOEFF_NORMED

for method in methods:
    img2 = img.copy()
    
    result = cv.matchTemplate(img2, template , method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if method in [cv.TM_CCOEFF_NORMED]:
        location = max_loc
    else:
        location = min_loc

    bottom_right = (location[0] + w, location[1] + h)
    cv.rectangle(img2, location, bottom_right, 255, 5)
    cv.imshow('match', img2)
    cv.waitKey(0)
    cv.destroyAllWindows() 