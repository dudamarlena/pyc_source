# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/input/tail.py
# Compiled at: 2012-10-07 05:08:42
from os import stat
from mole.input import Input
import os, sys
from stat import *
from math import floor
from time import sleep, time

class FileTail(object):
    """
    Tail a file, even if its rotated/truncated.
    Inspiration came from the perl module File::Tail.
    """

    def __init__(self, file, start_pos='end', interval=0.1, max_interval=5, max_wait=60, reopen_check='inode'):
        self.start_pos = start_pos
        self.reopen_check = reopen_check
        self.max_wait = max_wait
        self.max_interval = max_interval
        self.interval = interval
        if self.interval > self.max_interval:
            self.interval = self.max_interval
        self.open(file, start_pos=start_pos)
        self._buffer = []
        self.last_time = time()
        self.last_count = 0

    def open(self, file, start_pos='head'):
        """Open the file to tail and initialize our state."""
        fh = open(file, 'r')
        if start_pos == 'end' or start_pos == 'tail':
            fh.seek(0, os.SEEK_END)
        elif start_pos == 'start' or start_pos == 'head':
            pass
        elif start_pos is not None:
            if start_pos >= 0:
                fh.seek(start_pos, os.SEEK_SET)
            else:
                fh.seek(abs(start_pos), os.SEEK_END)
        pos = fh.tell()
        if pos > os.stat(file)[ST_SIZE]:
            pos = fh.tell()
        self.fh = fh
        self.pos = pos
        self.stat = os.fstat(fh.fileno())
        self.file = file
        return

    def reopen(self):
        """
        Attempt to reopen the current file. If it doesn't appear to have
        changed (been rotated) then the current file handle is not changed.
        """
        if not self.fh or self.fh.closed:
            try:
                self.open(self.file, start_pos='head')
            except IOError:
                return False

            return True
        fh = self.fh
        pos = self.pos
        cur = self.stat
        try:
            self.open(self.file, 'head')
        except IOError as e:
            return False

        new = self.stat
        if self.reopen_check == 'inode' and new.st_ino == cur.st_ino or self.reopen_check == 'time' and new.st_mtime <= floor(self.last_time) and new.st_size == pos:
            self.fh = fh
            self.pos = pos
            self.stat = cur
            return False
        return True

    def __iter__(self):
        """
            Return iterator to support:
                for line in filetail:
                    print line
        """
        self.wait_count = 0
        return self

    def __next__(self):
        """Interator "next" call."""
        return self.next()

    def next(self):
        line = None
        self.wait_count = 0
        while not line:
            line = self.fh.readline()
            if line != '':
                self.last_time = time()
                self.last_count = 1
            else:
                self.wait()

        return line

    def wait(self):
        if self.wait_count == 0:
            self.pos = self.fh.tell()
            self.stat = os.fstat(self.fh.fileno())
        self.wait_count += 1
        elapsed = time() - self.last_time
        if elapsed >= self.max_wait:
            self.last_time = time()
            if self.reopen():
                return
        if self.last_count:
            delay = elapsed
        else:
            delay = self.interval
        if delay > self.max_interval:
            delay = self.max_interval
        sleep(delay)

    def tell(self):
        return self.fh.tell()

    def seek(self, pos):
        self.fh.seek(pos)


class InputTail(Input):
    """The Tail monitor input."""

    def __init__(self, name, interval=5):
        self.name = name
        self.interval = interval
        self.tail = FileTail(name, start_pos='start', max_interval=interval)

    def __iter__(self):
        return iter(self.tail)

    def tell(self):
        return self.tail.tell()

    def seek(self, pos):
        self.tail.seek(pos)