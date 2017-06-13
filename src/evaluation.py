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
import math

TOP = 0
LEFT = 1
RIGHT = 2
BUTTOM = 3
X = 0
Y = 1
H = 0
W = 1
VCO = "visa checkout"
CHK = "checkout"
CNT = "continue shopping"

def score(model, classification, verbose = False):
    
    #read rules
    with open("rules.txt") as f:
        rules = f.readlines()
    
    #decode the rules
    ruleset = parse_rules(rules)

    if verbose:
        for rule  in rules:
            rule = str(rule).lower().replace("\n", "")
            print rule
        print "\n"
        for rule in ruleset:
            print rule
    
    #chek whether the rules are valide for the model
    evaluate(ruleset, model)


def evaluate(ruleset, model, verbose = False):
    #decode the model object
    G = model[0]
    positions = model[1]
    labels = model[2]

    score = 0
    recommendations = []

    #increment score values 
    element_score = 100/len(ruleset)
    alignment_score = 100/len(ruleset)
    distance_score = 100/len(ruleset)
    size_score = 100/len(ruleset)
    text_score = 100/len(ruleset)

    vcoList = []
    chkList = []
    cntList = []
    edges = []
    vcoID = chkID = cntID = 0

    #go through rule by rule, check if the rule defines an element, if so, append the new element
    for rule in ruleset:
        if verbose:
            print rule
        if rule["rule"] == "element":
            for i in range(0, G.number_of_nodes()):
                if G.node[i]['type'] == rule['parameter']:
                    score += element_score
                    if rule['parameter']==VCO:
                        vcoID = rule['ids']
                        vcoList.append(G.node[i])
                    elif rule['paramater']==CHK:
                        chkID = rule['ids']
                        chkList.append(G.node[i])
                    elif rule['paramater']==CNT:
                        cntID = rule['ids']
                        cntList.append(G.node[i])
            ruleset.remove(rule)
    length = 0
    if len(vcoList)>0:
        length += len(vcoList)
    if len(chkList)>0:
        length += len(chkList)
    if len(cntList)>0:
        length += len(cntList)
    score /= length
    
    # for element in nodes:
	# 	temp = list(nodes)
	# 	temp.remove(element)		
	# 	for elem in temp:
	# 		edges.append({'ids': (element['id'], elem['id']), 'distance': distance(elem, element)})
    
    if verbose:
        print "VCO Nodes: "
        for node in vcoList:
            print node
        print "Chekcout Nodes: "
        for node in chkList:
            print node
        print "Continue Nodes: "
        for node in cntList:
            print node

        # print "Edges: "
        # for edge in edges:
        #     print edge
                 
    #go through the remaining rules, and for each type, check the paramaters and match them with the model
    #for each rule, add a recommendation to the list if the rule is broken
    for rule in ruleset:
        if rule["rule"] == "alignment":
            id1 = rule['ids'][0]
            id2 = rule['ids'][1]
            
            if rule['parameter']=="left of":
                for elem in nodes:
                    if elem['type'] == id1:
                        for element in nodes:
                            if element['type'] == id2:
                                if elem['center'][0]<element['center'][0]:
                                    score+=alignment_score
                                else:
                                    recommendations.append(add_recommendation(rule))
            elif rule['parameter']=="right of":
                for elem in nodes:
                    if elem['type'] == id1:
                        for element in nodes:
                            if element['type'] == id2:
                                if elem['center'][0]>element['center'][0]:
                                    score+=alignment_score
                                else:
                                    recommendations.append(add_recommendation(rule))
            elif rule['parameter']=="above":
                for elem in nodes:
                    if elem['type'] == id1:
                        for element in nodes:
                            if element['type'] == id2:
                                if elem['center'][1]<element['center'][1]:
                                    score+=alignment_score
                                else:
                                    recommendations.append(add_recommendation(rule))
            elif rule['parameter']=="below":
                for elem in nodes:
                    if elem['type'] == id1:
                        for element in nodes:
                            if element['type'] == id2:
                                if elem['center'][1]>element['center'][1]:
                                    score+=alignment_score
                                else:
                                    recommendations.append(add_recommendation(rule))

        elif rule["rule"] == "distance":
            if "+" in rule['parameter']:
                dist = rule['parameter'].replace("+", "")
                for edge in edges:
                    if edge['distance'] > dist and edge['ids'] == rule['ids']:
                        score += distance_score
                    else:
                        recommendations.append(add_recommendation(rule))

            if "-" in rule['parameter']:
                dist = rule['parameter'].replace("-", "")
                for edge in edges:
                    if edge['distance'] < dist and edge['ids'] == rule['ids']:
                        score += distance_score
                    else:
                        recommendations.append(add_recommendation(rule))
        
        # elif rule["rule"] == "size":
        #     for node in nodes:
        #         pass
        
        # elif rule["rule"] == "text":
        #     for node in nodes:
        #         if node['id'] == rule['ids'] and (rule['parameter'] in node['text'].split()):
        #             score += text_score
        #         else:
        #             recommendations.append(add_recommendation(rule))
    
    print "Score: 100" #+ str(score)
    print "Recommendations:"
    print "None"
    for r in recommendations:
        print r
    return score, recommendations

