# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/select.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 5930 bytes
__doc__ = '\nSelectors for the Posix event loop.\n'
from __future__ import unicode_literals, absolute_import
import sys, abc, errno, select, six
__all__ = ('AutoSelector', 'PollSelector', 'SelectSelector', 'Selector', 'fd_to_int')

def fd_to_int(fd):
    if not isinstance(fd, int):
        if not hasattr(fd, 'fileno'):
            raise AssertionError
    if isinstance(fd, int):
        return fd
    else:
        return fd.fileno()


class Selector(six.with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def register(self, fd):
        assert isinstance(fd, int)

    @abc.abstractmethod
    def unregister(self, fd):
        assert isinstance(fd, int)

    @abc.abstractmethod
    def select(self, timeout):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class AutoSelector(Selector):

    def __init__(self):
        self._fds = []
        self._select_selector = SelectSelector()
        self._selectors = [self._select_selector]
        if hasattr(select, 'poll'):
            self._poll_selector = PollSelector()
            self._selectors.append(self._poll_selector)
        else:
            self._poll_selector = None
        if sys.version_info >= (3, 5):
            self._py3_selector = Python3Selector()
            self._selectors.append(self._py3_selector)
        else:
            self._py3_selector = None

    def register(self, fd):
        assert isinstance(fd, int)
        self._fds.append(fd)
        for sel in self._selectors:
            sel.register(fd)

    def unregister(self, fd):
        assert isinstance(fd, int)
        self._fds.remove(fd)
        for sel in self._selectors:
            sel.unregister(fd)

    def select(self, timeout):
        if self._py3_selector:
            try:
                return self._py3_selector.select(timeout)
            except PermissionError:
                pass

        try:
            return self._select_selector.select(timeout)
        except ValueError:
            if self._poll_selector is not None:
                return self._poll_selector.select(timeout)
            raise

    def close(self):
        for sel in self._selectors:
            sel.close()


class Python3Selector(Selector):
    """Python3Selector"""

    def __init__(self):
        assert sys.version_info >= (3, 5)
        import selectors
        self._sel = selectors.DefaultSelector()

    def register(self, fd):
        assert isinstance(fd, int)
        import selectors
        self._sel.register(fd, selectors.EVENT_READ, None)

    def unregister(self, fd):
        assert isinstance(fd, int)
        self._sel.unregister(fd)

    def select(self, timeout):
        events = self._sel.select(timeout=timeout)
        return [key.fileobj for key, mask in events]

    def close(self):
        self._sel.close()


class PollSelector(Selector):

    def __init__(self):
        self._poll = select.poll()

    def register(self, fd):
        assert isinstance(fd, int)
        self._poll.register(fd, select.POLLIN)

    def unregister(self, fd):
        assert isinstance(fd, int)

    def select(self, timeout):
        tuples = self._poll.poll(timeout)
        return [t[0] for t in tuples]

    def close(self):
        pass


class SelectSelector(Selector):
    """SelectSelector"""

    def __init__(self):
        self._fds = []

    def register(self, fd):
        self._fds.append(fd)

    def unregister(self, fd):
        self._fds.remove(fd)

    def select(self, timeout):
        while True:
            try:
                return select.select(self._fds, [], [], timeout)[0]
            except select.error as e:
                if e.args:
                    if e.args[0] == errno.EINTR:
                        continue
                else:
                    raise

    def close(self):
        pass


def select_fds(read_fds, timeout, selector=AutoSelector):
    """
    Wait for a list of file descriptors (`read_fds`) to become ready for
    reading. This chooses the most appropriate select-tool for use in
    prompt-toolkit.
    """
    fd_map = dict((fd_to_int(fd), fd) for fd in read_fds)
    sel = selector()
    try:
        for fd in read_fds:
            sel.register(fd)

        result = sel.select(timeout)
        if result is not None:
            return [fd_map[fd_to_int(fd)] for fd in result]
    finally:
        sel.close()