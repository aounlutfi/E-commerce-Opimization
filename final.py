import web_classification as clas
import web_capture as cap
import image_processing as im
import threading

file = open("urls","r") 
urls = file.readlines()

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
        im.image_processing()
        print "Exiting " + self.name

#for url in urls:
url = 'http://google.com'
print("for " + url)
soup = cap.web_capture(url)
if (soup ==1 ):
	print ('error url refused access')
	#break 
else:
	#cThread = classificationThread(1, "classification")
	#iThread = imageThread(2, "image processing")
	
	#cThread.start()
	#iThread.start()

	#cThread.join()
	#iThread.join()

	##start modeling