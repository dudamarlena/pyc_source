# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/core.py
# Compiled at: 2020-04-15 05:31:07
# Size of source mod 2**32: 21166 bytes
import logging, random, sys, traceback
from time import time
import gevent, gevent.lock
from gevent import GreenletExit, monkey
monkey.patch_all()
from .clients import HttpSession
from .exception import InterruptTaskSet, LocustError, RescheduleTask, RescheduleTaskImmediately, StopLocust, MissingWaitTimeError
from .runners import STATE_CLEANUP, LOCUST_STATE_RUNNING, LOCUST_STATE_STOPPING, LOCUST_STATE_WAITING
from .util import deprecation
logger = logging.getLogger(__name__)

def task(weight=1):
    """
    Used as a convenience decorator to be able to declare tasks for a TaskSet 
    inline in the class. Example::
    
        class ForumPage(TaskSet):
            @task(100)
            def read_thread(self):
                pass
            
            @task(7)
            def create_thread(self):
                pass
    """

    def decorator_func(func):
        func.idapload_task_weight = weight
        return func

    if callable(weight):
        func = weight
        weight = 1
        return decorator_func(func)
    return decorator_func


def seq_task(order):
    """
    Used as a convenience decorator to be able to declare tasks for a TaskSequence
    inline in the class. Example::

        class NormalUser(TaskSequence):
            @seq_task(1)
            def login_first(self):
                pass

            @seq_task(2)
            @task(25) # You can also set the weight in order to execute the task for `weight` times one after another.
            def then_read_thread(self):
                pass

            @seq_task(3)
            def then_logout(self):
                pass
    """

    def decorator_func(func):
        func.idapload_task_order = order
        if not hasattr(func, 'idapload_task_weight'):
            func.idapload_task_weight = 1
        return func

    return decorator_func


class NoClientWarningRaiser(object):
    __doc__ = '\n    The purpose of this class is to emit a sensible error message for old test scripts that \n    inherits from Locust, and expects there to be an HTTP client under the client attribute.\n    '

    def __getattr__(self, _):
        raise LocustError('No client instantiated. Did you intend to inherit from HttpLocust?')


class Locust(object):
    __doc__ = '\n    Represents a "user" which is to be hatched and attack the system that is to be load tested.\n    \n    The behaviour of this user is defined by the task_set attribute, which should point to a \n    :py:class:`TaskSet <idapload.core.TaskSet>` class.\n    \n    This class should usually be subclassed by a class that defines some kind of client. For \n    example when load testing an HTTP system, you probably want to use the \n    :py:class:`HttpLocust <idapload.core.HttpLocust>` class.\n    '
    host = None
    min_wait = None
    max_wait = None
    wait_time = None
    wait_function = None
    task_set = None
    weight = 10
    client = NoClientWarningRaiser()
    _catch_exceptions = True
    _setup_has_run = False
    _teardown_is_set = False
    _lock = gevent.lock.Semaphore()
    _state = False

    def __init__(self, environment):
        super(Locust, self).__init__()
        deprecation.check_for_deprecated_wait_api(self)
        self.environment = environment
        with self._lock:
            if hasattr(self, 'setup'):
                if self._setup_has_run is False:
                    self._set_setup_flag()
                    try:
                        self.setup()
                    except Exception as e:
                        try:
                            self.environment.events.idapload_error.fire(idapload_instance=self, exception=e, tb=(sys.exc_info()[2]))
                            logger.error('%s\n%s', e, traceback.format_exc())
                        finally:
                            e = None
                            del e

            if hasattr(self, 'teardown'):
                if self._teardown_is_set is False:
                    self._set_teardown_flag()
                    self.environment.events.quitting.add_listener(self.teardown)

    @classmethod
    def _set_setup_flag(cls):
        cls._setup_has_run = True

    @classmethod
    def _set_teardown_flag(cls):
        cls._teardown_is_set = True

    def run(self, runner=None):
        task_set_instance = self.task_set(self)
        try:
            task_set_instance.run()
        except StopLocust:
            pass
        except (RescheduleTask, RescheduleTaskImmediately) as e:
            try:
                raise LocustError("A task inside a Locust class' main TaskSet (`%s.task_set` of type `%s`) seems to have called interrupt() or raised an InterruptTaskSet exception. The interrupt() function is used to hand over execution to a parent TaskSet, and should never be called in the main TaskSet which a Locust class' task_set attribute points to." % (type(self).__name__, self.task_set.__name__)) from e
            finally:
                e = None
                del e

        except GreenletExit as e:
            try:
                if runner:
                    runner.state = STATE_CLEANUP
                if hasattr(task_set_instance, 'on_stop'):
                    task_set_instance.on_stop()
                raise
            finally:
                e = None
                del e


