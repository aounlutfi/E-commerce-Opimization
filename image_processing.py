import numpy as np
import cv2
import time

from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from skimage.segmentation import felzenszwalb
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float, img_as_ubyte
import tesserocr 


def image_processing(image, verbose = False):
    
    if verbose:
        print "---NEW IMAGE---"
    time_start = time.time()
    id = 0

    time_vco_start = time.time()
    #element = find_visa_checkout(image, id, verbose)
    time_vco_finish = time.time()

    time_button_start = time.time()
    find_buttons_seg(image, True)
    time_button_finish = time.time()



    id+=1

    
    elements = []




    time_end = time.time()

    # print "Elements: "
    # for element in elements:
    #     print "ID: " + str(element["id"])
    #     print "Type: " + element["type"] 
    #     print "Boundries: " + str(element["boundries"])
    #     print "Center: " + str(element["center"])
    #     print "Dimentions: " + str(element["dimentions"])
    #     #print "Text: " + elem.text

    debug = "\n-----------------NEW TEST----------------------------\n"
    debug += "Total Time: " + str(time_end-time_start) + "\n"
    debug += "Average VCO Time: " + str(np.mean(time_vco_finish - time_vco_start)) + "\n"
    debug += "Average Button time: " + str(np.mean(time_button_finish - time_button_start)) + "\n"
    #debug += "---------------------------------------\n"
    #debug += "Segments Times: \n"
    #debug += str(time_segment_finish - time_segment_start)
    debug += "-----------------END OF TEST-----------------------------\n"

    file = open("debug.txt", 'a')
    file.write(debug)
    return elements


def find_visa_checkout(image, id, verbose = False):
    MIN_MATCH_COUNT = 10
    name = "Visa Checkout"
    vco = True
    template = cv2.imread('templates/template_vco.jpg',cv2.IMREAD_GRAYSCALE)


    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(image,None)
    kp2, des2 = sift.detectAndCompute(template,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m_n in matches:
      if len(m_n) != 2:
        continue
      (m,n) = m_n
      if m.distance < 0.6*n.distance:
        good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        try:
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = image.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            if(verbose):

                template = cv2.polylines(template,[np.int32(dst)],True,255,3, cv2.LINE_AA)

                img = image    
                draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                               singlePointColor = None,
                               matchesMask = matchesMask, # draw only inliers
                               flags = 2)
                img = cv2.drawMatches(img,kp1,template,kp2,good,None,**draw_params)
                plt.imshow(img, 'gray'),plt.show()
                plt.gcf().clear()
                img = image    


            good_points_list = []
            points_array = np.int32([kp1[elem.queryIdx].pt  for elem in good])
            points_list = [tuple(elem) for elem in points_array]
            for pt in points_list:
                if(matchesMask[points_list.index(pt)]):
                    good_points_list.append(pt)

            if(verbose):
                corners = find_corners(good_points_list, vco)
                cv2.rectangle(img,corners['top_left'],corners['buttom_right'],(0,0,0))
                plt.imshow(img, 'gray'),plt.show()
                plt.gcf().clear()

            boundries = find_boundries(good_points_list, vco)

            cropped = image[boundries["buttom"]:boundries["top"], boundries["left"]:boundries["right"]]
            cropped = Image.fromarray(cropped)

            center = calculate_center(boundries["top"], boundries["buttom"], boundries["left"], boundries["right"])
            dimentions = calculate_dimentions(boundries["top"], boundries["buttom"], boundries["left"], boundries["right"])

            element = {"id": id, "type": name, "boundries": boundries, "center": center, "dimentions": dimentions, "image": cropped}
            id+=1

            print "Matched " + name
            if(True):
                print "ID: " + str(element["id"])
                print "Type: " + element["type"] 
                print "Boundries: " + str(element["boundries"])
                print "Center: " + str(element["center"])
                print "Dimentions: " + str(element["dimentions"])
                print "Text: " + element["type"]
                plt.imshow(element["image"], 'gray'),plt.show()
                print "-----------------"

            return element

        except Exception, e:
            print "Not enough good matches for " + name
            return None
    
    else:
        print ("Not enough matches are found - %d/%d for " % (len(good),MIN_MATCH_COUNT)) + name
        return None


def find_corners(points, VCO = False):
    
    #find max and min points and apply padding
    maxy=max([q[1] for q in points]) + 10
    miny=min([q[1] for q in points]) - 10
    maxx=max([q[0] for q in points]) + 10
    minx=min([q[0] for q in points]) - 10

    if(VCO):
        minx -= (maxx-minx)/2

    top_left=(minx,maxy)
    top_right=(maxx,maxy)
    buttom_left=(minx,miny)
    buttom_right=(maxx,miny)

    corners = {"top_left" : top_left, "top_right": top_right, "buttom_left": buttom_left, "buttom_right": buttom_right}
    return corners

def find_boundries(points, VCO = False):
    
   #find max and min points and apply padding
    maxy=max([q[1] for q in points]) + 10
    miny=min([q[1] for q in points]) - 10
    maxx=max([q[0] for q in points]) + 10
    minx=min([q[0] for q in points]) - 10

    if(VCO):
        minx -= (maxx-minx)/2

    boundries = {"top" : maxy, "left": minx, "right": maxx, "buttom": miny}
    return boundries

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
    miny=min([q[1] for q in found])
    #top
    maxy=max([q[1] for q in found])
    #right
    maxx=max([q[0] for q in found])
    #left
    minx=min([q[0] for q in found])
    
    boundry_list = {"top" : maxy, "left": minx, "right": maxx, "buttom": miny}
    return boundry_list

