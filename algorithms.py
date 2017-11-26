import copy
import itertools

def solveDynamic(triangle):
    triangle = copy.deepcopy(triangle)
    # Starts the search at second to last level
    triangle.currentLevel = triangle.totalLevels - 1

    # Continues until it reaches the apex.
    while triangle.currentLevel != 0:  # O(Log(n)) where n is number of vertices

        # Finds the index of the vertex on the current level in the list
        triangle.levelIndex = triangle.levelStartIndex[triangle.currentLevel]

        # Finds the index of the vertex on the below level in the list
        nextLevelIndex = triangle.levelStartIndex[triangle.currentLevel + 1]

        # Compares the next possible vertices in the Child and collapses the greater one onto the current vertex.
        for vertex in range(nextLevelIndex - 1, triangle.levelIndex - 1, -1):  # O(log n) where n is number of vertices

            if triangle.master[triangle.findRightChild(vertex)] > triangle.master[triangle.findLeftChild(vertex)]:
                triangle.master[vertex] += triangle.master[triangle.findRightChild(vertex)]
            else:
                triangle.master[vertex] += triangle.master[triangle.findLeftChild(vertex)]

        triangle.currentLevel -= 1
    return triangle.master[1]


def solveExhaust(triangle):
    'solves a triangle using exhaustive search'
    t = triangle
    # sols = 2**(t.totalLevels-1)
    max_sum = t.master[1]
    for bin_path in itertools.product("01", repeat=t.totalLevels - 1):
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
    for i in range(triangle.totalLevels - 1):
        # O(n) where n is levels
        if triangle.master[triangle.findLeftChild(node)] > triangle.master[triangle.findRightChild(node)]:
            node = triangle.findLeftChild(node)
            greedy_sum += triangle.master[node]
        else:
            node = triangle.findRightChild(node)
            greedy_sum += triangle.master[node]
    return greedy_sum