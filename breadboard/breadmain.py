from .chips import *
from .graph import BreadGraph
from .exceptions import *


class BreadBoard(object):
    def __init__(self, x_body=1):
        # Basic Coordinate Set For Visualization
        # x_body = breadboard length
        self.X_body = np.arange(0, 30 * x_body) + 1
        self.X_plug = np.arange(0, 25 * x_body) - 0.5
        for i in range(1, len(self.X_plug) // 5):
            self.X_plug[5 * i::] += (2 - 0.5 * (x_body - 1))

        self.Y_body = np.arange(5, 15)
        self.Y_body[5::] += 2
        self.Y_body_map = {chr(65 + i): j for i, j in zip(range(len(self.Y_body)), self.Y_body)}
        self.Y_body_map_inverse = dict(reversed(item) for item in self.Y_body_map.items())

        self.Y_plug_below = np.arange(0, 2)
        self.Y_plug_above = np.arange(20, 22)

        self.connected = set()

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
            chip = Chip7400(x, self.Y_body_map[y], self.num_chips[chip_type])
            self.num_chips[chip_type] += 1
        elif chip_type == 7408:
            chip = Chip7408(x, self.Y_body_map[y], self.num_chips[chip_type])
            self.num_chips[chip_type] += 1
        elif chip_type == 7486:
            chip = Chip7486(x, self.Y_body_map[y], self.num_chips[chip_type])
            self.num_chips[chip_type] += 1
        else:
            raise NonSupportingChipException(chip_type)
        self.chips.append(chip)
        for x_ in chip.x:
            node = str(x_) + str(self.Y_body_map_inverse[chip.y[0]])
            self.plugin(node)

            node = str(x_) + str(self.Y_body_map_inverse[chip.y[-1]])
            self.plugin(node)

    def add_input(self, x, y, name, value):
        """
        :param x: X_coord
        :param y: y_coord in alphabet
        :param name: Input Node name
        :param value: Input Value
        :return:
        """
        # add input cable
        if type(value) is not bool:
            raise NonBooleanInputException()

        self.plugin(str(x) + str(y))

        input_node = self.graph.add_node(x, self.Y_body_map[y], name=name, gate='transmit', value=value)
        self.inputs.append(input_node)

    def add_output(self, from_name, output_name, x, y):
        """
        from certain node, extract output node (maybe bulb, in real world)
        :param from_name: from_node name
        :param output_name: output_node name, (Sum, Carry etc)
        :param x: output_node x coord
        :param y: output_node y coord (in alphabet)
        :return:
        """
        # add output cable
        if from_name not in self.graph.nodes.keys():
            raise NonExistingNodeException()

        self.plugin(str(x) + str(y))

        self.graph.add_node(x, self.Y_body_map[y], name=output_name, gate='transmit',
                            value=None)

        self.graph.add_edge(from_name, output_name)

    def add_line(self, from_name, to_name):
        self.graph.add_node(int(to_name[:-1]), self.Y_body_map[to_name[-1:]], to_name, gate='transmit')
        self.plugin(to_name)

        self.graph.add_edge(from_name, to_name)

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

    def calculate(self, verbose=False):
        self.outputs = self.graph.calculate(verbose)

        return self.outputs

    def plugin(self, coord_name):
        if coord_name in self.connected:
            raise DuplicatedConnectException(coord_name)

        self.connected.add(coord_name)
