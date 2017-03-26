from collections import Counter

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
