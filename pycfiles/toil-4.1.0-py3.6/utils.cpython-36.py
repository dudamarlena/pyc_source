# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/jobStores/utils.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 11009 bytes
from builtins import object
import codecs, logging, os, errno
from abc import ABCMeta
from abc import abstractmethod
from toil.lib.threading import ExceptionalThread
from future.utils import with_metaclass
log = logging.getLogger(__name__)

class WritablePipe(with_metaclass(ABCMeta, object)):
    __doc__ = "\n    An object-oriented wrapper for os.pipe. Clients should subclass it, implement\n    :meth:`.readFrom` to consume the readable end of the pipe, then instantiate the class as a\n    context manager to get the writable end. See the example below.\n\n    >>> import sys, shutil\n    >>> class MyPipe(WritablePipe):\n    ...     def readFrom(self, readable):\n    ...         shutil.copyfileobj(codecs.getreader('utf-8')(readable), sys.stdout)\n    >>> with MyPipe() as writable:\n    ...     _ = writable.write('Hello, world!\\n'.encode('utf-8'))\n    Hello, world!\n\n    Each instance of this class creates a thread and invokes the readFrom method in that thread.\n    The thread will be join()ed upon normal exit from the context manager, i.e. the body of the\n    `with` statement. If an exception occurs, the thread will not be joined but a well-behaved\n    :meth:`.readFrom` implementation will terminate shortly thereafter due to the pipe having\n    been closed.\n\n    Now, exceptions in the reader thread will be reraised in the main thread:\n\n    >>> class MyPipe(WritablePipe):\n    ...     def readFrom(self, readable):\n    ...         raise RuntimeError('Hello, world!')\n    >>> with MyPipe() as writable:\n    ...     pass\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n\n    More complicated, less illustrative tests:\n\n    Same as above, but proving that handles are closed:\n\n    >>> x = os.dup(0); os.close(x)\n    >>> class MyPipe(WritablePipe):\n    ...     def readFrom(self, readable):\n    ...         raise RuntimeError('Hello, world!')\n    >>> with MyPipe() as writable:\n    ...     pass\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n    >>> y = os.dup(0); os.close(y); x == y\n    True\n\n    Exceptions in the body of the with statement aren't masked, and handles are closed:\n\n    >>> x = os.dup(0); os.close(x)\n    >>> class MyPipe(WritablePipe):\n    ...     def readFrom(self, readable):\n    ...         pass\n    >>> with MyPipe() as writable:\n    ...     raise RuntimeError('Hello, world!')\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n    >>> y = os.dup(0); os.close(y); x == y\n    True\n    "

    @abstractmethod
    def readFrom(self, readable):
        """
        Implement this method to read data from the pipe.

        :param file readable: the file object representing the readable end of the pipe. Do not
        explicitly invoke the close() method of the object, that will be done automatically.
        """
        raise NotImplementedError()

    def _reader(self):
        with os.fdopen(self.readable_fh, 'rb') as (readable):
            self.readable_fh = None
            self.readFrom(readable)
            self.reader_done = True

    def __init__(self):
        super(WritablePipe, self).__init__()
        self.readable_fh = None
        self.writable = None
        self.thread = None
        self.reader_done = False

    def __enter__(self):
        self.readable_fh, writable_fh = os.pipe()
        self.writable = os.fdopen(writable_fh, 'wb')
        self.thread = ExceptionalThread(target=(self._reader))
        self.thread.start()
        return self.writable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writable.close()
        try:
            try:
                if self.thread is not None:
                    self.thread.join()
            except Exception as e:
                if exc_type is None:
                    raise
                else:
                    log.error('Swallowing additional exception in reader thread: %s', str(e))

        finally:
            readable_fh = self.readable_fh
            if readable_fh is not None:
                os.close(readable_fh)


