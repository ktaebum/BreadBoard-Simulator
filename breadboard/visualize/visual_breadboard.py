from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
import re


class BreadBoardVisual(object):
    y_coord2alphabet = None

    def __init__(self, breadboard):
        self.breadboard = breadboard

        plt.ion()  # interactive on
        self.ax = None
        self.fig = None
        self.draw_basic_map()

        # For delete
        self.lines = {}
        self.points = {}
        self.chips = {}

        self.input_texts = {}
        self.output_texts = {}

        self.input_position = 0
        self.output_position = 0

    def draw_single_input(self, node_name):
        node = self.breadboard.graph.nodes[node_name]

        in_graph_text = self.ax.text(node.x - 0.2, node.y + 0.2, node.name)
        out_graph_text = self.ax.text(self.breadboard.X_body[0] - 11, self.input_position,
                                      node.name + ' = ' + str(node.value), size=15)

        self.input_texts[node_name] = (in_graph_text, out_graph_text)
        self.input_position += 5

    def draw_single_output(self, node_name):
        node = self.breadboard.graph.nodes[node_name]
        in_graph_text = self.ax.text(node.x - 0.2, node.y + 0.2, node.name)
        out_graph_text = self.ax.text(self.breadboard.X_body[-1] + 4, self.output_position,
                                      node.name + ' = ' + str(node.value),
                                      size=15)

        self.output_texts[node_name] = (in_graph_text, out_graph_text)
        self.output_position += 5

    def draw_single_transmit_line(self, from_node_name, to_node_name):
        from_node = self.breadboard.graph.nodes[from_node_name]
        to_node = self.breadboard.graph.nodes[to_node_name]
        self.lines[from_node_name + to_node_name] \
            = self.ax.plot((from_node.x, to_node.x), (from_node.y, to_node.y),
                           color=from_node.color)
        self.points[from_node_name] = \
            self.ax.scatter(from_node.x, from_node.y, color=from_node.color, marker='o')

        self.points[to_node_name] = \
            self.ax.scatter(to_node.x, to_node.y, color=to_node.color, marker='o')

    def draw_single_chip(self, chip):
        self.ax.add_patch(
            patches.Rectangle(
                (chip.x[0], chip.y[0]),
                len(chip.x) - 1,
                len(chip.y) - 1,
                color='black',
                alpha=0.2
            )
        )
        self.ax.text(chip.x[0] + 0.6, chip.y[0] + 1.2, chip.name, color='black', size=10)

    def clear_input(self):
        for text in self.input_texts.values():
            text[0].remove()
            text[1].remove()

        self.input_texts = {}

    def clear_output(self):
        for text in self.output_texts.values():
            text[0].remove()
            text[1].remove()

        self.output_texts = {}

    def remove_single_transmit_line(self, line_name):
        """
        if line connects point 3A and 6H,
        line name is defined as 3A6H
        :param line_name: delete target line name
        :return:
        """
        pass

    def write_input(self):
        self.input_position = 0
        for input_node in self.breadboard.inputs:
            in_graph_text = self.ax.text(input_node.x - 0.2, input_node.y + 0.2, input_node.name)
            out_graph_text = self.ax.text(self.breadboard.X_body[0] - 11, self.input_position,
                                          input_node.name + ' = ' + str(input_node.value), size=15)

            self.input_texts[input_node.name] = (in_graph_text, out_graph_text)
            self.input_position += 5

    def write_output(self):
        if self.breadboard.outputs is None:
            return
        self.output_position = 0
        for output_node in self.breadboard.outputs:
            node = self.breadboard.graph.nodes[output_node]
            in_graph_text = self.ax.text(node.x - 0.2, node.y + 0.2, node.name)
            out_graph_text = self.ax.text(self.breadboard.X_body[-1] + 4, self.output_position,
                                          node.name + ' = ' + str(node.value),
                                          size=15)
            self.output_texts[node.name] = (in_graph_text, out_graph_text)
            self.output_position += 5

    def draw_transmit_edges(self):
        graph = self.breadboard.graph
        nodes = graph.nodes.values()
        for node in nodes:
            for edge in node.edges:
                if edge.gate != 'transmit':
                    continue
                self.ax.plot((node.x, edge.x), (node.y, edge.y), color=node.color)
                self.ax.plot(node.x, node.y, color=node.color)
                self.ax.plot(edge.x, edge.y, color=node.color)

    def draw_chips(self):
        for chip in self.breadboard.chips:
            self.ax.add_patch(
                patches.Rectangle(
                    (chip.x[0], chip.y[0]),
                    len(chip.x) - 1,
                    len(chip.y) - 1,
                    color='black'
                )
            )

            self.ax.text(chip.x[0] + 0.8, chip.y[0] + 1.2, chip.name, color='white', size=15)

    def draw_basic_map(self):
        self.fig = plt.figure(figsize=(16, 9))

        Xb, Yb = np.meshgrid(self.breadboard.X_body, self.breadboard.Y_body)
        Xp1, Yp1 = np.meshgrid(self.breadboard.X_plug, self.breadboard.Y_plug_below)
        Xp2, Yp2 = np.meshgrid(self.breadboard.X_plug, self.breadboard.Y_plug_above)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('BreadBoard', fontsize=22)
        for y in self.breadboard.Y_body:
            self.ax.axhline(y, linestyle='--', color='lightgrey')

        for x in self.breadboard.X_body:
            self.ax.axvline(x, ymax=0.44, linestyle='--', color='lightgrey')
            self.ax.axvline(x, ymin=0.56, linestyle='--', color='lightgrey')

        self.ax.plot(Xb, Yb, '.', color='black')
        self.ax.plot(Xp1, Yp1, '.', color='black')
        self.ax.plot(Xp2, Yp2, '.', color='black')

        self.ax.axhline(self.breadboard.Y_plug_below[-1] + 0.5, color='blue')
        self.ax.axhline(self.breadboard.Y_plug_below[0] - 0.5, color='red')

        self.ax.axhline(self.breadboard.Y_plug_above[-1] + 0.5, color='blue')
        self.ax.axhline(self.breadboard.Y_plug_above[0] - 0.5, color='red')

        self.ax.set_xticks(self.breadboard.X_body)
        self.ax.set_yticks(self.breadboard.Y_body)
        y_label = []
        BreadBoardVisual.y_coord2alphabet = {}
        for i in range(len(self.breadboard.Y_body)):
            y_label.append(chr(65 + i))
            BreadBoardVisual.y_coord2alphabet[self.breadboard.Y_body[i]] = chr(65 + i)

        self.ax.set_yticklabels(y_label)
