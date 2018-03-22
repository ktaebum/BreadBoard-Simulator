from queue import Queue
from matplotlib import colors as mcolors
from breadboard.tools.gates import *
from .exceptions import *
from .visualize.visual_breadboard import BreadBoardVisual

import random


class BreadGraph:
    # color_set = list(dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys())
    color_set = list(mcolors.XKCD_COLORS.values())
    random.shuffle(color_set)

    def __init__(self):
        self.num_nodes = 0
        self.nodes = {}

    def reset_graph(self):
        self.num_nodes = 0
        self.nodes = {}

    def delete_node(self, node_name):
        line_to_deletes = []
        delete_node = self.nodes.pop(node_name)
        for node in self.nodes.values():
            for edge in node.edges:
                if edge.name == node_name:
                    line_to_deletes.append((node.name, edge.name))
                    node.edges.remove(edge)

        del delete_node
        return line_to_deletes

    def delete_edge(self, from_node_name, to_node_name):
        from_node = self.nodes[from_node_name]
        from_node.edges.remove(to_node_name)

        return from_node_name, to_node_name

    def add_node(self, x, y, name, gate, value=None):
        if name in self.nodes.keys():
            raise DuplicatedNodeException()

        # if gate == 'transmit' and value is None:
        #     raise TransmitNoneValueException()

        new_node = BreadGraph.BreadNode(x, y, name, gate, value, BreadGraph.color_set.pop())
        self.nodes[name] = new_node
        self.num_nodes += 1
        return new_node

    def add_edge(self, from_node, to_node):
        # It is a digraph, must build DAG
        if self.nodes[to_node] in self.nodes[from_node].edges:
            # already connected
            return
        self.nodes[from_node].edges.append(self.nodes[to_node])

    def calculate(self, verbose=False):
        # Calculate result based on topological sort
        # step1: identify source nodes
        node_in_degree = {key: 0 for key in self.nodes.keys()}
        for name in self.nodes.keys():
            node = self.nodes[name]
            for edge in node.edges:
                node_in_degree[edge.name] += 1

        # step2: enqueue nodes whose in_degree == 0
        queue = Queue()
        for name in node_in_degree.keys():
            if node_in_degree[name] == 0:
                self.nodes[name].calculate_gate()
                if verbose:
                    print('Node' + str(self.nodes[name]) + ' Calculated, with value = ' + str(self.nodes[name].value))
                queue.put(name)

        result = {}
        # step3: update via traversing graph
        while queue.qsize() > 0:
            name = queue.get()
            node = self.nodes[name]

            if len(node.edges) == 0:
                # this should be a result node
                result[name] = node.value

            for edge in node.edges:
                node_in_degree[edge.name] -= 1
                if edge.gate == 'transmit':
                    edge.value = node.value
                else:
                    edge.value.append(node.value)  # value propagation
                if node_in_degree[edge.name] == 0:
                    edge.calculate_gate()
                    if verbose:
                        print(
                            'Node' + str(edge) + ' Calculated, with value = ' + str(edge.value))
                    queue.put(edge.name)

        return result

    class BreadNode:
        def __init__(self, x, y, name, gate, value, color):
            """
            :param x: for visualize
            :param y: for visualize
            :param name: node name
            :param gate: transmit or any other gate
            :param value: if gate == transmit, must be a single boolean value. Else, list of input
            :param color: for visualize
            """
            self.x = x
            self.y = y
            if gate == 'transmit':
                self.value = value
            else:
                self.value = []
            self.gate = gate
            self.name = name
            self.color = color
            self.edges = []

        def calculate_gate(self):
            if self.gate == 'transmit':
                return
            else:
                if len(self.value) != 2:
                    raise GateNodeNotContainTwoValues()
                if self.gate == 'NAND':
                    self.value = NAND_gate(*self.value)
                elif self.gate == 'AND':
                    self.value = AND_gate(*self.value)
                elif self.gate == 'OR':
                    self.value = OR_gate(*self.value)
                elif self.gate == 'NOR':
                    self.value = NOR_gate(*self.value)
                elif self.gate == 'XOR':
                    self.value = XOR_gate(*self.value)

        def __hash__(self):
            return hash(self.name)

        def __eq__(self, other):
            if type(other) != type(self):
                return False

            return self.name == other.name

        def __str__(self):
            if BreadBoardVisual.y_coord2alphabet is not None:
                return "(%d %s): %s (%s)" % (self.x, BreadBoardVisual.y_coord2alphabet[self.y], self.name, self.gate)
            return "(%d, %d): %s (%s)" % (self.x, self.y, self.name, self.gate)
