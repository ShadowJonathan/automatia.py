import json
from os import makedirs
from os.path import expanduser

import automatia
from automatia.internal.loader import load_module

home = expanduser("~")
try:
    makedirs(home + "/.automatia")
except OSError as oe:
    if oe.errno != 17:
        raise oe

installed_packages = {}
resolved_packages = []


def load_packages():
    global installed_packages
    global resolved_packages

    try:
        with open(home + "/.automatia/modlist.json") as jsonfile:
            data = json.load(jsonfile)
    except IOError:
        data = {}

    automatia.Debug("modlist.json:", data)

    installed_packages = data or dict()

    resolved_packages = check_packages(installed_packages)
    return resolved_packages


def check_packages(packages):
    """

    :param dict[str, bool] packages:
    :rtype: list[_Module]
    """

    modules = []
    for package, off in packages.items():
        M = load_package(package)
        if M is None:
            if off:
                continue
            automatia.Warn(package, "has failed to load, possibly this module has been removed, or a faulty version "
                                    "has been installed")
            automatia.Warn(package, "will now be removed from the module list.")
            remove_package(package)
        else:
            if not off:
                add_package(package)
                automatia.Debug("found package", package, "again")
            modules.append(M)
    return modules


def load_package(package):
    try:
        m = load_module(package)
        i = m.a()
        if not isinstance(i, automatia.AutomatiaModule):
            raise TypeError
        return _Module(i, package)
    except ImportError:
        automatia.Debug(package, "ImportError")
        return None
    except AttributeError:
        automatia.Debug(package, "AttributeError")
        return None
    except KeyError:
        automatia.Debug(package, "KeyError")
        return None
    except TypeError:
        automatia.Debug(package, "TypeError")
        return None


def remove_package(package):
    global installed_packages
    installed_packages[package] = False
    save_list()


def perm_remove_package(package):
    global installed_packages
    del installed_packages[package]
    save_list()


def add_package(package):
    global installed_packages
    installed_packages[package] = True
    save_list()


def save_list():
    global installed_packages
    with open(home + "/.automatia/modlist.json", "w") as jsonfile:
        json.dump(installed_packages, jsonfile)


class _Module:
    def __init__(self, m, package_path=None):
        """

        :param automatia.AutomatiaModule m:
        """

        self.m = m
        self.pp = package_path
        self.p = 0
        self.a = []
        self.b = []

        self.a_ok = False
        self.b_ok = False

        self.checked = False

    def init(self, shelf):
        """
        :param shelf: Shelf
        """
        self.p, self.a, self.b = self.m.resolve_priority()
        shelf.register_triggers(self.a, self.b)

    def check(self, URL):
        self.checked = True
        return self.m.Match(URL)

    def ischecked(self):
        return self.checked

    def uncheck(self):
        self.checked = False

    def do(self, URL):
        try:
            return self.m.Do(URL)
        except Exception as E:
            return automatia.Fail("EXC", E)

    def after_prioritized(self, package):
        for a in self.a:
            if a.isafter(package):
                return True
        return False

    def before_prioritized(self, package):
        for b in self.b:
            if b.isbefore(package):
                return True
        return False

    def mark_after_ok(self):
        self.a_ok = True

    def mark_before_ok(self):
        self.b_ok = True

    def invalidate_prioritization_after(self):
        self.a = []

    def invalidate_prioritization_before(self):
        self.b = []

    def __str__(self):
        return '<Automatia Module "{}" @ \'{}\'>'.format(self.Name(), self.pp or "unknown")

    __repr__ = __str__

    def Name(self):
        return self.m.FriendlyName()
