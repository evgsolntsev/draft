import random

import numpy as np


START_CHARACTER = "^"
END_CHARACTER = "$"


class Vertex(dict):

    weight_sum = 0.0
    """Sum of all edges' weight."""

    def __init__(self, iterable=None):
        super(Vertex, self).__init__()
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        """Updates Vertex with new data.

        :param word: add another edge or updates existing
        """

        self.weight_sum += 1
        if iterable in self:
            self[iterable] += 1
        else:
            self[iterable] = 1

    def get_edge(self):
        """Returns next word using weighted random."""

        choices = list(self.keys())
        weights = [v / self.weight_sum for v in self.values()]
        return choices[np.random.choice(list(range(len(choices))), p=weights)]


class Model(dict):
    def __init__(self, order):
        super(Model, self).__init__()
        self.order = order

    def process(self, data):
        """Process new data.

        :param list data:
        """

        data = [START_CHARACTER] + data.copy() + [END_CHARACTER]
        for i in range(len(data) - self.order):
            window = tuple(data[i:i + self.order])
            if window not in self:
                self[window] = Vertex()
            self[window].update(tuple(data[i + 1:i + self.order + 1]))

    def generate_sentence(self):
        k = random.choice([
            key for key in self.keys() if key[0] == START_CHARACTER])

        result = []
        while k[-1] != END_CHARACTER:
            result.append(k[0])
            k = self[k].get_edge()
        return " ".join((result + list(k))[1:-1])
