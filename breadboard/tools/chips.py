import numpy as np


class Chip(object):
    chip_map = {
        # Chip Mapping (chip set num -> operation)
        7400: 'NAND',
        7408: 'AND',
        7486: 'XOR'
    }

    total_chips = 0

    def __init__(self, x, y, chip_type):
        self.x = np.arange(x, x + 7)  # x coord range
        self.y = np.arange(y, y + 4)  # y coord range

        self.connected = {i: [False, False] for i in range(1, 5)}

        self.input1s = {
            1: (self.x[1], self.y[-1]),
            2: (self.x[4], self.y[-1]),
            3: (self.x[0], self.y[0]),
            4: (self.x[3], self.y[0])
        }

        self.input2s = {
            1: (self.x[2], self.y[-1]),
            2: (self.x[5], self.y[-1]),
            3: (self.x[1], self.y[0]),
            4: (self.x[4], self.y[0]),
        }

        self.outputs = {
            1: (self.x[3], self.y[-1]),
            2: (self.x[6], self.y[-1]),
            3: (self.x[2], self.y[0]),
            4: (self.x[5], self.y[0]),
        }

        self.name = 'Chip%d' % chip_type


class Chip7400(Chip):
    def __init__(self, x, y, chip_type):
        super(Chip7400, self).__init__(x, y, chip_type)
        self.name = '%d:7400 (NAND)_%d' % (self.total_chips, chip_type)
        Chip.total_chips += 1


class Chip7486(Chip):
    def __init__(self, x, y, chip_type):
        super(Chip7486, self).__init__(x, y, chip_type)
        self.name = '%d:7486 (XOR)_%d' % (self.total_chips, chip_type)
        Chip.total_chips += 1


class Chip7408(Chip):
    def __init__(self, x, y, chip_type):
        super(Chip7408, self).__init__(x, y, chip_type)
        self.name = '%d:7408 (AND)_%d' % (self.total_chips, chip_type)
        Chip.total_chips += 1
