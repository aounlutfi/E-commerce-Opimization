import numpy as np
import cv2
import time
import operator

import matplotlib.pyplot as plt

from pytesser import image_to_string
from PIL import Image, ImageOps
from skimage.segmentation import felzenszwalb
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float, img_as_ubyte

TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1

def image_processing(image, verbose=False):

    print "---NEW IMAGE---"

    time_start = time.time()

    elements, seg_num, seg_times = find_buttons_seg(image, verbose)

    time_end = time.time()

    elem = "\n-------------------NEW TEST-------------------------------\n"
    elem += "Elements " + str(len(elements)) + ": \n"
    for element in elements:
        elem += "ID: " + str(element["id"])+ ": \n"
        elem += "Type: " + element["type"] + ": \n"
        elem += "Boundries: " + str(element["boundries"])+ ": \n"
        elem += "Center: " + str(element["center"])+ ": \n"
        elem += "Dimentions: " + str(element["dimentions"])+ ": \n"
        elem += "Text: " + element["text"]+ ": \n"
        elem += "-------\n"
    elem += "\n-----------------END OF TEST-------------------------------\n"

    file = open("tests/elements.txt", 'a')
    file.write(elem)
    file.close()

    total_time = time_end-time_start
    total_seg_time = sum(seg_times)
    avg_seg_time = total_seg_time/seg_num
    pp_time = total_time - total_seg_time

    debug = "\n-------------------NEW TEST-------------------------------\n"
    debug += "Total Time: " + str(total_time) + "\n"
    debug += "Pre-processing Time: " + str(pp_time) + "\n"
    debug += "Total segmentation Time: " + str(total_seg_time) + "\n"
    debug += "Number of Segments: " + str(seg_num) + "\n"
    debug += "Average Segments Time: " + str(avg_seg_time) + "\n"
    debug += "Total Number of Elements: " + str(len(elements)) + "\n"
    debug += "\n-----------------END OF TEST-----------------------------\n"

    file = open("tests/image_processing_debug.txt", 'a')
    file.write(debug)
    file.close()

    return elements




def find_buttons_seg(image, verbose=False):

    id = 0

    kernel_edge_enhance = np.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0
    image = cv2.filter2D(image, -1, kernel_edge_enhance)

    img = img_as_float(image)
    segments = felzenszwalb(img, scale=500, sigma=6, min_size=250)
    num_segments =  len(np.unique(segments))
    print "- number of Segments: " + str(num_segments)

    if verbose:
        segmented_img = img_as_ubyte(mark_boundaries(img, segments))
        plt.imshow(segmented_img), plt.show()

    seg_time_start = []
    seg_time_finish = []
    elements = []

    for n in range(0, num_segments):
        seg_time_start.append(time.time())

        boundries = find_segment_corners(segments, n)
        segment_image = image[boundries[LEFT]:boundries[RIGHT], boundries[BUTTOM]:boundries[TOP]]
        segment_image = (segment_image*255).astype(int)

        img = Image.fromarray(np.uint8(segment_image*255))
        
        try:

            text = image_to_string(img)
            text = "".join([s for s in text.strip().splitlines(True) if s.strip("\r\n").strip()])
            text = text.encode('ascii', 'ignore').decode('ascii')
            text = text.lower()

            if verbose:
                print text
                plt.imshow(segment_image), plt.show()

            cnt = "continue"
            shp = "shopping"
            chk = "checkout"
            visa = "visa"
            book = "book"
            pch = "purchase"
            scu = "secure"
            pay = "pay"


            if(len(text.split())<4):
                if (visa in text.split() and chk in text.split()) or (visa in text.split() and len(text.split())<3):
                    elements.append(add_element(boundries, "visa checkout", text, id))
                    id+=1
                    print "matched visa checkout button"
                elif (chk in text.split()):
                    elements.append(add_element(boundries, "checkout", text, id))
                    id+=1
                    print "matched checkout button"
                elif book in text.split():
                    elements.append(add_element(boundries, "checkout", text, id))
                    id+=1
                    print "matched book button"
                elif pch in text.split():
                    elements.append(add_element(boundries, "checkout", text, id))
                    id+=1
                    print "matched purchase button"
                elif scu in text.split():
                    elements.append(add_element(boundries, "checkout", text, id))
                    id+=1
                    print "matched secure button"
                elif shp in text and cnt in text:
                    elements.append(add_element(boundries, "continue shopping", text, id))
                    id+=1
                else:
                    print "No button found in segment " + str(n)
            else:
                print "No button found in segment " + str(n)
        except Exception, e:
            print e

        seg_time_finish.append(time.time())

    return elements, num_segments, list(map(operator.sub, seg_time_finish, seg_time_start))

def add_element(boundries, name, text, id):
    
    center = calculate_center(boundries[TOP], boundries[BUTTOM], boundries[LEFT], boundries[RIGHT])
    dimentions = calculate_dimentions(boundries[TOP], boundries[BUTTOM], boundries[LEFT], boundries[RIGHT])

    element = {"id": id, "type": name, "boundries": boundries, "center": center, "dimentions": dimentions, "text":text}

    return element

def find_segment_corners(array, segment):

    #find segment boundries
    width = len(array[0])
    found = []
    posn = 0
    for row in array:
        for col in row:
            if col == segment:
                found.append((posn // width, posn % width))
            posn += 1

    #buttom
    miny = min([q[1] for q in found])
    #top
    maxy = max([q[1] for q in found])
    #right
    maxx = max([q[0] for q in found])
    #left
    minx = min([q[0] for q in found])

    boundry_list = (maxy, minx, maxx, miny)
    return boundry_list

def calculate_center(top, buttom, left, right):
    x = (top + buttom)/2
    y = (left + right)/2
    center = (x,y)
    return center

def calculate_dimentions(top, buttom, left, right):
    h = (top - buttom)
    w = (right - left)
    dimentions = (h,w)
    return dimentions