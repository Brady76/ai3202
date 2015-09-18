Command line input:
python Astarmaze.py <Heuristic Choice (1 or 2)> <World(1 or 2).txt>
Example:
python Astarmaze.py 1 World1.txt

My function for my second heuristic was:
def heuristic2(goalnode, nextnode):
	vertical = abs(goalnode[0] - nextnode[0])
	horizontal = abs(goalnode[1] - nextnode[1])
	distance = math.sqrt((vertical*vertical) + (horizontal * horizontal))
	return distance * 10
	
So my basic equation is a^2 + b^2 = c^2

I thought this would be better than the Manhattan heuristic because it improves on it's concept of getting a 
distance between where we're at and the goal.

Performance:
My heuristic found a path 26 points shorter but evaluated 15 more nodes.

Manhattan heuristic path for World1:
(0, 9)
(0, 8)
(0, 7)
(0, 6)
(0, 5)
(1, 4)
(2, 3)
(2, 2)
(3, 1)
(4, 1)
(5, 1)
(6, 1)
(7, 0)

My heuristic path for World1:
(0, 9)
(0, 8)
(1, 7)
(2, 7)
(3, 6)
(3, 5)
(4, 4)
(5, 4)
(6, 3)
(7, 2)
(7, 1)
(7, 0)
