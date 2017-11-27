__author__ = 'Andrew Mason'
from Triangle import *


class Anneal:
    def __init__(self, triangle, temperature, frozen_state, iterations, cooling_rate):
        self.triangle = triangle
        self.temperature = temperature
        self.frozen_state = frozen_state
        self.iterations = iterations
        self.cooling_rate = cooling_rate
        self.total_levels = triangle.totalLevels

        # currently accepted path
        self.current_path = []
        # set initial path

        # currently accepted path weight sum
        self.current_weight = 0

        self.next_path = []
        self.next_weight = 0
        self.delta_e = 0.0

        # Final path and weight
        self.solution_path, self.solution_weight = self.begin()

    def set_path(self):
        current_node = 1
        self.current_path = [[self.triangle[current_node], 0]]
        for i in range(1, self.total_levels):
            if random.randint(0, 1) == 0:
                parent = current_node
                rc = self.triangle[self.triangle.findRightChild(current_node)]
                current_node = self.triangle.findLeftChild(current_node)
                self.current_path.append([self.triangle[current_node], rc, "Left"])
            else:
                parent = current_node
                lc = self.triangle[self.triangle.findLeftChild(current_node)]
                current_node = self.triangle.findRightChild(current_node)
                self.current_path.append([self.triangle[current_node], lc, "Right"])
        return self.current_path

    def random_change(self):
        if self.current_path:
            self.next_path = self.current_path
            rand_level = random.randint(2, self.total_levels - 1)
            if rand_level != self.total_levels - 1:
                below_change = self.next_path[rand_level - 1][2]
                if below_change != self.next_path[rand_level][2]:
                    old_v = self.next_path[rand_level][0]
                    new_v = self.next_path[rand_level][1]
                    self.next_path[rand_level][0] = new_v
                    self.next_path[rand_level][1] = old_v
                    if self.next_path[rand_level][2] == "Left":
                        self.next_path[rand_level][2] = "Right"
                    else:
                        self.next_path[rand_level][2] = "Left"
        return self.next_path

    def get_total_weight(self, path):
        weight = 0
        for v in path:
            weight = weight + v[0]
        return weight

    def eval_delta_e(self):
        if self.delta_e >= 0:
            return True
        else:
            if self.metropolis() > random.random():
                return True
            else:
                return False

    def metropolis(self):
        try:
            m = 1 / (1 + math.exp((1.0 / self.temperature) * (-self.delta_e)))
        except OverflowError:
            m = float('inf')
        return m

    def begin(self):
        self.current_path = self.set_path()
        self.current_weight = self.get_total_weight(self.current_path)
        while self.temperature >= self.frozen_state:

            i = 1
            while i <= self.iterations:
                # Set next_path
                self.next_path = self.random_change()
                # Set next_weight
                self.next_weight = self.get_total_weight(self.next_path)
                # Set
                self.delta_e = self.next_weight - self.current_weight
                change_prob = self.eval_delta_e()
                if change_prob:
                    self.current_path = self.next_path
                    self.current_weight = self.next_weight
                i += 1
            self.temperature *= self.cooling_rate
        return self.current_path, self.current_weight