class HttpLocust(Locust):
    __doc__ = '\n    Represents an HTTP "user" which is to be hatched and attack the system that is to be load tested.\n    \n    The behaviour of this user is defined by the task_set attribute, which should point to a \n    :py:class:`TaskSet <idapload.core.TaskSet>` class.\n    \n    This class creates a *client* attribute on instantiation which is an HTTP client with support \n    for keeping a user session between requests.\n    '
    client = None
    trust_env = False

    def __init__(self, *args, **kwargs):
        (super(HttpLocust, self).__init__)(*args, **kwargs)
        if self.host is None:
            raise LocustError('You must specify the base host. Either in the host attribute in the Locust class, or on the command line using the --host option.')
        session = HttpSession(base_url=(self.host),
          request_success=(self.environment.events.request_success),
          request_failure=(self.environment.events.request_failure))
        session.trust_env = self.trust_env
        self.client = session


class TaskSetMeta(type):
    __doc__ = "\n    Meta class for the main Locust class. It's used to allow Locust classes to specify task execution \n    ratio using an {task:int} dict, or a [(task0,int), ..., (taskN,int)] list.\n    "

    def __new__(mcs, classname, bases, classDict):
        new_tasks = []
        for base in bases:
            if hasattr(base, 'tasks') and base.tasks:
                new_tasks += base.tasks

        if 'tasks' in classDict:
            if classDict['tasks'] is not None:
                tasks = classDict['tasks']
                if isinstance(tasks, dict):
                    tasks = tasks.items()
                for task in tasks:
                    if isinstance(task, tuple):
                        task, count = task
                        for i in range(count):
                            new_tasks.append(task)

                    else:
                        new_tasks.append(task)

        for item in classDict.values():
            if hasattr(item, 'idapload_task_weight'):
                for i in range(0, item.idapload_task_weight):
                    new_tasks.append(item)

        classDict['tasks'] = new_tasks
        return type.__new__(mcs, classname, bases, classDict)


