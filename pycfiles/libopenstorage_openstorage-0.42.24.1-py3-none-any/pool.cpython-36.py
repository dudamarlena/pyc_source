# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/threaded/pool.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 6628 bytes
"""Module implementing the Pool for :mod:``requests_toolbelt.threaded``."""
import multiprocessing, requests
from . import thread
from .._compat import queue

class Pool(object):
    __doc__ = "Pool that manages the threads containing sessions.\n\n    :param queue:\n        The queue you're expected to use to which you should add items.\n    :type queue: queue.Queue\n    :param initializer:\n        Function used to initialize an instance of ``session``.\n    :type initializer: collections.Callable\n    :param auth_generator:\n        Function used to generate new auth credentials for the session.\n    :type auth_generator: collections.Callable\n    :param int num_process:\n        Number of threads to create.\n    :param session:\n    :type session: requests.Session\n    "

    def __init__(self, job_queue, initializer=None, auth_generator=None, num_processes=None, session=requests.Session):
        if num_processes is None:
            num_processes = multiprocessing.cpu_count() or 1
        if num_processes < 1:
            raise ValueError('Number of processes should at least be 1.')
        self._job_queue = job_queue
        self._response_queue = queue.Queue()
        self._exc_queue = queue.Queue()
        self._processes = num_processes
        self._initializer = initializer or _identity
        self._auth = auth_generator or _identity
        self._session = session
        self._pool = [thread.SessionThread(self._new_session(), self._job_queue, self._response_queue, self._exc_queue) for _ in range(self._processes)]

    def _new_session(self):
        return self._auth(self._initializer(self._session()))

    @classmethod
    def from_exceptions(cls, exceptions, **kwargs):
        r"""Create a :class:`~Pool` from an :class:`~ThreadException`\ s.

        Provided an iterable that provides :class:`~ThreadException` objects,
        this classmethod will generate a new pool to retry the requests that
        caused the exceptions.

        :param exceptions:
            Iterable that returns :class:`~ThreadException`
        :type exceptions: iterable
        :param kwargs:
            Keyword arguments passed to the :class:`~Pool` initializer.
        :returns: An initialized :class:`~Pool` object.
        :rtype: :class:`~Pool`
        """
        job_queue = queue.Queue()
        for exc in exceptions:
            job_queue.put(exc.request_kwargs)

        return cls(job_queue=job_queue, **kwargs)

    @classmethod
    def from_urls(cls, urls, request_kwargs=None, **kwargs):
        """Create a :class:`~Pool` from an iterable of URLs.

        :param urls:
            Iterable that returns URLs with which we create a pool.
        :type urls: iterable
        :param dict request_kwargs:
            Dictionary of other keyword arguments to provide to the request
            method.
        :param kwargs:
            Keyword arguments passed to the :class:`~Pool` initializer.
        :returns: An initialized :class:`~Pool` object.
        :rtype: :class:`~Pool`
        """
        request_dict = {'method': 'GET'}
        request_dict.update(request_kwargs or {})
        job_queue = queue.Queue()
        for url in urls:
            job = request_dict.copy()
            job.update({'url': url})
            job_queue.put(job)

        return cls(job_queue=job_queue, **kwargs)

    def exceptions(self):
        """Iterate over all the exceptions in the pool.

        :returns: Generator of :class:`~ThreadException`
        """
        while True:
            exc = self.get_exception()
            if exc is None:
                break
            yield exc

    def get_exception(self):
        """Get an exception from the pool.

        :rtype: :class:`~ThreadException`
        """
        try:
            request, exc = self._exc_queue.get_nowait()
        except queue.Empty:
            return
        else:
            return ThreadException(request, exc)

    def get_response(self):
        """Get a response from the pool.

        :rtype: :class:`~ThreadResponse`
        """
        try:
            request, response = self._response_queue.get_nowait()
        except queue.Empty:
            return
        else:
            return ThreadResponse(request, response)

    def responses(self):
        """Iterate over all the responses in the pool.

        :returns: Generator of :class:`~ThreadResponse`
        """
        while True:
            resp = self.get_response()
            if resp is None:
                break
            yield resp

    def join_all(self):
        """Join all the threads to the master thread."""
        for session_thread in self._pool:
            session_thread.join()


class ThreadProxy(object):
    proxied_attr = None

    def __getattr__(self, attr):
        """Proxy attribute accesses to the proxied object."""
        get = object.__getattribute__
        if attr not in self.attrs:
            response = get(self, self.proxied_attr)
            return getattr(response, attr)
        else:
            return get(self, attr)


class ThreadResponse(ThreadProxy):
    __doc__ = 'A wrapper around a requests Response object.\n\n    This will proxy most attribute access actions to the Response object. For\n    example, if you wanted the parsed JSON from the response, you might do:\n\n    .. code-block:: python\n\n        thread_response = pool.get_response()\n        json = thread_response.json()\n\n    '
    proxied_attr = 'response'
    attrs = frozenset(['request_kwargs', 'response'])

    def __init__(self, request_kwargs, response):
        self.request_kwargs = request_kwargs
        self.response = response


class ThreadException(ThreadProxy):
    __doc__ = 'A wrapper around an exception raised during a request.\n\n    This will proxy most attribute access actions to the exception object. For\n    example, if you wanted the message from the exception, you might do:\n\n    .. code-block:: python\n\n        thread_exc = pool.get_exception()\n        msg = thread_exc.message\n\n    '
    proxied_attr = 'exception'
    attrs = frozenset(['request_kwargs', 'exception'])

    def __init__(self, request_kwargs, exception):
        self.request_kwargs = request_kwargs
        self.exception = exception


def _identity(session_obj):
    return session_obj


__all__ = [
 'ThreadException', 'ThreadResponse', 'Pool']