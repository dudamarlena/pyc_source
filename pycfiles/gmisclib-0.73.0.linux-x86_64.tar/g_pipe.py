# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_pipe.py
# Compiled at: 2010-06-22 06:59:49
"""A multithreaded version of os.popen2().  Note that the argument list
isn't quite the same."""
import subprocess as S

class pfd(object):
    """Pseudo-file descriptor.  Just like a FD, except
                that it waits for the process at the end of the pipe
                to terminate when you close it.
                """

    def __init__(self, p):
        self.fd = p.stdout
        assert p is not None
        self.p = p
        self.mode = 'r'
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

    def flush(self):
        pass

    def xreadlines(self, sizehint=-1):
        return self.fd.xreadlines(sizehint)

    def close(self):
        if not self.closed:
            self.fd.close()
            self.closed = True
            self.p.wait()
        return self.p.returncode

    def __del__(self):
        self.close()


def popen2(path, args, bufsize=0):
    """Forks off a process, and returns the processes
        input and output file descriptors.  The latter is really
        a pfd (defined above).

        Path and args are passed directly into os.execvp().
        """
    p = S.Popen(args, executable=path, stdin=S.PIPE, stdout=S.PIPE, close_fds=True)
    return (p.stdin, pfd(p))


def test--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL           0  'popen2'
                3  LOAD_CONST               'sed'
                6  LOAD_CONST               'sed'
                9  LOAD_CONST               '-e'
               12  LOAD_CONST               's/or/er/'
               15  BUILD_LIST_3          3 
               18  CALL_FUNCTION_2       2  None
               21  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST            0  'si'
               27  STORE_FAST            1  'so'

 L.  90        30  LOAD_FAST             0  'si'
               33  LOAD_ATTR             1  'write'
               36  LOAD_CONST               'hello, world!\nsecond line\n'
               39  CALL_FUNCTION_1       1  None
               42  POP_TOP          

 L.  91        43  LOAD_FAST             0  'si'
               46  LOAD_ATTR             2  'close'
               49  CALL_FUNCTION_0       0  None
               52  POP_TOP          

 L.  92        53  LOAD_FAST             1  'so'
               56  LOAD_ATTR             3  'readline'
               59  CALL_FUNCTION_0       0  None
               62  LOAD_CONST               'hello, werld!\n'
               65  COMPARE_OP            2  ==
               68  POP_JUMP_IF_TRUE     77  'to 77'
               71  LOAD_ASSERT              AssertionError
               74  RAISE_VARARGS_1       1  None

 L.  93        77  LOAD_FAST             1  'so'
               80  LOAD_ATTR             5  'readlines'
               83  CALL_FUNCTION_0       0  None
               86  STORE_FAST            2  'a'

 L.  94        89  LOAD_GLOBAL           6  'len'
               92  LOAD_FAST             2  'a'
               95  CALL_FUNCTION_1       1  None
               98  LOAD_CONST               1
              101  COMPARE_OP            2  ==
              104  POP_JUMP_IF_TRUE    113  'to 113'
              107  LOAD_ASSERT              AssertionError
              110  RAISE_VARARGS_1       1  None

 L.  95       113  LOAD_FAST             2  'a'
              116  LOAD_CONST               0
              119  BINARY_SUBSCR    
              120  LOAD_CONST               'second line\n'
              123  COMPARE_OP            2  ==
              126  POP_JUMP_IF_TRUE    135  'to 135'
              129  LOAD_ASSERT              AssertionError
              132  RAISE_VARARGS_1       1  None

 L.  96       135  LOAD_FAST             1  'so'
              138  LOAD_ATTR             2  'close'
              141  CALL_FUNCTION_0       0  None
              144  STORE_FAST            3  'tmp'

 L.  97       147  LOAD_FAST             3  'tmp'
              150  LOAD_CONST               None
              153  COMPARE_OP            8  is
              156  POP_JUMP_IF_TRUE    172  'to 172'
              159  LOAD_ASSERT              AssertionError
              162  LOAD_CONST               'tmp=%s'
              165  LOAD_FAST             3  'tmp'
              168  BINARY_MODULO    
              169  RAISE_VARARGS_2       2  None
              172  LOAD_CONST               None
              175  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 172


if __name__ == '__main__':
    test()
    test()