# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/statprof.py
# Compiled at: 2019-09-22 10:12:27
"""
statprof is intended to be a fairly simple statistical profiler for
python. It was ported directly from a statistical profiler for guile,
also named statprof, available from guile-lib [0].

[0] http://wingolog.org/software/guile-lib/statprof/

To start profiling, call statprof.start():
>>> start()

Then run whatever it is that you want to profile, for example:
>>> import test.pystone; test.pystone.pystones()

Then stop the profiling and print out the results:
>>> stop()
>>> display()
  %   cumulative      self
 time    seconds   seconds  name
 26.72      1.40      0.37  pystone.py:79:Proc0
 13.79      0.56      0.19  pystone.py:133:Proc1
 13.79      0.19      0.19  pystone.py:208:Proc8
 10.34      0.16      0.14  pystone.py:229:Func2
  6.90      0.10      0.10  pystone.py:45:__init__
  4.31      0.16      0.06  pystone.py:53:copy
    ...

All of the numerical data with the exception of the calls column is
statistically approximate. In the following column descriptions, and
in all of statprof, "time" refers to execution time (both user and
system), not wall clock time.

% time
    The percent of the time spent inside the procedure itself (not
    counting children).

cumulative seconds
    The total number of seconds spent in the procedure, including
    children.

self seconds
    The total number of seconds spent in the procedure itself (not
    counting children).

name
    The name of the procedure.

By default statprof keeps the data collected from previous runs. If you
want to clear the collected data, call reset():
>>> reset()

reset() can also be used to change the sampling frequency. For example,
to tell statprof to sample 50 times a second:
>>> reset(50)

This means that statprof will sample the call stack after every 1/50 of
a second of user + system time spent running on behalf of the python
process. When your process is idle (for example, blocking in a read(),
as is the case at the listener), the clock does not advance. For this
reason statprof is not currently not suitable for profiling io-bound
operations.

The profiler uses the hash of the code object itself to identify the
procedures, so it won't confuse different procedures with the same name.
They will show up as two different rows in the output.

Right now the profiler is quite simplistic.  I cannot provide
call-graphs or other higher level information.  What you see in the
table is pretty much all there is. Patches are welcome :-)

Threading
---------

Because signals only get delivered to the main thread in Python,
statprof only profiles the main thread. However because the time
reporting function uses per-process timers, the results can be
significantly off if other threads' work patterns are not similar to the
main thread's work patterns.

Implementation notes
--------------------

The profiler works by setting the unix profiling signal ITIMER_PROF to
go off after the interval you define in the call to reset(). When the
signal fires, a sampling routine is run which looks at the current
procedure that's executing, and then crawls up the stack, and for each
frame encountered, increments that frame's code object's sample count.
Note that if a procedure is encountered multiple times on a given stack,
it is only counted once. After the sampling is complete, the profiler
resets profiling timer to fire again after the appropriate interval.

Meanwhile, the profiler keeps track, via os.times(), how much CPU time
(system and user -- which is also what ITIMER_PROF tracks), has elapsed
while code has been executing within a start()/stop() block.

The profiler also tries to avoid counting or timing its own code as
much as possible.
"""
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