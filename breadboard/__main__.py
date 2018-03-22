from .breadmain import BreadBoard
from .visualize.visual_breadboard import BreadBoardVisual

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BreadBoard Simulator')
    parser.add_argument('-n', '--num', type=int,
                        help='how many bread board to use')

    args = parser.parse_args()

    if args.num:
        board = BreadBoard(args.num)
    else:
        board = BreadBoard(1)

    BreadBoardVisual(board)

    while True:
        command = input()
        if command == 'exit':
            exit(0)
        print(command)
