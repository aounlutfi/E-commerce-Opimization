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

import urllib2

from bs4 import BeautifulSoup
from selenium import webdriver

IMG = 1
HTML = 2

#settings:  0 to execute web capture and html capture
#           1 for image capture
#           2 for web capture
#set verbose to True for detailed output
def web_capture(url, settings = 0, verbose = False):

    print ("Starting website capture...")


	#IMAGE	
    if(settings == 1 or settings == 0):
    	#Load webdriver and take screenshot
        web = webdriver.PhantomJS()
        web.get(url)
        web.save_screenshot('screenshot.png')
        print("- Obtained screenshot")
        web.quit

	#HTML
    if (settings == 2 or settings == 0):
    	#header: user agenst
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

    	#Open url and read html text
    	#request header sets user agent to mozilla or apple or chrome to spoof websites that produce error 403
        request = urllib2.Request(url, headers=hdr)

        try:
            page = urllib2.urlopen(request)
            soup = BeautifulSoup(page, 'html.parser')
            print ("- Obtained HTML text") 
            if (verbose):
                print soup
            return soup
        except urllib2.HTTPError, e:
            print e.fp.read()
            return 1

