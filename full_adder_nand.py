from breadboard.breadmain import BreadBoard
from breadboard.visualize.visual_breadboard import BreadBoardVisual

breadboard = BreadBoard()

breadboard.add_chip(3, 'E', 7400)
breadboard.add_chip(12, 'E', 7400)
breadboard.add_chip(21, 'E', 7400)

breadboard.add_input(1, 'H', 'A', True)
breadboard.add_input(2, 'I', 'B', True)
breadboard.add_input(19, 'J', 'Cin', False)

# u1
breadboard.add_line('A', '4G')
breadboard.add_line('B', '5H')

breadboard.connect_line2chip('4G', 'u1', 0, 1)
breadboard.connect_line2chip('5H', 'u1', 0, 1)

# u2
breadboard.add_line('u1', '7G')
breadboard.add_line('A', '8G')

breadboard.connect_line2chip('7G', 'u2', 0, 2)
breadboard.connect_line2chip('8G', 'u2', 0, 2)

# u3
breadboard.add_line('u1', '6D')
breadboard.add_line('B', '7D')

breadboard.connect_line2chip('6D', 'u3', 0, 4)
breadboard.connect_line2chip('7D', 'u3', 0, 4)

# u4
breadboard.add_line('u3', '13G')
breadboard.add_line('u2', '14G')

breadboard.connect_line2chip('13G', 'u4', 1, 1)
breadboard.connect_line2chip('14G', 'u4', 1, 1)

# u5
breadboard.add_line('Cin', '16I')
breadboard.add_line('u4', '17I')

breadboard.connect_line2chip('17I', 'u5', 1, 2)
breadboard.connect_line2chip('16I', 'u5', 1, 2)

# u6
breadboard.add_line('u5', '15C')
breadboard.add_line('u4', '16C')

breadboard.connect_line2chip('15C', 'u6', 1, 4)
breadboard.connect_line2chip('16C', 'u6', 1, 4)

# u7
breadboard.add_line('u5', '22H')
breadboard.add_line('Cin', '23H')

breadboard.connect_line2chip('22H', 'u7', 2, 1)
breadboard.connect_line2chip('23H', 'u7', 2, 1)

# u8
breadboard.add_line('u6', '25J')
breadboard.add_line('u7', '26J')

breadboard.connect_line2chip('25J', 'u8', 2, 2)
breadboard.connect_line2chip('26J', 'u8', 2, 2)

# u9
breadboard.add_line('u5', '24A')
breadboard.add_line('u1', '25A')

breadboard.connect_line2chip('24A', 'u9', 2, 4)
breadboard.connect_line2chip('25A', 'u9', 2, 4)

breadboard.add_output('u8', 'S', 29, 'H')
breadboard.add_output('u9', 'Cout', 29, 'C')

breadboard.calculate(True)

BreadBoardVisual(breadboard)
