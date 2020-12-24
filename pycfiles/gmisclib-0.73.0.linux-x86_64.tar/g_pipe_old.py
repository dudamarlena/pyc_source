# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_pipe_old.py
# Compiled at: 2007-11-10 17:06:43
"""A multithreaded version of os.popen2().  Note that the argument list
isn't quite the same."""
import os

class pfd(object):
    """Pseudo-file descriptor.  Just like a FD, except
                that it waits for the process at the end of the pipe
                to terminate when you close it.
                """

    def __init__(self, fd, cpid):
        self.fd = os.fdopen(fd, 'r')
        self.cpid = cpid
        self.mode = 'r'
        self.waitval = None
        self.closed = False
        self.readline = self.fd.readline
        self.next = self.fd.next
        self.flush = self.fd.flush
        self.__iter__ = self.fd.__iter__
        self.read = self.fd.read
        self.readlines = self.fd.readlines
        self.fileno = self.fd.fileno
        return

    def read(self):
        return self.fd.read()

    def readline(self):
        return self.fd.readline()

    def readlines(self):
        return self.fd.readlines()

    def next(self):
        return self.fd.next()

    def __iter__(self):
        return self.fd.__iter__()

    def flush():
        pass

    def xreadlines(self, sizehint=-1):
        return self.fd.xreadlines(sizehint)

    def close(self):
        if not self.closed:
            self.fd.close()
            self.closed = True
            pid, t2 = os.waitpid(self.cpid, 0)
            if t2 == 0:
                self.waitval = None
            else:
                self.waitval = t2
        return self.waitval

    def __del__(self):
        self.close()


def popen2(path, args):
    """Forks off a process, and returns the processes
        input and output file descriptors.  The latter is really
        a pfd (defined above).

        Path and args are passed directly into os.execvp().
        """
    rci, wci = os.pipe()
    rco, wco = os.pipe()
    cpid = os.fork()
    if cpid == 0:
        os.close(rco)
        os.close(wci)
        os.dup2(rci, 0)
        os.dup2(wco, 1)
        os.execvp(path, args)
        os._exit(127)
    os.close(rci)
    os.close(wco)
    return (os.fdopen(wci, 'w'), pfd(rco, cpid))


def test():
    si, so = popen2('sed', ['sed', '-e', 's/or/er/'])
    si.write('hello, world!\nsecond line\n')
    si.close()
    assert so.readline() == 'hello, werld!\n'
    a = so.readlines()
    assert len(a) == 1
    assert a[0] == 'second line\n'
    tmp = so.close()
    assert tmp is None
    return


if __name__ == '__main__':
    test()
    test()