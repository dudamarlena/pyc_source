# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/profiling.py
# Compiled at: 2009-10-07 18:08:46
"""Profiling support code"""
MAX_PROFILING_LINES_TO_PRINT = 30

def _helper_class(profiler_name):
    if profiler_name == 'hotshot':
        return HotshotHelper
    if profiler_name == 'profile':
        return ProfileHelper
    assert False


def profiling_decorator(profiler_name, filename):

    def decorator(callable):

        def wrapper(*args, **kwargs):
            helper = _helper_class(profiler_name)(filename, callable, *args, **kwargs)
            print "Profiling information saved to file '%s'" % helper.filename
            helper.run()
            helper.print_stats(MAX_PROFILING_LINES_TO_PRINT)
            return helper.result

        return wrapper

    return decorator


class ProfilingHelper(object):
    __module__ = __name__

    def __init__(self, filename, callable, *args, **kwargs):
        self.filename = filename
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.result = None
        return

    def print_stats(self, *args):
        self.stats().sort_stats('time').print_stats(*args)

    def run(self):
        raise NotImplementedError

    def stats(self):
        raise NotImplementedError


class HotshotHelper(ProfilingHelper):
    __module__ = __name__

    def run(self):
        import hotshot
        p = hotshot.Profile(self.filename)
        try:
            self.result = p.runcall(self.callable, *self.args, **self.kwargs)
        finally:
            p.close()

    def stats(self):
        from hotshot import stats
        try:
            return stats.load(self.filename)
        except hotshot.ProfilerError:
            raise IOError("Error reading stats from '%s', file may be corrupt" % filename)


class ProfileHelper(ProfilingHelper):
    __module__ = __name__

    def run(self):

        def run_callable():
            """A local function we can refer to in a string with profile.run"""
            self.result = self.callable(*self.args, **self.kwargs)

        try:
            from cProfile import Profile
        except ImportError:
            from profile import Profile

        self.p = Profile().runctx('run_callable()', globals(), locals())
        self.p.dump_stats(self.filename)

    def stats(self):
        import pstats
        return pstats.Stats(self.p)