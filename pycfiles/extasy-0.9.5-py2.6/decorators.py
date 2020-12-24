# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\decorators.py
# Compiled at: 2010-11-20 06:10:24
import extasy, pycukes, pyhistorian, sys
_extasy_hooks = {'StartTest': [], 'EndTest': []}

def extasy_decorator__init__(self, *args):
    self._messages = [ extasy.lang.get(message) for message in args ]
    self._args = ()
    self._context = sys._getframe(1)
    self._set_step_attrs(self._context.f_locals)
    step = self.__class__.name
    self._steps = self._context.f_locals[('_%ss' % step)]
    for message in self._messages:
        self._steps.append((None, message, self._args))

    return


def extasy_decorator__call__(self, method=None):
    for message in self._messages:
        del self._steps[-1]

    for message in self._messages:
        self._steps.append((method, message, self._args))

    return method


Given = type('Given', (pycukes.Given,), {'__init__': extasy_decorator__init__, '__call__': extasy_decorator__call__})
When = type('When', (pycukes.When,), {'__init__': extasy_decorator__init__, '__call__': extasy_decorator__call__})
Then = type('Then', (pycukes.Then,), {'__init__': extasy_decorator__init__, '__call__': extasy_decorator__call__})

def StartTest(f):
    global _extasy_hooks
    _extasy_hooks['StartTest'].append(f)
    return f


def EndTest(f):
    _extasy_hooks['EndTest'].append(f)
    return f


def execute_hooks(name):
    extasy.scope.reset()
    for f in _extasy_hooks[name]:
        f(extasy)


class BeforeScenario(pyhistorian.Step):
    name = 'before_each'

    def __init__(self, title, *args):
        self._title_to_run = title
        self._args = args
        self._context = sys._getframe(1)
        self._set_step_attrs(self._context.f_locals)
        step = self.__class__.name
        self._steps = self._context.f_locals[('_%ss' % step)]

    def __call__(self, f):

        def wrapped(context, *args, **kwargs):
            if context.title == self._title_to_run:
                return f(context, *args, **kwargs)

        self._message = wrapped
        self._steps.append((None, self._message, self._args))
        return wrapped


class AfterScenario(BeforeScenario):
    name = 'after_each'