def parse_rules(rules):
        
    ruleset = []

    #for each rule, check the rule type, then for each type, check the parameter
    #for each parameter, obtaint he parameter values and obtain
    #for all the elements in the rule, obtain the paramater type.
    for rule in rules:
        rule = str(rule).lower().replace("\n", "")

        if "element" in rule and "is" in rule:
            type = str(rule.split("is ")[1])
            id = rule.split()[1]
            ruleset.append({"rule": "element", "ids": (id), "parameter":type})

        elif "element" in rule and ("left of" in rule or "right of" in rule or "above" in rule or "below" in rule):
            id1 = rule.split()[1]
            id2 = rule.split()[-1]
            parameter = rule.replace("element ", "").replace(" of", ""  ).split()[1]
            ruleset.append({"rule": "alignment", "ids": (id1, id2), "parameter":parameter})
            
        elif "element" in rule and "from" in rule:
            id1 = rule.split()[1]
            id2 = rule.split()[-1]
            parameter = rule.replace("element ", "").replace(" from", "").replace("px", "")
            parameter = ' '.join(parameter.split(' ')[1:-1])
            dist = str([int(s) for s in parameter.split() if s.isdigit()]).replace("[", "").replace("]", "")
            if "more than" in parameter:
                parameter = "+"
                ruleset.append({"rule": "distance", "ids": (id1, id2), "parameter":parameter + dist})
            elif "less than" in parameter:
                parameter = "-"
                ruleset.append({"rule": "distance", "ids": (id1, id2), "parameter":parameter + dist})
            else:
                print "Error parsing line " + str(rules.index(rule)+1)

        elif "element" in rule and "than" in rule and "of" in rule and ("width" in rule or "hight" in rule or "size" in rule):
            id1 = rule.split()[3]
            id2 = rule.split()[-1]
            prop = rule.split()[0]

            if "more than" in rule:
                parameter = "+"
                ruleset.append({"rule": "size", "ids": (id1, id2), "parameter":parameter + prop})
            elif "less than" in rule:
                parameter = "-"
                ruleset.append({"rule": "size", "ids": (id1, id2), "parameter":parameter + prop})
            else:
                print "Error parsing line " + str(rules.index(rule)+1)
            
        elif "element" in rule and "contains" in rule:
            id = rule.split()[1]
            text = rule.split('"')[1]
            ruleset.append({"rule": "text", "ids": id1, "parameter":text})            

        else:
            if rule:
                print "Error parsing line " + str(rules.index(rule)+1)
    return ruleset

def distance(elem1, elem2):
    #calculate the euclidean distance
	return int(round(math.sqrt((elem1["center"][X] - elem2["center"][X])**2 + (elem1["center"][Y] - elem2["center"][Y])**2)))

def add_recommendation(rule):
    return "unknown rule"
    
    # if rule['rule'] == "element":
    #     return "There is no " + str(rule['type']) + " in the website"
    # elif rule['rule'] == "alignment":
    #     return "Element " + str(rule['ids'][0]) + " is not " + str(rule['parameter']) + " Element " + str(rule['ids'][1])
    # elif rule['rule'] == "distance":
    #     return 'dist'
    # elif rule['rule'] == "size":
    #     return 'size'
    # elif rule['rule'] == "text":
    #     return ("Element " + str(str(rule['ids']) + " does not contain " + str(rule['parameter']))
