from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np


class BreadBoardVisual(object):
    def __init__(self, breadboard):
        self.breadboard = breadboard

        self.ax = None
        self.fig = None
        self.draw_basic_map()
        self.draw_chips()
        self.draw_transmit_edges()
        self.write_input()
        self.write_output()

        plt.show()

    def write_input(self):
        y = 0
        for input_node in self.breadboard.inputs:
            self.ax.text(input_node.x - 0.2, input_node.y + 0.2, input_node.name)
            self.ax.text(-6, y, input_node.name + ' = ' + str(input_node.value), size=15)
            y += 5

    def write_output(self):
        if self.breadboard.outputs is None:
            return
        y = 0
        for output_node in self.breadboard.outputs:
            node = self.breadboard.graph.nodes[output_node]
            self.ax.text(node.x - 0.2, node.y + 0.2, node.name)
            self.ax.text(34, y, node.name + ' = ' + str(node.value), size=15)
            y += 5

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
        self.ax.set_yticklabels([chr(65 + i) for i in range(len(self.breadboard.Y_body))])
