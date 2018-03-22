class NonSupportingChipException(Exception):
    def __init__(self, chip_type):
        self.chip_type = chip_type

    def __str__(self):
        return 'Chip %d is Not-Valid Yet :(' % self.chip_type
