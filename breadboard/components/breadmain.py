from breadboard.tools.chips import *
from .graph import BreadGraph
from breadboard.exceptions import *


class BreadBoard(object):
    def __init__(self):
        # Basic Coordinate Set For Visualization
        # x_body = breadboard length
        body_length = 45

        self.X_body = np.arange(0, body_length) + 1
        self.X_plug = np.arange(0, body_length - 5) - 0.5
        for i in range(1, len(self.X_plug) // 5):
            self.X_plug[5 * i::] += 1.1

        self.Y_body = np.arange(5, 15)
        self.Y_body[5::] += 2
        self.Y_body_map = {chr(65 + i): j for i, j in zip(range(len(self.Y_body)), self.Y_body)}
        self.Y_body_map_inverse = dict(reversed(item) for item in self.Y_body_map.items())

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

    def add_chip(self, position, chip_type):
        x = int(position[:-1])
        y = position[-1:]

        if chip_type == 7400:
            chip = Chip7400(x, self.Y_body_map[y], self.num_chips[chip_type])
        elif chip_type == 7408:
            chip = Chip7408(x, self.Y_body_map[y], self.num_chips[chip_type])
        elif chip_type == 7486:
            chip = Chip7486(x, self.Y_body_map[y], self.num_chips[chip_type])
        else:
            raise NonSupportingChipException(chip_type)

        for x_ in chip.x:
            node_name = str(x_) + self.Y_body_map_inverse[chip.y[0]]
            if node_name in self.graph.nodes.keys():
                print('Cannot insert chip!, Something is already in %s' % node_name)
                return
            node_name = str(x_) + self.Y_body_map_inverse[chip.y[-1]]
            if node_name in self.graph.nodes.keys():
                print('Cannot insert chip!, Something is already in %s' % node_name)
                return

        self.num_chips[chip_type] += 1
        self.chips.append(chip)
        return chip

    def add_input(self, name, target):
        """
        :param name: input name
        :param target: input coordinate
        :return:
        """
        # add input cable
        input_node = self.graph.add_node(int(target[:-1]), self.Y_body_map[target[-1:]], name=name, gate='transmit')
        self.inputs.append(input_node)

    def add_output(self, from_name, output_name, position):
        """
        from certain node, extract output node (maybe bulb, in real world)
        :param from_name: from_node name
        :param output_name: output_node name, (Sum, Carry etc)
        :param position: coordinate position
        :return:
        """
        # add output cable
        if from_name not in self.graph.nodes.keys():
            raise NonExistingNodeException()

        self.graph.add_node(int(position[:-1]), self.Y_body_map[position[-1:]], name=output_name, gate='transmit')

        self.graph.add_edge(from_name, output_name)

    def add_line(self, from_name, to_name):
        if from_name not in self.graph.nodes:
            raise NonExistingNodeException()

        self.graph.add_node(int(to_name[:-1]), self.Y_body_map[to_name[-1:]], to_name, gate='transmit')

        self.graph.add_edge(from_name, to_name)

    def extract_gate_output(self, to_node_name, chip_number, gate_number):
        """
        Extract gate output node to other area
        :param to_node_name: destination position
        :param chip_number: target chip
        :param gate_number: target gate
        :return:
        """
        if chip_number >= len(self.chips):
            raise NonExistingChip(chip_number)

        if gate_number < 1 or gate_number > 4:
            raise ValueError('Gate Number Should be Within 1 to 4')

        chip = self.chips[chip_number]

        if chip.connected[gate_number] != [True, True]:
            raise NonFullGateExtractionException(chip.name, gate_number)

        coord_to_position_name = lambda x, y: str(x) + self.Y_body_map_inverse[y]

        coord_x, coord_y = chip.outputs[gate_number][0], chip.outputs[gate_number][1]
        output_gate_name = coord_to_position_name(coord_x, coord_y)

        self.add_line(output_gate_name, to_node_name)

        return output_gate_name

    def connect_line_to_gate(self, from_node_name, chip_number, gate_number):

        if chip_number >= len(self.chips):
            raise NonExistingChip(chip_number)

        if gate_number < 1 or gate_number > 4:
            raise ValueError('Gate Number Should be Within 1 to 4')

        chip = self.chips[chip_number]

        if from_node_name not in self.graph.nodes:
            raise NonExistingNodeException()

        if chip.connected[gate_number] == [True, True]:
            raise FullGateException(chip.name, gate_number)

        coord_to_position_name = lambda x, y: str(x) + self.Y_body_map_inverse[y]

        if chip.connected[gate_number][0]:
            coord_x, coord_y = chip.input2s[gate_number][0], chip.input2s[gate_number][1]
            chip.connected[gate_number][1] = True
            gate_name = coord_to_position_name(coord_x, coord_y)
            self.graph.add_node(coord_x, coord_y, gate_name,
                                gate='transmit')
            self.graph.add_edge(from_node_name, gate_name)
            # Since gate is full, connect each gate input to gate output
            gate_input2 = gate_name
            coord_x, coord_y = chip.input1s[gate_number][0], chip.input1s[gate_number][1]
            gate_input1 = coord_to_position_name(coord_x, coord_y)
            coord_x, coord_y = chip.outputs[gate_number][0], chip.outputs[gate_number][1]
            output_gate_name = coord_to_position_name(coord_x, coord_y)
            self.graph.add_node(coord_x, coord_y, output_gate_name,
                                gate=Chip.chip_map[int(chip.__class__.__name__[-4:])])
            self.graph.add_edge(gate_input2, output_gate_name)
            self.graph.add_edge(gate_input1, output_gate_name)
        else:
            coord_x, coord_y = chip.input1s[gate_number][0], chip.input1s[gate_number][1]
            chip.connected[gate_number][0] = True
            gate_name = str(coord_x) + self.Y_body_map_inverse[coord_y]
            self.graph.add_node(coord_x, coord_y, gate_name,
                                gate='transmit')
            self.graph.add_edge(from_node_name, gate_name)

        return gate_name

    def delete_line(self, from_node_name, to_node_name):
        pass

    def calculate(self, input_values, verbose=False):
        assert len(input_values) == len(self.inputs), 'Must input boolean item for all variables!'
        for i in range(len(self.inputs)):
            self.inputs[i].value = input_values[i]
            if verbose:
                print('Input %s, with value %s' % (self.inputs[i].name, input_values[i]))
        self.outputs = self.graph.calculate(verbose)

        return self.outputs
