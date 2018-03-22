class TransmitNoneValueException(Exception):
    def __str__(self):
        return 'Transmit Should Propagate Boolean Value!'


class DuplicatedConnectException(Exception):
    def __init__(self, node_name):
        self.y = node_name[-1:]
        self.x = node_name[:-1]

    def __str__(self):
        return 'Node (%s, %s) is Already Plugged In!' % (self.x, self.y)


class NonExistingChip(Exception):
    def __init__(self, chip_number):
        self.chip_number = chip_number

    def __str__(self):
        return 'Chip Number %d does not exist!' % self.chip_number


class FullGateException(Exception):
    def __init__(self, chip_name, gate_number):
        self.chip_name = chip_name
        self.gate_number = gate_number

    def __str__(self):
        return '%s\'s %d gate is full!' % (self.chip_name, self.gate_number)


class NonFullGateExtractionException(Exception):
    def __init__(self, chip_name, gate_number):
        self.chip_name = chip_name
        self.gate_number = gate_number

    def __str__(self):
        return '%s\'s %d gate is not full to extract!' % (self.chip_name, self.gate_number)
