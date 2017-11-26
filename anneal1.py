__author__ = 'Andrew Mason'
import random
import math
import time
from Triangle import *

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

def randomChange(path, levels,t):
    randLevel = random.randint(1, levels-1)
    if randLevel != levels-1:
        currentIndex = path[randLevel][2]
        belowIndex = path[randLevel + 1][2]
        begin = t.levelStartIndex[t.getLevel(belowIndex)]
        end = t.levelStartIndex[t.getLevel(belowIndex)]+t.getLevel(belowIndex)-1
        if belowIndex != begin and belowIndex != end:
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
        outPath = outPath + str(r[0]) + " -> "
    outPath = outPath[:-3]
    return outPath


def anneal(t, levels):
    start = time.clock()
    temperature = 100
    startTemp = temperature
    tMin = 0.0001
    iterations = 100
    alpha = 0.97
    
    currentPath = setPath(t, levels)
    currentEnergy = getEnergy(currentPath)
    solutionPath = currentPath
    solutionEnergy = currentEnergy
    while (temperature >= tMin):
        i = 1
        while (i <= iterations):
            nextPath = randomChange(currentPath,levels,t)
            nextEnergy = getEnergy(nextPath)
            changeProb = deltaE(currentEnergy, nextEnergy, temperature)
            if changeProb==True:
                currentPath = nextPath 
                currentEnergy = nextEnergy
            i += 1
        temperature = temperature*alpha
        solutionPath = currentPath
        solutionEnergy = currentEnergy
    stop = time.clock()
    #print "Solution Path: " + printPretty(solutionPath)
    print "Solution Energy: " + str(solutionEnergy)
    print "Starting Temperature: " + str(startTemp)
    print "Time elapsed for a " + str(levels) + " level path: " + str(stop - start) + " seconds"

def main():
    randLevels = input("Enter number of levels: ")
    # randLevels = random.randint(2,15)
    t = Triangle(int(randLevels))
   # print(repr(t))
    print "\nSimulated Annealing"
    print "###############################"
    anneal(t, randLevels)  

if __name__== "__main__":
    main()