class DuplicatedNodeException(Exception):
    def __str__(self):
        return 'Node Name Should be Unique!'


class NonExistingNodeException(Exception):
    def __str__(self):
        return 'Non-Existing Node!'


class NonBooleanInputException(Exception):
    def __str__(self):
        return 'Input Value Should be Boolean Value!'


class GateNodeNotContainTwoValues(Exception):
    def __str__(self):
        return 'Gate Node Should Contain 2 Values Before Calculated'
