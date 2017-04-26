import networkx as nx
import matplotlib.pyplot as plt
import math
import time

TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1

def modeling(elements, image = None, verbose = False):
	
	elements = clean_duplicates(elements, verbose)
	print "number of clean elements: " + str(len(elements))
	G = nx.Graph()
	G.clear()

	i = 0
	labels = {}
	positions = []
	for element in elements:
		G.add_node(i)
		G.node[i] = element

		labels[i] = i
		positions.append(element["center"])
		
		i += 1
	
	dist = []
	i = 0
	for element in elements:
		temp = list(elements)
		temp.remove(element)		
		for elem in temp:
			G.add_edge(elem["id"], element['id'])
			d = distance(elem, element)
			dist.append((i, "distance: " + str(d)))
 			G.edge[elem['id']][element['id']] = d
			i+=1

	if verbose:
		for i in range(0, G.number_of_nodes()):
			print G.node[i]
		print "links: " + str(G.number_of_edges())
		print G.edges()
		for element in elements:
			temp = list(elements)
			temp.remove(element)		
			for elem in temp:
				e = G.edge[elem['id']][element['id']]
				if e:
					print e
	
	model = "\n-------------------MODEL-------------------------------\n"
	model += "nodes: " + str(G.number_of_nodes()) + "\n"
	for i in range(0, G.number_of_nodes()):
		model += str(G.node[i]) + "\n"
	model += "links: " + str(G.number_of_edges()) + "\n"
	model += str(G.edges()) + "\n"
	for element in elements:
		temp = list(elements)
		temp.remove(element)		
		for elem in temp:
			e = G.edge[elem['id']][element['id']]
			if e:
				model += str(e) + "\n"
	
	file = open("tests/model.txt", 'a')
	file.write(model)
	file.close()

	nx.draw_networkx_edges(G, positions)
	nx.draw_networkx_edge_labels(G, positions,  font_size = 6)
	nx.draw_networkx_nodes(G, positions, node_size=500, alpha=0.7)
	nx.draw_networkx_labels(G,positions,labels, font_color='w')
	if image is not None:
		plt.imshow(image, "gray")
	try:
		if verbose:
			plt.show()
		plt.savefig("tests/" + str(time.time()) + "_model.jpg")
	except Exception, e:
		plt.savefig("tests/" + str(time.time()) + "_model.jpg")

	plt.clf()
	return (G, positions, labels)

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

def distance(elem1, elem2):
	return int(round(math.sqrt((elem1["center"][X] - elem2["center"][X])**2 + (elem1["center"][Y] - elem2["center"][Y])**2)))