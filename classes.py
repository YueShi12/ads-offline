class Patient:

    # initiliaze a patient by storing the variables given by the input
    def __init__(self, startI1, endI1, delay, lengthI2):
        # store it in lists, with first element always None to ease indexing
        self.startIs =  startI1
        self.endIs =  endI1
        self.delay = delay
        self.lengthI2 = lengthI2

