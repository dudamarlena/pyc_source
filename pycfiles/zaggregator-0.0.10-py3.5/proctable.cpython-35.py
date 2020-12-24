# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/proctable.py
# Compiled at: 2018-08-01 07:13:33
# Size of source mod 2**32: 4777 bytes
import psutil, logging, time
from zaggregator.procmirror import ProcessMirror
from zaggregator.procbundle import ProcBundle
from zaggregator.config import DEFAULT_INTERVAL, metrics

class ProcTable:
    __doc__ = '\n        Class represents cached process table for the sampling period\n    '

    def __init__(self):
        self._procs = []
        _pcs = list(psutil.process_iter())
        list(map(self._procs.append, map(ProcessMirror, _pcs, len(_pcs) * [self])))
        [process_call_guard(p.cpu_percent) for p in self._procs]
        time.sleep(DEFAULT_INTERVAL)
        pcpu = [process_call_guard(p.cpu_percent) for p in self._procs]
        list(map(lambda a, b: a.set_pcpu(b), self._procs, pcpu))
        self.mirrors = {}
        for p in self._procs:
            self.mirrors.setdefault(p.pid, p)

        self.bundles = []
        self._expendable = list(self._procs)
        pgids = list(set([p._pgid for p in self._procs]))
        mirrors_by_pgid = list(map(self.mirrors_by_pgid, pgids))
        mirrors_by_pgid.sort(key=lambda x: len(x), reverse=True)
        while len(self._expendable) > 0:
            for ms in mirrors_by_pgid:
                self.bundles.append(ProcBundle(ms, pt=self))
                self._clear_expendable()

        uniq_names = list(set(self.get_bundle_names()))
        for name in uniq_names:
            n = self._get_bundles_by_name(name)
            for b in n[1:]:
                n[0].merge(b)

    def _clear_expendable(self):
        """ Clean up expendable processes list from bundled processes """
        list(map(lambda p: self._expendable.remove(p) if p in self.bundled() and p in self._expendable else None, self._expendable))

    def mirrors_by_pgid(self, pgid: int) -> [ProcessMirror]:
        """ Returns ProcessMirrors by Process Group ID (pgid) """
        return list(filter(lambda x: x._pgid == pgid, self._procs))

    def mirror_by_pid(self, pid: int) -> ProcessMirror:
        """ Returns ProcessMirrors by process pid """
        if pid in self.mirrors.keys():
            return self.mirrors[pid]
        else:
            return

    def bundled(self) -> list:
        """
            Returns list of all ProcessMirrors in all registered ProcBundles
        """
        ret = []
        for b in self.bundles:
            ret.extend(b.proclist)

        return ret

    def get_bundle_names(self) -> list:
        """
            Returns list of names of registered ProcBundles
        """
        return [b.bundle_name for b in self.bundles]

    def _get_bundles_by_name(self, name: str):
        """
            Returns list of all registered bundles with the same name. In the
            normal state there shouldn't be any duplicates in the regisered
            Procbundle, so we need to get all the names to merge ProcBundles
            with similar names. Should't be called outside of ProcTable internal
            context.
        """
        if name in self.get_bundle_names():
            return list(filter(lambda x: x.bundle_name == name, self.bundles))

    def get_bundle_by_name(self, name: str):
        """
            Returns ProcBundle with desired name or None for non-existing bundles
        """
        if name in self.get_bundle_names():
            return list(filter(lambda x: x.bundle_name == name, self.bundles))[0]

    def get_idle(self, interval=DEFAULT_INTERVAL):
        """
            TODO: refactor this
        """
        return psutil.cpu_times_percent(interval=interval).idle

    def get_top_5s(self) -> [
 ProcBundle]:
        """
            Get top10 bundles by each of the metrics and return list of bundles
        """
        tops = []
        for m in metrics:
            func = lambda b: b.__getattribute__(m)
            tops.extend(sorted(self.bundles, key=func, reverse=True)[:5])

        return list(set(tops))


def process_call_guard(func, *args, **kwargs):
    """ Singleton to handle situation when process died
        after registering, but before sampling """
    try:
        return func(*args, **kwargs)
    except psutil.NoSuchProcess:
        return False