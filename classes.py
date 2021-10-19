class Patient:

    # initiliaze a patient by storing the variables given by the input
    def __init__(self, startI1, endI1, delay, lengthI2):
        # store it in lists, with first element always None to ease indexing
        self.startIs = [None, startI1, None]
        self.endIs = [None, endI1, None]
        self.delay = delay
        self.lengthI2 = lengthI2

        self.slots = [None, None, None]

        self.locations = [None, None, None]
