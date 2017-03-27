import networkx as nx
import matplotlib.pyplot as plt

from PIL import Image

TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1

def modeling(elements, image, verbose = False):
	
	elements = clean_duplicates(elements, verbose)

	G = nx.Graph()

	i = 0
	labels = {}
	positions = []
	for element in elements:
		G.add_node(i)
		G.node[i] = element

		labels[i] = i
		positions.append(element["center"])
		
		i += 1
	
		

	if verbose:
		print "nodes: " + str(G.number_of_nodes())
		for i in range(0, G.number_of_nodes()):
			print G.node[i]
		print "links: " + str(G.number_of_edges())
	
	nx.draw_networkx_nodes(G, positions, node_size=1000)
	nx.draw_networkx_labels(G,positions,labels, font_color='w')
	plt.imshow(image, "gray")
	plt.show()


def clean_duplicates(elements, verbose):
	
	for element in elements:
		temp = list(elements)
		temp.remove(element)
		if verbose:
			print "checking id: " + str(element['id'])
		for elem in temp:
			if abs(elem["center"][X] - element["center"][X])<element["dimentions"][H] and abs(elem["center"][Y] - element["center"][Y])<element["dimentions"][W]:
				elements.remove(elem)
				if verbose:
					print 'removed ' + str(elem['id'])
			else:
				if verbose:
					print 'kept ' + str(elem['id']) 

	id = 0
	for element in elements:
		element["id"] = id
		id += 1
	return elements