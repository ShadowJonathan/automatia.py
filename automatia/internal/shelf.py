import automatia
from automatia.const.priority import After, Before, Gym, SleepOver
from automatia.const.state import *
from automatia.internal.param import Param
from automatia.internal.resolve import _Module

current_param = None


class Shelf(dict):
    def __init__(self):
        dict.__init__(self)
        self.triggers = {"before": [], "after": []}
        self._all = []
        self._names = []
        self._temp = {}
        self.y_cur = None
        self.x_cur = 0
        self._param = None

    # INIT

    def walk(self, modules):
        self._all = modules
        [m.init(self) for m in modules]
        self._names = [m.m.Name() for m in modules]
        [self.check_loop_after(m) for m in modules]
        [self.check_loop_before(m) for m in modules]
        self[SleepOver] = []
        self[Gym] = []
        for m in modules:
            self.shelf(m)
        automatia.Inform("Shelved and sorted {} modules.".format(len(modules)))

    def shelf(self, m):
        """
        :param _Module m:
        """
        p = m.p
        if self.get(p) is None:
            self[p] = []
        self[p].append(m)

    def set_param(self, param):
        global current_param
        self._param = param
        current_param = param

    def numkeys(self):
        return [r for r in reversed(sorted([k for k in self.keys() if isinstance(k, int)]))]

    # RESOLVE AND RUN

    def run(self, param):
        """
        :type param: Param
        """
        self.hardreset()
        self.set_param(param)
        while True:
            m = self.next()

            if m is None:
                automatia.Inform("Could not resolve", param.get())
                return

            try:
                self.do(m)
            except ReturnToMainLoop:
                continue

    def do(self, m):
        """:param _Module m:"""
        if m.ischecked():
            return

        automatia.Debug("Module:", m.m.FriendlyName())

        for a in m.a:
            automatia.Debug("[NEEDAFTER]", a)
            if not self.hasrun(a):
                return

        if self.trigger_before(m.m.Name()):
            self.innerloop(self.find_triggered_before(m.m.Name()), m.m.Name())

        r = m.check(self._param.get())

        if r:
            automatia.Debug("Running module", m, "with", self._param.get())
            automatia.Inform("Resolving", self._param.get(), 'with "{}"'.format(m.Name()))
            result = m.do(self._param.get())
            if not isinstance(result, State):
                automatia.Warn(m, "has returned an non-State object:", result)
                automatia.Warn("Automatia will now exit out of precaution")
                raise automatia.FinishFinal
            else:
                if isinstance(result, Finish):
                    raise automatia.FinishFinal
                elif isinstance(result, Result):
                    raise automatia.FinishResult(result.get(), m)
                elif isinstance(result, Continue):
                    return
                elif isinstance(result, Fail):
                    automatia.Error(m, "has returned a Fail")
                    automatia.Error(">", result.explain())
                    automatia.Error()
                    automatia.Error("Exiting...")
                    raise automatia.FinishNow
        else:
            if self.trigger_after(m.m.Name()):
                self.reset()
                raise ReturnToMainLoop

    def innerloop(self, modules=list(), name=""):
        for m in modules:
            automatia.Debug("[BEFORE]", m.m.Name(), "requested priority before", name)
            self.do(m)

    def hardreset(self):
        self.y_cur = None
        self.x_cur = 0
        [m.uncheck() for m in self._all]

    def reset(self):
        automatia.Debug("Reset Cursor")
        self.y_cur = None
        self.x_cur = 0

    def next(self):
        """:rtype: _Module|None"""
        if self.y_cur is None:
            self.y_cur = SleepOver

        l = self[self.y_cur]
        if len(l) < self.x_cur + 1:
            r = self.next_y()
            if r == Gym:
                return None
            else:
                return self.next()
        i = self.x_cur
        self.x_cur += 1
        return l[i]

    def next_y(self):
        nk = self.numkeys()
        self.x_cur = 0
        if self.y_cur == SleepOver:
            i = -1
        elif self.y_cur == Gym:
            return Gym
        else:
            i = nk.index(self.y_cur)
        if len(nk) > i + 1:
            self.y_cur = nk[i + 1]
        else:
            self.y_cur = Gym
        return None

    def hasrun(self, package):
        for m in self._all:
            automatia.Debug("[CHECKAGAINST]", m)
            if package.isafter(m.m.Name()):
                return m.ischecked()
        return package not in self._names

    # LOOP CHECKING

    def check_loop_after(self, m, temp_a=None, temp_b=None):
        """
        :param Optional[List[After]] temp_a: trail of followed packages this far
        :param Optional[List[Before]] temp_b: trail of packages that cannot be encountered,
        as they are prioritized the wrong way
        :param _Module m:
        """
        if m.a_ok:
            return
        if temp_a is None:
            temp_a = []
        else:
            temp_a = temp_a[:]

        if temp_b is None:
            temp_b = []
        else:
            temp_b = temp_b[:]

        if m.m.Name() in temp_a:
            raise DeadLockPrioritizationAfter(temp_a)
        elif m.m.Name() in temp_b:
            raise DeadLockPrioritizationAfter(temp_a)

        new = self.find_triggered_after(m)
        if len(new) == 0:
            [n.mark_after_ok() for n in temp_a]
            return
        else:
            temp_a.append(m)
            [temp_b.append(b) for b in self.find_triggered_before(m.m.Name())]

            for n in new:
                if n.a_ok:
                    continue
                try:
                    self.check_loop_after(n, temp_a, temp_b)
                except DeadLockPrioritizationAfter as dlpa:
                    [p.invalidate_prioritization_after() for p in dlpa.packages]
                    automatia.Warn("CLA DEADLOCK in module", n.m.Name(), "referencing after-prioritisation to an "
                                                                         "earlier module")
                    automatia.Warn("all modules in this chain will lose specific prioritisation")
                except DeadLockPrioritizationBefore as dlpb:
                    [p.invalidate_prioritization_before() for p in dlpb.packages]
                    automatia.Warn("CLA DEADLOCK in module", n.m.Name(),
                                   "being before-prioritized by an earlier module")
                    automatia.Warn("all modules in this chain will lose specific prioritisation")

    def check_loop_before(self, m, temp_b=None, temp_a=None):
        """
        :param Optional[List[Before]] temp_b: trail of followed packages this far
        :param Optional[List[After]] temp_a: trail of packages that cannot be encountered,
        as they are prioritized the wrong way
        :param _Module m:
        """
        if m.b_ok:
            return
        if temp_a is None:
            temp_a = []
        else:
            temp_a = temp_a[:]

        if temp_b is None:
            temp_b = []
        else:
            temp_b = temp_b[:]

        if m.m.Name() in temp_a:
            raise DeadLockPrioritizationAfter(temp_b)
        elif m.m.Name() in temp_b:
            raise DeadLockPrioritizationAfter(temp_b)

        new = self.find_triggered_before(m)
        if len(new) == 0:
            [n.mark_before_ok() for n in temp_a]
            return
        else:
            temp_b.append(m)
            [temp_a.append(a) for a in self.find_triggered_after(m.m.Name())]

            for n in new:
                if n.b_ok:
                    continue
                try:
                    self.check_loop_after(n, temp_a, temp_b)
                except DeadLockPrioritizationBefore as dlpb:
                    [p.invalidate_prioritization_before() for p in dlpb.packages]
                    automatia.Warn("CLB DEADLOCK in module", n.m.Name(),
                                   "being before-prioritized by an earlier module")
                    automatia.Warn("all modules in this chain will lose specific prioritisation")
                except DeadLockPrioritizationAfter as dlpa:
                    [p.invalidate_prioritization_after() for p in dlpa.packages]
                    automatia.Warn("CLB DEADLOCK in module", n.m.Name(), "referencing after-prioritisation to an "
                                                                         "earlier module")
                    automatia.Warn("all modules in this chain will lose specific prioritisation")

    def trigger_after(self, package):
        return package in self.triggers["after"]

    def trigger_before(self, package):
        return package in self.triggers["before"]

    def register_triggers(self, after, before):
        """
        :param list[After] after:
        :param list[Before] before:
        """

        automatia.Debug("register_triggers:", after, before)

        for a in after:
            if a.after not in self.triggers["after"]:
                self.triggers["after"].append(a.after)

        for b in before:
            if b.before not in self.triggers["before"]:
                self.triggers["before"].append(b.before)

    def find_triggered_before(self, package):
        found = []
        for m in self._all:
            if m.before_prioritized(package):
                found.append(m)
        return found

    def find_triggered_after(self, package):
        found = []
        for m in self._all:
            if m.after_prioritized(package):
                found.append(m)
        return found


class DeadLockPrioritizationAfter(Exception):
    def __init__(self, packages):
        self.packages = packages


class DeadLockPrioritizationBefore(Exception):
    def __init__(self, packages):
        self.packages = packages


class ReturnToMainLoop(Exception):
    pass
