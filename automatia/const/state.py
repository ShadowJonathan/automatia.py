class State:
    def __init__(self):
        pass


class Continue(State):
    """Continue running the query and acknowledge this module can't process this URL"""

    def __init__(self):
        State.__init__(self)


class Fail(State):
    """Fail the query, and give a reason why"""

    def __init__(self, *reason):
        State.__init__(self)
        self.reason = reason

    def explain(self):
        return " ".join([str(r) for r in self.reason])


class Result(State):
    """Return a result, a new URL to be processed through the shelf"""

    def __init__(self, URL):
        State.__init__(self)
        self.URL = URL

    def get(self):
        return self.URL


class Finish(State):
    """Finish the query"""

    def __init__(self):
        State.__init__(self)
