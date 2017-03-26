import cv2
import time

import web_classification as clas
import web_capture as cap
import image_processing as im
import modeling as m

from collections import Counter


verbose = True
# open('image_processing_debug.txt', 'w').close()
# open('elements.txt', 'w').close()

elements = []
image = 0


element1 = {"id": 0, "type": "Continue Shopping", "boundries": {'buttom': 652, 'top': 1142, 'right': 1054, 'left': 933}, "center": {'y': 993, 'x': 897}, "dimentions": {'h': 490, 'w': 121}, "text":"continue shopping"}
element2 = {"id": 0, "type": "Checkout", "boundries": {'buttom': 1175, 'top': 1646, 'right': 1045, 'left': 942}, "center": {'y': 993, 'x': 1410}, "dimentions": {'h': 471, 'w': 103}, "text":"secure clmdtmn"}
element3 = {"id": 0, "type": "Visa Checkout", "boundries": {'buttom': 1920, 'top': 2129, 'right': 1004, 'left': 967}, "center": {'y': 985, 'x': 2024}, "dimentions": {'h': 209, 'w': 37}, "text":"visa checkout"}
element4 = {"id": 0, "type": "Continue Shopping", "boundries": {'buttom': 750, 'top': 1043, 'right': 1017, 'left': 970}, "center": {'y': 993, 'x': 896}, "dimentions": {'h': 293, 'w': 47}, "text":"continue shopping"}

elements.append(element1)
elements.append(element2)
elements.append(element3)
elements.append(element4)

# img1 = cv2.imread('samples/merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
# img2 = cv2.imread('samples/merchant2.jpg',cv2.IMREAD_GRAYSCALE)    
# img3 = cv2.imread('samples/merchant3.jpg',cv2.IMREAD_GRAYSCALE)    
# img4 = cv2.imread('samples/merchant4.jpg',cv2.IMREAD_GRAYSCALE)    
# img5 = cv2.imread('samples/merchant5.jpg',cv2.IMREAD_GRAYSCALE)    
# img6 = cv2.imread('samples/merchant6.jpg',cv2.IMREAD_GRAYSCALE)    
# img7 = cv2.imread('samples/merchant7.jpg',cv2.IMREAD_GRAYSCALE)    
# img8 = cv2.imread('samples/merchant8.jpg',cv2.IMREAD_GRAYSCALE)
# img9 = cv2.imread('samples/merchant9.jpg',cv2.IMREAD_GRAYSCALE)



start = time.time()

#elements = im.image_processing(img1, verbose)
model1 = m.modeling(elements, image, verbose)
# elements2 = im.image_processing(img2, verbose)
# elements3 = im.image_processing(img3, verbose)
# elements4 = im.image_processing(img4, verbose)
# elements5 = im.image_processing(img5, verbose)
# elements6 = im.image_processing(img6, verbose)
# elements7 = im.image_processing(img7, verbose)
# elements8 = im.image_processing(img8, verbose)
# elements9 = im.image_processing(img9, verbose)

end = time.time()

print "Total time: " + str(end - start)