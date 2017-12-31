from __future__ import print_function

import sys
import termios
import tty

import automatia
import automatia.internal.shelf as shelf
from .sort import *


def inkey():
    fd = sys.stdin.fileno()
    remember_attributes = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
    sys.stdout.write(character)
    return character


class AutomaticHalt(Exception): pass


def isAutomatic():
    return automatia.isauto()


def printText(*message):
    """
    :param Any message:
    """
    print("[QUERY] " + " ".join([str(m) for m in message]))


def one_input(choices=[], fake=None):
    s = "[QUERY] ({})>".format(",".join(choices))
    if fake is not None:
        if fake in choices:
            print(s + ' (automatic) "' + fake + '"')
            return fake
        else:
            if isAutomatic():
                raise AutomaticHalt()
            else:
                printText(fake, "is not a valid choice.")
                return one_input(choices)
    else:
        while True:
            r = oi(s)
            if r not in choices:
                printText("Wrong input \"{}\": available inputs: {}".format(r, choices.__repr__()))
                continue
            else:
                return r


def oi(s):
    print(s, end="")
    r = inkey()
    print()
    return r


def line_input(choices=[], fake=None):
    print("[QUERY] ({})".format(",".join(choices)))
    if fake is not None:
        if fake in choices:
            print('[QUERY] > (automatic) "{}"'.format(fake))
            return fake
        else:
            if isAutomatic():
                raise AutomaticHalt()
            else:
                printText(fake, "is not a valid choice.")
                return line_input(choices)
    else:
        while True:
            r = li()
            if r not in choices:
                printText("Wrong input: available inputs: {}".format(choices.__repr__()))
                continue
            else:
                return r


def li():
    return input("[QUERY] >")


def showText(text="", s=""):
    if s != "":
        printText("[{}]:".format(s))
    for t in text.split("\n"):
        printText(t)


# QUERIES

def SimpleQuery(query="", have=""):
    return SQ(query, have, getnextarg())


def SQ(query="", have="", default=None):
    s = "SimpleQuery"
    if query != "":
        showText(query, s)
    q = []
    for c in have:
        if c == "d":
            q.append(Download())
        elif c == "r":
            q.append(Relation())
        elif c == "i":
            q.append(Information())
        elif c == "o":
            q.append(Other())
    return CQ("", q, default)


def ComplexQuery(query="", choices=[]):
    return CQ(query, choices, getnextarg())


def CQ(query="", choices=[], default=None):
    s = "ComplexQuery"
    if query != "":
        showText(query, s)
    printText("Choices:")
    for c in choices:
        if not isinstance(c, Input):
            raise TypeError(c.__repr__() + " is not of type Input")
        printText("({0.irepr}): {0.sinfo}".format(c))
    r = one_input([v.repr() for v in choices], default)
    for c in choices:
        if r == c.repr():
            if isAutomatic() and c.a_banned():
                raise AutomaticHalt()
            return c.selfval()


def BoolQuery(query=""):
    return BQ(query, getnextarg())


def BQ(query="", default=None):
    s = "BoolQuery"
    if query != "":
        showText(query, s)
    fake = None
    if default is not None:
        if default:
            fake = "y"
        else:
            fake = "n"

    r = one_input(["y", "n"], fake)
    return r == "y"


def StringQuery(query="", choices={}):
    return StQ(query, choices, getnextarg())


def StQ(query="", choices={}, default=None):
    """

    :param string query:
    :param dict[string, string] choices:
    :param Optional[string] default:
    """
    s = "StringQuery"
    if query != "":
        showText(query, s)
    printText("Choices:")

    if not isinstance(choices, dict):
        raise TypeError(choices.__repr__() + " is not of type dict")

    for k, v in choices.items():
        printText("({}): {}".format(k, v))

    return line_input(choices.keys(), default)


def getnextarg():
    return shelf.current_param and shelf.current_param.getnextarg()


def HasNextArg():
    return shelf.current_param and shelf.current_param.hasnextarg()

# SimpleQuery
# ComplexQuery
# StringQuery
# BoolQuery
# HasNextArg