def calculate_center(top, buttom, left, right):
    x = (top + buttom)/2
    y = (left + right)/2
    center = {"x": x, "y":y}
    return center

def calculate_dimentions(top, buttom, left, right):
    h = (top - buttom)
    w = (right - left)
    dimentions = {"h": h, "w":w}
    return dimentions


def find_buttons_seg(image, verbose = False):
    
    kernel_edge_enhance = np.array([[-1,-1,-1,-1,-1],
                                 [-1,2,2,2,-1],
                                 [-1,2,8,2,-1],
                                 [-1,2,2,2,-1],
                                 [-1,-1,-1,-1,-1]]) / 8.0

    image = cv2.filter2D(image, -1, kernel_edge_enhance)

    img = img_as_float(image)

    #perform segmentation // min size directly proportional to num of segments
    segments = felzenszwalb(img, scale=500, sigma=6, min_size=250)
    num_segments =  len(np.unique(segments))
    print "number of Segments: " + str(num_segments)

    if(verbose):
        segmented_img = img_as_ubyte(mark_boundaries(img, segments))
        plt.imshow(segmented_img), plt.show()

    verbose = False

    for n in range(0, num_segments):

            boundries = find_segment_corners(segments, n)
            segment_image = image[boundries["left"]:boundries["right"], boundries["buttom"]:boundries["top"]]
            segment_image = (segment_image*255).astype(int)

            up_ratio = 0.6
            down_ratio = 0.1
            img_up_size = tuple([up_ratio*image.shape[0],up_ratio*image.shape[1]])
            img_down_size = tuple([down_ratio*image.shape[0],down_ratio*image.shape[1]])
            
            # if( segment_image.shape[0] > img_down_size[0] and segment_image.shape[1] > img_down_size[1]):
            #     if( segment_image.shape[0] < img_up_size[0] and segment_image.shape[1] > img_up_size[1]):

            img = Image.fromarray(np.uint8(segment_image*255))
            
            try:

                text = tesserocr.image_to_text(img)

                if verbose:
                    print text
                    plt.imshow(segment_image, "gray"), plt.show()

                cnt = "continue"
                shp = "shopping"
                chk = "checkout"
                visa = "visa"
                book = "book"
                pch = "purchase"
                scu = "secure"
                pay = "pay"

                text = text.lower()

                if(shp not in text and len(text.split())<4):
                    if visa in text.split() and chk in text.split():
                        print "matched visa checkout button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    elif (chk in text.split()):
                        print "matched checkout button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    elif (cnt in text.split()):
                        print "matched continue button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    elif book in text.split():
                        print "matched book button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    elif pch in text.split():
                        print "matched purchase button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    elif scu in text.split():
                        print "matched secure button"
                        print text
                        plt.imshow(segment_image, "gray"), plt.show()
                    else:
                        print "No button found in segment " + str(n)
                else:
                    print "No button found in segment " + str(n)
            except Exception, e:
                pass

            


            #     else:
            #         print "Skipped segment " + str(n) + " because too small"
            # else:
            #     print "Skipped segment " + str(n) + " because too large" 

def find_buttons_cont(image, verbose = False):

    _,thresh = cv2.threshold(image,150,255,cv2.THRESH_BINARY_INV) # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    dilated = cv2.dilate(thresh,kernel,iterations = 10) # dilate
    _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

    kernel_edge_enhance = np.array([[-1,-1,-1,-1,-1],
                                 [-1,2,2,2,-1],
                                 [-1,2,8,2,-1],
                                 [-1,2,2,2,-1],
                                 [-1,-1,-1,-1,-1]]) / 8.0

    image = cv2.filter2D(image, -1, kernel_edge_enhance)

    verbose = False
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        # discard areas that are too large
        if h>400 or h<40 or w<40:
            continue

        cropped = image[y:y+h,x:x+w]

        img = Image.fromarray(np.uint8(cropped*255))

        text = tesserocr.image_to_text(img)

        if verbose:
            print text
            plt.imshow(cropped, "gray"), plt.show()

        cnt = "continue"
        chk = "checkout"
        visa = "visa"
        book = "book"
        pch = "purchase"
        scu = "secure"
        pay = "pay"

        text = text.lower()


        if(visa not in text and len(text.split())<4):
            if (chk in text.split()):
                print "matched checkout button"
                print text
                plt.imshow(cropped, "gray"), plt.show()
            elif (cnt in text.split()):
                print "matched checkout button"
                print text
                plt.imshow(cropped, "gray"), plt.show()
            elif book in text.split():
                print "matched checkout button"
                print text
                plt.imshow(cropped, "gray"), plt.show()
            elif pch in text.split():
                print "matched checkout button"
                print text
                plt.imshow(cropped, "gray"), plt.show()
            elif scu in text.split():
                print "matched checkout button"
                print text
                plt.imshow(cropped, "gray"), plt.show()

        # draw rectangle around contour on original image
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)

    # write original image with added contours to disk  
    if(verbose):
        plt.imshow(image), plt.show()


    # elements = []
    # element = {"id": id, "type": name, "boundries": boundries, "center": center, "dimentions": dimentions, "image": cropped}
    # id+=1

    # print "Matched " + name
    # if(True):
    #     print "ID: " + str(element["id"])
    #     print "Type: " + element["type"] 
    #     print "Boundries: " + str(element["boundries"])
    #     print "Center: " + str(element["center"])
    #     print "Dimentions: " + str(element["dimentions"])
    #     print "Text: " + element["type"]
    #     plt.imshow(element["image"], 'gray'),plt.show()
    #     print "-----------------"

    # return element
