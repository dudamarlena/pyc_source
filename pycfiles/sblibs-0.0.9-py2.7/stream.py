# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sblibs/display/stream.py
# Compiled at: 2017-09-18 18:37:05
"""

    This module have a collection of Streams class
    used to implement:

    * Unbuffered(Stream) :: stream wrapper auto flushured
    * Animation(Unbuferred) :: stream with erase methods
    * Clean(Unbuffered) ::  stream with handling paralell conflicts
    * Writing(Unbuffered) :: stream for writing delayed typing

"""
from __future__ import unicode_literals
import time, re
from threading import Lock
from decorating.base import Stream

class Unbuffered(Stream):
    """Unbuffered whose flush automaticly

    That way we don't need flush after a write.

    """
    lock = Lock()

    def __init__(self, stream):
        super(Unbuffered, self).__init__(stream)
        self.stream = stream

    def write(self, message, flush=True):
        """
        Function: write
        Summary: write method on the default stream
        Examples: >>> stream.write('message')
                  'message'
        Attributes:
            @param (message): str-like content to send on stream
            @param (flush) default=True: flush the stdout after write
        Returns: None
        """
        self.stream.write(message)
        if flush:
            self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class Animation(Unbuffered):
    """A stream unbuffered whose write & erase at interval

    After you write something, you can easily clean the buffer
    and restart the points of the older message.
    stream = Animation(stream, delay=0.5)
    self.write('message')

    """
    last_message = b''
    ansi_escape = re.compile(b'\\x1b[^m]*m')

    def __init__(self, stream, interval=0.05):
        super(Animation, self).__init__(stream)
        self.interval = interval

    def write(self, message, autoerase=True):
        """Send something for stdout and erased after delay"""
        super(Animation, self).write(message)
        self.last_message = message
        if autoerase:
            time.sleep(self.interval)
            self.erase(message)

    def erase(self, message=None):
        """Erase something whose you write before: message"""
        if not message:
            message = self.last_message
        super(Animation, self).write(b'\x1b[G')
        super(Animation, self).write(b'\x1b[K')

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class Clean(Unbuffered):
    """A stream wrapper to prepend '
' in each write

    This is used to not break the animations when he is activated

    So in the start_animation we do:
        sys.stdout = Clean(sys.stdout, <paralell-stream>)

    In the stop_animation we do:
        sys.stdout = sys.__stdout__Whose paralell_stream is a Animation object.

    """

    def __init__(self, stream, paralell_stream):
        super(Clean, self).__init__(stream)
        self.paralell_stream = paralell_stream

    def write(self, message, flush=False):
        """Write something on the default stream with a prefixed message"""
        with self.lock:
            self.paralell_stream.erase()
            super(Clean, self).write(message, flush)


class Writting(Unbuffered):
    """
        The Writting stream is a delayed stream whose
        simulate an user Writting something.

  The base class is the AnimationStream

    """

    def __init__(self, stream, delay=0.08):
        super(Writting, self).__init__(stream)
        self.delay = delay

    def write(self, message, flush=True):
        if isinstance(message, bytes):
            message = message.decode(b'utf-8')
        for char in message:
            time.sleep(self.delay * (4 if char == b'\n' else 1))
            super(Writting, self).write(char, flush)