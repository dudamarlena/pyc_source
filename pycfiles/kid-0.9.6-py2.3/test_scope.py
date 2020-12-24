# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_scope.py
# Compiled at: 2007-07-16 07:02:51
"""Unit Tests for Python scope."""
__revision__ = '$Rev: 421 $'
__author__ = 'David Stanek <dstanek@dstanek.com>'
__copyright__ = 'Copyright 2005, David Stanek'
from os.path import join as joinpath
from tempfile import mkdtemp
from shutil import rmtree
import kid

def setup_module(module):
    global tmpdir
    tmpdir = mkdtemp(prefix='kid_test_scope_')
    kid.path.insert(tmpdir)


def teardown_module(module):
    kid.path.remove(tmpdir)
    rmtree(tmpdir)


def test_scope_1():
    """Test for scoping issue reported in ticket #101.

    Parameters passed into the Template constructor override the
    parameters of functions created with py:def.
    """
    open(joinpath(tmpdir, 'scope.kid'), 'w').write('        <foo xmlns:py="http://purl.org/kid/ns#">\n            <bar py:def="foo(bar)" py:content="bar"/>\n            <bar py:replace="foo(0)" />\n        </foo>\n    ')
    s = kid.Template(file='scope.kid', bar=1).serialize()
    assert '<bar>0</bar>' in s