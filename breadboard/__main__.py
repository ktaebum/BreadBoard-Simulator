from .components.breadmain import BreadBoard
from .visualize.visual_breadboard import BreadBoardVisual
from .preprocess import map_commands
import re
import argparse
import os

command_map = map_commands()
command_log = []

verbose = False


def save_command_log(logs, file_name):
    file = open(file_name, 'w')
    for log in logs:
        file.write(log + '\n')
    file.close()


def parse_command(command):
    command_log.append(command)
    command = re.split(r'\s+', command)
    try:
        command[0] = command_map[command[0]]
    except KeyError:
        print('Non Supporting Command, Type Again')
        return

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
        input_values = [i in ['True', '1', 'T'] for i in command[1:]]
        interface.clear_input()
        interface.clear_output()
        board.calculate(input_values, verbose)
        interface.write_input()
        interface.write_output()
    elif command[0] == 'save':
        try:
            command_log.pop()
            save_command_log(command_log, command[1])
        except IndexError:
            print('Error: save command should have 1 argument')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, help='Input file name (contain path)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether print internal results or not')

    args = parser.parse_args()

    verbose = args.verbose

    board = BreadBoard()
    interface = BreadBoardVisual(board)

    if args.input:
        path = os.path.join(os.path.curdir, args.input)
        map_file = open(path, 'r')

        for line in map_file:
            parse_command(line[:-1])

        map_file.close()

    while True:
        print('(breadboard)$ ', end='')
        command = input()
        parse_command(command)
