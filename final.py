import web_classification as clas
import web_capture as cap
import image_processing as im
import modeling as m
import scoring as sc

import cv2
import threading

classification = None
model = None

class classificationThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "Starting " + self.name
        classification = clas.web_classification(soup)
        print "Exiting " + self.name

class imageThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "Starting " + self.name
        elements = im.image_processing(img)
        model = m.modeling(elements, img)
        print "Exiting " + self.name


# file = open("urls","r") 
# urls = file.readlines()
# for url in urls:

open('tests/image_processing_debug.txt', 'w').close()
open('tests/elements.txt', 'w').close()
open('tests/model.txt', 'w').close()

img = cv2.imread('samples/merchant1.jpg',cv2.IMREAD_GRAYSCALE)    
url = 'http://google.com'
print("for " + url)

soup = cap.web_capture(url)
if (soup ==1 ):
	print ('error url refused access')

else:
    cThread = classificationThread(1, "classification")
    iThread = imageThread(2, "image processing")
    
    cThread.start()
    iThread.start()
    
    cThread.join()
    iThread.join()
    
    score = sc.score(model, classification)