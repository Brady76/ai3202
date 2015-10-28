import getopt
import sys

class Node:
	def __init__(self):
		self.marginal = 0
		self.conditionals = {}
		self.name = ""
		self.parents = []
		self.grandparents = []
		self.children = []
		self.grandchildren = []
		
def initGraph():
	pollution = Node()
	smoker = Node()
	cancer = Node()
	xray = Node()
	dyspnoea = Node()
	
	pollution.children.append("c")
	pollution.grandchildren.append("x")
	pollution.grandchildren.append("d")
	
	smoker.children.append("c")
	smoker.grandchildren.append("x")
	smoker.grandchildren.append("d")
	
	cancer.parents.append("p")
	cancer.parents.append("s")
	cancer.children.append("x")
	cancer.children.append("d")
	
	xray.grandparents.append("p")
	xray.grandparents.append("s")
	xray.parents.append("c")
	
	dyspnoea.grandparents.append("p")
	dyspnoea.grandparents.append("s")
	dyspnoea.parents.append("c")
	
	#Below varies on prior values of pollution/marginal
	pollution.marginal = 0.9
	smoker.marginal = 0.3
	
	cancer.conditionals["~ps"] = 0.05
	cancer.conditionals["s~p"] = 0.05
	cancer.conditionals["ps"] = 0.03
	cancer.conditionals["sp"] = 0.03
	cancer.conditionals["~p~s"] = 0.02
	cancer.conditionals["~s~p"] = 0.02
	cancer.conditionals["p~s"] = 0.001
	cancer.conditionals["~sp"] = 0.001
	
	xray.conditionals["c"] = 0.9
	xray.conditionals["~c"] = 0.2
	
	dyspnoea.conditionals["c"] = 0.65
	dyspnoea.conditionals["~c"] = 0.3
	
	globaldict = {"smoker": smoker, "pollution": pollution, "cancer": cancer, "xray": xray, "dyspnoea": dyspnoea} 
	return globaldict 
	 
def setPrior(currGraph, nodename, priorvalue):
	if(nodename == "p" or nodename == "P"):
		node = currGraph["pollution"]
		node.marginal = priorvalue
		print("pollution success")
	elif(nodename == "s" or nodename == "S"):
		node = currGraph["smoker"]
		node.marginal = priorvalue
		print("smoker success")
	else:
		print("error")
		
def calcMarginal(currGraph, nodename):
	tilda = False
	retmarginal = 0
	
	if nodename[0] == "~":
		tilda = True
		nodename = nodename[1]
		print("tilda check success")
		
	if nodename == "s" or nodename =="S":
		node = currGraph["smoker"]
		retmarginal = node.marginal
		print("smoker success")
	elif nodename == "p" or nodename =="P": 
		node = currGraph["pollution"]
		retmarginal = node.marginal
		print("pollution success")
	elif nodename == "c" or nodename =="C":
		node = currGraph["cancer"] 
		retmarginal = ((node.conditionals["ps"]*currGraph["pollution"].marginal * currGraph["smoker"].marginal) + (node.conditionals["~ps"]*(1-currGraph["pollution"].marginal)*currGraph["smoker"].marginal) + (node.conditionals["~p~s"]*(1-currGraph["pollution"].marginal)*(1-currGraph["smoker"].marginal)) + (node.conditionals["p~s"]*currGraph["pollution"].marginal*(1-currGraph["smoker"].marginal)))
		print("cancer success")
	elif nodename == "x" or nodename =="X":
		node = currGraph["xray"]
		cancerMarginal = calcMarginal(currGraph, "c")
		retmarginal = (node.conditionals["c"] * cancerMarginal) + (node.conditionals["~c"] * (1-cancerMarginal))
		print("xray success")
	elif nodename == "d" or nodename =="D":  
		node = currGraph["dyspnoea"]
		cancerMarginal = calcMarginal(currGraph, "c")
		retmarginal = (node.conditionals["c"] * cancerMarginal) + (node.conditionals["~c"] * (1-cancerMarginal))
		print("dyspnoea success")
	else:
		print("marginal input error")
		
	if tilda == True:
		print nodename + ": " + str(1.0-retmarginal)	  
		return 1-retmarginal
	else:
		print nodename + ": " + str(retmarginal)
		return retmarginal

def main():
	Graph = initGraph()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			#print "flag", o
			#print "args", a
			#print a[0]
			#print float(a[1:])
			setPrior(Graph, a[0], float(a[1:]))
		elif o in ("-m"):
			#print "flag", o
			#print "args", a
			#print type(a)
			calcMarginal(Graph, a)
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("l")
			print a[:p]
			print a[p+1:]
			calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
		else:
			assert False, "unhandled option"
		
	# ...

if __name__ == "__main__":
	main()
