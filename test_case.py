'''
Created on Oct 12, 2017

@author: sampann
'''
import random
import time
from Triangle import *
from anneal_class import *
import algorithms

def print_pretty(path):
    out_path = ""
    for r in path:
        out_path = out_path + str(r[0]) + " -> "
    out_path = out_path[:-3]
    return out_path


def simulated_anneal(t):
    start_temp = 10
    frozen = .01
    iterations = 10
    alpha = .98
    a = Anneal(t, start_temp, frozen, iterations, alpha)
    # print_pretty(a.solution_path)
    return a.solution_weight, a.solution_path


def main():
    # This generates the triangle.
    print "Levels \t Dynamic Time \t Dynamic Weight \t Greedy Time \t Greedy Weight \t Simulated Annealing Time \t Simulated Annealing Weight"

    for levels in range(50, 5000, 50):
        t = Triangle(levels)

        start = time.clock()
        dynamic = algorithms.solveDynamic(t)
        end = time.clock()
        dynamicTime = end - start

        start = time.clock()
        greedy = algorithms.solveGreedy(t)
        end = time.clock()
        greedyTime = end - start

        start = time.clock()
        simWeight, simPath = simulated_anneal(t)
        end = time.clock()
        simTime = end - start
        # simPath = print_pretty(simPath)

        print("%s \t %s \t\t %s \t\t\t %s \t\t\t\t %s \t\t\t\t %s \t\t\t %s") % (levels, dynamicTime, dynamic, greedyTime, greedy, simTime, simWeight)


if __name__ == "__main__":
    main()


