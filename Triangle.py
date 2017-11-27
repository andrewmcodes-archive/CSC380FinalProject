import random
import math
import time


class Triangle:
    'creates random triangle with provided # of levels'

    def __init__(self, levels):
        self.totalLevels = levels
        self.master = [0]
        self.currentLevel = 1
        self.levelIndex = 1
        self.levelStartIndex = [0]
        self.createStartIndex()
        self.populate()

    ## Returns the index of the child
    def findLeftChild(self, currentNode):
        return currentNode + self.getLevel(currentNode)

    ## Returns the index of the child
    def findRightChild(self, currentNode):
        return currentNode + self.getLevel(currentNode) + 1

    # Creates array of index level references. (Index = level)
    def createStartIndex(self):
        levelIndex = 1
        for i in range(1, self.totalLevels + 1):
            self.levelStartIndex.append(levelIndex)
            levelIndex += i

    def getLevel_obsolete(self, currentNode):
        # Give me an index, and I'll tell you which level y'at
        # at worst, this can be an O(N) operation where N=levels
        for i in range(len(self.levelStartIndex)):
            try:
                self.levelStartIndex[i + 1]
            except IndexError:
                return i
            if self.levelStartIndex[i] <= currentNode and self.levelStartIndex[i + 1] > currentNode:
                return i

    def getLevel(self, currentNode):
        # Give me an index and I'll return the level it's on
        # O(1) operation my dude
        # level = (int) (-1 + sqrt(1 + 8*node_index)) / 2
        i = currentNode - 1
        return int((-1 + math.sqrt(1 + 8 * i)) / 2) + 1

    def populate(self):
        masterList = [0]
        levels = self.totalLevels
        numNodes = (levels * (levels + 1)) / 2
        for num in range(0, int(numNodes)):
            self.master.append(random.randint(0, 100))

    def __repr__(self):
        for x in range(1, len(self.master)):
            if x in self.levelStartIndex:
                print "\n"
            print self.master[x],
        return ''

    def __getitem__(self, i):
        return self.master[i]
