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
		#print("pollution success")
	elif(nodename == "s" or nodename == "S"):
		node = currGraph["smoker"]
		node.marginal = priorvalue
		#print("smoker success")
	else:
		print("error")
		
def calcMarginal(currGraph, nodename):
	tilda = False
	retmarginal = 0
	
	if nodename[0] == "~":
		tilda = True
		nodename = nodename[1]
		#print("tilda check success")
		
	if nodename == "s" or nodename =="S":
		node = currGraph["smoker"]
		retmarginal = node.marginal
		#print("smoker success")
	elif nodename == "p" or nodename =="P": 
		node = currGraph["pollution"]
		retmarginal = node.marginal
		#print("pollution success")
	elif nodename == "c" or nodename =="C":
		node = currGraph["cancer"] 
		retmarginal = ((node.conditionals["ps"]*currGraph["pollution"].marginal * currGraph["smoker"].marginal) + (node.conditionals["~ps"]*(1-currGraph["pollution"].marginal)*currGraph["smoker"].marginal) + (node.conditionals["~p~s"]*(1-currGraph["pollution"].marginal)*(1-currGraph["smoker"].marginal)) + (node.conditionals["p~s"]*currGraph["pollution"].marginal*(1-currGraph["smoker"].marginal)))
		#print("cancer success")
	elif nodename == "x" or nodename =="X":
		node = currGraph["xray"]
		cancerMarginal = calcMarginal(currGraph, "c")
		retmarginal = (node.conditionals["c"] * cancerMarginal) + (node.conditionals["~c"] * (1-cancerMarginal))
		#print("xray success")
	elif nodename == "d" or nodename =="D":  
		node = currGraph["dyspnoea"]
		cancerMarginal = calcMarginal(currGraph, "c")
		retmarginal = (node.conditionals["c"] * cancerMarginal) + (node.conditionals["~c"] * (1-cancerMarginal))
		#print("dyspnoea success")
	else:
		print("marginal input error")
		
	if tilda == True:
		print nodename + ": " + str(1.0-retmarginal)	  
		return 1-retmarginal
	else:
		print nodename + ": " + str(retmarginal)
		return retmarginal
		

