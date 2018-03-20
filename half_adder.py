from breadboard.breadmain import BreadBoardMain
from breadboard.visualize.visual_breadboard import BreadBoardVisual

breadboard = BreadBoardMain()

breadboard.add_chip(3, 'E', 7408)
breadboard.add_chip(14, 'E', 7486)

breadboard.add_input(1, 'H', 'A', True)
breadboard.add_input(2, 'I', 'B', True)

breadboard.add_line('A', '4F', 4, 'F')
breadboard.add_line('A', '15H', 15, 'H')

breadboard.add_line('B', '5F', 5, 'F')
breadboard.add_line('B', '16H', 16, 'H')

breadboard.connect_line2chip('4F', 'and', 0, 1)
breadboard.connect_line2chip('5F', 'and', 0, 1)

breadboard.add_line('and', 'C', 28, 'J')

breadboard.connect_line2chip('15H', 'xor', 1, 2)
breadboard.connect_line2chip('16H', 'xor', 1, 2)

breadboard.add_line('xor', 'S', 29, 'B')

breadboard.calculate(True)

BreadBoardVisual(breadboard)
