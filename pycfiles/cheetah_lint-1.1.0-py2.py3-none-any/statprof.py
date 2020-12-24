# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/statprof.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = '\nstatprof is intended to be a fairly simple statistical profiler for\npython. It was ported directly from a statistical profiler for guile,\nalso named statprof, available from guile-lib [0].\n\n[0] http://wingolog.org/software/guile-lib/statprof/\n\nTo start profiling, call statprof.start():\n>>> start()\n\nThen run whatever it is that you want to profile, for example:\n>>> import test.pystone; test.pystone.pystones()\n\nThen stop the profiling and print out the results:\n>>> stop()\n>>> display()\n  %   cumulative      self\n time    seconds   seconds  name\n 26.72      1.40      0.37  pystone.py:79:Proc0\n 13.79      0.56      0.19  pystone.py:133:Proc1\n 13.79      0.19      0.19  pystone.py:208:Proc8\n 10.34      0.16      0.14  pystone.py:229:Func2\n  6.90      0.10      0.10  pystone.py:45:__init__\n  4.31      0.16      0.06  pystone.py:53:copy\n    ...\n\nAll of the numerical data with the exception of the calls column is\nstatistically approximate. In the following column descriptions, and\nin all of statprof, "time" refers to execution time (both user and\nsystem), not wall clock time.\n\n% time\n    The percent of the time spent inside the procedure itself (not\n    counting children).\n\ncumulative seconds\n    The total number of seconds spent in the procedure, including\n    children.\n\nself seconds\n    The total number of seconds spent in the procedure itself (not\n    counting children).\n\nname\n    The name of the procedure.\n\nBy default statprof keeps the data collected from previous runs. If you\nwant to clear the collected data, call reset():\n>>> reset()\n\nreset() can also be used to change the sampling frequency. For example,\nto tell statprof to sample 50 times a second:\n>>> reset(50)\n\nThis means that statprof will sample the call stack after every 1/50 of\na second of user + system time spent running on behalf of the python\nprocess. When your process is idle (for example, blocking in a read(),\nas is the case at the listener), the clock does not advance. For this\nreason statprof is not currently not suitable for profiling io-bound\noperations.\n\nThe profiler uses the hash of the code object itself to identify the\nprocedures, so it won\'t confuse different procedures with the same name.\nThey will show up as two different rows in the output.\n\nRight now the profiler is quite simplistic.  I cannot provide\ncall-graphs or other higher level information.  What you see in the\ntable is pretty much all there is. Patches are welcome :-)\n\n\nThreading\n---------\n\nBecause signals only get delivered to the main thread in Python,\nstatprof only profiles the main thread. However because the time\nreporting function uses per-process timers, the results can be\nsignificantly off if other threads\' work patterns are not similar to the\nmain thread\'s work patterns.\n\n\nImplementation notes\n--------------------\n\nThe profiler works by setting the unix profiling signal ITIMER_PROF to\ngo off after the interval you define in the call to reset(). When the\nsignal fires, a sampling routine is run which looks at the current\nprocedure that\'s executing, and then crawls up the stack, and for each\nframe encountered, increments that frame\'s code object\'s sample count.\nNote that if a procedure is encountered multiple times on a given stack,\nit is only counted once. After the sampling is complete, the profiler\nresets profiling timer to fire again after the appropriate interval.\n\nMeanwhile, the profiler keeps track, via os.times(), how much CPU time\n(system and user -- which is also what ITIMER_PROF tracks), has elapsed\nwhile code has been executing within a start()/stop() block.\n\nThe profiler also tries to avoid counting or timing its own code as\nmuch as possible.\n'
try:
    import itimer
except ImportError:
    raise ImportError('statprof requires the itimer python extension.\nTo install it, enter the following commands from a terminal:\n\nwget http://www.cute.fi/~torppa/py-itimer/py-itimer.tar.gz\ntar zxvf py-itimer.tar.gz\ncd py-itimer\nsudo python setup.py install\n')

import signal, os
__all__ = [
 'start', 'stop', 'reset', 'display']

def clock():
    times = os.times()
    return times[0] + times[1]


