import web_classification as clas
import web_capture as cap
import image_processing as im
from collections import Counter
import cv2



img1 = cv2.imread('merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
img2 = cv2.imread('merchant2.jpg',cv2.IMREAD_GRAYSCALE)    
img3 = cv2.imread('merchant3.jpg',cv2.IMREAD_GRAYSCALE)    
img4 = cv2.imread('merchant4.jpg',cv2.IMREAD_GRAYSCALE)    


#elements1 = im.image_processing(img1, True)
#elements2 = im.image_processing(img2, True)
#elements3 = im.image_processing(img3, True)
#elements4 = im.image_processing(img4, True)

cap.web_capture("https://www.marriott.com/reservation/guestInfo.mi", verbose = True)

# debug = "Elements 1: \n" + str(elements1) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 2: \n" + str(elements2) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 3: \n" + str(elements3) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 4: \n" + str(elements4) + "\n"

# file = open("elements.txt", 'w')
# file.write(debug)