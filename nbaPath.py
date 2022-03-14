import sys
import argparse

""" 
This program calculate number of all posible game paths for given 
basketball game score.
"""

parser = argparse.ArgumentParser(description='All posible game size for basketball game')
parser.add_argument("-l", "--list", action="store_true", default=False, help="list all game posible way")
parser.add_argument(dest='score', type=int, nargs='+',help='give positional scoreA and scoreB')

args = parser.parse_args()


scoresArray = [1,2,4]
sc = scoresArray
#for i in range(3,120): 
#	n = sc[i-1] + sc[i-2] + sc[i-3]
#	sc.append(n)
#	print(i, n)

scoreLenHistogram = [{1:1}, {2:1}, {2:1,3:1}, {4:1,3:2,2:1} ]
"""
	unit Score histogram list.
	for score 0:
		there is 1 possible play
		0  -- lenght 1
	for score 1:
		there is 1 possible play
		0 1  -- length 2
	for score 2: 
		there is 2 possible play
		0 1 2  -- length 3
		0 2    -- length 2
	for score 3: 
		there is 4 possible play
		0 1 2 3 -- legth 4
		0 1 3  -- length 3
		0 2 3  -- length 3
		0 3    -- length 2
"""

def addLenHistogram (score, scoreLenHistogram):
	"""
		add new score to scoreLenHistogram List:
			new score =  (score-1)' +  (score-2)' + (score-3)'
	"""
	newD = {}
	for i in range(1, 4):
		for k, v in scoreLenHistogram[score - i].items():
			#print(index-i, newD)
			if k+1 in newD: newD[k+1] += v
			else: newD[k+1] = v
	scoreLenHistogram.append(newD)

def fillLenHistogram(maxScore, scoreLenHistogram):
	for i in range(4,maxScore+1):
		addLenHistogram(i,scoreLenHistogram)

def fillComb(maxScore):
	size = maxScore+2 
	ABcomb = [[0 for x in range(size)] for x in range(size)]
	"""
	ABcomb is an 2d list. 
	Gives value for scoreA and scoreB combination lenght
	"""
	"""
		initial Values for AB matrix is 1 
		for all values in column 1 and row 1
	"""
	for i in range(1,size):
		ABcomb[i][1] = 1
		ABcomb[1][i] = 1
	"""
		all other (i,j) values depends on sum of two neighbour diagonal
		value:
			(i,j) = (i-1,j)+ (i, j-1) 
	"""
	for i in range(2,size):
		for j in range(2,size):
			ABcomb[i][j]=ABcomb[i-1][j] + ABcomb[i][j-1]
	return ABcomb
#[print(line) for line in ABcomb]


def gamePathSize (scoreA, scoreB):
	"""
		get all posible length of scoreA and scoreB
	"""
	size = 0
	histA = scoreLenHistogram[scoreA]
	histB = scoreLenHistogram[scoreB]
	for lA, sA in histA.items():
		for lB, sB in histB.items():
			size += ABcomb[lA][lB] * sA * sB
			#print(ABcomb[lA][lB], lA, lB, sA, sB)
	#print(size)
	return size

"""
########################################
Graph Solution for all posible game plays
########################################
"""
def addNode( val, nodes):
	out = [val , []]
	nodes.append(out)
	for i in range (1,4):
		if val - i < 0: continue
		out[1].append(nodes[val-i])

def createAll (finalScore , nodes):
	for i in range(finalScore):
		addNode(i, nodes)

def findPath (start, stop, lengthw, path, out):
	if start[0] == stop:
		out.append(path+"0")
		#print (lengthw, path+"0")
	for new in start[1]:
		findPath(new, stop, lengthw+1, path+str(start[0])+"-", out)

def score(x, out, branch="") :
	#print ("NW ", x, branch)
	if x == 0 : 
		out.append(branch + 1)
		#out.append(branch + " " + "0")
		return None
	for i in range(1,4):
		#print ("II i:%d x:%d b:%s" % (i, x, branch))
		if x-i<0: continue
		#score (x-i, out, branch+str(" ")+str(x))
		score (x-i, out, branch+1)

def gameAllScores(scoreA, scoreB):
	scoreNodes = [] 
	createAll(max(scoreA, scoreB)+1, scoreNodes)
	pathA = []
	findPath (scoreNodes[scoreA], 0, 0, "", pathA)
	pathB = []
	findPath (scoreNodes[scoreB], 0, 0, "", pathB)
	for pA in pathA:
		for pB in pathB:
			crossMatch( pA.split("-"), pB.split("-") )

def crossMatch (A,B, out=""):
	if len(A)==1 and len(B)== 1:
		print (" ".join(out.split(" ")[::-1]))
		return None
	if len(A)>1:
		crossMatch (A[1:], B, out+" %s-%s"%(A[0],B[0]))
		#dene (A[1:], B, out+1)
	if len(B)>1:
		crossMatch (A, B[1:], out+" %s-%s"%(A[0],B[0]))
		#dene (A, B[1:], out+1)

"""
### calculate all posible 119 x 119 game value
Allpos = [[0 for x in range(120)] for x in range(120)]
for i in range(120):
	for j in range(120):
		_s = gamePathSize(i, j)
		print("{:e}".format(_s),end=",")
	print()
"""

if __name__ == "__main__":
	scoreA = args.score[0]
	scoreB = args.score[1]
	maxScore = max(scoreA, scoreB)
	fillLenHistogram(maxScore, scoreLenHistogram)
	ABcomb=fillComb(maxScore)
	_s = gamePathSize(scoreA, scoreB)
	print("Number of uniq game plays for score {}-{} is: {:e}".format(scoreA, scoreB, _s))
	if (args.list):
		gameAllScores(scoreA, scoreB)


