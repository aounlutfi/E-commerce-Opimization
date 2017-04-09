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

# img1 = cv2.imread('samples/merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
# img2 = cv2.imread('samples/merchant2.jpg',cv2.IMREAD_GRAYSCALE)    
# img3 = cv2.imread('samples/merchant3.jpg',cv2.IMREAD_GRAYSCALE)    
# img4 = cv2.imread('samples/merchant4.jpg',cv2.IMREAD_GRAYSCALE)    
# img5 = cv2.imread('samples/merchant5.jpg',cv2.IMREAD_GRAYSCALE)    
# img6 = cv2.imread('samples/merchant6.jpg',cv2.IMREAD_GRAYSCALE)    
# img7 = cv2.imread('samples/merchant7.jpg',cv2.IMREAD_GRAYSCALE)    
# img8 = cv2.imread('samples/merchant8.jpg',cv2.IMREAD_GRAYSCALE)
# img9 = cv2.imread('samples/merchant9.jpg',cv2.IMREAD_GRAYSCALE)

# elements1 = im.image_processing(img1, verbose)
# model = m.modeling(elements1, img1, verbose)

# elements2 = im.image_processing(img2, verbose)
# model = m.modeling(elements2, img2, verbose)

# elements3 = im.image_processing(img3, verbose)
# model = m.modeling(elements3, img3, verbose)

# elements4 = im.image_processing(img4, verbose)
# model = m.modeling(elements4, img4, verbose)

# elements5 = im.image_processing(img5, verbose)
# model = m.modeling(elements5, img5, verbose)

# elements6 = im.image_processing(img6, verbose)
# model = m.modeling(elements6, img6, verbose)

# elements7 = im.image_processing(img7, verbose)
# model = m.modeling(elements7, img7, verbose)

# elements8 = im.image_processing(img8, verbose)
# model = m.modeling(elements8, img8, verbose)

# elements9 = im.image_processing(img9, verbose)
# model = m.modeling(elements9, img9, verbose)


# elem = json.dumps(elements4)

# file = open("element", 'w')
# file.write(elem)
# file.close()

# file = open("element", 'r')
# elements = file.read()
# elements = json.loads(elements)
# elements = byteify(elements)

sc.score(model, verbose)