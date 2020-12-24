# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/spackl/file/base.py
# Compiled at: 2019-03-09 00:01:34
from spackl.util import ABC, abstractmethod

class BaseFile(ABC):
    _opened = False
    _data = None

    @property
    def opened(self):
        return self._opened

    @abstractmethod
    def _open(self):
        """
            Open the source file

            Should set self._data with the readable object
        """
        raise NotImplementedError()

    def open(self):
        """Open the source file

        Returns:
            None
        """
        if not self._opened:
            self._open()
        if self._data:
            self._opened = True

    @abstractmethod
    def _close(self):
        """
            Close any open file
        """
        raise NotImplementedError()

    def close(self):
        """Close any open file
        """
        if self._data:
            self._close()
        self._data = None
        self._opened = False
        return

    @abstractmethod
    def query(self, **kwargs):
        """
            Reads the open file object

            If not open, should call self.open() first

            Kwargs:
                kwargs : Arbitrary parameters to pass to the query method

            Returns:
                IOResult containing the file data
        """
        raise NotImplementedError()