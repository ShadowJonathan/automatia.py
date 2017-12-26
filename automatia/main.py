from __future__ import print_function
import sys
import six

CLI = False
DEBUG = False


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def setdebug(state):
    global DEBUG
    DEBUG = state

    Debug("Python:")
    for p in sys.version.split("\n"):
        Debug(p)


def setcli():
    global CLI
    CLI = True


def Warn(*message):
    """
    :param Any message:
    """
    print("[WARN] " + " ".join([str(m) for m in message]))


def Inform(*message):
    """
    :param Any message:
    """
    print("[AUTOMATIA] " + " ".join([str(m) for m in message]))


def Debug(*message):
    global DEBUG
    if DEBUG:
        Inform("[D] " + " ".join([str(m) for m in message]))


def Error(*message):
    """
    :param Any message:
    """
    eprint("[ERROR] " + " ".join([str(m) for m in message]))


class FinishFinal(Exception):
    pass


class FinishNow(FinishFinal):
    pass


class FinishResult(Exception):
    def __init__(self, URL, m=None):
        self.URL = URL
        self.m = m
