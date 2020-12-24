# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_compiler.py
# Compiled at: 2007-07-16 07:02:51
"""Kid package tests."""
__revision__ = '$Rev: 492 $'
__date__ = '$Date: 2007-07-06 21:38:45 -0400 (Fri, 06 Jul 2007) $'
__author__ = 'Ryan Tomayko (rtomayko@gmail.com)'
__copyright__ = 'Copyright 2004-2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
import sys
from os.path import join as joinpath, exists
import kid, kid.compiler, kid.test.test_kid
check_xml_file = kid.test.test_kid.check_xml_file

def setup_module(module):
    kid.test.test_kid.setup_module(module)


def teardown_module(module):
    kid.test.test_kid.teardown_module(module)


def assert_template_interface(t):
    assert hasattr(t, 'pull')
    assert hasattr(t, 'generate')
    assert hasattr(t, 'write')
    assert hasattr(t, 'serialize')


def test_import_hook():
    kid.enable_import()
    import test.test_if
    assert_template_interface(test.test_if)
    assert sys.modules.has_key('test.test_if')
    kid.disable_import()


def test_pyc_generation():
    from kid.test import template_dir
    kid.enable_import()
    assert not exists(joinpath(template_dir, 'test_content.pyc'))
    import test.test_content
    assert exists(joinpath(template_dir, 'test_content.pyc'))
    assert sys.modules.has_key('test.test_content')


def test_import_and_expand():
    from kid.test import output_dir
    kid.enable_import()
    import test.context as c
    C = c.Template
    out = joinpath(output_dir, 'context.out')
    t = C(foo=10, bar='bla bla')
    it = t.pull()
    for e in it:
        pass

    t.write(out)
    check_xml_file(out)