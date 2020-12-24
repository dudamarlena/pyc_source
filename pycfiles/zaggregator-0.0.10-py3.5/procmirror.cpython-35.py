# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/procmirror.py
# Compiled at: 2018-07-31 09:40:39
# Size of source mod 2**32: 2959 bytes
import psutil, logging, os

class ProcessMirror:
    __doc__ = '\n        Class provides cachable and transparent copy of psutil.Process\n        with some fields overwritten to avoid direct calling of\n        psutil.Process methods, as they are inconsistent for dead processes\n\n    '

    def __init__(self, proc: psutil.Process, proctable):
        """
            Class constructor
        """
        _dead = False
        self._children = list()
        self._parent = 0
        parent = None
        self._proc, self._pt = proc, proctable
        try:
            self._pgid = os.getpgid(proc.pid)
        except Exception as e:
            self._pgid = 0
            _dead = True

        if not _dead:
            parent = proc.parent()
        if parent:
            self._parent = parent.pid
        if not _dead:
            self._children = [p.pid for p in proc.children()]
        with proc.oneshot():
            if proc.is_running():
                self.rss = proc.memory_info().rss
                self.vms = proc.memory_info().vms
                self.ctx_vol = proc.num_ctx_switches().voluntary
                self.ctx_invol = proc.num_ctx_switches().involuntary
                self._cmdline = proc.cmdline()
                self.pcpu = None
            else:
                self.rss = 0
                self.vms = 0
                self.ctx_vol = 0
                self.ctx_invol = 0
                self.cmdline = []
                self.pcpu = 0.0

    def __str__(self):
        return '<{} name={} pid={} _pgid={} alive={} >\n'.format(self.__class__.__name__, self.name(), self.pid, self._pgid, self.alive)

    def __repr__(self):
        return self.__str__()

    def __getattribute__(self, name: str):
        """
            Masquerade psutil.Process's fields and methods
        """
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            if name == 'alive':
                return self._proc.is_running()
            if name == 'pidm':

                def __wrapper(x):
                    try:
                        return self._pt.mirrors[x]
                    except KeyError:
                        return False

                return _ProcessMirror__wrapper
            if name == 'parent':
                return lambda : self.pidm(self._parent)
            if name == 'children':
                return lambda : [self.pidm(p) for p in self._children]
            if name == 'cmdline':
                return lambda : self._cmdline
            if hasattr(self._proc, name):
                return getattr(self._proc, name)
            return object.__getattribute__(self, name)

    def set_pcpu(self, value):
        """
            CPU percent values cannot be cached, so we need this
            trick to set it for all ProcessMirrors in one pass
        """
        self.pcpu = value