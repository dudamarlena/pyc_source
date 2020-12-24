# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/parallel.py
# Compiled at: 2013-12-23 21:46:56
"""
Advanced API for parallel execution within GoLismero plugins.

.. note:: It's often best to keep your plugins as simple as possible, breaking
          down complex tasks into simple steps, and into multiple plugins if
          necessary. That way GoLismero can take care of multiprocessing and
          load balancing more efficiently.

          Still, in some cases, it comes in handy to be able to run something
          in parallel within a plugin. Just bear in mind that if your plugin
          uses too many threads and it gets called often, the total number of
          running threads in the machine would balloon quite fast!

          Also, there are situations where threads won't help at all. For
          example if the number of running threads is greater than the maximum
          number of allowed connections to the target host. Additionally, in the
          CPython VM, the Global Interpreter Lock (GIL) makes threads a lot less
          efficient than they should be, so running pure-Python computation
          tasks in parallel not only gives you no benefit, but may actually run
          slower! See: `GlobalInterpreterLock <http://wiki.python.org/moin/GlobalInterpreterLock>`_

.. warning:: Some parts of the GoLismero API doesn't guarantee thread safety!
             When in doubt, avoid sharing objects or mutable structures among
             threads, and pipe the API calls through the main thread.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'pmap', 'setInterval', 'TaskGroup', 'WorkerPool', 'Counter']
from .config import Config
from thread import get_ident
from threading import RLock, Semaphore, Thread, Event, Timer

class Counter(object):
    """
    Thread-safe counter.
    """

    def __init__(self, init_val=0):
        if type(init_val) not in (int, long, float):
            raise TypeError('Expected a number, got %r instead' % type(init_val))
        self.__value = init_val
        self.__lock = RLock()

    def reset(self):
        return self.setvalue(0)

    def inc(self):
        return self.add(1)

    def dec(self):
        return self.sub(1)

    def add(self, offset):
        if type(offset) not in (int, long, float):
            raise TypeError('Expected a number, got %r instead' % type(offset))
        with self.__lock:
            self.__value += offset
            return self.__value

    def sub(self, offset):
        if type(offset) not in (int, long, float):
            raise TypeError('Expected a number, got %r instead' % type(offset))
        with self.__lock:
            self.__value -= offset
            return self.__value

    def setvalue(self, value):
        if type(value) not in (int, long, float):
            raise TypeError('Expected a number, got %r instead' % type(value))
        with self.__lock:
            old_value = self.__value
            self.__value = value
            return old_value

    def getvalue(self):
        with self.__lock:
            return self.__value


def setInterval(interval, times=-1):
    """
    Decorator to execute a function periodically using a timer.
    The function is executed in a background thread.

    Example:

        >>> from golismero.api.parallel import setInterval
        >>> from time import gmtime, strftime
        >>> @setInterval(2) # Execute every 2 seconds until stopped.
        ... def my_func():
        ...     print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ...
        >>> handler = my_func()
        2013-07-25 22:40:55
        2013-07-25 22:40:57
        2013-07-25 22:40:59
        2013-07-25 22:41:01
        >>> handler.set() # Stop the execution.
        >>> @setInterval(2, 3) # Every 2 seconds, 3 times.
        ... def my_func():
        ...     print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ...
        >>> handler = my_func()
        2013-07-25 22:40:55
        2013-07-25 22:40:57
        2013-07-25 22:40:59

    :param: interval: Interval in seconds of how often the function will be
                      executed.
    :type interval: float | int

    :param times: Maximum number of times the function will be executed.
                  Negative values cause the function to be executed until
                  manually stopped, or until the process dies.
    :type times: int
    """
    if isinstance(interval, int):
        interval = float(interval)
    elif not isinstance(interval, float):
        if callable(interval):
            raise SyntaxError('Missing interval value')
        raise TypeError('Expected int or float, got %r instead' % type(interval))
    if not isinstance(times, int):
        raise TypeError('Expected int, got %r instead' % type(times))

    def outer_wrap(function):
        if not callable(function):
            raise TypeError('Expected function, got %r instead' % type(function))

        def wrap(*args, **kwargs):
            stop = Event()
            current_context = Config._context

            def inner_wrap():
                try:
                    Config._context
                except SyntaxError:
                    Config._context = current_context

                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    if stop.isSet():
                        break
                    function(*args, **kwargs)
                    i += 1

            t = Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop

        return wrap

    return outer_wrap


def pmap(func, *args, **kwargs):
    """
    Run a function in parallel.

    This function behaves pretty much like the built-in
    function map(), but it runs in parallel using threads:

        >>> from golismero.api.parallel import pmap
        >>> def triple(x):
        ...   return x * 3
        ...
        >>> pmap(triple, [1, 2, 3, 4, 5])
        [3, 6, 9, 12, 15]
        >>> def addition(x, y):
        ...   return x + y
        ...
        >>> pmap(addition, [1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        [3, 6, 9, 12, 15]
        >>> pmap((lambda x: x + 1), [1, 2, 3, 4, 5])
        [2, 3, 4, 5, 6]
        >>> def printer(x, y):
        ...    print "%s - %s" (x, y)
        ...
        >>> from functools import partial
        >>> pmap(partial(printer, "fixed_text"), [1, 2])
        fixed_text - 1
        fixed_text - 2
        >>> class Point(object):
        ...   def __init__(self, x, y):
        ...     self.x = x
        ...     self.y = y
        ...   def __repr__(self):
        ...     return "Point(%d, %d)" % (self.x, self.y)
        ...
        >>> pmap(Point, [1, 2, 3], [4, 5, 6])
        [Point(1, 4), Point(2, 5), Point(3, 6)]

    .. warning: Unlike the built-in map() function, exceptions raised
                by the callback function will be silently ignored.

    :param func: A function or any other executable object.
    :type func: callable

    :param args: One or more iterables or simple params containing the parameters for each call.
    :type args: simple_param, simple_param, iterable, iterable...

    :keyword pool_size: Maximum number of concurrent threads. Defaults to 4.
    :type pool_size: int

    :return: List with returned results, in the same order as the input data.
    :rtype: list
    """
    if len(args) <= 0:
        raise TypeError('Expected at least one positional argument')
    pool_size = kwargs.pop('pool_size', 4)
    if kwargs:
        if len(kwargs) > 1:
            msg = 'Unknown keyword arguments: '
        else:
            msg = 'Unknown keyword argument: '
        raise TypeError(msg + (', ').join(kwargs))
    if func is None:
        return map(None, *args)
    else:
        if len(args) == 1:
            data = [ (x,) for x in args[0] ]
        else:
            data = map(None, *args)
        if not data:
            return []
        if len(data) == 1:
            return [func(*data[0])]
        m_task_group = TaskGroup(func, data)
        m_pool = WorkerPool(pool_size)
        try:
            m_pool.add_task_group(m_task_group)
            m_pool.join_tasks()
        finally:
            m_pool.stop()

        return m_task_group.pack_output()


class Task(object):
    """
    A task to be executed.
    """

    def __init__(self, func, args, index, output):
        r"""
        :param func: A function or any other executable object.
        :type func: callable

        :param args: Tuple containing positional arguments.
        :type args: tuple

        :param index: Key for the output dictionary. Used later to sort the results.
        :type index: int

        :param output: Output dictionary that will receive the return value.
        :type output: dict(int -> \*)
        """
        if type(index) is not int:
            raise TypeError('Expected int, got %r instead' % type(index))
        if not hasattr(output, '__setitem__'):
            raise TypeError('Expected dict, got %r instead' % type(output))
        if not callable(func):
            raise TypeError('Expected callable (function, class, instance with __call__), got %r instead' % type(func))
        self.__func = func
        self.__args = args
        self.__index = index
        self.__output = output

    @property
    def func(self):
        """
        :returns: A function or any other executable object.
        :rtype: callable
        """
        return self.__func

    @property
    def args(self):
        """
        :returns: Tuple containing positional arguments.
        :rtype: tuple
        """
        return self.__args

    @property
    def index(self):
        """
        :returns: Key for the output dictionary. Used later to sort the results.
        :rtype: int
        """
        return self.__index

    @property
    def output(self):
        r"""
        :returns: Output dictionary that will receive the return value.
        :rtype: dict(int -> \*)
        """
        return self.__output

    def run(self):
        """
        Run the task.
        """
        try:
            x = self.__func(*self.__args)
            self.__output[self.__index] = x
        except:
            pass


class TaskGroup(object):
    """
    A group of tasks to be executed.
    """

    def __init__(self, func, data):
        r"""
        :param func: A function or any other executable object.
        :type func: callable

        :param data: List of tuples containing the parameters for each call.
        :type data: list(tuple(\*))
        """
        if not callable(func):
            raise TypeError('Expected callable (function, class, instance with __call__), got %r instead' % type(func))
        self.__func = func
        self.__data = data
        self.__output = {}

    @property
    def func(self):
        """
        :returns: A function or any other executable object.
        :rtype: callable
        """
        return self.__func

    @property
    def data(self):
        r"""
        :returns: List of tuples containing the parameters for each call.
        :rtype: list(tuple(\*))
        """
        return self.__data

    @property
    def output(self):
        r"""
        :returns: Output dictionary that will receive the return values.
        :rtype: dict(int -> \*)
        """
        return self.__output

    def __len__(self):
        """
        :returns: Number of individual tasks for this task group.
        :rtype: int
        """
        return len(self.data)

    def __iter__(self):
        """
        :returns: Iterator of individual tasks for this task group.
        :rtype: iter(Task)
        """
        func = self.func
        output = self.output
        index = 0
        for args in self.data:
            yield Task(func, args, index, output)
            index += 1

    def pack_output(self):
        """
        Converts the output dictionary into an ordered list, where each
        element is the return value for each tuple of positional arguments.
        Missing elements are replaced with None.

        .. warning: Do not call before calling WorkerPool.join_tasks()!
        """
        output = self.output
        if not output:
            return [None] * len(self.data)
        else:
            get = output.get
            max_index = max(output.iterkeys())
            max_index = max(max_index, len(self.data) - 1)
            return [ get(i) for i in xrange(max_index + 1) ]


class WorkerThread(Thread):
    """
    Worker threads.
    """

    def __init__(self):
        self.__task = None
        self._callback = None
        self.__continue = True
        self.__sem_available = Semaphore(0)
        self.__lock = RLock()
        self.__busy = False
        self.__context = None
        super(WorkerThread, self).__init__()
        self.daemon = True
        return

    def start(self):
        """
        Thread start function.

        .. warning: This method is called automatically,
                    do not call it yourself.
        """
        self.__context = Config._context
        try:
            super(WorkerThread, self).start()
        except:
            self.__context = None
            raise

        return

    def run(self):
        """
        Thread run function.

        .. warning: This method is called automatically,
                    do not call it yourself.
        """
        if self.ident != get_ident():
            raise SyntaxError("Don't call WorkerThread.run() yourself!")
        Config._context = self.__context
        self.__context = None
        while True:
            self.__sem_available.acquire()
            if not self.__continue:
                break
            with self.__lock:
                self.__busy = True
                if self.__task is not None:
                    self.__task.run()
                if self._callback is not None:
                    self._callback(self)
                self.__busy = False

        return

    def stop(self):
        """
        Signal the thread to stop.
        """
        self.__continue = False
        self.__sem_available.release()

    def terminate(self):
        """
        Force the thread to terminate.

        .. warning: Don't use this except in extreme circumstances!
                    The terminated thread's code may not have a proper chance
                    to clean up its resources or free its locks, and this may
                    lead to memory leaks and/or deadlocks!
        """
        if not self.isAlive():
            return
        else:
            import ctypes
            exc = ctypes.py_object(KeyboardInterrupt)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)
            if res == 0:
                raise SystemError('Nonexistent thread id?')
            elif res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), None)
                raise SystemError('PyThreadState_SetAsyncExc() failed')
            return

    def run_task(self, task):
        """
        Run a task in this worker thread.

        :param task: Task to run.
        :type task: Task
        """
        if not isinstance(task, Task):
            raise TypeError('Expected Task, got %r instead' % type(task))
        with self.__lock:
            if self.__busy:
                raise SystemError('Task is busy')
            self.__task = task
            self.__sem_available.release()


class WorkerPool(Thread):
    """
    Worker thread pool.
    """

    def __init__(self, pool_size=4):
        """
        :param pool_size: Maximum amount of concurrent threads allowed.
        :type pool_size: int
        """
        if not isinstance(pool_size, int):
            raise TypeError('Expected int, got %r instead' % type(pool_size))
        if pool_size < 1:
            raise ValueError('pool_size must be greater than 0')
        self.__lock = RLock()
        self.__sem_max_threads = Semaphore(pool_size)
        self.__sem_available_data = Semaphore(0)
        self.__sem_join = Semaphore(0)
        self.__count_task = 0
        self.__stop = False
        self.__join = False
        self.__pending_tasks = set()
        self.__busy_workers = set()
        self.__available_workers = set()
        self.__all_workers = set()
        add1 = self.__available_workers.add
        add2 = self.__all_workers.add
        callback = self._worker_thread_finished
        GT = WorkerThread
        for _ in xrange(pool_size):
            l_thread = GT()
            l_thread._callback = callback
            add1(l_thread)
            add2(l_thread)
            l_thread.start()

        super(WorkerPool, self).__init__()
        self.daemon = True
        self.start()

    def run(self):
        """
        Execute incoming background tasks until signaled to stop.

        .. warning: This method is called automatically,
                    do not call it yourself.
        """
        if self.ident != get_ident():
            raise SyntaxError("Don't call WorkerPool.run() yourself!")
        while True:
            self.__sem_available_data.acquire()
            with self.__lock:
                if self.__stop:
                    break
                task_group = self.__pending_tasks.pop()
                self.__count_task += len(task_group)
            for task in task_group:
                self.__sem_max_threads.acquire()
                with self.__lock:
                    f = self.__available_workers.pop()
                    self.__busy_workers.add(f)
                f.run_task(task)

    def _worker_thread_finished(self, thread):
        with self.__lock:
            self.__busy_workers.remove(thread)
            self.__available_workers.add(thread)
            self.__count_task -= 1
            self.__sem_max_threads.release()
            if self.__count_task <= 0 and self.__join:
                self.__sem_join.release()
                self.__join = False

    def join_tasks(self):
        """
        Block until all tasks are completed.
        """
        with self.__lock:
            self.__join = True
        self.__sem_join.acquire()

    def add_task_group(self, task_group):
        """
        Add a task group to the pool for execution.

        :param task_group: A task group.
        :type task_group: TaskGroup
        """
        with self.__lock:
            self.__pending_tasks.add(task_group)
            self.__sem_available_data.release()

    def stop(self):
        """
        Stop all threads in the pool.

        The pool cannot be used again after calling this method.
        """
        with self.__lock:
            self.__stop = True
            map(WorkerThread.stop, self.__all_workers)
            self.__sem_available_data.release()
        if self.ident != get_ident():
            self.join()

    def terminate(self):
        """
        Force exit killing all threads.

        The pool cannot be used again after calling this method.

        .. warning: Don't use this except in extreme circumstances!
                    The terminated thread's code may not have a proper chance
                    to clean up its resources or free its locks, and this may
                    lead to memory leaks and/or deadlocks!
        """
        import warnings
        warnings.warn('WorkerPool.terminate() called!', stacklevel=2)
        for worker in self.__all_workers:
            try:
                worker.terminate()
            except:
                import traceback
                traceback.print_exc()