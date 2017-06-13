# This file is part of E-Commerce Optimization (ECO) 

# The (ECO) can be obtained at https://github.com/aounlutfi/E-commerce-Opimization
# ECO Copyright (C) 2017 Aoun Lutfi, University of Wollongong in Dubai
# Inquiries: aounlutfi@gmail.com

# The ECO is free software: you can redistribute it and/or modify it under the 
# terms of the GNU Lesser General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later version.

# ECO is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
# See the GNU Less General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with TSAM. 
# If not, see <http://www.gnu.org/licenses/>.

# If you use the ECO or any part of it in any program or publication, please acknowledge 
# its authors by adding a reference to this publication:

# Lutfi, A., Fasciani, S. (2017) Towards Automated Optimization of Web Interfaces and 
# Application in E-commerce, Accepted for publications at International Journal of 
# Computing and Information Sciences.

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

#Constants 
TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1
VCO = "visa checkout"
CHK = "checkout"
CNT = "continue shopping"

def image_processing(image, verbose=False, debug=False):

    print "---NEW IMAGE---"

    time_start = time.time()
    #main processing 
    elements, seg_num, seg_times = find_buttons_seg(image, verbose)

    time_end = time.time()
    #debugging and logging data
    if debug:
        #store elements to file
        elem = "\n-------------------NEW TEST-------------------------------\n"
        elem += "Elements " + str(len(elements)) + " :\n"
        for element in elements:
            elem += "ID: " + str(element["id"])+ " \n"
            elem += "Type: " + element["type"] + " \n"
            elem += "Boundries: " + str(element["boundries"])+ " \n"
            elem += "Center: " + str(element["center"])+ " \n"
            elem += "Dimentions: " + str(element["dimentions"])+ " \n"
            elem += "Text: " + element["text"]+ " \n"
            elem += "-------\n"
        elem += "\n-----------------END OF TEST-------------------------------\n"

        #write to file
        file = open("tests/elements.txt", 'a')
        file.write(elem)
        file.close()

        #store time data to files
        #calculate time data
        total_time = time_end-time_start
        total_seg_time = sum(seg_times)
        avg_seg_time = total_seg_time/seg_num
        pp_time = total_time - total_seg_time

        #store time data
        debug = "\n-------------------NEW TEST-------------------------------\n"
        debug += "Total Time: " + str(total_time) + "\n"
        debug += "Pre-processing Time: " + str(pp_time) + "\n"
        debug += "Total segmentation Time: " + str(total_seg_time) + "\n"
        debug += "Number of Segments: " + str(seg_num) + "\n"
        debug += "Average Segments Time: " + str(avg_seg_time) + "\n"
        debug += "Total Number of Elements: " + str(len(elements)) + "\n"
        debug += "\n-----------------END OF TEST-----------------------------\n"

        #write to file
        file = open("tests/image_processing_debug.txt", 'a')
        file.write(debug)
        file.close()

    return elements


