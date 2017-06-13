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
	
	#remove redundant elements
	elements = clean_duplicates(elements, verbose)
	print "number of clean elements: " + str(len(elements))
	#setup graph
	G = nx.Graph()
	G.clear()

	i = 0
	labels = {}
	positions = []
	#attach elements to nodes
	for element in elements:
		G.add_node(i)
		G.node[i] = element

		labels[i] = i
		positions.append(element["center"])
		
		i += 1
	
	dist = []
	i = 0
	#attach distances to edges
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
	
	#save model details
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
	
	#save to file
	file = open("tests/model.txt", 'a')
	file.write(model)
	file.close()

	#draw model 
	nx.draw_networkx_edges(G, positions)
	nx.draw_networkx_edge_labels(G, positions,  font_size = 6)
	nx.draw_networkx_nodes(G, positions, node_size=500, alpha=0.7)
	nx.draw_networkx_labels(G,positions,labels, font_color='w')
	if image is not None:
		plt.imshow(image, "gray")
	#save model into an image
	try:
		if verbose:
			plt.show()
		plt.savefig("tests/" + str(time.time()) + "_model.jpg")
	except Exception, e:
		plt.savefig("tests/" + str(time.time()) + "_model.jpg")

	plt.clf()
	return (G, positions, labels)

def clean_duplicates(elements, verbose):
	#to clean duplicates, go through each element, and look through the remaining elemnts and see if there is a match
	#if a match exists, remove the duplicate
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
	#reset ids of elements
	for element in elements:
		element["id"] = id
		id += 1
	return elements

def distance(elem1, elem2):
	#calculate the distance using euclidean distance
	return int(round(math.sqrt((elem1["center"][X] - elem2["center"][X])**2 + (elem1["center"][Y] - elem2["center"][Y])**2)))