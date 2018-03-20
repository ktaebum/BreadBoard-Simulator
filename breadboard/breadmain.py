from .chips import *
from .graph import BreadGraph


class BreadBoardMain(object):
    chip_map = {
        # Chip Mapping (chip set num -> operation)
        7400: 'NAND',
        7408: 'AND',
        7486: 'XOR'
    }

    def __init__(self):
        # Basic Coordinate Set For Visualization
        self.X_body = np.arange(0, 30) + 1
        self.X_plug = np.arange(0, 25) - 0.5
        for i in range(1, 5):
            self.X_plug[5 * i::] += 2
        self.Y_body = np.arange(5, 15)
        self.Y_body[5::] += 2
        self.Y_body_map = {chr(65 + i): j for i, j in zip(range(len(self.Y_body)), self.Y_body)}
        self.Y_plug_below = np.arange(0, 2)
        self.Y_plug_above = np.arange(20, 22)

        # chip list
        self.chips = []
        self.num_chips = {
            7400: 0,
            7408: 0,
            7486: 0
        }

        self.graph = BreadGraph()

        self.inputs = []
        self.outputs = None

    def add_chip(self, x, y, chip_type):
        if chip_type == 7400:
            self.chips.append(Chip7400(x, self.Y_body_map[y], self.num_chips[chip_type]))
            self.num_chips[chip_type] += 1
        elif chip_type == 7408:
            self.chips.append(Chip7408(x, self.Y_body_map[y], self.num_chips[chip_type]))
            self.num_chips[chip_type] += 1
        elif chip_type == 7486:
            self.chips.append(Chip7486(x, self.Y_body_map[y], self.num_chips[chip_type]))
            self.num_chips[chip_type] += 1

    def add_input(self, x, y, name, value):
        input_node = self.graph.add_node(x, self.Y_body_map[y], name=name, gate='transmit', value=value)
        self.inputs.append(input_node)

    def connect_line2chip(self, from_node_name, gate_name, chip_number, gate_number):
        if chip_number >= len(self.chips):
            raise ValueError('Chip Number Exceeds Number of Chips')

        if gate_number < 1 or gate_number > 4:
            raise ValueError('Gate Number Should be Within 1 to 4')

        chip = self.chips[chip_number]
        if gate_name not in self.graph.nodes.keys():
            self.graph.add_node(chip.outputs[gate_number][0], chip.outputs[gate_number][1],
                                gate=Chip.chip_map[int(chip.__class__.__name__[-4:])],
                                name=gate_name)

        self.graph.add_edge(from_node_name, gate_name)

    def add_line(self, from_name, to_name, to_x=None, to_y=None):
        if to_name not in self.graph.nodes.keys():
            self.graph.add_node(to_x, self.Y_body_map[to_y], to_name, gate='transmit',
                                value=self.graph.nodes[from_name].value)

        self.graph.add_edge(from_name, to_name)

    def calculate(self, verbose=False):
        self.outputs = self.graph.calculate(verbose)

        return self.outputs
