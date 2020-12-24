# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytest_trepan/__init__.py
# Compiled at: 2018-07-28 15:32:17
"""`pytest-trepan` is a pytest_ plugin running the `trepan debugger
<https://pypi.python.org/pypi?:action=display&name=trepan>`_.

After installing, to set a breakpoint to enter the trepan debugger::

    import pytest
    def test_function():
        pytest.trepan()    # get thee into the debugger!
        x = 1
        ...

The above will look like it is stopped at the *pytest.trepan()*
call. This is most useful when this is the last statement of a
scope. If you want to stop instead before ``x = 1`` pass ``immediate=False`` or just ``False``::

    import pytest
    def test_function():
        ...
        pytest.trepan(immediate=False)
        # same as py.trepan(False)
        x = 1
        ...

You can also pass as keyword arguments any parameter accepted by *trepan.api.debug()*.

To have the debugger entered on error, use the ``--trepan`` option::

    $ py.test --trepan ...

"""
__docformat__ = 'restructuredtext'
from .version import VERSION