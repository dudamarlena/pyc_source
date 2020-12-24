# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/ExtensionSilence.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 4873 bytes
import os

class ExtensionSilence:
    __doc__ = 'Context manager which uses low-level file descriptors to suppress\n    output to stdout/stderr, optionally redirecting to the named file(s).\n \n    >>> import sys, numpy.f2py\n    >>> # build a test fortran extension module with F2PY\n    ...\n    >>> with open(\'hellofortran.f\', \'wb\') as f:\n    ...     f.write(\'\'\'    ...       integer function foo (n)\n    ...           integer n\n    ...           print *, "Hello from Fortran!"\n    ...           print *, "n = ", n\n    ...           foo = n\n    ...       end\n    ...       \'\'\')\n    ...\n    >>> sys.argv = [\'f2py\', \'-c\', \'-m\', \'hellofortran\', \'hellofortran.f\']\n    >>> with ExtensionSilence():\n    ...     # assuming this succeeds, since output is suppressed\n    ...     numpy.f2py.main()\n    ...\n    >>> import hellofortran\n    >>> foo = hellofortran.foo(1)\n     Hello from Fortran!\n     n =  1\n    >>> print "Before silence"\n    Before silence\n    >>> with ExtensionSilence(stdout=\'output.txt\', mode=\'wb\'):\n    ...     print "Hello from Python!"\n    ...     bar = hellofortran.foo(2)\n    ...     with ExtensionSilence():\n    ...         print "This will fall on deaf ears"\n    ...         baz = hellofortran.foo(3)\n    ...     print "Goodbye from Python!"\n    ...\n    ...\n    >>> print "After silence"\n    After silence\n    >>> # ... do some other stuff ...\n    ...\n    >>> with ExtensionSilence(stderr=\'output.txt\', mode=\'a\'):\n    ...     # appending to existing file\n    ...     print >> sys.stderr, "Hello from stderr"\n    ...     print "Stdout redirected to os.devnull"\n    ...\n    ...\n    >>> # check the redirected output\n    ...\n    >>> with open(\'output.txt\', \'r\') as f:\n    ...     print "=== contents of \'output.txt\' ==="\n    ...     print f.read()\n    ...     print "================================"\n    ...\n    === contents of \'output.txt\' ===\n    Hello from Python!\n     Hello from Fortran!\n     n =  2\n    Goodbye from Python!\n    Hello from stderr\n \n    ================================\n    >>> foo, bar, baz\n    (1, 2, 3)\n    >>>\n \n    '

    def __init__(self, stdout=os.devnull, stderr=os.devnull, mode='wb'):
        self.outfiles = (stdout, stderr)
        self.combine = stdout == stderr
        self.mode = mode

    def __enter__(self):
        import sys
        self.sys = sys
        self.saved_streams = saved_streams = (
         sys.__stdout__, sys.__stderr__)
        self.fds = fds = [s.fileno() for s in saved_streams]
        self.saved_fds = map(os.dup, fds)
        for s in saved_streams:
            s.flush()

        if self.combine:
            null_streams = [
             open(self.outfiles[0], self.mode, 0)] * 2
            if self.outfiles[0] != os.devnull:
                sys.stdout, sys.stderr = map(os.fdopen, fds, ['wb'] * 2, [0] * 2)
        else:
            null_streams = [open(f, self.mode, 0) for f in self.outfiles]
        self.null_fds = null_fds = [s.fileno() for s in null_streams]
        self.null_streams = null_streams
        map(os.dup2, null_fds, fds)

    def __exit__(self, *args):
        sys = self.sys
        for s in self.saved_streams:
            s.flush()

        map(os.dup2, self.saved_fds, self.fds)
        sys.stdout, sys.stderr = self.saved_streams
        for s in self.null_streams:
            s.close()

        return False