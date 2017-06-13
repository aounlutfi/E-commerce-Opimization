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

import re
import nltk.data

from bs4 import BeautifulSoup
from nltk.corpus import stopwords # Import the stop word list
from collections import Counter


#set verbose to True for detailed output
def web_classification(html, verbose = False):

    nltk.data.path.append("nltk_data")

    #cleaning:
    #remove html tags
    for script in html(["script", "style"]):
        script.extract()   
    
    if (verbose):
        print ("- Removed scripts and styles")

    #convert to text
    text = html.get_text()

    #apply bag of words
    words = bag_of_words(text)
    if(verbose):
        print ("- Applied bag of words ")

    #prepare histogram of words frequencies
    word_list = words.split(" ")
    hist = Counter (word_list)

    if(verbose):
        print(hist)

    #keywords
    airlines_keys = ["airline", "boarding", "ticket", 'tickets' , "travel", "airplane", "fight", "flights", "booking"]
    hotels_keys = ["hotel", 'hotels', "room", "rooms", "night", 'nights', "booking"]
    tickets_keys = ['ticket', 'tickets', 'cinema', 'show', 'shows', 'performance', 'performances', 'movie', 'movies']
    food_keys = ['food', 'delivery', 'meal', 'meals', 'order', 'combo']
    generic_keys = ['generic', 'electronics', 'flowers', 'fashion', 'kids', 'delivery', 'phone', 'tv', 'computer', 'toy', 'toys', 'flower', 'florist']

    #scores
    airline_score = 0
    hotels_score = 0
    tickets_score = 0
    food_score = 0
    generic_score = 0

    #check for keywords and increment score if a keyword is found
    for word in hist:
        if word in hotels_keys:
            hotels_score+= hist[word]
        if word in airlines_keys:
            airline_score+=hist[word]
        if word in tickets_keys:
            tickets_score+=hist[word]
        if word in food_keys:
            food_score+=hist[word]
        if word in generic_keys:
            generic_score+=hist[word]

    #find the word wth the highest score
    classification_list = {'airline':airline_score, 'hotel':hotels_score,'tickets':tickets_score, 'food':food_score, 'generic':generic_score}
    v=list(classification_list.values())
    k=list(classification_list.keys())
    classification = k[v.index(max(v))]

    print ("- The website is " + classification)
    return classification


def bag_of_words( text ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    # 1. break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # 2. break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # 3. drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # 4. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", text) 
    # 5. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    # 6. In Python, searching a set is much faster than searching a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 7. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    # 8. Join the words back into one string separated by space, and return the result.
    return( " ".join( meaningful_words ))