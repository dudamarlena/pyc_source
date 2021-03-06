# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\fittings.py
# Compiled at: 2017-12-11 20:12:50
import sys, stackless, stacklesslib.util
from stacklesslib.util import QueueChannel, atomic
from stacklesslib.errors import CancelledError, AsyncCallFailed

class SyncToAsync(object):
    """
    A syncronous to asynchronous call interface.  A synchronous client can
    use this to make calls to an object that supports an asynchronous calling
    interface.
    The "initiate_call" attribute must be set or defined in a subclass to
    start the asynchrouns call.  The call should then call the "on_success" or
    "on_failure" methods to signal completion.
    """

    def __init__(self):
        self.channel = QueueChannel()
        self.tasklet = None
        return

    def initiate_call(self, args, kwds):
        """This class doesn't know how to initate the call.  Subclass or set
        instance attribute to do that
        """
        raise NotImplementedError()

    def wait(self):
        """Get the result from the call"""
        return self.channel.receive()

    def on_success(self, value):
        """Success callback for the async call.
        Sends sends the value to the caller.
        """
        if not self.return_value(value):
            self.abandoned_success(value)

    def on_failure(self, value):
        """Failure callback for the async call.
        Raises an AsyncCallFailed(value) error to the caller.
        """
        if not self.raise_exception(AsyncCallFailed, value):
            self.abandoned_failure(value)

    def on_success_va(self, *args):
        """Varargs version of on_success"""
        return self.on_success(args)

    def on_success_vakw(self, *args, **kwargs):
        """Varargs and keywords version of on_failure"""
        return self.on_success((args, kwargs))

    def on_failure_va(self, *args):
        """Varargs version of on_success"""
        return self.on_failure(args)

    def on_failure_vakw(self, *args, **kwargs):
        """Varargs and keywords version of on_failure"""
        return self.on_failure((args, kwargs))

    def return_value(self, value):
        """
        Returns a value to the caller.
        Returns False if the caller abandoned the call
        """
        try:
            self.channel.send(value)
        except (ValueError, StopIteration):
            return False

        return True

    def raise_exception(self, exc, val=None, tb=None):
        """
        Raises an exception to the caller.
        Returns False if the caller abandoned the call
        """
        try:
            self.channel.send_throw(exc, val, tb)
        except (ValueError, StopIteration):
            return False

        return True

    def abandoned_success(self, value):
        """
        Called on success when the caller has left.
        Does nothing.
        """
        pass

    def abandoned_failure(self, value):
        """
        Called on failure when the caller has left.
        Calls abandoned_success
        """
        self.abandoned_success(value)

    def cancel(self, *args):
        """rase the CancelledError on any waiting tasklet"""
        with atomic():
            if self.tasklet:
                self.tasklet.throw(CancelledError, args)

    def __call__(self, *args, **kwds):
        with atomic():
            self.tasklet = stackless.getcurrent()
            try:
                self.initiate_call(args, kwds)
                return self.wait()
            finally:
                self.channel.close()
                self.tasklet = None

        return


class AsyncToSync(object):
    """
    Convert from an asynchronous calling model to a synchronous one.  A tasklet is created to
    perform the synchronous call.  On success it will call 'on_success' with the return
    value as the single argument.  If the call raises an exception, 'on_failure' is called
    with the sys.exc_info() tuple as an argument.
    """

    def __init__(self, function, on_success=None, on_failure=None, dispatcher=stacklesslib.util.tasklet_run):
        """
        Set up the conversion call. "function" is the callable to call.
        "on_success" and "on_failure" are the callback functions for success, and exception respectively.
        "dispatcher" is a tasklet creation function.
        """
        self.function = function
        self.on_success = on_success
        self.on_failure = on_failure
        self.dispatcher = dispatcher

    def initiate_call(self, args=(), kwds={}):
        """
        Perform the call.  If successful, then either self.on_success or self.on_failure will be
        called in due time.
        """
        self.dispatcher(self.worker, (args, kwds))

    def worker(self, args, kwds):
        try:
            r = self.function(*args, **kwds)
        except BaseException as e:
            self.on_failure(sys.exc_info())
        else:
            self.on_success(r)