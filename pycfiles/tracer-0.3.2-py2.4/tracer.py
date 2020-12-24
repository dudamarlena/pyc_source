# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracer.py
# Compiled at: 2013-03-24 03:33:01
"""Centralized Trace management around sys.settrace. We allow several
sets of trace events to get registered and unregistered. We allow
certain functions to be registered to be not traced. We allow tracing
to be turned on and off temporarily without losing the trace
functions.
"""
import operator, sys, inspect, threading, types

def superTuple(typename, *attribute_names):
    """ create and return a subclass of `tuple', with named attributes """
    nargs = len(attribute_names)

    class supertup(tuple):
        __module__ = __name__
        __slots__ = ()

        def __new__(cls, *args):
            if len(args) != nargs:
                raise TypeError('%s takes exactly %d arguments (%d given)' % (typename, nargs, len(args)))
            return tuple.__new__(cls, args)

        def __repr__(self):
            return '%s(%s)' % (typename, (', ').join(map(repr, self)))

    for (index, attr_name) in enumerate(attribute_names):
        setattr(supertup, attr_name, property(operator.itemgetter(index)))

    supertup.__name__ = typename
    return supertup


Trace_entry = superTuple('Trace_entry', 'trace_fn', 'event_set', 'ignore_frameid')
HOOKS = []
STARTED_STATE = False
ALL_EVENT_NAMES = ('c_call', 'c_exception', 'c_return', 'call', 'exception', 'line',
                   'return')
EVENT2SHORT = {'c_call': 'C>', 'c_exception': 'C!', 'c_return': 'C<', 'call': '->', 'exception': '!!', 'line': '--', 'return': '<-'}
ALL_EVENTS = frozenset(ALL_EVENT_NAMES)
TRACE_SUSPEND = False
debug = False

def null_trace_hook(frame, event, arg):
    """A trace hook that doesn't do anything. Can use this to "turn off"
    tracing by setting frame.f_trace. Setting sys.settrace(None) sometimes
    doesn't work...
    """
    pass


def check_event_set(event_set):
    """Check `event_set' for validity. Raise TypeError if not valid."""
    if event_set is not None and not event_set.issubset(ALL_EVENTS):
        raise TypeError('event set is neither None nor a subset of ALL_EVENTS')
    return


def find_hook(trace_fn):
    """Find `trace_fn' in `hooks', and return the index of it.
    return None is not found."""
    global HOOKS
    try:
        i = [ entry.trace_fn for entry in HOOKS ].index(trace_fn)
    except ValueError:
        return

    return i


def option_set(options, value, default_options):
    if not options:
        return default_options.get(value)
    elif value in options:
        return options[value]
    else:
        return default_options.get(value)
    return


def _tracer_func(frame, event, arg):
    """The internal function set by sys.settrace which runs
    all of the user-registered trace hook functions."""
    global TRACE_SUSPEND
    global debug
    if debug:
        print '%s -- %s:%d' % (event, frame.f_code.co_filename, frame.f_lineno)
    if TRACE_SUSPEND:
        return _tracer_func
    tracer_func_frame = inspect.currentframe()
    for i in range(len(HOOKS)):
        hook = HOOKS[i]
        if hook.ignore_frameid == id(frame):
            continue
        if hook.event_set is None or event in hook.event_set:
            if not hook.trace_fn(frame, event, arg):
                HOOKS[i] = Trace_entry(hook.trace_fn, hook.event_set, id(frame))

    return _tracer_func


DEFAULT_ADD_HOOK_OPTS = {'position': -1, 'start': False, 'event_set': ALL_EVENTS, 'backlevel': 0}

def add_hook(trace_fn, options=None):
    """Add _trace_fn_ to the list of callback functions that get run
    when tracing is turned on. The number of hook functions
    registered is returned.

    A check is made on _trace_fn_ to make sure it is a function
    which takes 3 parameters: a _frame_, an _event_, and an arg which
    sometimes arg is _None_.

    _options_ is a dictionary having potential keys: _position_, _start_,
    _event_set_, and _backlevel_.

    If the event_set option-key is included, it should be is an event
    set that trace_fn will get run on. Use _set()_ or _frozenset()_ to
    create this set. ALL_EVENT_NAMES is a tuple contain a list of
    the event names. ALL_EVENTS is a frozenset of these.

    _position_ is the index of where the hook should be place in the
    list, so 0 is first and -1 _after_ is last item; the default is
    the very back of the list (-1). -2 is _after_ the next to last
    item.

    _start_ is a boolean which indicates the hooks should be started
    if they aren't already.

    _backlevel_ is an integer indicates that the calling should
    continue backwards in return call frames and is the number of
    levels to skip ignore. 0 means that the caller of add_hook() is
    traced as well as all new frames the caller subsequently calls. 1
    means that all the caller of _add_hook()_ is ignored but prior
    parent frames are traced, and None means that no previous parent
    frames should be traced.
    """
    if inspect.ismethod(trace_fn):
        argcount = 4
    elif inspect.isfunction(trace_fn):
        argcount = 3
    else:
        raise TypeError('trace_fn should be something isfunction() or ismethod() blesses')
    try:
        if hasattr(trace_fn, 'func_code'):
            code = trace_fn.func_code
        elif hasattr(trace_fn, '__code__'):
            code = trace_fn.__code__
        else:
            raise TypeError('trace fn %s should should have a func_code or __code__ attribute', repr(trace_fn))
        if argcount != code.co_argcount:
            raise TypeError('trace fn %s should take exactly %d arguments (takes %d)' % (repr(trace_fn), argcount, trace_fn.__code__.co_argcount))
    except:
        raise TypeError

    get_option = lambda key: option_set(options, key, DEFAULT_ADD_HOOK_OPTS)
    event_set = get_option('event_set')
    check_event_set(event_set)
    ignore_frame = inspect.currentframe()
    backlevel = get_option('backlevel')
    if backlevel is not None:
        if int != type(backlevel):
            raise TypeError('backlevel should be an integer type, is %s' % backlevel)
        frame = ignore_frame
        while frame and backlevel >= 0:
            backlevel -= 1
            frame = frame.f_back

        while frame:
            frame.f_trace = _tracer_func
            frame = frame.f_back

    entry = Trace_entry(trace_fn, event_set, ignore_frame)
    position = get_option('position')
    if position == -1:
        HOOKS.append(entry)
    else:
        if position < -1:
            position += 1
        HOOKS[position:position] = [
         entry]
    if get_option('start'):
        start()
    return len(HOOKS)


