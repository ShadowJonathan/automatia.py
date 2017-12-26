import re
import sys

import automatia
import automatia.internal.param as param
import automatia.internal.resolve as resolve
import automatia.internal.shelf as shelf
import automatia.internal.util as util
import automatia.reflect as reflect

args = sys.argv

if len(args) > 0 and re.match(r".*automatia.*", args[0], re.I) is not None:
    args.pop(0)  # remove automatia from first arg

if "-D" in args:
    args.remove("-D")
    automatia.Inform("Debug ON")
    automatia.setdebug(True)

first_arg = len(args) > 0 and args[0] or None


def main():
    automatia.setcli()

    print("########### AUTOMATIA CLI")

    if first_arg is None:
        automatia.Debug("No first arg")
        print_help()
        return
    elif not util.is_url(first_arg):
        automatia.Debug("First arg not an url")
        alt()
        return

    params = param.make_params(sys.argv)

    packages = resolve.load_packages()
    s = shelf.Shelf()
    s.walk(packages)
    automatia.Debug("Modules:", s)
    automatia.Debug("Params", params)

    def do(p):
        try:
            s.run(p)
        except automatia.FinishNow:
            exit(1)
        except automatia.FinishFinal:
            return
        except automatia.FinishResult as fr:
            if reflect.BoolQuery('"{}" wants to re-issue a new URL: "{}"\nRe-issue new URL?'.format(fr.m.Name(),
                                                                                                    fr.URL), True):
                do(param.Param(fr.URL, p.cmds[:]))

    for p in params:
        do(p)

    automatia.Debug("Finished")


def print_help():
    pass


def alt():
    global args
    if first_arg == "help" or first_arg == "-h":
        print_help()
    elif first_arg == "list":
        packages = resolve.load_packages()
        if len(packages) == 1:
            automatia.Inform("1 package")
        else:
            automatia.Inform(len(packages), "packages")
        automatia.Inform("|{:17s}|{:12s} @ {}".format('FriendlyName', 'Name', 'Path'))
        for p in packages:
            automatia.Inform("|\"{:16s}|\"{:11s} @ '{}'".format(p.m.FriendlyName() + '"', p.m.Name() + '"', p.pp))
    elif first_arg == "remove":
        args.remove("remove")
        packages = resolve.load_packages()
        for a in args:
            for p in packages:
                if p.m.Name() == a or p.m.FriendlyName() == a or p.pp == a:
                    resolve.perm_remove_package(p.pp)
                    automatia.Inform("Removed", p.pp)
                    break

    elif first_arg == "add":
        args.remove("add")
        resolve.load_packages()
        if len(args) == 1 and args[0] == "common":
            args = ["automatia.common.quickyt"]
        for a in args:
            m = resolve.load_package(a)
            if m is None:
                automatia.Warn(a, "is not a valid Automatia package, check debug with '-D' for technical details.")
            else:
                automatia.Inform("Added", a)
                resolve.add_package(a)
    else:
        automatia.Inform('Unknown parameter "{}"'.format(first_arg))
        print_help()
