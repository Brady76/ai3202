import sys
functionCall = sys.argv[1]
def emissionProbability():
	if functionCall == "e":
		print("Emission Probability")
	countingDictionary = {}
	with open("typos20.data","r") as textfile:
		for a in textfile.readlines():
			if (a[0],a[2]) in countingDictionary:
				countingDictionary[(a[0],a[2])] = countingDictionary[(a[0],a[2])] + 1
			else:
				countingDictionary[(a[0],a[2])] = 2

	probabilityDictionary = {}
	for i in sorted(countingDictionary):
		numCount = countingDictionary[i]
		denCount = 26
		t1 = i[0]
		for i2 in countingDictionary:
			t2 = i2[0]
			if t1 == t2:
				denCount = denCount + countingDictionary[i2]
		probabilityDictionary[i] = numCount/denCount
		if functionCall == "e":
			print(i,countingDictionary[i])
			print(i,probabilityDictionary[i])
	return probabilityDictionary

def transitionProbability():
	if functionCall == "t":
		print("Transition Probability")
	countingDictionary = {}
	fileStringArray = []
	with open("typos20.data","r") as textfile:
		for a in textfile.readlines():
			fileStringArray.append(a[0])
	index = 0
	for i in fileStringArray:
		if index+1 == len(fileStringArray):
			break
		elif (fileStringArray[index],fileStringArray[index+1]) in countingDictionary:
			countingDictionary[(fileStringArray[index],fileStringArray[index+1])] = countingDictionary[(fileStringArray[index],fileStringArray[index+1])] + 1
		else:
			countingDictionary[(fileStringArray[index],fileStringArray[index+1])] = 2
		index += 1

	probabilityDictionary = {}
	for i in sorted(countingDictionary):
		numCount = countingDictionary[i]
		denCount = 27
		t1 = i[0] 
		for i2 in countingDictionary:
			t2 = i2[0]
			if t1 == t2:
				denCount = denCount + countingDictionary[i2]
		probabilityDictionary[i] = numCount/denCount
		if functionCall == "t":
			print(i,countingDictionary[i])
			print(i,probabilityDictionary[i])
	return probabilityDictionary

def probabilityDistribution():
	print("Initial Probability Distribution:")
	emissionProbability2 = emissionProbability()
	transitionProbability2 = transitionProbability()
	with open("typos20.data","r") as textfile:
		for a in textfile.readlines():
			initialstateS = a[0]
			initialstateO = a[2]
			break
	print ("Emission Probabilities")
	for i in emissionProbability2:
		t1 = i[0]
		t2 = i[1]
		if t1 == initialstateS:
			print (i,emissionProbability2[i]) 
		#If we were supposed to make the initial distribution based off of the output instead of the state, I wanted to make sure the code was here
		#if t2 == initialstateO:
		#	print(i,emissionProbability2[i])
		#	print(counter)
	print("Transition Probabilities")
	for i in transitionProbability2:
		t1 = i[0]
		t2 = i[1]
		if t1 == initialstateS:
			print (i,transitionProbability2[i]) 
		#If we were supposed to make the initial distribution based off of the output instead of the state, I wanted to make sure the code was here
		#if t2 == initialstateO:
		#	print(i,transitionProbability2[i])
		#	print(counter)

if(functionCall == 'e'):
	emissionProbability()
elif(functionCall == 't'):
	transitionProbability()
elif(functionCall == 'p'):
	probabilityDistribution()