def clear_hooks():
    """Clear all trace hooks."""
    global HOOKS
    HOOKS = []


def clear_hooks_and_stop():
    """ clear all trace hooks and stop tracing """
    global STARTED_STATE
    if STARTED_STATE:
        stop()
    clear_hooks()


def size():
    """Returns the number of trace hooks installed, an integer."""
    return len(HOOKS)


def is_started():
    """Returns _True_ if tracing has been started. Until we assume Python 2.6
    or better, keeping track is done by internal tracking. Thus calls to
    sys.settrace outside of Tracer won't be detected.(
    """
    return STARTED_STATE


def remove_hook(trace_fn, stop_if_empty=False):
    """Remove `trace_fn' from list of callback functions run when
    tracing is turned on. If `trace_fn' is not in the list of
    callback functions, None is returned. On successful
    removal, the number of callback functions remaining is
    returned."""
    i = find_hook(trace_fn)
    if i is not None:
        del HOOKS[i]
        if 0 == len(HOOKS) and stop_if_empty:
            stop()
            return 0
        return len(HOOKS)
    return


DEFAULT_START_OPTS = {'trace_fn': None, 'add_hook_opts': DEFAULT_ADD_HOOK_OPTS, 'include_threads': False}

def start(options=None):
    """Start using all previously-registered trace hooks. If
    _options[trace_fn]_ is not None, we'll search for that and add it, if it's
    not already added."""
    global STARTED_STATE
    get_option = lambda key: option_set(options, key, DEFAULT_START_OPTS)
    trace_fn = get_option('trace_fn')
    if trace_fn is not None:
        add_hook(trace_fn, get_option('add_hook_opts'))
    if get_option('include_threads'):
        threading.settrace(_tracer_func)
    if sys.settrace(_tracer_func) is None:
        STARTED_STATE = True
        return len(HOOKS)
    if trace_fn is not None:
        remove_hook(trace_fn)
    raise NotImplementedError("sys.settrace() doesn't seem to be implemented")
    return


def stop():
    """Stop all trace hooks"""
    global STARTED_STATE
    if sys.settrace(None) is None:
        STARTED_STATE = False
        return len(HOOKS)
    raise NotImplementedError("sys.settrace() doesn't seem to be implemented")
    return


if __name__ == '__main__':
    t = list(EVENT2SHORT.keys())
    t.sort()
    print 'EVENT2SHORT.keys() == ALL_EVENT_NAMES: %s' % (tuple(t) == ALL_EVENT_NAMES)
    trace_count = 10
    import tracefilter
    ignore_filter = tracefilter.TraceFilter([find_hook, stop, remove_hook])

    def my_trace_dispatch(frame, event, arg):
        global ignore_filter
        global trace_count
        if ignore_filter.is_included(frame):
            return
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        s = '%s - %s:%d' % (event, filename, lineno)
        if 'call' == event:
            s += ', %s()' % frame.f_code.co_name
        if arg:
            print '%s arg %s' % (s, arg)
        else:
            print s
        if trace_count > 0:
            trace_count -= 1
            return my_trace_dispatch
        else:
            print 'Max trace count reached - turning off tracing'
            return
        return


    def foo():
        print 'foo'


    print '** Tracing started before start(): %s' % is_started()
    start()
    print '** Tracing started after start(): %s' % is_started()
    add_hook(my_trace_dispatch)
    eval('1+2')
    stop()
    y = 5
    start()
    foo()
    z = 5
    for i in range(6):
        print i

    trace_count = 25
    remove_hook(my_trace_dispatch, stop_if_empty=True)
    print '** Tracing started: %s' % is_started()
    print "** Tracing only 'call' now..."
    add_hook(my_trace_dispatch, {'start': True, 'event_set': frozenset(('call', ))})
    foo()
    stop()
    exit(0)