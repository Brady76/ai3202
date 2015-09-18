import Queue
import math
import sys
#Holds all terrainTypes
Matrix = []
myfile = open(sys.argv[2],'r')
Matrix = [[int(n) for n in line.split()] for line in myfile]
#Holds coordinates
Coordinates = []
for x in range(8):
    for y in range(10):
        Coordinates.append([x, y])
print Coordinates
        
openList = Queue.PriorityQueue()
openList.put((1,(7,0)))
came_from = {}
cost_so_far = {}
came_from[(7,0)] = None
cost_so_far[(7,0)] = 0
location_to_terrain = {}
previoussquares = {}
#indexes coordinates to terrain values 
for x in range(8):
	for y in range(10):
		location_to_terrain[(x,y)] = Matrix[x][y]
#print(location_to_terrain[(7,1)])
		
#Finds neighboring squares
def neighbors(node):
	dirs = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
	result = []
	for dir in dirs:
		neighbor = [node[0] + dir[0], node[1] + dir[1]]
		#only append if the index exists
		if neighbor in Coordinates  and location_to_terrain[(tuple(neighbor))] != 2:
			result.append([node[0] + dir[0],node[1] + dir[1]])
	return result

def cost(currentnode,nextnode):
	cost = 0
	#Horizontal cases
	if(currentnode[0] + 1 == nextnode[0] and currentnode[1] == nextnode[1]):
		cost += 10
	elif(currentnode[0] - 1 == nextnode[0] and currentnode[1] == nextnode[1]):
		cost += 10
	elif(currentnode[1] + 1 == nextnode[1] and currentnode[0] == nextnode[0]):
		cost += 10
	elif(currentnode[1] - 1 == nextnode[1] and currentnode[0] == nextnode[0]):
		cost += 10
	#Diagnol cases
	elif(currentnode[0] + 1 == nextnode[0] and currentnode[1] + 1 == nextnode[1]):
		cost += 14
	elif(currentnode[0] + 1 == nextnode[0] and currentnode[1] - 1 == nextnode[1]):
		cost += 14
	elif(currentnode[0] - 1 == nextnode[0] and currentnode[1] + 1 == nextnode[1]):
		cost += 14
	elif(currentnode[0] - 1 == nextnode[0] and currentnode[1] - 1 == nextnode[1]):
		cost += 14
	#If the terrain has mountains 
	if(location_to_terrain[tuple(nextnode)] == 1):
		cost += 10
	return cost
	
def heuristic(goalnode, nextnode):
	vertical = abs(goalnode[0] - nextnode[0])
	horizontal = abs(goalnode[1] - nextnode[1])
	return (vertical + horizontal) * 10

def heuristic2(goalnode, nextnode):
	vertical = abs(goalnode[0] - nextnode[0])
	horizontal = abs(goalnode[1] - nextnode[1])
	distance = math.sqrt((vertical*vertical) + (horizontal * horizontal))
	return distance * 10
	
path = []
def findpath(endnode):
	if endnode != (7,0):
		print(previoussquares[endnode])
		findpath(previoussquares[endnode])
		
goal = (0,9)	
nodes_evaluated = 0
print sys.argv[1]
if(sys.argv[1] == '1'):
	heuristictwo = False
else:
	heuristictwo = True
while not openList.empty():
   current = openList.get()[1]
   if current == (0,9):
      break
   for next in neighbors(current):
      new_cost = cost_so_far[tuple(current)] + cost(current, next)
      #if the node hasn't been added to our closed list, or if our newly calculated cost is less than it already is we need to replace it 
      if tuple(next) not in cost_so_far or new_cost < cost_so_far[tuple(next)]:
         nodes_evaluated += 1
         cost_so_far[tuple(next)] = new_cost
         if(heuristictwo == False):
			 priority = (new_cost + heuristic(goal, next))
         else:
			 priority = (new_cost + heuristic2(goal, next))
         openList.put((priority,tuple(next)))
         previoussquares[tuple(next)] = current
         came_from[tuple(next)] = current

print "Path is as follows: "
print (0,9)
findpath((0,9))
print "Nodes evaluated is: ", nodes_evaluated
print "Path cost is: ", cost_so_far[(0,9)]

