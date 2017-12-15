import cv2
import time
import json

import matplotlib
matplotlib.use('agg')

import src.web_classification as clas
import src.web_capture as cap
import src.image_processing as im
import src.modeling as m
import src.evaluation as ev

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


def save (elem, name):
    elem = json.dumps(elem)
    file = open("tests/" + name, 'w')
    file.write(elem)
    file.close()

def load(name):
    file = open("tests/" + name, 'r')
    elements = file.read()
    elements = json.loads(elements)
    elements = byteify(elements)
    return elements
    
open('tests/image_processing_debug.txt', 'w').close()
open('tests/elements.txt', 'w').close()
open('tests/model.txt', 'w').close()

img = cv2.imread('samples/merchant4.jpg',cv2.IMREAD_GRAYSCALE)    

verbose = False

elements = im.image_processing(img, verbose)
model = m.modeling(elements, img, verbose)
score, recommendations = ev.score(model, None, verbose)
