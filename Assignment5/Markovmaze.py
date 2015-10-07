import Queue
import math
import sys
#Holds all terrainTypes
epsilon = float(sys.argv[1])
Matrix = []
myfile = open(sys.argv[2],'r')
Matrix = [[int(n) for n in line.split()] for line in myfile]
#Holds coordinates
Coordinates = []
for x in range(8):
    for y in range(10):
        Coordinates.append([x, y])
#print Coordinates

discount = 0.9
utility = {}
direction = {}
location_to_terrain = {}

#indexes coordinates to terrain values 
for x in range(8):
	for y in range(10):
		location_to_terrain[(x,y)] = Matrix[x][y]

#Initializes utility of each square to be their reward		
for x in range(8):
	for y in range(10):
		utility[(x,y)] = 0

def reward(currentnode):
	#Blank space
	if(location_to_terrain[tuple(currentnode)] == 0):
		return 0
	#Mountains
	elif(location_to_terrain[tuple(currentnode)] == 1 ):
		return -1
	#Walls
	elif(location_to_terrain[tuple(currentnode)] == 2 ):
		return ("-inf")
	#Snake
	elif(location_to_terrain[tuple(currentnode)] == 3 ):
		return -2
	#Barn
	elif(location_to_terrain[tuple(currentnode)] == 4 ):
		return 1
	#Out of Bounds
	elif(location_to_terrain[tuple(currentnode)] == None):
		return 0
	#Goal
	elif(location_to_terrain[tuple(currentnode)] == 50 ):
		return 50
		
def bellman(node):
	up = [node[0] - 1, node[1]]
	right = [node[0], node[1] + 1]
	down = [node[0] + 1, node[1]]
	left = [node[0], node[1] - 1]
	dirs = [up, right, down, left]
	for dir in dirs:
		if(dir[0] < 0 or dir[0] > 7):
			utility[tuple(dir)] = 0
		if(dir[1] < 0 or dir[1] > 9):
			utility[tuple(dir)] = 0
	upvalue = (0.8 * utility[tuple(up)]) + (0.1 * utility[tuple(left)]) + (0.1 * utility[tuple(right)])
	rightvalue = (0.8 * utility[tuple(right)]) + (0.1 * utility[tuple(up)]) + (0.1 * utility[tuple(down)])
	downvalue = (0.8 * utility[tuple(down)]) + (0.1 * utility[tuple(right)]) + (0.1 * utility[tuple(left)])
	leftvalue = (0.8 * utility[tuple(left)]) + (0.1 * utility[tuple(up)]) + (0.1 * utility[tuple(down)])
	values = [upvalue,rightvalue,downvalue,leftvalue]
	maxvalue = max(values)
	maxvalueindex = values.index(maxvalue)
	return (maxvalue, maxvalueindex)
			
delta = 1
counter = 0
while(delta > epsilon*((1-discount)/discount)):
	counter += 1
	delta = 0
	u = 0
	for i,row in enumerate(Matrix):
		for j,col in enumerate(row):
			if(location_to_terrain[(i,j)] != 2):
				u = utility[(i,j)]
				rewardvalue = reward((i,j))
				umax = bellman((i,j))
				uprime = rewardvalue + discount * umax[0]
				utility[(i,j)] = uprime
				direction[(i,j)] = umax[1]
				if(abs(u - uprime)) > delta:
					delta = abs(u - uprime)
					#print "Delta is: ", delta
					#print "The upper bound is: ", epsilon*((1-discount)/discount)
					#print "i is: ", i, " j is: ", j
	#print "Iteration count: ", counter
	#for x in range(8):
	#	for y in range(10):
	#		if(location_to_terrain[(x,y)] != 2):
	#			print "(",x,",",y,")  ", (utility[(x,y)]), " Direction: ", direction[(x,y)]


current = [7,0]
totalutil = utility[tuple(current)]
while(current != [0,9]):
	print "Current location is: ", current, " current utility is: ", utility[tuple(current)]
	#up
	if(direction[tuple(current)] == 0):
		current = [current[0] - 1, current[1]]
	#right
	elif(direction[tuple(current)] == 1):
		current = [current[0], current[1] + 1]
	#down
	elif(direction[tuple(current)] == 2):
		current = [current[0] + 1, current[1]]
	#left
	elif(direction[tuple(current)] == 3):
		current = [current[0], current[1] - 1]
	totalutil += utility[tuple(current)]

print "Current location is: ", current, " current utility is: ", utility[tuple(current)]

