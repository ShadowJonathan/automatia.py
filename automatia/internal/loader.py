import imp
import sys


class DummyLoader(object):
    def load_module(self, name):
        names = name.split("__")
        path = None
        f = None
        info = None
        for name in names:
            f, path, info = imp.find_module(name, path)
            path = [path]
        return imp.load_module(name, f, path[0], info)

    def find_module(self, name, path=None):
        if name.find("__") != -1 and not name.startswith("__") and name.find(".") == -1:
            return DummyLoader()
        else:
            return None


if not sys.meta_path:
    sys.meta_path.append(DummyLoader())
else:
    sys.meta_path[0] = DummyLoader()


def load_module(name):
    names = name.split(".")
    path = None
    f = None
    info = None
    for name in names:
        f, path, info = imp.find_module(name, path)
        path = [path]
    return imp.load_module(name, f, path[0], info)
