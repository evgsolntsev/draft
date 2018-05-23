import numpy as np


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

        return np.random.choice(
            self.keys(), p=[v / self.weight_sum for v in self.values()])


class Model(dict):
    def __init__(self, order):
        super(Model, self).__init__()
        self.order = order

    def process(self, data):
        """Process new data.

        :param list data:
        """

        for i in range(len(data) - self.order - 1):
            window = data[i:i + self.order]
            if window not in self:
                self[window] = Vertex()
            self[window].update(data[i + 1:i + self.order + 1])
