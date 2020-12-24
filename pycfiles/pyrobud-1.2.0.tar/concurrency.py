# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/concurrency/concurrency.py
# Compiled at: 2015-01-26 11:58:05
__doc__ = '\nConcurrency support for pyRobot.\n\nThis module provides:\n\n- an implementation of :class:`SignalingThread` (threads that explicitely\n  handle signals like cancelation)\n- heavily modified Python futures to support robot action management.\n- A future executor that simply spawn one thread per future (action) instead of\n  a thread pool.\n\nThese objects should not be directly used. Users should instead rely on the\n:meth:`~robots.concurrency.action.action` decorator.\n\nHelpful debugging commands::\n\n    >>> sys._current_frames()\n    >>> inspect.getouterframes(sys._current_frames()[<id>])[0][0].f_locals\n\n'
import logging
logger = logging.getLogger('robots.actions')
import sys, uuid
MAX_FUTURES = 20
MAX_TIME_TO_COMPLETE = 1
ACTIVE_SLEEP_RESOLUTION = 0.1
try:
    from concurrent.futures import Future, TimeoutError
except ImportError:
    import sys
    sys.stderr.write('[error] install python-concurrent.futures\n')
    sys.exit(1)

import os.path, weakref, threading, thread
from collections import deque
import traceback
from .signals import ActionCancelled, ActionPaused

class SignalingThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.debugger_trace = None
        return

    def cancel(self):
        self.__cancel = True

    def pause(self):
        self.__pause = True

    def _Thread__bootstrap(self):
        """ The name come from Python name mangling for 
        __double_leading_underscore_names

        Note that in Python3, __bootstrap becomes _bootstrap, thus
        making it easier to override.
        """
        if threading._trace_hook is not None:
            self.debugger_trace = threading._trace_hook
        else:
            self.debugger_trace = None
        self.__cancel = False
        self.__pause = False
        sys.settrace(self.__signal_emitter)
        self.name = 'Ranger action thread (initialization)'
        super(SignalingThread, self)._Thread__bootstrap()
        return

    def __signal_emitter(self, frame, event, arg):
        if self.__cancel:
            if frame.f_globals['__name__'] == 'threading':
                pass
            else:
                self.__cancel = False
                desc = 'Cancelling thread <%s>:\n' % self.name
                tb = traceback.extract_stack(frame, limit=6)
                for f in tb:
                    file, line, fn, instruction = f
                    desc += ' - in <%s> (l.%s of %s): %s\n' % (fn, line, os.path.basename(file), instruction)

                logger.debug(desc)
                raise ActionCancelled()
        if self.__pause:
            self.__pause = False
            logger.debug('Pausing thread <%s>' % self.name)
            raise ActionPaused()
        if self.debugger_trace:
            return self.debugger_trace
        else:
            return self.__signal_emitter


class RobotActionThread(SignalingThread):

    def __init__(self, future, initialized, fn, args, kwargs):
        SignalingThread.__init__(self)
        initialized.set()
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            result = self.fn(self.future, str(self.future), *self.args, **self.kwargs)
            self.future.set_result(result)
            logger.debug('Action <%s>: completed.' % str(self.future))
        except BaseException:
            e = sys.exc_info()[1]
            logger.error('Exception in action <%s>: %s' % (str(self.future), e))
            logger.error(traceback.format_exc())
            self.future.set_exception(e)


class RobotAction(Future):

    def __init__(self, actionname):
        Future.__init__(self)
        self.actionname = actionname
        self.thread = None
        self.id = uuid.uuid4()
        self.subactions = []
        self.parent_action = None
        self.has_acquired_resource = False
        return

    def add_subaction(self, action):
        self.subactions = [ a for a in self.subactions if a() is not None and a().thread() is not None ]
        self.subactions.append(action)
        logger.debug('Added sub-action %s to action %s' % (str(action()), str(self)))
        return

    def set_parent(self, action):
        self.parent_action = action

    def childof(self, action):
        """ Returns true if this action is a child of the given action, ie, has
        been spawned from the given action or any of its descendants.
        """
        parent = self.parent_action()
        if parent is None:
            return False
        else:
            if parent is action:
                return True
            return parent.childof(action)

    def set_thread(self, thread):
        self.thread = thread

    def cancel(self):
        thread = self.thread()
        if thread is None:
            logger.debug('Action <%s>: already done' % self)
            return
        else:
            logger.debug("Action <%s>: signaling cancelation to action's thread" % self)
            thread.cancel()
            logger.debug('Action <%s>: %s subactions to cancel' % (self, len(self.subactions)))
            for weak_subaction in self.subactions:
                subaction = weak_subaction()
                if subaction:
                    logger.debug('Action <%s>: Cancelling subaction %s...' % (self, subaction))
                    subaction.cancel()

            logger.debug('Action <%s>: now waiting for completion' % self)
            try:
                self.exception(timeout=MAX_TIME_TO_COMPLETE)
            except TimeoutError:
                raise RuntimeError('Unable to cancel action %s (still running %s after cancellation)!' % (self, MAX_TIME_TO_COMPLETE))

            logger.debug('Action <%s>: successfully cancelled' % self)
            return

    def result(self):
        if self.parent_action and self.parent_action():
            threading.current_thread().name = 'Action %s (waiting for sub-action %s)' % (self.parent_action(), self)
        else:
            threading.current_thread().name = 'Main thread (waiting for sub-action %s)' % self
        while True:
            try:
                return super(RobotAction, self).result(ACTIVE_SLEEP_RESOLUTION)
            except TimeoutError:
                pass

    def wait(self):
        """ alias for result()
        """
        return self.result()

    def __lt__(self, other):
        """ Overrides the comparision operator (used by ==, !=, <, >) to
        first wait for the result of the future.
        """
        return self.result().__lt__(other)

    def __le__(self, other):
        return self.result().__le__(other)

    def __eq__(self, other):
        return self.result().__eq__(other)

    def __ne__(self, other):
        return self.result().__ne__(other)

    def __gt__(self, other):
        return self.result().__gt__(other)

    def __ge__(self, other):
        return self.result().__ge__(other)

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.actionname + '[' + self.__repr__() + ']'


