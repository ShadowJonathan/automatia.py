from automatia.internal.util import flatten, is_url


def make_params(*args):
    args = flatten(args)
    l = []  # done parameters
    p = ""  # working URL
    cmd = []  # working cmds

    def flush(l):

        if p:
            l.append(Param(p, cmd))

    for a in args:
        if is_url(a):
            flush(l)
            p = a
            cmd = []
        else:
            cmd.append(a)

    flush(l)

    return l


# "http://... o r author d http://... d" ->
# [Param(url="http://...", sub=["o", "r", "author", "d"]), Param(url="http://...", sub=["d"])]
class Param:
    def __init__(self, url=None, sub=[]):
        if url is None:
            raise TypeError
        self.URL = url
        self.sub = sub
        self.cmds = sub[:]

    def get(self):
        return self.URL

    def hasnextarg(self):
        return len(self.cmds) > 0

    def getnextarg(self):
        return len(self.cmds) > 0 and self.cmds.pop(0) or None

    def __str__(self):
        return "Param(url={}, sub={})".format(self.URL.__repr__(), self.sub.__repr__())

    __repr__ = __str__
