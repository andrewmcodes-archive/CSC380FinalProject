__author__ = 'Andrew Mason'
import random
import math
import time
from Triangle import *


def set_path(t, levels):
    current_node = 1
    arr = [[t[current_node],0,1]]
    for i in range(1, levels):
        x = random.randint(0,1)
        if x == 0:
            parent = current_node
            rc = t[t.findRightChild(current_node)]
            current_node = t.findLeftChild(current_node)
            arr.append([t[current_node], current_node, i, rc, parent])
        else:
            parent = current_node
            lc = t[t.findLeftChild(current_node)]
            current_node = t.findRightChild(current_node)
            arr.append([t[current_node], current_node, i, lc, parent])
    return arr


def random_change(path, levels, t):
    rand_level = random.randint(1, levels-1)
    if rand_level != levels-1:
        # current_index = path[rand_level][2]
        below_index = path[rand_level + 1][2]
        begin = t.levelStartIndex[t.getLevel(below_index)]
        end = t.levelStartIndex[t.getLevel(below_index)]+t.getLevel(below_index)-1
        if below_index != begin and below_index != end:
            old_v = path[rand_level][0]
            new_v = path[rand_level][3]
            path[rand_level][0] = new_v
            path[rand_level][3] = old_v
    return path


def get_total_weight(path):
    weight = 0
    for v in path:
        weight = weight + v[0]
    return weight


def metropolis(eval_delta_e, temperature):
    try:
        m = 1 / (1 + math.exp((1.0/temperature) * (-eval_delta_e)))
    except OverflowError:
        m = float('inf')
    return m

    
def delta_e(current_energy, next_energy, temperature):
    eval_delta_e = next_energy - current_energy
    if eval_delta_e >= 0:
        return True
    else:
        if metropolis(eval_delta_e, temperature) > random.random():
            return True
        else:
            return False


def print_pretty(path):
    out_path = ""
    for r in path:
        out_path = out_path + str(r[0]) + " -> "
    out_path = out_path[:-3]
    return out_path


def anneal(t, levels):
    start = time.clock()
    temperature = 100
    start_temp = temperature
    frozen_state = 0.0001
    iterations = 100
    cooling_rate = 0.97
    
    current_path = set_path(t, levels)
    current_weight = get_total_weight(current_path)
    solution_path = current_path
    solution_weight = current_weight
    while temperature >= frozen_state:
        i = 1
        while i <= iterations:
            next_path = random_change(current_path, levels, t)
            next_energy = get_total_weight(next_path)
            change_prob = delta_e(current_weight, next_energy, temperature)
            if change_prob:
                current_path = next_path
                current_weight = next_energy
            i += 1
        temperature = temperature*cooling_rate
        solution_path = current_path
        solution_weight = current_weight
    stop = time.clock()
    print "Solution Path: " + print_pretty(solution_path)
    print "Solution Energy: " + str(solution_weight)
    print "Starting Temperature: " + str(start_temp)
    print "Time elapsed for a " + str(levels) + " level path: " + str(stop - start) + " seconds"


def main():
    rand_levels = input("Enter number of levels: ")
    # rand_levels = random.randint(2,15)
    t = Triangle(int(rand_levels))
    # print(repr(t))
    print "\nSimulated Annealing"
    print "###############################"
    anneal(t, rand_levels)


if __name__== "__main__":
    main()