def find_buttons_seg(image, verbose=False):

    id = 0

    #apply edge enhancing filter
    kernel_edge_enhance = np.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0
    image = cv2.filter2D(image, -1, kernel_edge_enhance)

    #segment image into segments
    img = img_as_float(image)
    segments = felzenszwalb(img, scale=500, sigma=6, min_size=250)
    num_segments =  len(np.unique(segments))
    print "number of Segments: " + str(num_segments)

    segmented_img = img_as_ubyte(mark_boundaries(img, segments))
    plt.imshow(segmented_img)
    
    try:
        if verbose:
            plt.show()
        plt.savefig("tests/" + str(time.time()) + "_segmented.jpg")
    except Exception, e:
        plt.savefig("tests/" + str(time.time()) + "_segmented.jpg")

    seg_time_start = []
    seg_time_finish = []
    elements = []

    #template for visa checkout
    template = cv2.imread("vco_template.jpg",cv2.IMREAD_GRAYSCALE)

    #go through each element
    for n in range(0, num_segments):
        seg_time_start.append(time.time())

        #obtain segment boundaries
        boundries = find_segment_corners(segments, n)
        segment_image = image[boundries[LEFT]:boundries[RIGHT], boundries[BUTTOM]:boundries[TOP]]

        #check if segment is too small, then ignore
        if abs(boundries[LEFT]-boundries[RIGHT])<10 or abs(boundries[BUTTOM]-boundries[TOP]) < 10:
            print "segment " + str(n) + " too small to process"
        else:

            try:                
                if verbose:
                    print text
                    plt.imshow(segment_image), plt.show()
                
                #match segment with visa checkout template
                if match_template(template, segment_image, verbose):
                    #if segment is too large ignore, else the add a visa checkout segment
                    if abs(boundries[LEFT]-boundries[RIGHT])<250 and abs(boundries[BUTTOM]-boundries[TOP])<1000:
                        elements.append(add_element(boundries, VCO, "Visa Checkout", id))
                        id+=1
                        print "matched visa checkout button"
                    else:
                        print "segment" + str(n) + " too large for visa checkout"
                else:
                    #obtain text using OCR
                    text = OCR(segment_image)

                    #string constants to search
                    cnt = "continue"
                    shp = "shopping"
                    chk = "checkout"
                    book = "book"
                    pch = "purchase"
                    scu = "secure"
                    pay = "pay"
                    visa = "visa"
                    back = "back"
                    cncl = "cancel"
                    
                    #check if text length less than 4, then check for each constant, if there is a match, add the relevant element
                    if(len(text.split())<4):
                        if (chk in text.split() and visa not in text.split()):
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched checkout button"
                        elif book in text.split():
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched book button"
                        elif pch in text.split():
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched purchase button"
                        elif scu in text.split():
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched secure button"
                        elif pay in text.split():
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched pay button"
                        elif cnt in text.split() and shp not in text.split():
                            elements.append(add_element(boundries, CHK, text, id))
                            id+=1
                            print "matched chekcout button"
                        elif shp in text.split() and cnt in text.split():
                            elements.append(add_element(boundries, CNT, text, id))
                            id+=1
                            print "matched continue button"
                        elif cncl in text.split() or back in text.split():
                            elements.append(add_element(boundries, CNT, text, id))
                            id+=1
                            print "matched continue button"
                        else:
                            print "No button found in segment " + str(n)
                    else:
                        print "No button found in segment " + str(n)
            
            except Exception, e:
                print e

        seg_time_finish.append(time.time())
    print "number of elements: " + str(len(elements))
    return elements, num_segments, list(map(operator.sub, seg_time_finish, seg_time_start))

def add_element(boundries, name, text, id):
    #add returns a new element dictionary as per the input details, calculates the center and dimentions from the boundaries

    center = calculate_center(boundries[TOP], boundries[BUTTOM], boundries[LEFT], boundries[RIGHT])
    dimentions = calculate_dimentions(boundries[TOP], boundries[BUTTOM], boundries[LEFT], boundries[RIGHT])

    element = {"id": id, "type": name, "boundries": boundries, "center": center, "dimentions": dimentions, "text":text}

    return element

def find_segment_corners(array, segment):
    #returns a touple indicating the boundaries of the segment
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
    #calculates the center from 4 boundaries
    x = (top + buttom)/2
    y = (left + right)/2
    center = (x,y)
    return center

def calculate_dimentions(top, buttom, left, right):
    #calculates the dimentions from 4 boundaries
    h = (top - buttom)
    w = (right - left)
    dimentions = (h,w)
    return dimentions

def match_template(img1, img2, verbose = False):
    #matches 2 images using sift keypoints descriptor 
    img2 = cv2.copyMakeBorder(img2, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=0)

    #detect keypoints and calculate descriptors
    sift = cv2.SIFT()
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    #configure the FLANN matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    #obtain the matches
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    #identify if enough matches exist
    MIN_MATCH_COUNT = 10
    if len(good)>MIN_MATCH_COUNT:
        if verbose:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3)
            img3 = cv2.drawMatches(img1,kp1,img2,kp2,good)
            cv2.imshow("matches", img3)
        return True
        
    else: return False



  
def OCR(img):
    #obtain text using Tesseract OCR engine
    img = (img*255).astype(int)  
    img = Image.fromarray(np.uint8(img*255))
    #python wrapper for Tesseract
    text = image_to_string(img)
    #clean and format text
    text = "".join([s for s in text.strip().splitlines(True) if s.strip("\r\n").strip()])
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    return text



def drawMatches(img1, kp1, img2, kp2, matches):
    """
    Implementation of cv2.drawMatches by rayryeng as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)

    # Also return the image if you'd like a copy
    return out