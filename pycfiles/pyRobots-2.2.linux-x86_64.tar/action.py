# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/concurrency/action.py
# Compiled at: 2015-01-26 11:58:05
import logging
logger = logging.getLogger('robots.actions')
import time, threading, robots
from robots.introspection import introspection
from .signals import ActionCancelled
from .concurrency import FakeFuture

def action(fn):
    """ When applied to a function, this decorator turns it into
    a asynchronous task, starts it in a different thread, and returns
    a 'future' object that can be used to query the result/cancel it/etc.

    The main methods available on these 'future' object include
    :meth:`.RobotAction.wait` to wait until the action completes, and
    :meth:`.RobotAction.cancel` to request the action to stop (ie, it raises an
    :class:`.ActionCancelled` signal within the action thread). See
    :class:`.RobotAction` for the full list of available methods.

    Action implementation may want to handle the
    :class:`.ActionCancelled` signal to properly process
    cancellation requests.

    Usage example:

    .. code-block:: python

        @action
        def safe_walk(robot):
        try:
            robot.walk()
        except ActionCancelled:
            robot.go_back_to_rest_pose()

        action = robot.safe_walk()
        time.sleep(1)
        action.cancel()

    In this example, after one second, the ``safe_walk`` action is cancelled.
    This sends the signal :class:`.ActionCancelled` to the
    action, that can appropriately terminate.

    """

    def lockawarefn(future, actionname, *args, **kwargs):
        try:
            if hasattr(fn, '_locked_res'):
                for res, wait in fn._locked_res:
                    if wait:
                        threading.current_thread().name = 'Robot Action %s, waiting on resource %s' % (actionname, res)
                        need_to_wait = False
                        if res.owner is not None:
                            need_to_wait = True
                            logger.info('Robot action <%s> is waiting on resource %s' % (actionname, res))
                        res.acquire(wait, acquirer=fn.__name__)
                        if need_to_wait:
                            logger.info('Robot action <%s> has acquired resource %s' % (actionname, res))
                        else:
                            logger.info('Robot action <%s> acquired free resource %s  ' % (actionname, res))

        except ActionCancelled:
            threading.current_thread().name = 'Idle Robot action thread'
            logger.debug('Action <%s> cancelled while it was waiting for a lock on a resource.' % actionname)
            return

        try:
            try:
                future.has_acquired_resource = True
                threading.current_thread().name = 'Robot Action %s (running)' % actionname
                logger.debug('Starting action <%s> now.' % actionname)
                try:
                    result = fn(*args, **kwargs)
                except TypeError:
                    logger.error("Exception when invoking action <%s>. Did you forget to add the parameter 'robot'?" % actionname)
                    raise

                logger.debug('Action <%s> returned.' % actionname)
                return result
            except ActionCancelled:
                logger.warning('Action cancellation ignored by %s. Forced stop!' % actionname)

        finally:
            if hasattr(fn, '_locked_res'):
                for res, wait in fn._locked_res:
                    res.release()

            threading.current_thread().name = 'Idle Robot action thread'

        return

    lockawarefn.__name__ = fn.__name__
    lockawarefn.__doc__ = fn.__doc__

    def innerfunc(*args, **kwargs):
        if len(args) == 0 or not isinstance(args[0], robots.GenericRobot):
            raise Exception('No robot instance passed to the action!')
        robot = args[0]
        if hasattr(fn, '_locked_res'):
            for res, wait in fn._locked_res:
                if not wait:
                    got_the_lock = res.acquire(False, acquirer=fn.__name__)
                    if not got_the_lock:
                        logger.info('Required resource <%s> locked while attempting to start %s. Cancelling it as required.' % (res.name, fn.__name__))
                        return FakeFuture(None)

        if robot.immediate:
            res = FakeFuture(lockawarefn(*args, **kwargs))
            return res
        else:
            executor = robot.executor
            if args and kwargs:
                future = executor.submit(lockawarefn, *args, **kwargs)
            elif args:
                future = executor.submit(lockawarefn, *args)
            else:
                future = executor.submit(lockawarefn)
            if introspection:
                introspection.action_started(fn.__name__, str('FUTURE ID BROKEN'), str('ACTION ID BROKEN TDB'), args[1:], kwargs)
                future.add_done_callback(lambda x: introspection.action_completed(fn.__name__, str('future.id BROKEN')))
            return future
            return

    innerfunc.__name__ = fn.__name__
    innerfunc.__doc__ = fn.__doc__
    innerfunc._action = True
    return innerfunc