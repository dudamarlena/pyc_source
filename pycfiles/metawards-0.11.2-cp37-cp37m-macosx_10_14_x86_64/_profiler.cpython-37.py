# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_profiler.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 4037 bytes
import time
__all__ = [
 'Profiler', 'NullProfiler']

class NullProfiler:
    __doc__ = 'This is a null profiler that does nothing'

    def __init__(self, name: str=None, parent=None):
        pass

    def is_null(self) -> bool:
        return True

    def __str__(self):
        return 'No profiling data collected'

    def start(self, name: str=None):
        return self

    def stop(self):
        return self


class Profiler:
    __doc__ = 'This is a simple profiling class that supports manual\n       instrumenting of the code. It is used for sub-function\n       profiling.\n    '

    def __init__(self, name: str=None, parent=None):
        self._name = name
        self._parent = parent
        self._children = []
        self._start = None
        self._end = None

    def is_null(self) -> bool:
        """Return whether this is a null profiler"""
        return False

    def _to_string(self):
        """Used to write the results of profiling as a report"""
        lines = []
        t = self.total()
        if self._name is None:
            if self._parent is None:
                self._name = 'Total time'
        elif t:
            if len(self._children) > 0:
                ct = self.child_total()
                if ct:
                    lines.append('%s: %.3f ms (%.3f ms)' % (self._name, t, ct))
                else:
                    lines.append('%s: %.3f ms (???) ms' % (self._name, t))
            else:
                lines.append('%s: %.3f ms' % (self._name, t))
        elif self._start is None:
            lines.append(f"{self._name}")
        else:
            lines.append(f"{self._name}: still timing...")
        for child in self._children:
            clines = child._to_string()
            lines.append(f"  \\-{clines[0]}")
            if len(clines) > 1:
                for l in clines[1:]:
                    lines.append(f"    {l}")

        return lines

    def __str__(self):
        """Return the results of profiling as a report"""
        return '\n'.join(self._to_string())

    def name(self) -> str:
        """Return the name of this profiler"""
        return self._name

    def child_total(self) -> float:
        """Return the sum of time spent in the child profilers"""
        sum = None
        for child in self._children:
            t = child.total()
            if t is not None:
                if sum is None:
                    sum = t
                else:
                    sum += t

        return sum

    def total(self) -> float:
        """Return the amount of time that was recorded for this
           profiler in milliseconds (accurate to ~nanoseconds)
        """
        if self._parent is None:
            return self.child_total()
        if self._end:
            return (self._end - self._start) * 1e-06
        return

    def start(self, name: str):
        """Start profiling the section called 'name'. This
           returns the updated profiler, e.g.

           p = Profiler()

           p = p.start("long_loop")

           #\xa0run some code

           p = p.end()

           print(p)
        """
        p = Profiler(name=name, parent=self)
        self._children.append(p)
        p._start = time.time_ns()
        return p

    def stop(self):
        """Stop profiling. This records the end time
           and returns the parent profiler (if we have one)
        """
        end = time.time_ns()
        if self._start is None:
            print(f"WARNING: You cannot stop profiler {self._name} as it has not been started!")
        else:
            if self._end is not None:
                print(f"WARNING: You cannot stop profiler {self._name} as it has already been stopped!")
            else:
                self._end = end
        if self._parent:
            return self._parent
        return self