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
        self.set_path()
        # currently accepted path weight sum
        self.current_weight = self.get_total_weight(self.current_path)

        self.next_path = []
        self.next_weight = 0
        self.delta_e = 0.0

        # Final path and weight
        self.solution_path, self.solution_weight = self.begin()

    def set_path(self):
        current_node = 1
        self.current_path = [[self.triangle[current_node], 0, 1]]
        for i in range(1, self.total_levels):
            if random.randint(0, 1) == 0:
                parent = current_node
                rc = self.triangle[self.triangle.findRightChild(current_node)]
                current_node = self.triangle.findLeftChild(current_node)
                self.current_path.append([self.triangle[current_node], current_node, i, rc, parent])
            else:
                parent = current_node
                lc = self.triangle[self.triangle.findLeftChild(current_node)]
                current_node = self.triangle.findRightChild(current_node)
                self.current_path.append([self.triangle[current_node], current_node, i, lc, parent])

    def random_change(self):
        if self.current_path:
            self.next_path = self.current_path
            rand_level = random.randint(1, self.total_levels - 1)
            if rand_level != self.total_levels - 1:
                below_index = self.next_path[rand_level + 1][2]
                begin = self.triangle.levelStartIndex[self.triangle.getLevel(below_index)]
                end = self.triangle.levelStartIndex[self.triangle.getLevel(below_index)] + self.triangle.getLevel(below_index) - 1
                if below_index != begin and below_index != end:
                    old_v = self.next_path[rand_level][0]
                    new_v = self.next_path[rand_level][3]
                    self.next_path[rand_level][0] = new_v
                    self.next_path[rand_level][3] = old_v

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
        while self.temperature >= self.frozen_state:
            i = 1
            while i <= self.iterations:
                # Set next_path
                self.random_change()
                # Set next_weight
                self.next_weight = self.get_total_weight(self.current_path)
                # Set
                self.delta_e = self.next_weight - self.current_weight
                change_prob = self.eval_delta_e()
                if change_prob:
                    self.current_path = self.next_path
                    self.current_weight = self.next_weight
                i += 1
            self.temperature = self.temperature * self.cooling_rate
        return self.current_path, self.current_weight


# def print_pretty(path):
#     out_path = ""
#     for r in path:
#         out_path = out_path + str(r[0]) + " -> "
#     out_path = out_path[:-3]
#     print out_path
#
# def main():
#     levels = 5
#     start_temp = 10
#     frozen = .0001
#     iterations = 100
#     alpha = .97
#     t = Triangle(levels)
#     a = Anneal(t, start_temp, frozen, iterations, alpha)
#     print_pretty(a.solution_path)
#     print a.solution_weight
#
#
# if __name__== "__main__":
#     main()