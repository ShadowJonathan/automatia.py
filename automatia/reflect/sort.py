# Input

# Download
# Relation
# Information (fail on auto)
# Other

DOWN = "DOWN"
REL = "REL"
INFO = "INFO"
OTHER = "OT"


class Input:
    def __init__(self, inputrepr="", info="", selfval=None):
        if inputrepr == "" or len(inputrepr) > 1 or info == "" or selfval is None:
            raise TypeError()
        self.irepr = inputrepr
        self.sinfo = info
        self.sval = selfval

    def repr(self):
        return self.irepr

    def getinfo(self):
        return self.sinfo

    def selfval(self):
        return self.sval

    def a_banned(self):
        return False


class Download(Input):
    def __init__(self):
        Input.__init__(self, "d", "Generic download", DOWN)


class Relation(Input):
    def __init__(self):
        Input.__init__(self, "r", "Relational info", REL)


class Information(Input):
    def __init__(self):
        Input.__init__(self, "i", "Information (not in automatic mode)", INFO)

    def a_banned(self):
        return True


class Other(Input):
    def __init__(self):
        Input.__init__(self, "o", "Other", OTHER)