class FakeFuture:
    """ Used in the 'immediate' mode.
    """

    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result

    def wait(self):
        return self._result


class RobotActionExecutor:

    def __init__(self):
        self.futures = []
        self.futures_lock = threading.Lock()

    def submit(self, fn, *args, **kwargs):
        with self.futures_lock:
            self.futures = [ f for f in self.futures if not f.done() ]
        name = fn.__name__
        if args and not kwargs:
            name += '(%s)' % (', ').join([ str(a) for a in args[1:] ])
        else:
            if kwargs and not args:
                name += '(%s)' % (', ').join([ '%s=%s' % (str(k), str(v)) for k, v in kwargs.items() ])
            elif args and kwargs:
                name += '(%s, ' % (', ').join([ str(a) for a in args[1:] ])
                name += '%s)' % (', ').join([ '%s=%s' % (str(k), str(v)) for k, v in kwargs.items() ])
            if len([ f for f in self.futures if f.has_acquired_resource ]) > MAX_FUTURES:
                raise RuntimeError('You have more than %s actions running in parallel! Likely a bug in your application logic!' % MAX_FUTURES)
            f = RobotAction(name)
            initialized = threading.Event()
            t = RobotActionThread(f, initialized, fn, args, kwargs)
            f.set_thread(weakref.ref(t))
            current_action = self.get_current_action()
            if current_action:
                f.set_parent(weakref.ref(current_action))
                current_action.add_subaction(weakref.ref(f))
            t.start()
            while not initialized.is_set():
                pass

        with self.futures_lock:
            self.futures.append(f)
        return f

    def get_current_action(self):
        """Returns the RobotAction linked to the current thread.
        """
        thread_id = threading.current_thread().ident
        with self.futures_lock:
            for f in self.futures:
                if not f.done():
                    thread = f.thread()
                    if thread is not None and thread.ident == thread_id:
                        return f

        logger.debug('The current thread (<%s>) is not a robot action (main thread?)' % threading.current_thread().name)
        return

    def cancel_all(self):
        """ Blocks until all the currently running actions are actually stopped.
        """
        with self.futures_lock:
            for f in self.futures:
                if not f.done():
                    f.cancel()

            self.futures = []

    def cancel_all_others(self):
        """ Blocks until all the currently running actions *except the calling
        one* are actually stopped.

        """
        thread_id = threading.current_thread().ident
        with self.futures_lock:
            for f in self.futures:
                if not f.done():
                    thread = f.thread()
                    if thread is not None and thread.ident == thread_id:
                        myself = f
                        continue
                    f.cancel()

            self.futures = [
             myself]
        return

    def actioninfo(self, future_id):
        with self.futures_lock:
            future = [ f for f in self.futures if id(f) == future_id ]
            if not future:
                return 'No task with ID %s. Maybe the task is already done?' % future_id
            future = future[0]
            desc = 'Task <%s>\n' % future
            thread = future.thread()
            if thread:
                frame = sys._current_frames()[thread.ident]
                tb = traceback.extract_stack(frame, limit=6)
                for f in tb:
                    file, line, fn, instruction = f
                    desc += ' - in <%s> (l.%s of %s): %s\n' % (fn, line, os.path.basename(file), instruction)

                return desc
            return 'Task ID %s is already done.' % future_id

    def __str__(self):
        with self.futures_lock:
            return 'Running tasks:\n' + ('\n').join([ 'Task %s (id: %s, thread: <%s>)' % (f, id(f), str(f.thread())) for f in self.futures if not f.done() ])