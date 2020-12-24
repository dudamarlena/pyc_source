# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/remote_pdb.py
# Compiled at: 2010-12-12 04:36:57
"""Simple Remote Python Debugger."""
import pdb, socket, sys

class RemoteDebugger(pdb.Pdb):
    """Provides a remote Python debugger.

    Sample Usage:
    >>> debugger = RemoteDebugger()
    >>> debugger.set_trace()

    And then connect via telnet <hostname> 10987.
    """

    def __init__(self, port=10987):
        """Constructor.

        Args:
        port: The port number to use.
        """
        self.old_stdout = sys.stdout
        self.old_stdin = sys.stdin
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), port))
        self.sock.listen(1)
        (client, address) = self.sock.accept()
        fp = client.makefile('rw')
        pdb.Pdb.__init__(self, completekey='tab', stdin=fp, stdout=fp)
        sys.stdout = sys.stdin = fp

    def do_continue(self, unused_arg):
        sys.stdout = self.old_stdout
        sys.stdin = self.old_stdin
        self.sock.close()
        self.set_continue()
        return 1

    do_c = do_cont = do_continue