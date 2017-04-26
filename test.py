import cv2
import time
import json

import web_classification as clas
import web_capture as cap
import image_processing as im
import modeling as m
import scoring as sc

from collections import Counter

verbose = False

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('ascii')
    else:
        return input

open('tests/image_processing_debug.txt', 'w').close()
open('tests/elements.txt', 'w').close()
open('tests/model.txt', 'w').close()

img1 = cv2.imread('samples/merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
img2 = cv2.imread('samples/merchant2.jpg',cv2.IMREAD_GRAYSCALE)    
img3 = cv2.imread('samples/merchant3.jpg',cv2.IMREAD_GRAYSCALE)    
img4 = cv2.imread('samples/merchant4.jpg',cv2.IMREAD_GRAYSCALE)    
img5 = cv2.imread('samples/merchant5.jpg',cv2.IMREAD_GRAYSCALE)    
img6 = cv2.imread('samples/merchant6.jpg',cv2.IMREAD_GRAYSCALE)    
img7 = cv2.imread('samples/merchant7.jpg',cv2.IMREAD_GRAYSCALE)    
img8 = cv2.imread('samples/merchant8.jpg',cv2.IMREAD_GRAYSCALE)
img9 = cv2.imread('samples/merchant9.jpg',cv2.IMREAD_GRAYSCALE)

elements1 = im.image_processing(img1, verbose)
model1 = m.modeling(elements1, img1, verbose)
# img, elements, model = img1, elements1, model1

elements2 = im.image_processing(img2, verbose)
model2 = m.modeling(elements2, img2, verbose)
# img, elements, model = img2, elements2, model2

elements3 = im.image_processing(img3, verbose)
model3 = m.modeling(elements3, img3, verbose)
# img, elements, model = img3, elements3, model3

elements4 = im.image_processing(img4, verbose)
model4 = m.modeling(elements4, img4, verbose)
# img, elements, model = img4, elements4, model4

elements5 = im.image_processing(img5, verbose)
model5 = m.modeling(elements5, img5, verbose)
# img, elements, model = img5, elements5, model5

elements6 = im.image_processing(img6, verbose)
model6 = m.modeling(elements6, img6, verbose)
# img, elements, model = img6, elements6, model6

elements7 = im.image_processing(img7, verbose)
model7 = m.modeling(elements7, img7, verbose)
# img, elements, model = img7, elements7, model7

elements8 = im.image_processing(img8, verbose)
model8 = m.modeling(elements8, img8, verbose)
# img, elements, model = img8, elements8, model8

elements9 = im.image_processing(img9, verbose)
model9 = m.modeling(elements9, img9, verbose)
# img, elements, model = img9, elements9, model9


# elem = json.dumps(elements4)
# file = open("tests/element", 'w')
# file.write(elem)
# file.close()

# file = open("tests/element", 'r')
# elements = file.read()
# elements = json.loads(elements)
# elements = byteify(elements)
# elements4 = elements

#model = m.modeling(elements, img, verbose)
#score, recommendations = sc.score(model, verbose)
