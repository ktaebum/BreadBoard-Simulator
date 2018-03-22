from .breadmain import BreadBoard
from .visualize.visual_breadboard import BreadBoardVisual

import re

exits = ['exit', 'quit', 'q']
inputs = ['input', 'in']
outputs = ['output', 'out']
lines = ['line', 'l']
chips = ['chip', 'c']
helps = ['help', 'h']
clean = ['clean', 'reset', 'clear', 'cl', 're']
delete = ['delete', 'del']
connects = ['connect', 'con']
runs = ['run', 'exec', 'simulate']

command_map = {}

for c in exits:
    command_map[c] = 'exit'

for c in inputs:
    command_map[c] = 'input'

for c in outputs:
    command_map[c] = 'output'

for c in lines:
    command_map[c] = 'line'

for c in chips:
    command_map[c] = 'chip'

for c in clean:
    command_map[c] = 'clean'

for c in delete:
    command_map[c] = 'delete'

for c in connects:
    command_map[c] = 'connect'

for c in runs:
    command_map[c] = 'run'

if __name__ == '__main__':
    board = BreadBoard(2)
    interface = BreadBoardVisual(board)

    while True:
        print('>> ', end='')
        command = re.split(r'\s+', input())
        try:
            command[0] = command_map[command[0]]
        except KeyError:
            print('Non Supporting Command, Type Again')
            continue
        if command[0] == 'exit':
            exit(0)
        elif command[0] == 'input':
            try:
                board.add_input(command[1], command[2])
                interface.draw_single_input(command[1])
            except IndexError:
                print('Error: input command should have 2 argument')
        elif command[0] == 'output':
            try:
                board.add_output(command[1], command[2], command[3])
                interface.draw_single_output(command[2])
                interface.draw_single_transmit_line(command[1], command[2])
            except IndexError:
                print('Error: output command should have 3 argument')
        elif command[0] == 'line':
            try:
                if len(command) >= 4:
                    gate_name = board.extract_gate_output(command[1], int(command[2]), int(command[3]))
                    interface.draw_single_transmit_line(command[1], gate_name)
                else:
                    board.add_line(command[1], command[2])
                    interface.draw_single_transmit_line(command[1], command[2])
            except IndexError:
                print('Error: line command should have at least 2 arguments')
        elif command[0] == 'chip':
            try:
                chip = board.add_chip(command[1], int(command[2]))
                interface.draw_single_chip(chip)
            except IndexError:
                print('Error: chip command should have 2 argument')
        elif command[0] == 'show':
            pass
        elif command[0] == 'help':
            pass
        elif command[0] == 'clean':
            pass
        elif command[0] == 'delete':
            try:
                delete_type = command[1]
                if delete_type == 'chip':
                    pass
                elif delete_type == 'line':
                    pass
                elif delete_type == 'input':
                    pass
                elif delete_type == 'output':
                    pass
            except IndexError:
                print('Error: Delete command should have at least argument')
        elif command[0] == 'connect':
            # connect wire to gate
            try:
                gate_name = board.connect_line_to_gate(command[1], int(command[2]), int(command[3]))
                interface.draw_single_transmit_line(command[1], gate_name)
            except IndexError:
                print('Error: connect command should have 3 argument')
        elif command[0] == 'run':
            input_values = [bool(i) for i in command[1:]]
            interface.clear_input()
            interface.clear_output()
            board.calculate(input_values, True)
            interface.write_input()
            interface.write_output()