def calcConditional(currGraph, arg, given):
	ret = 0
	tilda = False
	if given[0] == "~":
		given = given[1]
		tilda = True
	if len(given) == 0:
		ret = calcMarginal(arg)
	elif len(given) == 1: 
		if arg == "p":
			if given == "s":
				print currGraph["pollution"].marginal
		#	elif given == "c":
		#	elif given == "x":
		#	elif given == "d":
		elif arg == "s":
			if given == "p":
				print currGraph["smoker"].marginal
			elif given == "c":
				prob = (calcConditional(currGraph, "c", "s") * currGraph["smoker"].marginal) / calcMarginal(currGraph, "c")
				print prob 
		#	elif given == "x":
			elif given == "d":
				prob = (calcConditional(currGraph, "d", "s") * currGraph["smoker"].marginal) / calcMarginal(currGraph, "d")
				print prob
				return prob
			elif given == "s":
				print 1
				return 1
		elif arg == "c":
			if tilda == True:
				#print "c_given_p_high"
				if given == "p":
					print "c|~p"
					x = currGraph["xray"]
					c = currGraph["cancer"]
					s = currGraph["smoker"]
					p = currGraph["pollution"]
					d = currGraph["dyspnoea"]
					prob = ((c.conditionals["~ps"] * (1-p.marginal) * s.marginal) + (c.conditionals["~p~s"] * (1-p.marginal) * (1-s.marginal))) / (1-p.marginal)
					print prob
					return prob
			elif given == "p":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				prob = ((c.conditionals["ps"] * p.marginal * s.marginal) + (c.conditionals["p~s"] * p.marginal * (1-s.marginal)))/p.marginal
				print prob
				return prob				
			elif given == "s":
				x = currGraph["xray"]
				node = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				prob =((node.conditionals["sp"]*currGraph["smoker"].marginal*currGraph["pollution"].marginal) + (node.conditionals["s~p"]*currGraph["smoker"].marginal*(1-currGraph["pollution"].marginal)))/currGraph["smoker"].marginal
				print prob
				return prob
			elif given == "c":
				print 1
				return 1
		#	elif given == "x":
			elif given == "d":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				print "entered"
				prob = (d.conditionals["c"] * calcMarginal(currGraph, "c") ) / calcMarginal(currGraph, "d")
				print prob
				return prob
	
		elif arg == "x":
			node = currGraph["xray"]
			cancer = currGraph["cancer"]
			smoker = currGraph["smoker"]
			pollution = currGraph["pollution"]
			dyspnoea = currGraph["dyspnoea"]
		#	elif given == "p":
			if given == "s":
				numerator = (node.conditionals["c"] * cancer.conditionals["ps"]*smoker.marginal*pollution.marginal) + (node.conditionals["c"] * cancer.conditionals["~ps"]*smoker.marginal*(1-pollution.marginal)) + (node.conditionals["~c"] * (1-cancer.conditionals["ps"]) * smoker.marginal * pollution.marginal) + (node.conditionals["~c"] * (1-cancer.conditionals["~ps"]) * smoker.marginal * (1-pollution.marginal))
				denominator = (cancer.conditionals["ps"] * pollution.marginal * smoker.marginal) + (cancer.conditionals["~ps"] * (1-pollution.marginal) * smoker.marginal) + ((1-cancer.conditionals["ps"])* pollution.marginal * smoker.marginal) + ((1-cancer.conditionals["~ps"]) * (1-pollution.marginal) * smoker.marginal)
				prob = numerator/denominator
				print prob
				return prob
			elif given == "c":
				print currGraph["xray"].conditionals["c"]
				return currGraph["xray"].conditionals["c"]
			elif given == "d":
				prob = ((node.conditionals["c"]*calcMarginal(currGraph, "c")*dyspnoea.conditionals["c"]) + (node.conditionals["~c"]*calcMarginal(currGraph, "~c")*dyspnoea.conditionals["~c"])) / calcMarginal(currGraph, "d")
				print prob
				return prob
		elif arg == "d":
			if tilda == True:
				if given == "p":
					x = currGraph["xray"]
					c = currGraph["cancer"]
					s = currGraph["smoker"]
					p = currGraph["pollution"]
					d = currGraph["dyspnoea"]
					numerator = (d.conditionals["c"] * (c.conditionals["~ps"]*s.marginal*(1-p.marginal))) + (d.conditionals["c"] * (c.conditionals["~p~s"]*(1-s.marginal)*(1-p.marginal))) + (d.conditionals["~c"] * ((1-c.conditionals["~ps"])*s.marginal*(1-p.marginal))) + (d.conditionals["~c"] * ((1-c.conditionals["~p~s"])*(1-s.marginal)*(1-p.marginal)))
					denominator = (c.conditionals["~ps"]*(1-p.marginal)*s.marginal) + (c.conditionals["~p~s"]*(1-p.marginal)*(1-s.marginal)) + ((1-c.conditionals["~ps"])*(1-p.marginal)*s.marginal) + ((1-c.conditionals["~p~s"])*(1-p.marginal)*(1-s.marginal))
					prob = numerator/denominator
					print prob 
					return prob
			#	elif given == "p":
			#	elif given == "s":
			#	elif given == "c":
			#	elif given == "x":
			else:
				if given == "s":
					print "d|s"
					x = currGraph["xray"]
					c = currGraph["cancer"]
					s = currGraph["smoker"]
					p = currGraph["pollution"]
					d = currGraph["dyspnoea"]
					numerator = (d.conditionals["c"] * (c.conditionals["ps"]*s.marginal*p.marginal)) + (d.conditionals["c"] * (c.conditionals["~ps"]*s.marginal*(1-p.marginal))) + (d.conditionals["~c"] * ((1- c.conditionals["ps"])*s.marginal*p.marginal)) + (d.conditionals["~c"] * ((1- c.conditionals["~ps"])*s.marginal*(1-p.marginal)))
					denominator = (c.conditionals["ps"]*p.marginal*s.marginal) + (c.conditionals["~ps"]*(1-p.marginal)*s.marginal) + ((1-c.conditionals["ps"])*p.marginal*s.marginal) + ((1-c.conditionals["~ps"])*(1-p.marginal)*s.marginal)
					prob = numerator/denominator
					print prob
					return prob
				elif given == "c":
					print "d|c"
					x = currGraph["xray"]
					c = currGraph["cancer"]
					s = currGraph["smoker"]
					p = currGraph["pollution"]
					d = currGraph["dyspnoea"]
					prob = (calcConditional(currGraph, "c", "d") * calcMarginal(currGraph, "d")) / calcMarginal(currGraph, "c")
					print prob
					return prob
				elif given == "d":
					print 1
					return 1
					
		elif arg == "~p":
			if given == "d":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				prob = (calcConditional(currGraph, "d", "~p") * (1-p.marginal)) / calcMarginal(currGraph, "d")
				print prob
				return prob
			elif given == "c":
				print "entered"
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				prob = (calcConditional(currGraph, "c", "~p") * (1-p.marginal)) / calcMarginal(currGraph, "c")
				print prob
				return prob
			elif given == "s":
				print calcMarginal(currGraph, "~p")
				return calcMarginal(currGraph, "~p")
		
	if len(given) == 2:
		if arg == "c":
			if given == "sd" or given == "ds":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				numerator = (d.conditionals["c"] * c.conditionals["ps"] * p.marginal * s.marginal) + (d.conditionals["c"] * c.conditionals["~ps"] * (1-p.marginal) * s.marginal)
				denominator = (d.conditionals["c"] * c.conditionals["ps"] * p.marginal * s.marginal) + (d.conditionals["c"] * c.conditionals["~ps"] * (1-p.marginal) * s.marginal) + (d.conditionals["~c"] * (1-c.conditionals["ps"]) * p.marginal * s.marginal) + (d.conditionals["~c"] * (1-c.conditionals["~ps"]) * (1-p.marginal) * s.marginal)
				prob = numerator/denominator
				print prob
				return prob
		elif arg == "d":
			if given == "cs" or given == "sc":
				print currGraph["dyspnoea"].conditionals["c"]
				return currGraph["dyspnoea"].conditionals["c"]
			if given == "ds" or given == "sd":
				print 1
				return 1
		elif arg == "s":
			if given == "cp" or given == "pc":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				numerator = s.marginal * c.conditionals["ps"] * p.marginal
				denominator = c.conditionals["ps"] * p.marginal * s.marginal + c.conditionals["p~s"] * p.marginal * (1-s.marginal)
				prob = numerator / denominator
				print prob
				return prob
		elif arg == "~p":
			if given == "cs" or given == "sc":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				numerator = c.conditionals["~ps"] * s.marginal * (1-p.marginal)
				denominator = c.conditionals["~ps"]* s.marginal * (1-p.marginal) + c.conditionals["ps"]* s.marginal * p.marginal
				prob = numerator/denominator
				print prob
				return prob
			elif given == "ds" or given == "sd":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				numerator = (d.conditionals["c"]*c.conditionals["~ps"]*(1-p.marginal)*s.marginal) + (d.conditionals["~c"]*(1-c.conditionals["~ps"])*(1-p.marginal)*s.marginal)
				denominator = (d.conditionals["c"]*c.conditionals["~ps"]*(1-p.marginal)*s.marginal) + (d.conditionals["c"]*c.conditionals["ps"]*p.marginal*s.marginal) + (d.conditionals["~c"]*(1-c.conditionals["~ps"])*(1-p.marginal)*s.marginal) + (d.conditionals["~c"]*(1-c.conditionals["ps"])*p.marginal*s.marginal)
				prob = numerator/denominator
				print prob
				return prob
		elif arg == "x":
			if given == "ds" or given == "sd":
				x = currGraph["xray"]
				c = currGraph["cancer"]
				s = currGraph["smoker"]
				p = currGraph["pollution"]
				d = currGraph["dyspnoea"]
				numerator = (x.conditionals["c"] * d.conditionals["c"] * c.conditionals["~ps"] * (1-p.marginal) * s.marginal) + (x.conditionals["~c"] * d.conditionals["~c"] * (1-c.conditionals["~ps"]) * (1-p.marginal) * s.marginal) + (x.conditionals["c"] * d.conditionals["c"] * c.conditionals["ps"] * p.marginal * s.marginal) + (x.conditionals["~c"] * d.conditionals["~c"] * (1-c.conditionals["ps"]) * p.marginal * s.marginal)
				denominator = (d.conditionals["c"] * c.conditionals["~ps"] * (1-p.marginal)  *  s.marginal) + (d.conditionals["~c"] * (1-c.conditionals["~ps"]) * (1-p.marginal) * s.marginal) + (d.conditionals["c"] * c.conditionals["ps"] * p.marginal * s.marginal) + (d.conditionals["~c"] * (1-c.conditionals["ps"]) * p.marginal * s.marginal)
				prob = numerator/denominator
				print prob
				return prob
			elif given == "cs" or given == "sc":
				print currGraph["xray"].conditionals["c"]
				return currGraph["xray"].conditionals["c"]
	
def parseString(nodenames):
	nodeList = []
	i = 0
	while (i < len(nodenames)):
		if nodenames[i] == "~":
			i = i + 1
			nodename = nodenames[i-1] + nodenames[1]
			nodeList.append(nodename)
		else:
			nodeList.append(nodename)
		i += 1
	return nodeList

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
			#print "flag", o
			#print "args", a
			#print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("l")
			#print a[:p]
			#print a[p+1:]
			calcConditional(Graph, a[:p], a[p+1:])
		elif o in ("-j"):
			#print "flag", o
			#print "args", a
			calcJoint(Graph, a)
		else:
			assert False, "unhandled option"
		
	# ...

if __name__ == "__main__":
	main()
