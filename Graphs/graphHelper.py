import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from graph import Graph
import collections

########################################################################
# Import Data & Set up Folium Map
########################################################################

points = pd.read_csv("city_coordinates.csv", delimiter= ",")

# Creating random Edges
probability_of_edge = 0.07
random_state = np.random.RandomState(seed=420)
randomEdges = random_state.choice([0,1], 
                                  size=(len(points), len(points)), 
                                  p = [1 - probability_of_edge,probability_of_edge])
np.fill_diagonal(randomEdges, 0)
for i in range(0, len(randomEdges)):
    for j in range(i+1, len(randomEdges)):
            randomEdges[i][j] = randomEdges[j][i]

undirectedGraph = Graph()
names = points.Name
for i in names:
    undirectedGraph.add_node(i)

for i in range(len(randomEdges)):
    origin = names.iloc[i]
    for destination in points.Name[randomEdges[i] == 1]:
        undirectedGraph.add_edge(origin, destination)


########################################################################
# Basic Plotting Methods
########################################################################

def plotMap():
	map = folium.Map(location=[39.764519, -104.995196], zoom_start=4)
	for node in undirectedGraph.nodes():
		folium.Marker(points[points.Name == node][['Latitude', 'Longitude']].values[0], popup = node).add_to(map)

	for edge in undirectedGraph.edges():
		val = points[(points.Name == edge[0])|(points.Name == edge[1])][["Latitude", "Longitude"]].values
		folium.PolyLine(val, color="blue", weight=1, opacity=1).add_to(map)

	return map

def plotDFS(origin, destination):
	parents = DFS(origin, destination)
	route = getRoute(parents, destination)
	return plotRoute(route)

def plotBFS(origin, destination):
	parents = BFS(origin, destination)
	route = getRoute(parents, destination)
	return plotRoute(route)

def plotRoute(route):
	
	map = folium.Map(location=[39.764519, -104.995196], zoom_start=4)
	for node in undirectedGraph.nodes():
		folium.Marker(points[points.Name == node][['Latitude', 'Longitude']].values[0], popup = node).add_to(map)

	for edge in undirectedGraph.edges():
		val = points[(points.Name == edge[0])|(points.Name == edge[1])][["Latitude", "Longitude"]].values
		folium.PolyLine(val, color="blue", weight=1, opacity=1).add_to(map)

	if (len(route) > 1):
		for i in range(len(route)-1):
			key = route[i]
			destination = route[i+1]
			val = points[(points.Name == key)|(points.Name == destination)][["Latitude", "Longitude"]].values
			folium.PolyLine(val, color="red", weight=5, opacity=1).add_to(map)

	return map

def DFS(origin, destination):
	
	parents = {el:None for el in undirectedGraph.nodes()}

	#initial stack
	stack = []

	#add origin to the stack
	stack.append(origin)
	discovered = []
	counter = 1
	print("Node Searched in each Iteration")
	while (len(stack) != 0):
		curNode = stack.pop()
		print("Iteration " + str(counter) + ": " + curNode)
		counter = counter + 1
		if curNode == destination:
			break

		if (curNode not in discovered):
			discovered.append(curNode)
			for neighbor in undirectedGraph.neighbors(curNode):
				if neighbor not in discovered:
					parents[neighbor] = curNode
					stack.append(neighbor)
	return parents

def BFS(origin, destination):

	parents = {el:None for el in undirectedGraph.nodes()}

	#initial queue
	queue = collections.deque()

	#add origin to the queue
	queue.append(origin)
	discovered = []
	counter = 1
	print("Node Searched in each Iteration")
	while (len(queue) != 0):
		curNode = queue.popleft()
		print("Iteration " + str(counter) + ": " + curNode)
		counter = counter + 1
		if curNode == destination:
			break

		if (curNode not in discovered):
			discovered.append(curNode)
			for neighbor in undirectedGraph.neighbors(curNode):
				if neighbor not in discovered:
					parents[neighbor] = curNode
					queue.append(neighbor)
	return parents

def getRoute(parents, destination):
    route = [destination]
    
    #find the parent node of the destination
    curNode = parents[destination]
    
    while (curNode != None):
        #prepend the parent
        route = [curNode] + route
        curNode = parents[curNode]
    
    return route









