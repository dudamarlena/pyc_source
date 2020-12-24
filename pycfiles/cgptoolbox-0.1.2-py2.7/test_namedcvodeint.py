# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_namedcvodeint.py
# Compiled at: 2013-01-14 06:47:43
"""Tests for :mod:`cgp.cvodeint.namedcvodeint`."""
from nose.tools import raises
import numpy as np
from ..cvodeint.namedcvodeint import Namedcvodeint

def test_autorestore():
    """Verify that time and state get restored when exiting context manager."""
    n = Namedcvodeint()
    tlist = []
    ylist = []
    for _ in range(2):
        with n.autorestore():
            t, y, _flag = n.integrate(t=1)
        tlist.append(t)
        ylist.append(y)

    np.testing.assert_array_equal(*tlist)
    np.testing.assert_array_equal(*ylist)


@raises(Exception)
def test_autorestore_check_size():
    """Require correct size for state vector."""
    n = Namedcvodeint()
    with n.autorestore(_y=(1, 2, 3)):
        pass


def test_no_p():
    """Test with an ODE without parameters."""

    def ode(_t, y, ydot, _g_data):
        """ODE right-hand side."""
        ydot[:] = -y

    n = Namedcvodeint(ode, t=[0, 1], y=np.ones(1.0).view([('y', float)]))
    with n.autorestore():
        n.integrate()