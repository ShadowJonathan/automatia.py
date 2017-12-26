SleepOver = "top"
Gym = "bottom"


def after(*packages):
    """Use to make sure your module only gets checked after another package."""
    return After(packages)


def before(*packages):
    """Use to make sure your module only gets checked before another package."""
    return Before(packages)


class After:
    def __init__(self, this):
        """
        :type this: list[After]|string
        """
        self.after = this
        self.multi = isinstance(this, (list, tuple))
        if self.multi:
            self.after = [After(p) for p in self.after if not isinstance(p, After)]  # FIXME prob loop

    def isafter(self, package):
        return self.after == package

    def __str__(self):
        return '<After "{}">'.format(self.after)

    __repr__ = __str__


class Before:
    def __init__(self, this):
        """
        :type this: list[Before]|string
        """
        self.before = this
        self.multi = isinstance(this, (list, tuple))
        if self.multi:
            self.before = [Before(p) for p in self.before if not isinstance(p, Before)]  # FIXME prob loop

    def isbefore(self, package):
        return self.before == package

    def __str__(self):
        return '<Before "{}">'.format(self.before)

    __repr__ = __str__
