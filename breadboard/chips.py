import numpy as np


class Chip(object):
    chip_map = {
        # Chip Mapping (chip set num -> operation)
        7400: 'NAND',
        7408: 'AND',
        7486: 'XOR'
    }

    total_chips = 0

    def __init__(self, x, y, chip_num):
        self.x = np.arange(x, x + 7)  # x coord range
        self.y = np.arange(y, y + 4)  # y coord range

        self.input1s = {
            3: (self.x[0], self.y[0]),
            4: (self.x[3], self.y[0]),
            1: (self.x[1], self.y[-1]),
            2: (self.x[4], self.y[-1])
        }

        self.input2s = {
            3: (self.x[1], self.y[0]),
            4: (self.x[4], self.y[0]),
            1: (self.x[2], self.y[-1]),
            2: (self.x[5], self.y[-1])
        }

        self.outputs = {
            3: (self.x[2], self.y[0]),
            4: (self.x[5], self.y[0]),
            1: (self.x[3], self.y[-1]),
            2: (self.x[6], self.y[-1])
        }

        self.name = 'Chip%d' % chip_num


class Chip7400(Chip):
    def __init__(self, x, y, chip_num):
        super(Chip7400, self).__init__(x, y, chip_num)
        self.name = '%d:7400 (NAND)_%d' % (self.total_chips, chip_num)
        Chip.total_chips += 1


class Chip7486(Chip):
    def __init__(self, x, y, chip_num):
        super(Chip7486, self).__init__(x, y, chip_num)
        self.name = '%d:7486 (XOR)_%d' % (self.total_chips, chip_num)
        Chip.total_chips += 1


class Chip7408(Chip):
    def __init__(self, x, y, chip_num):
        super(Chip7408, self).__init__(x, y, chip_num)
        self.name = '%d:7408 (AND)_%d' % (self.total_chips, chip_num)
        Chip.total_chips += 1