class TaskSet(object, metaclass=TaskSetMeta):
    __doc__ = "\n    Class defining a set of tasks that a Locust user will execute. \n    \n    When a TaskSet starts running, it will pick a task from the *tasks* attribute, \n    execute it, and then sleep for the number of seconds returned by it's *wait_time* \n    function. If no wait_time method has been declared on the TaskSet, it'll call the \n    wait_time function on the Locust by default. It will then schedule another task \n    for execution and so on.\n    \n    TaskSets can be nested, which means that a TaskSet's *tasks* attribute can contain \n    another TaskSet. If the nested TaskSet it scheduled to be executed, it will be \n    instantiated and called from the current executing TaskSet. Execution in the\n    currently running TaskSet will then be handed over to the nested TaskSet which will \n    continue to run until it throws an InterruptTaskSet exception, which is done when \n    :py:meth:`TaskSet.interrupt() <idapload.core.TaskSet.interrupt>` is called. (execution \n    will then continue in the first TaskSet).\n    "
    tasks = []
    min_wait = None
    max_wait = None
    wait_function = None
    idapload = None
    parent = None
    _setup_has_run = False
    _teardown_is_set = False
    _lock = gevent.lock.Semaphore()

    def __init__(self, parent):
        deprecation.check_for_deprecated_wait_api(self)
        self._task_queue = []
        self._time_start = time()
        if isinstance(parent, TaskSet):
            self.idapload = parent.idapload
        else:
            if isinstance(parent, Locust):
                self.idapload = parent
            else:
                raise LocustError('TaskSet should be called with Locust instance or TaskSet instance as first argument')
        self.parent = parent
        if not self.min_wait:
            self.min_wait = self.idapload.min_wait
        if not self.max_wait:
            self.max_wait = self.idapload.max_wait
        if not self.wait_function:
            self.wait_function = self.idapload.wait_function
        with self._lock:
            if hasattr(self, 'setup'):
                if self._setup_has_run is False:
                    self._set_setup_flag()
                    try:
                        self.setup()
                    except Exception as e:
                        try:
                            self.idapload.environment.events.idapload_error.fire(idapload_instance=self, exception=e, tb=(sys.exc_info()[2]))
                            logger.error('%s\n%s', e, traceback.format_exc())
                        finally:
                            e = None
                            del e

            if hasattr(self, 'teardown'):
                if self._teardown_is_set is False:
                    self._set_teardown_flag()
                    self.environment.events.quitting.add_listener(self.teardown)

    @classmethod
    def _set_setup_flag(cls):
        cls._setup_has_run = True

    @classmethod
    def _set_teardown_flag(cls):
        cls._teardown_is_set = True

    def run(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        try:
            if hasattr(self, 'on_start'):
                self.on_start()
        except InterruptTaskSet as e:
            try:
                if e.reschedule:
                    raise RescheduleTaskImmediately(e.reschedule).with_traceback(sys.exc_info()[2])
                else:
                    raise RescheduleTask(e.reschedule).with_traceback(sys.exc_info()[2])
            finally:
                e = None
                del e

        while True:
            try:
                if not self._task_queue:
                    self.schedule_task(self.get_next_task())
                try:
                    if self.idapload._state == LOCUST_STATE_STOPPING:
                        raise GreenletExit()
                    self.execute_next_task()
                    if self.idapload._state == LOCUST_STATE_STOPPING:
                        raise GreenletExit()
                except RescheduleTaskImmediately:
                    if self.idapload._state == LOCUST_STATE_STOPPING:
                        raise GreenletExit()
                except RescheduleTask:
                    self.wait()
                else:
                    self.wait()
            except InterruptTaskSet as e:
                try:
                    if e.reschedule:
                        raise RescheduleTaskImmediately(e.reschedule) from e
                    else:
                        raise RescheduleTask(e.reschedule) from e
                finally:
                    e = None
                    del e

            except StopLocust:
                raise
            except GreenletExit:
                raise
            except Exception as e:
                try:
                    self.idapload.environment.events.idapload_error.fire(idapload_instance=self, exception=e, tb=(sys.exc_info()[2]))
                    if self.idapload._catch_exceptions:
                        logger.error('%s\n%s', e, traceback.format_exc())
                        self.wait()
                    else:
                        raise
                finally:
                    e = None
                    del e

    def execute_next_task(self):
        task = self._task_queue.pop(0)
        (self.execute_task)(task['callable'], *(task['args']), **task['kwargs'])

    def execute_task(self, task, *args, **kwargs):
        print(' Args and kargs ', *args, **kwargs)
        if hasattr(task, '__self__') and task.__self__ == self:
            task(*args, **kwargs)
        else:
            if hasattr(task, 'tasks') and issubclass(task, TaskSet):
                (task(self).run)(*args, **kwargs)
            else:
                task(self, *args, **kwargs)

    def schedule_task(self, task_callable, args=None, kwargs=None, first=False):
        """
        Add a task to the Locust's task execution queue.
        
        *Arguments*:
        
        * task_callable: Locust task to schedule
        * args: Arguments that will be passed to the task callable
        * kwargs: Dict of keyword arguments that will be passed to the task callable.
        * first: Optional keyword argument. If True, the task will be put first in the queue.
        """
        task = {'callable':task_callable, 
         'args':args or [],  'kwargs':kwargs or {}}
        if first:
            self._task_queue.insert(0, task)
        else:
            self._task_queue.append(task)

    def get_next_task(self):
        if not self.tasks:
            raise Exception('No tasks defined. use the @task decorator or set the tasks property of the TaskSet')
        return random.choice(self.tasks)

    def wait_time(self):
        """
        Method that returns the time (in seconds) between the execution of tasks. 
        
        Example::
        
            from idapload import TaskSet, between
            class Tasks(TaskSet):
                wait_time = between(3, 25)
        """
        if self.idapload.wait_time:
            return self.idapload.wait_time()
        if self.min_wait is not None:
            if self.max_wait is not None:
                return random.randint(self.min_wait, self.max_wait) / 1000.0
        raise MissingWaitTimeError('You must define a wait_time method on either the %s or %s class' % (
         type(self.idapload).__name__,
         type(self).__name__))

    def wait(self):
        self.idapload._state = LOCUST_STATE_WAITING
        self._sleep(self.wait_time())
        self.idapload._state = LOCUST_STATE_RUNNING

    def _sleep(self, seconds):
        gevent.sleep(seconds)

    def interrupt(self, reschedule=True):
        """
        Interrupt the TaskSet and hand over execution control back to the parent TaskSet.
        
        If *reschedule* is True (default), the parent Locust will immediately re-schedule,
        and execute, a new task
        
        This method should not be called by the root TaskSet (the one that is immediately, 
        attached to the Locust class' *task_set* attribute), but rather in nested TaskSet
        classes further down the hierarchy.
        """
        raise InterruptTaskSet(reschedule)

    @property
    def client(self):
        """
        Reference to the :py:attr:`client <idapload.core.Locust.client>` attribute of the root 
        Locust instance.
        """
        return self.idapload.client


class TaskSequence(TaskSet):
    __doc__ = "\n    Class defining a sequence of tasks that a Locust user will execute.\n\n    When a TaskSequence starts running, it will pick the task in `index` from the *tasks* attribute,\n    execute it, and call its *wait_function* which will define a time to sleep for.\n    This defaults to a uniformly distributed random number between *min_wait* and\n    *max_wait* milliseconds. It will then schedule the `index + 1 % len(tasks)` task for execution and so on.\n\n    TaskSequence can be nested with TaskSet, which means that a TaskSequence's *tasks* attribute can contain\n    TaskSet instances as well as other TaskSequence instances. If the nested TaskSet is scheduled to be executed, it will be\n    instantiated and called from the current executing TaskSet. Execution in the\n    currently running TaskSet will then be handed over to the nested TaskSet which will\n    continue to run until it throws an InterruptTaskSet exception, which is done when\n    :py:meth:`TaskSet.interrupt() <idapload.core.TaskSet.interrupt>` is called. (execution\n    will then continue in the first TaskSet).\n\n    In this class, tasks should be defined as a list, or simply define the tasks with the @seq_task decorator\n    "

    def __init__(self, parent):
        super(TaskSequence, self).__init__(parent)
        self._index = 0
        self.tasks.sort(key=(lambda t:         if hasattr(t, 'idapload_task_order'):
t.idapload_task_order # Avoid dead code: 1))

    def get_next_task(self):
        task = self.tasks[self._index]
        self._index = (self._index + 1) % len(self.tasks)
        return task