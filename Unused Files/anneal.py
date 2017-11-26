
__author__ = 'Andrew Mason'
import random
import math
import time
import itertools
class Triangle:
    'creates random triangle with provided # of levels' 
    def __init__(self,levels):
        self.totalLevels = levels
        self.master = [0]
        self.currentLevel = 1
        self.levelIndex = 1
        self.levelStartIndex = [0]
        self.createStartIndex()
        self.populate()
    ## Returns the index of the child
    def findLeftChild(self,currentNode):
        return currentNode + self.getLevel(currentNode)
    ## Returns the index of the child
    def findRightChild(self,currentNode):
        return currentNode + self.getLevel(currentNode)+1
    # Creates array of index level references. (Index = level)
    def createStartIndex(self):
        levelIndex = 1
        for i in range(1, self.totalLevels+1):
            self.levelStartIndex.append(levelIndex)
            levelIndex += i
    def getLevel_obsolete(self,currentNode):
    # Give me an index, and I'll tell you which level y'at
    # at worst, this can be an O(N) operation where N=levels
        for i in range(len(self.levelStartIndex)):
            try:
                self.levelStartIndex[i+1]
            except IndexError:
                return i
            if self.levelStartIndex[i] <= currentNode and self.levelStartIndex[i+1] > currentNode:
                return i
    def getLevel(self,currentNode):
        #Give me an index and I'll return the level it's on
        #O(1) operation my dude
		# level = (int) (-1 + sqrt(1 + 8*node_index)) / 2 
        i=currentNode-1
        return int((-1+math.sqrt(1+8*i))/2)+1
    def populate(self):
        masterList = [0]
        levels = self.totalLevels
        numNodes = (levels*(levels+1))/2
        for num in range (0,int(numNodes)):
            self.master.append(random.randint(0,100))
    def __repr__(self):
        for x in range(1,len(self.master)):
            if x in self.levelStartIndex:
                print "\n"
            print self.master[x],
        return ''
    def __getitem__(self, i):
        return self.master[i]

def setPath(t, levels):
    currentNode = 1
    arr = [[t[currentNode],0,1]]
    for i in range(1, levels):
        x = random.randint(0,1)
        # move to left child
        if x == 0:
            parent = currentNode
            rc = t[t.findRightChild(currentNode)]
            currentNode = t.findLeftChild(currentNode)
            arr.append([t[currentNode], currentNode, i, rc, parent])
        #move to right child 
        else:
            parent = currentNode
            lc = t[t.findLeftChild(currentNode)]
            currentNode = t.findRightChild(currentNode)
            arr.append([t[currentNode], currentNode, i, lc, parent])
    return arr

def randomChange(path, levels, t):
    randLevel = random.randint(1, levels-1)
    if path[randLevel-1][2] == path[randLevel][4]:
        oldV = path[randLevel][0]
        newV = path[randLevel][3]
        path[randLevel][0] = newV
        path[randLevel][3] = oldV
    return path

def getEnergy(path):
    energy = 0
    for v in path:
        energy = energy + v[0]
    return energy

def metropolis(evalDeltaE, temperature):
    try:
        m = 1 / (1 + math.exp((1.0/temperature) * (-(evalDeltaE))))
    except OverflowError:
        m = float('inf')
    return m
    
def deltaE(currentEnergy, nextEnergy, temperature):
    evalDeltaE = nextEnergy - currentEnergy
    if evalDeltaE >= 0:
        return True
    else:
        if metropolis(evalDeltaE, temperature) > random.random():
            return True
        else:
            return False
def printPretty(path):
    outPath = ""
    for r in path:
        outPath = outPath + str(r[0]) + " + "
    outPath = outPath[:-3]
    return outPath


def anneal(t, levels):
    start = time.clock()
    temperature = 100
    startTemp = temperature
    tMin = 0.0001
    iterations = 1000
    alpha = 0.99
    
    currentPath = setPath(t, levels)
    print printPretty(currentPath)
    currentEnergy = getEnergy(currentPath)
    solutionPath = currentPath
    solutionEnergy = currentEnergy
    while (temperature >= tMin):
        i = 1
        while (i <= iterations):
            nextPath = randomChange(currentPath,levels, t)
            nextEnergy = getEnergy(nextPath)
            changeProb = deltaE(currentEnergy, nextEnergy, temperature)
            if changeProb==True:
                currentPath = nextPath 
                currentEnergy = nextEnergy
            i += 1
        solutionPath = currentPath
        temperature = temperature*alpha
        
    stop = time.clock()
    print "Solution Path: " + printPretty(solutionPath)
    print "Solution Energy: " + str(getEnergy(solutionPath))
    print "Starting Temperature: " + str(startTemp)
    print "Time elapsed for a " + str(levels) + " level path: " + str(stop - start) + " seconds"

def solveDynamic(triangle):
    triangle = copy.deepcopy(triangle)
    # Starts the search at second to last level
    triangle.currentLevel = triangle.totalLevels - 1
    
    #Continues until it reaches the apex.
    while triangle.currentLevel != 0:  # O(Log(n)) where n is number of vertices
        
        # Finds the index of the vertex on the current level in the list
        triangle.levelIndex = triangle.levelStartIndex[triangle.currentLevel]
        
        # Finds the index of the vertex on the below level in the list
        nextLevelIndex = triangle.levelStartIndex[triangle.currentLevel+1]
        
        # Compares the next possible vertices in the Child and collapses the greater one onto the current vertex. 
        for vertex in range(nextLevelIndex-1,triangle.levelIndex-1,-1): # O(log n) where n is number of vertices

            if triangle.master[triangle.findRightChild(vertex)] > triangle.master[triangle.findLeftChild(vertex)]:
                triangle.master[vertex] += triangle.master[triangle.findRightChild(vertex)]
            else:
                triangle.master[vertex] += triangle.master[triangle.findLeftChild(vertex)]
        
        triangle.currentLevel -= 1
    return triangle.master[1]

def solveExhaust(triangle):
    'solves a triangle using exhaustive search'
    t = triangle
    #sols = 2**(t.totalLevels-1)
    max_sum = t.master[1]
    for bin_path in itertools.product("01",repeat=t.totalLevels-1):
        node_index = 1
        temp_sum = t.master[1]
        for move_bit in bin_path:
            if move_bit == '0':
                temp_sum += t.master[t.findLeftChild(node_index)]
                node_index = t.findLeftChild(node_index)
            else:
                temp_sum += t.master[t.findRightChild(node_index)]
                node_index = t.findRightChild(node_index)
        if temp_sum > max_sum:
            max_sum = temp_sum
    return max_sum
        
def solveGreedy(triangle):
    greedy_sum = triangle.master[1]
    node = 1
    for i in range(triangle.totalLevels-1):
    #O(n) where n is levels
        if triangle.master[triangle.findLeftChild(node)] > triangle.master[triangle.findRightChild(node)]:
            node = triangle.findLeftChild(node)
            greedy_sum += triangle.master[node]
        else:
            node = triangle.findRightChild(node)
            greedy_sum += triangle.master[node]
    return greedy_sum
def main():
    randLevels = 5
    # randLevels = random.randint(2,15)
    t = Triangle(randLevels)
    print(repr(t))
    print "\nSimulated Annealing"
    print "###############################"
    anneal(t, randLevels)  
    x = solveExhaust(t)
    print "Exhaust Answer"
    print x 
    y = solveGreedy(t)
    print "Greedy"
    print y
if __name__== "__main__":
    main()
