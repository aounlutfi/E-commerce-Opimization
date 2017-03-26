from collections import Counter

TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1

def modeling(elements, image, verbose):

	elements = clean_duplicates(elements, verbose)


def clean_duplicates(elements, verbose):
	
	for element in elements:
		print element
		for elem in elements:
			print elem
			if len(elem and elements)==7:
				print "ignored elem"
				pass
			else:
				if abs(elem["center"]["x"] - element["center"]["x"])<element["dimentions"]["h"] and abs(elem["center"]["y"] - element["center"]["y"])<element["dimentions"]["w"]:
					"removed elem"
					elements.remove(elem)
				else:
					print "nothing done"
			print "-------"
