def map_commands():
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
    saves = ['save', 's']

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

    for c in saves:
        command_map[c] = 'save'

    return command_map
