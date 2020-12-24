# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/dectools.py
# Compiled at: 2013-11-12 16:48:22
import sys, traceback, pdb
from classtools import assign_to_self
from functools import update_wrapper
import time

class keep_trying(object):

    def __init__(self, errors=(
 Exception,), try_time=1, wait_time=0.002, errorcall=None):
        assign_to_self(self, locals())

    def __call__(self, function):

        def decorated_function(*args, **kwargs):
            start = time.time()
            before = start - (self.wait_time + 1)
            test_condition = True
            while test_condition:
                try:
                    tosleep = self.wait_time - (time.time() - before)
                    if tosleep > 0:
                        time.sleep(tosleep)
                    before = time.time()
                    return function(*args, **kwargs)
                except Exception as E:
                    if not issubclass(type(E), self.errors):
                        raise E
                    if self.errorcall:
                        self.errorcall(E, *args, **kwargs)

                test_condition = time.time() - start < self.try_time

            raise E

        update_wrapper(decorated_function, function)
        return decorated_function


class IgnoreExceptions(object):
    """
    Inputs:
        errors: list/tuple of exceptions to ignore
        errorreturn: value which should be returned on ignored exception
        errorcall: function which should be called on ignored exception.  Consider
        using standardErrCall, which is in this module.
    Returns:
        returns standard function return if no error, otherwise returns errorreturn

    common usage:
    @IgnoreExceptions([ZeroDivisionError], errorreturn = -1)
    def divide(x):
        return 1.0 / x
    >>> divide(4)
    0.25
    >>> divide(0)
    -1
    """

    def __init__(self, errors, errorreturn=None, errorcall=None):
        self.errors = tuple(errors)
        self.errorreturn = errorreturn
        self.errorcall = errorcall

    def __call__(self, function):

        def decorated_function(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as E:
                if not issubclass(type(E), self.errors):
                    raise E
                if self.errorcall is not None:
                    self.errorcall(E, *args, **kwargs)
                return self.errorreturn

            return

        update_wrapper(decorated_function, function)
        return decorated_function


def getStdErrOut(E, *args, **kwargs):
    printed = 'Exception Skipped: ' + str(E) + '\n'
    if len(args) > 0:
        printed += 'args:    ' + str(args)[1:-1] + '\n'
    if len(kwargs) > 0:
        printed += 'kwargs: ' + str(kwargs)[1:-1] + '\n'
    if len(args) == 0 and len(kwargs) == 0:
        printed += 'No Arguments\n'
    else:
        if len(printed) < 500:
            return printed
        else:
            return printed[:500]


def getStandardErrorOut(*args, **kwargs):
    return getStdErrOut(*args, **kwargs)


def standardErrCall(E, *args, **kwargs):
    """
    @IgnoreExceptions([Exception],errorcall = standardErrCall(log)
    prints the passed exception information and the args + kwargs received.
    prints a maximum of 500 characters"""
    traceback.print_tb(sys.exc_info()[2])
    print getStdErrOut(E, *args, **kwargs)
    print ''


def pdbErrorCall(E, *args, **kwargs):
    traceback.print_tb(sys.exc_info()[2])
    print E
    tb = sys.exc_info()[2]
    pdb.post_mortem(tb)


def standard_error_call(*args, **kwargs):
    """
    @IgnoreExceptions([Exception],errorcall = standard_error_call)
    """
    return standardErrCall(*args, **kwargs)


class standardExceptionLog(object):
    """ common usage:
    @IgnoreExceptions([Exception],errorcall = standardExceptionLog(log))
    """

    def __init__(self, log):
        self.log = log

    def __call__(self, E, *args, **kwargs):
        self.log.exception(getStdErrOut(E, *args, **kwargs))


def pdb_on_exception(function):
    """decorates function to go to pdb when there is an exception.  Consider
    importing exceptDebug instead"""

    def decorated_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as E:
            traceback.print_tb(sys.exc_info()[2])
            print E
            tb = sys.exc_info()[2]
            pdb.post_mortem(tb)

    update_wrapper(decorated_function, function)
    return decorated_function


class debug(object):

    def __init__(self, DEBUG):
        self.DEBUG = DEBUG

    def __call__(self, function):
        if self.DEBUG:
            return pdb_on_exception(function)
        else:
            return function


class ensure_delay(object):
    """decorator function to ensure that the member functions decorated
    will not execute before delay is done

    Note: this is intended to be used with a class, where you want to
    ensure delay between different member functions.  Some functions
    may need a different delay than other functions.  One use case would
    be for I/O opperation with equipment -- perhaps you want to ensure that
    there is some delay before certian functions are executed.  This will
    do that, and keep track of all times across other decorated functions."""

    def __init__(self, delay, sleep_time=0.05, debug=False):
        self.delay = delay
        self.sleep_time = sleep_time
        self.debug = debug

    def __call__(self, function):

        def decorated_function(*args, **kwargs):
            parent = args[0]
            try:
                time_since_last = time.time() - parent.__last_time
            except AttributeError:
                time_since_last = time.time() - self.delay - 1

            while time_since_last < self.delay:
                time.sleep(self.sleep_time)
                time_since_last = time.time() - parent.__last_time

            parent.__last_time = time.time()
            out = function(*args, **kwargs)
            if self.debug:
                print time.time(), time_since_last
            return out

        update_wrapper(decorated_function, function)
        return decorated_function


def makelog(function):
    log = 'hello'
    function.log = log

    def returnfunction(*args, **kwargs):
        return function(*args, **kwargs)

    return returnfunction


class keeptime(object):
    """
    keeps amount of time spent executing function in self.time (cumlative)
    """

    def __init__(self):
        self.time = 0

    def __call__(self, function):

        def decorated_function(*args, **kwargs):
            start = time.time()
            out = function(*args, **kwargs)
            self.time += time.time() - start
            return out

        update_wrapper(decorated_function, function)
        decorated_function.time_keeper = self
        return decorated_function


class force_iter(object):
    """
    Can force any number of inputs to be iterators.
    Useful if you want your function to be able to handle either single inputs
    or list-like inputs.
    inputs = None        : converts all inputs to iterators
    inputs = n           : converts the first n inputs to iterators
                              ignores excess inputs
                              also ignores keyword inputs
                              first input is 1 !!!
                              Does not accept inputs <= 0
    inputs = iterable     : converts the inputs defined into iterators
                              ignores excess inputs
                              use strings to specify key word arguments

    example:
        @force_iter(2)
        def myfunction(x, y, z, d):
             pass # do stuff

        x and y will allways have the __iter__ atribute, z and d will be whatever
        they were originally

    """

    def __init__(self, inputs=None):
        self.inputs = inputs

    def __call__(self, function):

        def returnfunction(*args, **kwargs):
            args = list(args)
            if self.inputs == None:
                for i, n in enumerate(args):
                    if '__iter__' not in dir(n):
                        args[i] = (
                         n,)

                for key, item in kwargs.items():
                    if '__iter__' not in dir(item):
                        kwargs[key] = (
                         item,)

            elif type(self.inputs) == int:
                if len(args) < len(self.inputs):
                    count = len(args)
                for i in xrange(count):
                    if '__iter__' not in args[i]:
                        args[i] = (
                         args[i],)

            elif '__iter__' in dir(self.inputs):
                for check in self.inputs:
                    if type(check) == int:
                        if check <= 0:
                            raise ValueError('an element was less than 0')
                        if check <= len(args):
                            if '__iter__' not in dir(args[(check - 1)]):
                                args[check - 1] = (
                                 args[(check - 1)],)
                    elif kwargs.has_key(check):
                        if '__iter__' not in dir(kwargs[check]):
                            kwargs[check] = (
                             kwargs[check],)

            else:
                raise ValueError('Invalid inputs into force_iter' + str(self.inputs))
            return function(*args, **kwargs)

        return returnfunction


@makelog
def xyz(x, y, z):
    print x, y, z
    print 'printing log', log


def dev1():

    @IgnoreExceptions([ZeroDivisionError], errorreturn=-1)
    def divide(x):
        return 1.0 / x

    @IgnoreExceptions([ValueError], errorcall=standardErrCall)
    def doexception(*args, **kwargs):
        return float('slkdjf')

    doexception()
    doexception(1, 2, 3, 5, answer='42', variable='foo')

    @pdb_on_exception
    def testingpdb():
        a = 'this is a'
        x = 1 / 0
        print x

    class testingclass(object):

        @IgnoreExceptions([ZeroDivisionError], errorreturn=-1)
        def test(self):
            print 1 / 0

    t = testingclass()
    t.test()
    time.sleep(1)


def dev_delay_ensured():

    class delay_ensured(object):

        @ensure_delay(3)
        def a(self):
            print 'hello', time.time()

        @ensure_delay(3)
        def b(self):
            print 'goodbye', time.time()

    d = delay_ensured()
    d.a()
    d.b()
    d.a()
    d.a()
    print 'done'
    print 'still here'


if __name__ == '__main__':
    print 'and here'

    def print_all(*args, **kwargs):
        print args, kwargs


    @keep_trying((ZeroDivisionError, Exception), errorcall=print_all, try_time=4, wait_time=1)
    def gonna_try():
        print 'tried'
        bob


    gonna_try()