

class InvalidBlockSizeError(Exception):
    def __init__(self, msg="Block size cannot be greater than image width/height or smaller than zero"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

class InvalidFrequenciesNumberError(Exception):
    def __init__(self, msg="Error: d value cannot be bigger than 2*F-2 or smaller than 0"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg