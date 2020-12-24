# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/statprof.py
# Compiled at: 2015-07-17 06:24:31
from __future__ import absolute_import, division, print_function, unicode_literals
import os, runpy, signal, sys
from collections import defaultdict
from contextlib import contextmanager
from six import moves, exec_, iteritems, itervalues
__all__ = [
 b'DisplayFormat', b'start', b'stop', b'reset', b'display', b'profile']

def clock():
    times = os.times()
    return times[0] + times[1]


class ProfileState(object):

    def __init__(self, frequency=None):
        self.profile_level = 0
        self.reset(frequency)

    def is_active(self):
        return self.profile_level > 0

    def reset(self, frequency=None):
        assert self.profile_level == 0, b"Can't reset() while statprof is running"
        self.accumulated_time = 0.0
        self.last_start_time = None
        self.sample_count = 0
        if frequency:
            self.sample_interval = 1.0 / frequency
        elif not hasattr(self, b'sample_interval'):
            self.sample_interval = 0.001
        self.remaining_prof_time = None
        self.profile_level = 0
        self.count_calls = False
        self.gc_time_taken = 0
        return

    def accumulate_time(self, stop_time):
        self.accumulated_time += stop_time - self.last_start_time

    def start(self):
        state.profile_level += 1
        if state.profile_level == 1:
            self.last_start_time = clock()
            rpt = self.remaining_prof_time
            self.remaining_prof_time = None
            signal.signal(signal.SIGPROF, profile_signal_handler)
            signal.setitimer(signal.ITIMER_PROF, rpt or self.sample_interval, 0.0)
            self.gc_time_taken = 0
        return

    def stop(self):
        assert self.profile_level > 0, b'statprof is not running'
        self.profile_level -= 1
        if self.profile_level == 0:
            self.accumulate_time(clock())
            self.last_start_time = None
            rpt = signal.setitimer(signal.ITIMER_PROF, 0.0, 0.0)
            signal.signal(signal.SIGPROF, signal.SIG_IGN)
            self.remaining_prof_time = rpt[0]
            self.gc_time_taken = 0
        return


state = ProfileState()

class CodeKey(object):
    cache = {}
    __slots__ = ('filename', 'lineno', 'name')

    def __init__(self, filename, lineno, name):
        self.filename = filename
        self.lineno = lineno
        self.name = name

    @classmethod
    def create_from_frame(cls, frame):
        code = frame.f_code
        return cls(code.co_filename, frame.f_lineno, code.co_name)

    def __eq__(self, other):
        try:
            return self.lineno == other.lineno and self.filename == other.filename and self.name == other.name
        except Exception:
            return False

    def __hash__(self):
        return hash((self.lineno, self.filename, self.name))

    def __repr__(self):
        return b'%s(%s)' % (
         self.__class__.__name__,
         (b', ').join(b'%r' % getattr(self, k) for k in self.__slots__))

    @classmethod
    def get(cls, frame):
        k = (frame.f_code.co_filename, frame.f_lineno)
        try:
            return cls.cache[k]
        except KeyError:
            v = cls.create_from_frame(frame)
            cls.cache[k] = v
            return v


class CallData(object):
    all_calls = {}
    __slots__ = ('key', 'call_count', 'cum_sample_count', 'self_sample_count')

    def __init__(self, key):
        """
        :type key: :class:`CodeKey`
        """
        self.key = key
        self.call_count = 0
        self.cum_sample_count = 0
        self.self_sample_count = 0

    @classmethod
    def get(cls, key):
        try:
            return cls.all_calls[key]
        except KeyError:
            v = CallData(key)
            cls.all_calls[key] = v
            return v


def sample_stack_procs(frame):
    state.sample_count += 1
    key = CodeKey.get(frame)
    CallData.get(key).self_sample_count += 1
    keys_seen = set()
    while frame:
        key = CodeKey.get(frame)
        keys_seen.add(key)
        frame = frame.f_back

    for key in keys_seen:
        CallData.get(key).cum_sample_count += 1


