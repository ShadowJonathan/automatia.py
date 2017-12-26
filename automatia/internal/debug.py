import automatia


def debug(*message):
    if not automatia.CLI:
        d.Print(info=message)


class DebugDummy(automatia.AutomatiaModule):
    def Name(self):
        return "debug"

d = DebugDummy()
