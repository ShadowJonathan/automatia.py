from __future__ import print_function

import sys

import automatia
import automatia.const.priority as priority
from automatia.const.state import State, Continue


# Bad practice: load everything in imports at the beginning of the file
# Good practice: limit imports to checking if can download URL, have everything import at processing


class AutomatiaModule:
    # Overwritables

    def Match(self, url):
        """Returns True when this module can process `url`"""
        automatia.Warn("[NOTIMPLEMENTED] module", self.Name(), " has not implemented Match(), skipping...")
        return False

    def Name(self):
        """Returns the name of the module"""
        automatia.Warn("[NOTIMPLEMENTED] module has not implemented Name(), skipping...")
        return "undefined"

    def FriendlyName(self):
        """Returns a friendly, human-readable name, or the package name"""
        return self.Name()

    def Priority(self):
        """Give a number, or use SleepOver/Gym:

        SleepOver: Basically the same effect as when someone has slept in a sleeping bag in front of a store; you'll
        be first.

        Gym: Did you ever have that gym period where teams were picked, and you were picked last? This is what this
        does, if no other Modules could process the url, it'll go through modules that picked this priority.

        Use priority.after("package1", "package2"...) to make sure this package executes after other packages,
        if downloaded. Note: Circular resolves will invalidate that chain, and display a warning.
        :rtype: tuple[int|priority.After|priority.Before|string]|int|priority.After|priority.Before|string
        """
        return priority.Gym

    def Do(self, URL):
        """
        Straightforward, is called once this module can process the url.
        :param string URL:
        :rtype: State
        """
        automatia.Warn("[NOTIMPLEMENTED] module", self.Name(), " has not implemented Do(), skipping...")
        return Continue()

    # Funcs

    def __init__(self):
        pass

    def Print(self, *message, **kwargs):
        """Please use this command when printing information"""

        print("{}[\"{}\"] ".format(kwargs.get("beginning") or "", self.FriendlyName()) + " ".join([str(i) for i in message]),
                       end=kwargs.get("end") or "\n")
        sys.stdout.flush()

    def resolve_priority(self):
        result = self.Priority()
        if not isinstance(result, tuple):
            result = (result,)

        p_num = 0
        a = []
        b = []

        automatia.Debug(self.Name(), "priority output:", result)

        for r in result:
            if isinstance(r, (int, str)):
                p_num = r
            elif isinstance(r, priority.After):
                if r.multi:
                    [a.append(A) for A in r.after]
                else:
                    a.append(r)
            elif isinstance(r, priority.Before):
                if r.multi:
                    [b.append(B) for B in r.before]
                else:
                    b.append(r)
            else:
                automatia.Warn("found unknown type", type(r), "from module", self.Name(), "while resolving "
                                                                                          "priorities.")
        return p_num, a, b
