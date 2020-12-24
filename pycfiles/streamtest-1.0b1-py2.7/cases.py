# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/streamtest/cases.py
# Compiled at: 2018-05-11 00:39:01
from unittest import TestCase
from .context import _StreamContext

class CatchStreamTestCase(TestCase):

    def catch_stream(slef, stream_type):
        """A function to return the context manager.

        Args:
            stream_type (str): The string of stream type: 'stdout' or 'stderr'

        Example:

            >>> with self.catch_stream("stdout") as stream:
            ...     print "Hello World!"

            >>> assert stream == "Hello World!"

        """
        context = _StreamContext(stream_type)
        return context