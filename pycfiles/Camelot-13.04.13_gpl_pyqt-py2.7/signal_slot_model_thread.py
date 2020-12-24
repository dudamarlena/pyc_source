# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/model_thread/signal_slot_model_thread.py
# Compiled at: 2013-04-11 17:47:52
"""
Created on Sep 9, 2009

@author: tw55413
"""
import logging, sys
logger = logging.getLogger('camelot.view.model_thread.signal_slot_model_thread')
from PyQt4 import QtCore
from camelot.core.utils import pyqt
from camelot.core.threading import synchronized
from camelot.view.model_thread import AbstractModelThread, object_thread, setup_model
from camelot.view.controls.exception import register_exception
if pyqt:
    wrap_none = lambda x: x
    unwrap_none = lambda x: x
else:

    class Null(object):
        pass


    null = Null()

    def wrap_none(func):

        def new_func(*args):
            y = func(*args)
            if y == None:
                return null
            else:
                return y

        return new_func


    def unwrap_none(func):

        def new_func(x):
            if x == null:
                x = None
            return func(x)

        return new_func


class Task(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)
    exception = QtCore.pyqtSignal(object)

    def __init__(self, request, name='', args=()):
        """A task to be executed in a different thread
        :param request: the function to execture
        :param name: a string with the name of the task to be used in the gui
        :param args: a tuple with the arguments to be passed to the request
        """
        QtCore.QObject.__init__(self)
        self._request = request
        self._name = name
        self._args = args

    def clear(self):
        """clear this tasks references to other objects"""
        self._request = None
        self._name = None
        self._args = None
        return

    def execute(self):
        logger.debug('executing %s' % self._name)
        try:
            result = self._request(*self._args)
            self.finished.emit(result)
        except StopIteration:
            self.finished.emit(StopIteration())
        except Exception as e:
            exc_info = register_exception(logger, 'exception caught in model thread while executing %s' % self._name, e)
            self.exception.emit(exc_info)
            sys.exc_clear()
        except:
            logger.error('unhandled exception in model thread')
            exc_info = ('Unhandled exception',
             sys.exc_info()[0],
             None,
             'Please contact the application developer', '')
            self.exception.emit(exc_info)
            sys.exc_clear()

        return


class TaskHandler(QtCore.QObject):
    """A task handler is an object that handles tasks that appear in a queue,
    when its handle_task method is called, it will sequentially handle all tasks
    that are in the queue.
    """
    task_handler_busy_signal = QtCore.pyqtSignal(bool)

    def __init__(self, queue):
        """:param queue: the queue from which to pop a task when handle_task
        is called"""
        QtCore.QObject.__init__(self)
        self._mutex = QtCore.QMutex()
        self._queue = queue
        self._tasks_done = []
        self._busy = False
        logger.debug('TaskHandler created.')

    def busy(self):
        """:return True/False: indicating if this task handler is busy"""
        return self._busy

    @QtCore.pyqtSlot()
    def handle_task(self):
        """Handle all tasks that are in the queue"""
        self._busy = True
        self.task_handler_busy_signal.emit(True)
        task = self._queue.pop()
        while task:
            task.execute()
            task.clear()
            self._tasks_done.append(task)
            task = self._queue.pop()

        self.task_handler_busy_signal.emit(False)
        self._busy = False


class SignalSlotModelThread(AbstractModelThread):
    """A model thread implementation that uses signals and slots
    to communicate between the model thread and the gui thread

    there is no explicit model thread verification on these methods,
    since this model thread might not be THE model thread.
    """
    task_available = QtCore.pyqtSignal()

    def __init__(self, setup_thread=setup_model):
        """
        @param setup_thread: function to be called at startup of the thread to initialize
        everything, by default this will setup the model.  set to None if nothing should
        be done.
        """
        super(SignalSlotModelThread, self).__init__(setup_thread)
        self._task_handler = None
        self._mutex = QtCore.QMutex()
        self._request_queue = []
        self._connected = False
        self._setup_busy = True
        return

    def run(self):
        self.logger.debug('model thread started')
        self._task_handler = TaskHandler(self)
        self._task_handler.task_handler_busy_signal.connect(self._thread_busy, QtCore.Qt.QueuedConnection)
        self._thread_busy(True)
        try:
            self._setup_thread()
        except Exception as e:
            exc_info = register_exception(logger, 'Exception when setting up the SignalSlotModelThread', e)
            self.setup_exception_signal.emit(exc_info)

        self._thread_busy(False)
        self.logger.debug('thread setup finished')
        self._task_handler.handle_task()
        self._setup_busy = False
        self.exec_()
        self.logger.debug('model thread stopped')

    @QtCore.pyqtSlot(bool)
    def _thread_busy(self, busy_state):
        self.thread_busy_signal.emit(busy_state)

    @synchronized
    def post(self, request, response=None, exception=None, args=()):
        if not self._connected and self._task_handler:
            self.task_available.connect(self._task_handler.handle_task, QtCore.Qt.QueuedConnection)
            self._connected = True
        if response:
            name = '%s -> %s.%s' % (request.__name__, response.im_self.__class__.__name__, response.__name__)
        else:
            name = request.__name__
        task = Task(wrap_none(request), name=name, args=args)
        if response:
            assert response.im_self != None
            assert isinstance(response.im_self, QtCore.QObject)
            task.finished.connect(unwrap_none(response), QtCore.Qt.QueuedConnection)
        if exception:
            task.exception.connect(exception, QtCore.Qt.QueuedConnection)
        self._request_queue.append(task)
        self.task_available.emit()
        return

    @synchronized
    def stop(self):
        self.quit()
        return True

    @synchronized
    def pop(self):
        """Pop a task from the queue, return None if the queue is empty"""
        if len(self._request_queue):
            task = self._request_queue.pop(0)
            return task

    @synchronized
    def busy(self):
        """Return True or False indicating wether either the model or the
        gui thread is doing something"""
        while not self._task_handler:
            import time
            time.sleep(1)

        app = QtCore.QCoreApplication.instance()
        return app.hasPendingEvents() or len(self._request_queue) or self._task_handler.busy() or self._setup_busy

    def wait_on_work(self):
        """Wait for all work to be finished, this function should only be used
        to do unit testing and such, since it will block the calling thread until
        all work is done"""
        assert object_thread(self)
        app = QtCore.QCoreApplication.instance()
        while self.busy():
            app.processEvents()