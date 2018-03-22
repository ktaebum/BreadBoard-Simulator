class TransmitNoneValueException(Exception):
    def __str__(self):
        return 'Transmit Should Propagate Boolean Value!'


class DuplicatedConnectException(Exception):
    def __init__(self, node_name):
        self.y = node_name[-1:]
        self.x = node_name[:-1]

    def __str__(self):
        return 'Node (%s, %s) is Already Plugged In!' % (self.x, self.y)
