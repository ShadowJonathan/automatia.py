import six


# TODO MAKE THIS A THING
class But: pass


class PythonVersion:
    def __init__(self, version):
        """
        Specify which python version (2 or 3) your module needs to run. Automatia will try to reload itself in that
        python version with `python2` or `python3` as it's interprenter, and then try to load the module (force it,
        if needed) and execute it.
        :param int version:
        """
        self.reqversion = version

    def _why(self):
        if six.PY2 and self.reqversion == 2:
            return True
        elif six.PY2 and self.reqversion == 3:
            return ReloadWith3
        elif six.PY3 and self.reqversion == 2:
            return ReloadWith2
        elif six.PY3 and self.reqversion == 3:
            return True
        else:
            # Uncaught
            return False


ReloadWith3 = "rel3"
ReloadWith2 = "rel2"
