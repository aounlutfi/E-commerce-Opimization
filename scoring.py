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


def score(model, classification, verbose = False):
    
    with open("rules.txt") as f:
        rules = f.readlines()
    
    ruleset = parse_rules(rules)

    if verbose:
        for rule  in rules:
            rule = str(rule).lower().replace("\n", "")
            print rule
        print "\n"
        for rule in ruleset:
            print rule

    evaluate(ruleset, model)


def evaluate(ruleset, model, verbose = False):
    G = model[0]
    positions = model[1]
    labels = model[2]

    score = 0

    element_score = 100/len(ruleset)
    alignment_score = 100/len(ruleset)
    distance_score = 100/len(ruleset)
    size_score = 100/len(ruleset)
    text_score = 100/len(ruleset)

    nodes = []
    edges = []


    for rule in ruleset:
        if verbose:
            pass
        if rule["rule"] == "element":
            for i in range(0, G.number_of_nodes()):
                if G.node[i]['type'] == rule['parameter']:
                    score = score + element_score
                    temp = dict(G.node[i])
                    temp['id'] = rule['ids']
                    nodes.append(temp)
    
    for element in nodes:
		temp = list(nodes)
		temp.remove(element)		
		for elem in temp:
			edges.append({'id': (element['id'], elem['id']), 'distance':distance(elem, element)})
    
    if verbose:
        print "Nodes: "
        for node in nodes:
            print node
        print "Edges: "
        for edge in edges:
            print edge
                 
    
    for rule in ruleset:
        if rule["rule"] == "alignment":
            pass
        elif rule["rule"] == "distance":
            if "+" in rule['parameter']:
                dist = rule['parameter'].remove("+")
                for edge in edges:
                    pass
            if "-" in rule['parameter']:
                dist = rule['parameter'].replace("+", "")
                for edge in edges:
                    pass
        elif rule["rule"] == "size":
            pass
        elif rule["rule"] == "text":
            pass
    
def parse_rules(rules):
        
    ruleset = []

    for rule in rules:
        
        rule = str(rule).lower().replace("\n", "")

        if "element" in rule and "is" in rule:
            type = str(rule.split("is ")[1])
            id = rule.split()[1]
            ruleset.append({"rule": "element", "ids": (id), "parameter":type})

            #element 1 is visa checkout
        
        elif "element" in rule and ("left of" in rule or "right of" in rule or "above" in rule or "below" in rule):
            id1 = rule.split()[1]
            id2 = rule.split()[-1]
            parameter = rule.replace("element ", "").replace(" of", "").split()[1]
            ruleset.append({"rule": "alignment", "ids": (id1, id2), "parameter":parameter})
            
            #element 1 left of element 2

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
            
            #element 1 no more than 100px from element 2
            
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
            
            #width of element 1 more than element 2    
            
        elif "element" in rule and "contains" in rule:
            id = rule.split()[1]
            text = rule.split('"')[1]
            ruleset.append({"rule": "text", "ids": id1, "parameter":text})            
            
            #element 2 contains "checkout"

        else:
            if rule:
                print "Error parsing line " + str(rules.index(rule)+1)
    return ruleset

def distance(elem1, elem2):
	return int(round(math.sqrt((elem1["center"][X] - elem2["center"][X])**2 + (elem1["center"][Y] - elem2["center"][Y])**2)))
