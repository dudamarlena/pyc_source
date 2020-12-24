# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\replacements\greenlet.py
# Compiled at: 2017-12-11 20:12:50
import weakref, sys, stackless
from stacklesslib.base import atomic
__version__ = '0.3.2'

class Scheduler(object):
    """A scheduler that switches between tasklets like greenlets"""

    def __init__(self):
        self.prev = self.value = None
        return

    def create(self, function):
        """Create a new tasklet, bound to a function that will return a tuple
           on exit: (t, v)
           t = the target tasklet to switch to, and v the value to provide
        """

        def top(args, kwargs):
            self._start(function, args, kwargs)

        return stackless.tasklet(top)

    def start(self, t, args=(), kwargs={}):
        """Start a context previously created"""
        prev = stackless.getcurrent()
        if t.thread_id != prev.thread_id:
            raise error("can't switch to a different thread")
        with atomic():
            t(args, kwargs)
            self.prev = prev
            t.run()
            return self._return()

    def _return(self):
        if self.prev is not None:
            self.prev.remove()
            self.prev = None
        value, self.value = self.value, None
        if value is None:
            raise RuntimeError('unexpected switch to tasklet')
        return value

    def _start(self, function, args, kwargs):
        self.prev.remove()
        self.prev = None
        r, v = function(*args, **kwargs)
        with atomic():
            self.value = v
            self.previous = None
            r.run()
        return

    def switch(self, target, value=None):
        prev = stackless.getcurrent()
        if prev is target:
            return value
        if target.thread_id != prev.thread_id:
            raise error("can't switch to a different thread")
        with atomic():
            self.prev = prev
            self.value = value
            target.run()
            assert self.prev != prev
            return self._return()


class NewScheduler(Scheduler):
    """A version of the above for use when tasklets support the .switch method"""

    def start(self, t, args=(), kwargs={}):
        """Start a context previously created"""
        prev = stackless.getcurrent()
        if t.thread_id != prev.thread_id:
            raise error("can't switch to a different thread")
        with atomic():
            t(args, kwargs)
            t.switch()
            return self._return()

    def _return(self):
        value, self.value = self.value, None
        if value is None:
            raise RuntimeError('unexpected switch to tasklet')
        return value

    def _start(self, function, args, kwargs):
        r, v = function(*args, **kwargs)
        with atomic():
            self.value = v
            r.run()

    def switch(self, target, value=None):
        prev = stackless.getcurrent()
        if prev is target:
            return value
        if target.thread_id != prev.thread_id:
            raise error("can't switch to a different thread")
        with atomic():
            self.value = value
            target.switch()
            return self._return()


if hasattr(stackless.tasklet, 'switch'):
    Scheduler = NewScheduler

class error(Exception):
    pass


class GreenletExit(BaseException):
    pass


class ErrorWrapper(object):

    def __enter__(self):
        pass

    def __exit__(self, tp, val, tb):
        if tp:
            if isinstance(val, TaskletExit):
                raise GreenletExit(*val.args), None, tb
            if type(val) is RuntimeError:
                raise error, val, tb
        return


ErrorWrapper = ErrorWrapper()
taskletmap = weakref.WeakValueDictionary()
scheduler = Scheduler()

def _getmain():
    return _lookup(stackless.getmain())


def getcurrent():
    return _lookup(stackless.getcurrent())


def _lookup(s):
    try:
        return taskletmap[s]
    except KeyError:
        return greenlet(parent=s)


class greenlet(object):

    def __init__(self, run=None, parent=None):
        self.dead = False
        if run is not None:
            self.run = run
        if isinstance(parent, stackless.tasklet):
            self._started = True
            self._tasklet = parent
            if parent.is_main:
                self.parent = self
                self._main = self
                self._garbage = []
            else:
                self.parent = self._main = _getmain()
        else:
            self._started = False
            self._tasklet = scheduler.create(self._greenlet_main)
            if parent is None:
                parent = getcurrent()
            self.parent = parent
            self._main = parent._main
            del self._main._garbage[:]
        taskletmap[self._tasklet] = self
        return

    def __del__(self):
        if self:
            if stackless.getcurrent() == self._tasklet:
                return
            taskletmap[self._tasklet] = self
            old = self.parent
            self.parent = getcurrent()
            try:
                try:
                    self.throw()
                except error:
                    self._main._garbage.append(self)

            finally:
                self.parent = old

    @property
    def gr_frame(self):
        if self._tasklet is stackless.getcurrent():
            return self._tasklet.frame
        else:
            f = self._tasklet.frame
            try:
                return f.f_back.f_back.f_back
            except AttributeError:
                return

            return

    def __nonzero__(self):
        return self._started and not self.dead

    def switch(self, *args, **kwds):
        return self._Result(self._switch((False, args, kwds)))

    def throw(self, t=None, v=None, tb=None):
        if not t:
            t = GreenletExit
        return self._Result(self._switch((t, v, tb)))

    def _switch(self, arg):
        with ErrorWrapper:
            if not self._started:
                run = self.run
                try:
                    del self.run
                except AttributeError:
                    pass

                self._started = True
                return scheduler.start(self._tasklet, ((run, arg),))
            else:
                if not self:
                    return scheduler.switch(self._parent()._tasklet, arg)
                return scheduler.switch(self._tasklet, arg)

    @staticmethod
    def _Result(arg):
        """Convert the switch args into a single return value or raise exception"""
        err, args, kwds = arg
        if not err:
            if not kwds:
                if len(args) == 1:
                    return args[0]
                if not args:
                    return
                return args
            if args:
                return (args, kwds)
            return kwds
        raise err, args, kwds
        return

    @staticmethod
    def _greenlet_main(arg):
        run, (err, args, kwds) = arg
        try:
            if not err:
                result = run(*args, **kwds)
                arg = (False, (result,), None)
            else:
                raise err, args, kwds
        except GreenletExit as e:
            arg = (
             False, (e,), None)
        except:
            arg = sys.exc_info()

        c = getcurrent()
        c.dead = True
        p = c._parent()
        return (
         p._tasklet, arg)

    def _parent(self):
        p = self.parent
        while not p:
            p = p.parent

        return p

    getcurrent = staticmethod(getcurrent)
    error = error
    GreenletExit = GreenletExit