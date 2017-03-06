import web_classification as clas
import web_capture as cap
import image_processing as im
from collections import Counter
import cv2



img1 = cv2.imread('samples/merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
img2 = cv2.imread('samples/merchant2.jpg',cv2.IMREAD_GRAYSCALE)    
img3 = cv2.imread('samples/merchant3.jpg',cv2.IMREAD_GRAYSCALE)    
img4 = cv2.imread('samples/merchant4.jpg',cv2.IMREAD_GRAYSCALE)    
img5 = cv2.imread('samples/merchant5.jpg',cv2.IMREAD_GRAYSCALE)    
img6 = cv2.imread('samples/merchant6.jpg',cv2.IMREAD_GRAYSCALE)    
img7 = cv2.imread('samples/merchant7.jpg',cv2.IMREAD_GRAYSCALE)    
img8 = cv2.imread('samples/merchant8.jpg',cv2.IMREAD_GRAYSCALE)
img9 = cv2.imread('samples/merchant8.jpg',cv2.IMREAD_GRAYSCALE)

elements1 = im.image_processing(img1, True)
#elements2 = im.image_processing(img2, True)
#elements3 = im.image_processing(img3, True)
#elements4 = im.image_processing(img4, True)
#elements5 = im.image_processing(img5, True)
#elements6 = im.image_processing(img6, True)
#elements7 = im.image_processing(img7, True)
#elements8 = im.image_processing(img8, True)
#elements9 = im.image_processing(img9, True)

# debug = "Elements 1: \n" + str(elements1) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 2: \n" + str(elements2) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 3: \n" + str(elements3) + "\n"
# debug += "---------------------------------------\n"
# debug += "Elements 4: \n" + str(elements4) + "\n"

# file = open("elements.txt", 'w')
# file.write(debug)