class ProfileState(object):

    def __init__(self, frequency=None):
        self.reset(frequency)

    def reset(self, frequency=None):
        self.accumulated_time = 0.0
        self.last_start_time = None
        self.sample_count = 0
        if frequency:
            self.sample_interval = 1.0 / frequency
        elif not hasattr(self, 'sample_interval'):
            self.sample_interval = 1.0 / 100.0
        self.remaining_prof_time = None
        self.profile_level = 0
        self.count_calls = False
        self.gc_time_taken = 0
        return

    def accumulate_time(self, stop_time):
        self.accumulated_time += stop_time - self.last_start_time


state = ProfileState()
call_data = {}

class CallData(object):

    def __init__(self, code):
        self.name = code.co_name
        self.filename = code.co_filename
        self.lineno = code.co_firstlineno
        self.call_count = 0
        self.cum_sample_count = 0
        self.self_sample_count = 0
        call_data[code] = self


def get_call_data(code):
    return call_data.get(code, None) or CallData(code)


def sample_stack_procs(frame):
    state.sample_count += 1
    get_call_data(frame.f_code).self_sample_count += 1
    code_seen = {}
    while frame:
        code_seen[frame.f_code] = True
        frame = frame.f_back

    for code in code_seen:
        get_call_data(code).cum_sample_count += 1


def profile_signal_handler(signum, frame):
    if state.profile_level > 0:
        state.accumulate_time(clock())
        sample_stack_procs(frame)
        itimer.setitimer(itimer.ITIMER_PROF, state.sample_interval, 0.0)
        state.last_start_time = clock()


def is_active():
    return state.profile_level > 0


def start():
    state.profile_level += 1
    if state.profile_level == 1:
        state.last_start_time = clock()
        rpt = state.remaining_prof_time
        state.remaining_prof_time = None
        signal.signal(signal.SIGPROF, profile_signal_handler)
        itimer.setitimer(itimer.ITIMER_PROF, rpt or state.sample_interval, 0.0)
        state.gc_time_taken = 0
    return


def stop():
    state.profile_level -= 1
    if state.profile_level == 0:
        state.accumulate_time(clock())
        state.last_start_time = None
        rpt = itimer.setitimer(itimer.ITIMER_PROF, 0.0, 0.0)
        signal.signal(signal.SIGPROF, signal.SIG_IGN)
        state.remaining_prof_time = rpt[0]
        state.gc_time_taken = 0
    return


def reset(frequency=None):
    assert state.profile_level == 0, "Can't reset() while statprof is running"
    call_data.clear()
    state.reset(frequency)


class CallStats(object):

    def __init__(self, call_data):
        self_samples = call_data.self_sample_count
        cum_samples = call_data.cum_sample_count
        nsamples = state.sample_count
        secs_per_sample = state.accumulated_time / nsamples
        basename = os.path.basename(call_data.filename)
        self.name = '%s:%d:%s' % (basename, call_data.lineno, call_data.name)
        self.pcnt_time_in_proc = self_samples / nsamples * 100
        self.cum_secs_in_proc = cum_samples * secs_per_sample
        self.self_secs_in_proc = self_samples * secs_per_sample
        self.num_calls = None
        self.self_secs_per_call = None
        self.cum_secs_per_call = None
        return

    def display(self):
        print '%6.2f %9.2f %9.2f  %s' % (self.pcnt_time_in_proc,
         self.cum_secs_in_proc,
         self.self_secs_in_proc,
         self.name)


def display():
    if state.sample_count == 0:
        print 'No samples recorded.'
        return
    _l = [ CallStats(x) for x in call_data.values() ]
    _l = [ (x.self_secs_in_proc, x.cum_secs_in_proc, x) for x in _l ]
    _l.sort(reverse=True)
    _l = [ x[2] for x in _l ]
    print '%5.5s %10.10s   %7.7s  %-8.8s' % ('%  ', 'cumulative', 'self', '')
    print '%5.5s  %9.9s  %8.8s  %-8.8s' % ('time', 'seconds', 'seconds', 'name')
    for x in _l:
        x.display()

    print '---'
    print 'Sample count: %d' % state.sample_count
    print 'Total time: %f seconds' % state.accumulated_time