class ReadablePipe(with_metaclass(ABCMeta, object)):
    __doc__ = "\n    An object-oriented wrapper for os.pipe. Clients should subclass it, implement\n    :meth:`.writeTo` to place data into the writable end of the pipe, then instantiate the class\n    as a context manager to get the writable end. See the example below.\n\n    >>> import sys, shutil\n    >>> class MyPipe(ReadablePipe):\n    ...     def writeTo(self, writable):\n    ...         writable.write('Hello, world!\\n'.encode('utf-8'))\n    >>> with MyPipe() as readable:\n    ...     shutil.copyfileobj(codecs.getreader('utf-8')(readable), sys.stdout)\n    Hello, world!\n\n    Each instance of this class creates a thread and invokes the :meth:`.writeTo` method in that\n    thread. The thread will be join()ed upon normal exit from the context manager, i.e. the body\n    of the `with` statement. If an exception occurs, the thread will not be joined but a\n    well-behaved :meth:`.writeTo` implementation will terminate shortly thereafter due to the\n    pipe having been closed.\n\n    Now, exceptions in the reader thread will be reraised in the main thread:\n\n    >>> class MyPipe(ReadablePipe):\n    ...     def writeTo(self, writable):\n    ...         raise RuntimeError('Hello, world!')\n    >>> with MyPipe() as readable:\n    ...     pass\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n\n    More complicated, less illustrative tests:\n\n    Same as above, but proving that handles are closed:\n\n    >>> x = os.dup(0); os.close(x)\n    >>> class MyPipe(ReadablePipe):\n    ...     def writeTo(self, writable):\n    ...         raise RuntimeError('Hello, world!')\n    >>> with MyPipe() as readable:\n    ...     pass\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n    >>> y = os.dup(0); os.close(y); x == y\n    True\n\n    Exceptions in the body of the with statement aren't masked, and handles are closed:\n\n    >>> x = os.dup(0); os.close(x)\n    >>> class MyPipe(ReadablePipe):\n    ...     def writeTo(self, writable):\n    ...         pass\n    >>> with MyPipe() as readable:\n    ...     raise RuntimeError('Hello, world!')\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Hello, world!\n    >>> y = os.dup(0); os.close(y); x == y\n    True\n    "

    @abstractmethod
    def writeTo(self, writable):
        """
        Implement this method to read data from the pipe.

        :param file writable: the file object representing the writable end of the pipe. Do not
        explicitly invoke the close() method of the object, that will be done automatically.
        """
        raise NotImplementedError()

    def _writer(self):
        try:
            with os.fdopen(self.writable_fh, 'wb') as (writable):
                self.writeTo(writable)
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise

    def __init__(self):
        super(ReadablePipe, self).__init__()
        self.writable_fh = None
        self.readable = None
        self.thread = None

    def __enter__(self):
        readable_fh, self.writable_fh = os.pipe()
        self.readable = os.fdopen(readable_fh, 'rb')
        self.thread = ExceptionalThread(target=(self._writer))
        self.thread.start()
        return self.readable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.readable.close()
        try:
            if self.thread is not None:
                self.thread.join()
        except:
            if exc_type is None:
                raise


class ReadableTransformingPipe(ReadablePipe):
    __doc__ = "\n    A pipe which is constructed around a readable stream, and which provides a\n    context manager that gives a readable stream.\n    \n    Useful as a base class for pipes which have to transform or otherwise visit\n    bytes that flow through them, instead of just consuming or producing data.\n    \n    Clients should subclass it and implement :meth:`.transform`, like so:\n    \n    >>> import sys, shutil\n    >>> class MyPipe(ReadableTransformingPipe):\n    ...     def transform(self, readable, writable):\n    ...         writable.write(readable.read().decode('utf-8').upper().encode('utf-8'))\n    >>> class SourcePipe(ReadablePipe):\n    ...     def writeTo(self, writable):\n    ...         writable.write('Hello, world!\\n'.encode('utf-8'))\n    >>> with SourcePipe() as source:\n    ...     with MyPipe(source) as transformed:\n    ...         shutil.copyfileobj(codecs.getreader('utf-8')(transformed), sys.stdout)\n    HELLO, WORLD!\n    \n    The :meth:`.transform` method runs in its own thread, and should move data\n    chunk by chunk instead of all at once. It should finish normally if it\n    encounters either an EOF on the readable, or a :class:`BrokenPipeError` on\n    the writable. This means tat it should make sure to actually catch a\n    :class:`BrokenPipeError` when writing.\n    \n    See also: :class:`toil.lib.misc.WriteWatchingStream`.\n    \n    "

    def __init__(self, source):
        super(ReadableTransformingPipe, self).__init__()
        self.source = source

    @abstractmethod
    def transform(self, readable, writable):
        """
        Implement this method to ship data through the pipe.

        :param file readable: the input stream file object to transform.

        :param file writable: the file object representing the writable end of the pipe. Do not
        explicitly invoke the close() method of the object, that will be done automatically.
        """
        raise NotImplementedError()

    def writeTo(self, writable):
        self.transform(self.source, writable)