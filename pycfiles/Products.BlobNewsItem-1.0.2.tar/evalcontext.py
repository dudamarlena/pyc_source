# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/evalexception/evalcontext.py
# Compiled at: 2012-02-27 07:41:58
from cStringIO import StringIO
import traceback, threading, pdb, sys
exec_lock = threading.Lock()

class EvalContext(object):
    """
    Class that represents a interactive interface.  It has its own
    namespace.  Use eval_context.exec_expr(expr) to run commands; the
    output of those commands is returned, as are print statements.

    This is essentially what doctest does, and is taken directly from
    doctest.
    """

    def __init__(self, namespace, globs):
        self.namespace = namespace
        self.globs = globs

    def exec_expr(self, s):
        out = StringIO()
        exec_lock.acquire()
        save_stdout = sys.stdout
        try:
            debugger = _OutputRedirectingPdb(save_stdout)
            debugger.reset()
            pdb.set_trace = debugger.set_trace
            sys.stdout = out
            try:
                code = compile(s, '<web>', 'single', 0, 1)
                exec code in self.namespace, self.globs
                debugger.set_continue()
            except KeyboardInterrupt:
                raise
            except:
                traceback.print_exc(file=out)
                debugger.set_continue()

        finally:
            sys.stdout = save_stdout
            exec_lock.release()

        return out.getvalue()


class _OutputRedirectingPdb(pdb.Pdb):
    """
    A specialized version of the python debugger that redirects stdout
    to a given stream when interacting with the user.  Stdout is *not*
    redirected when traced code is executed.
    """

    def __init__(self, out):
        self.__out = out
        pdb.Pdb.__init__(self)

    def trace_dispatch(self, *args):
        save_stdout = sys.stdout
        sys.stdout = self.__out
        try:
            return pdb.Pdb.trace_dispatch(self, *args)
        finally:
            sys.stdout = save_stdout