def profile_signal_handler(signum, frame):
    if state.profile_level > 0:
        state.accumulate_time(clock())
        sample_stack_procs(frame)
        signal.setitimer(signal.ITIMER_PROF, state.sample_interval, 0.0)
        state.last_start_time = clock()


def is_active():
    return state.is_active()


def start():
    """Install the profiling signal handler, and start profiling."""
    state.start()


def stop():
    """Stop profiling, and uninstall the profiling signal handler."""
    state.stop()


def reset(frequency=None):
    """Clear out the state of the profiler.  Do not call while the
    profiler is running.

    The optional frequency argument specifies the number of samples to
    collect per second."""
    state.reset(frequency)
    CallData.all_calls.clear()
    CodeKey.cache.clear()


@contextmanager
def profile():
    start()
    try:
        yield
    finally:
        stop()
        display()


class CallStats(object):

    def __init__(self, call_data):
        """
        :type call_data: :class:`CallData`
        """
        self_samples = call_data.self_sample_count
        cum_samples = call_data.cum_sample_count
        nsamples = state.sample_count
        secs_per_sample = state.accumulated_time / nsamples
        self.lineno = call_data.key.lineno
        self.filename = call_data.key.filename
        self.function = call_data.key.name
        self.pcnt_time_in_proc = self_samples / nsamples * 100
        self.cum_secs_in_proc = cum_samples * secs_per_sample
        self.self_secs_in_proc = self_samples * secs_per_sample
        self.num_calls = None
        self.self_secs_per_call = None
        self.cum_secs_per_call = None
        return


class DisplayFormat:
    BY_LINE = 0
    BY_METHOD = 1


class DisplayOrder:
    LOCAL = 0
    CUMULATIVE = 1


class PathFormat:
    FULL_PATH = 0
    FILENAME_ONLY = 1
    NO_FORMATTING = 2


def display(fp=None, format=DisplayFormat.BY_LINE, path_format=PathFormat.FULL_PATH, order=DisplayOrder.LOCAL):
    """Print statistics, either to stdout or the given file object.

    :type format: One of :class:`DisplayFormat.BY_*` constants
    :param all_paths_absolute: Print all the file names with full paths.
    """

    def p(whatever):
        print(whatever, file=fp)

    if fp is None:
        fp = sys.stdout
    if state.sample_count == 0:
        p(b'No samples recorded.')
        return
    else:
        stats = [ CallStats(x) for x in itervalues(CallData.all_calls) ]
        try:
            path_transformation = {PathFormat.FULL_PATH: os.path.abspath, PathFormat.FILENAME_ONLY: os.path.basename, 
               PathFormat.NO_FORMATTING: lambda path: path}[path_format]
        except KeyError:
            raise Exception(b'Invalid path format')
        else:
            for stat in stats:
                stat.filename = path_transformation(stat.filename)

            try:
                method = {DisplayFormat.BY_LINE: display_by_line, DisplayFormat.BY_METHOD: display_by_method}[format]
            except KeyError:
                raise Exception(b'Invalid display format')

        method(stats, fp, order)
        p(b'---')
        p(b'Sample count: %d' % state.sample_count)
        p(b'Total time: %f seconds' % state.accumulated_time)
        return


def display_by_line(stats, fp, order):
    """Print the profiler data with each sample line represented
    as one row in a table."""
    try:
        sort_key = {DisplayOrder.LOCAL: lambda x: x.self_secs_in_proc, 
           DisplayOrder.CUMULATIVE: lambda x: x.cum_secs_in_proc}[order]
    except KeyError:
        raise Exception(b'Invalid display order')

    stats.sort(reverse=True, key=sort_key)

    def p(whatever):
        print(whatever, file=fp)

    p(b'%5.5s %10.10s   %7.7s  %-8.8s' % ('%  ', 'cumulative', 'self', ''))
    p(b'%5.5s  %9.9s  %8.8s  %-8.8s' % ('time', 'seconds', 'seconds', 'name'))
    for x in stats:
        p(b'%6.2f %9.2f %9.2f  %s' % (
         x.pcnt_time_in_proc, x.cum_secs_in_proc, x.self_secs_in_proc,
         b'%s:%d:%s' % (x.filename, x.lineno, x.function)))


