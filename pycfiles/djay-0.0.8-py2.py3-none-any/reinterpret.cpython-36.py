# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/assertion/reinterpret.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 1921 bytes
import sys, py
from _pytest.assertion.util import BuiltinAssertionError
u = py.builtin._totext

class AssertionError(BuiltinAssertionError):

    def __init__(self, *args):
        (BuiltinAssertionError.__init__)(self, *args)
        if args:
            if len(args) > 1:
                toprint = args
            else:
                toprint = args[0]
            try:
                self.msg = u(toprint)
            except Exception:
                self.msg = u('<[broken __repr__] %s at %0xd>' % (
                 toprint.__class__, id(toprint)))

        else:
            f = py.code.Frame(sys._getframe(1))
            try:
                source = f.code.fullsource
                if source is not None:
                    try:
                        source = source.getstatement((f.lineno), assertion=True)
                    except IndexError:
                        source = None
                    else:
                        source = str(source.deindent()).strip()
            except py.error.ENOENT:
                source = None

            if source:
                self.msg = reinterpret(source, f, should_fail=True)
            else:
                self.msg = '<could not determine information>'
        if not self.args:
            self.args = (
             self.msg,)


if sys.version_info > (3, 0):
    AssertionError.__module__ = 'builtins'
else:
    if sys.version_info >= (2, 6) or sys.platform.startswith('java'):
        from _pytest.assertion.newinterpret import interpret as reinterpret
    else:
        from _pytest.assertion.oldinterpret import interpret as reinterpret