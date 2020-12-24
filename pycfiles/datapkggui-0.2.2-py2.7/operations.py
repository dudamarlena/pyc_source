# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datapkggui/operations.py
# Compiled at: 2011-10-28 10:17:49
__author__ = 'dgraziotin'
import os, threading, wx, lib, inspect, ctypes, shutil
OPERATION_MESSAGE_ID = wx.NewId()
OPERATION_STATUS_ID = {'started': wx.NewId(), 
   'finished': wx.NewId(), 
   'error': wx.NewId(), 
   'info': wx.NewId()}

def OPERATION_MESSAGE_HANDLER(frame, method):
    frame.Connect(-1, -1, OPERATION_MESSAGE_ID, method)


class KillOperationException(Exception):
    """
    An exception used to Kill an Operation
    """

    def __init__(self, message):
        Exception.__init__(self, message)


class OperationMessage(wx.PyEvent):
    """
    An Event that is used as data format for communication from threads to the GUI.
    An OperationMessage has a type (e.g. SearchOperation), a status (e.g. "finished") and some data (e.g. Packages)
    """

    def __init__(self, type, status, data=None):
        wx.PyEvent.__init__(self)
        self.SetEventType(OPERATION_MESSAGE_ID)
        self.type = type
        self.status = status
        self.data = data


class Operation(threading.Thread):
    """
    Base class defining an operation. The constructor is only responsible for linking a wx object (e.g. a Frame)
    that will be signaled.
    """

    def __init__(self, linked_wxobject):
        threading.Thread.__init__(self)
        self.m_wxobject = linked_wxobject
        self.setDaemon(True)

    def run(self):
        raise NotImplementedError

    def RaiseException(self, exception_type):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        if not inspect.isclass(exception_type):
            raise TypeError('Only types can be raised (not instances)')
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, ctypes.py_object(exception_type))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, 0)
            raise SystemError('PyThreadState_SetAsyncExc failed')


class DownloadOperation(Operation):
    """
    It calls lib.download in a separate thread for retrieving the package and its resources.
    """

    def __init__(self, linked_wxobject, package, download_dir):
        Operation.__init__(self, linked_wxobject)
        self.package = package
        self.download_dir = download_dir
        self.start()

    def run(self):
        wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['started']))
        try:
            result = lib.download('ckan://' + self.package.name, self.download_dir)
        except Exception as e:
            shutil.rmtree(self.download_dir + os.sep + self.package.name, ignore_errors=True)
            wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['error'], str(e)))
            return

        wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['finished']))


class SearchOperation(Operation):
    """
    Given a query, it searches in Ckan using the query. If there are no exceptions,
    it communicates to the main GUI that the the search was finished, returning the retrieved Packages
    in an OperationMessage object.
    """

    def __init__(self, linked_wxobject, query):
        self.query = query
        Operation.__init__(self, linked_wxobject)
        self.start()

    def run(self):
        wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['started']))
        try:
            results = lib.search('ckan://', self.query)
        except Exception as e:
            wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['error'], str(e)))
            return

        wx.PostEvent(self.m_wxobject, OperationMessage(self.__class__, OPERATION_STATUS_ID['finished'], results))