def get_line_source(filename, lineno):
    """Gets the line text for the line in the file."""
    lineno -= 1
    fp = None
    try:
        try:
            fp = open(filename)
            for i, line in enumerate(fp):
                if i == lineno:
                    return line

        except Exception:
            pass

    finally:
        if fp:
            fp.close()

    return b''


def display_by_method(stats, fp, order):
    """Print the profiler data with each sample function represented
    as one row in a table.  Important lines within that function are
    output as nested rows.  Sorted by self-time per line."""

    def p(whatever):
        print(whatever, file=fp)

    p(b'%5.5s %10.10s   %7.7s  %-8.8s' % ('%  ', 'cumulative', 'self', ''))
    p(b'%5.5s  %9.9s  %8.8s  %-8.8s' % ('time', 'seconds', 'seconds', 'name'))
    grouped = defaultdict(list)
    for call in stats:
        grouped[(call.filename + b':' + call.function)].append(call)

    functiondata = []
    for fname, samples in iteritems(grouped):
        total_cum_sec = 0
        total_self_sec = 0
        total_percent = 0
        for sample in samples:
            total_cum_sec += sample.cum_secs_in_proc
            total_self_sec += sample.self_secs_in_proc
            total_percent += sample.pcnt_time_in_proc

        functiondata.append((fname,
         total_cum_sec,
         total_self_sec,
         total_percent,
         samples))

    try:
        sort_key = {DisplayOrder.LOCAL: lambda x: x[2], DisplayOrder.CUMULATIVE: lambda x: x[1]}[order]
    except KeyError:
        raise Exception(b'Invalid display order')

    functiondata.sort(reverse=True, key=sort_key)
    for function in functiondata:
        p(b'%6.2f %9.2f %9.2f  %s' % (
         function[3],
         function[1],
         function[2],
         function[0]))
        function[4].sort(reverse=True, key=lambda i: i.self_secs_in_proc)
        for call in function[4]:
            if call.pcnt_time_in_proc > 1:
                source = get_line_source(call.filename, call.lineno).strip()
                if len(source) > 25:
                    source = source[:20] + b'...'
                p(b'%33.0f%% %6.2f   line %s: %s' % (
                 call.pcnt_time_in_proc,
                 call.self_secs_in_proc,
                 call.lineno,
                 source))


def main():
    """Run the given script under the profiler, when invoked as a module
    (python -m statprof ...), and display the profile report once done.
    """
    if not sys.argv[1:] or sys.argv[1] in ('--help', '-h'):
        print(b'usage: python -m statprof [-c cmd | -m mod | file] [<args>]')
        sys.exit(2)
    scriptfile = sys.argv[1]
    if scriptfile.startswith(b'-c'):
        del sys.argv[0]
        if scriptfile == b'-c':
            scriptfile = sys.argv[1]
            del sys.argv[1]
        else:
            scriptfile = scriptfile[2:]
            sys.argv[0] = b'-c'
        with profile():
            exec_(scriptfile, vars(moves.builtins))
    elif scriptfile.startswith(b'-m'):
        if scriptfile == b'-m':
            scriptfile = sys.argv[2]
            del sys.argv[1:3]
        else:
            scriptfile = scriptfile[2:]
            del sys.argv[1]
        with profile():
            runpy.run_module(scriptfile, run_name=b'__main__', alter_sys=True)
    else:
        del sys.argv[0]
        with profile():
            runpy.run_path(scriptfile, run_name=b'__main__')


if __name__ == b'__main__':
    import statprof
    statprof.main()