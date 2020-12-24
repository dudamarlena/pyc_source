# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/tests/test_releaserdocs.py
# Compiled at: 2008-04-29 08:14:25
"""
Generic Test case for iw.releaser doctest
"""
__docformat__ = 'restructuredtext'
import shutil, subprocess, unittest, doctest, sys, os
from os.path import join
from zope.testing import doctest
from zope.testing import renormalizing
from iw.releaser import testing
current_dir = os.path.dirname(__file__)
package_dir = os.path.join(current_dir, 'data', 'my.package')
backup_dir = package_dir + '_backup'
import zc.buildout.tests, zc.buildout.testing
from zc.buildout.testing import normalize_path
try:
    from subprocess import CalledProcessError
except ImportError:
    CalledProcessError = Exception

def cmd(cmd):
    if cmd == 'svn info':
        return [
         'Path: .', 'URL: http://xxx/my.package/trunk', '...']
    raise NotImplementedError


def check_cmd(cmd):
    for starter in ('svn ', 'python ', 'bin/buildout', 'bin\\buildout'):
        if cmd.startswith(starter):
            return True

    if 'bin/buildout' in cmd:
        return True
    raise CalledProcessError(cmd, 'ok')


def _checkout_tag(*args, **kw):
    pass


def setUp(test):
    import iw.releaser.base, iw.releaser.packet
    iw.releaser.base.command = cmd
    iw.releaser.base.check_command = check_cmd
    iw.releaser.packet._checkout_tag = _checkout_tag
    iw.releaser.packet._run_setup = _checkout_tag
    import base, packet
    base.command = cmd
    base.check_command = check_cmd
    packet._checkout_tag = _checkout_tag
    packet._run_setup = _checkout_tag
    files = ('setup.py', 'CHANGES')
    for file_ in files:
        target = join(package_dir, file_)
        shutil.copyfile(target, target + '.old')

    testing.releaserSetUp(test)


def tearDown(test):
    files = ('setup.py', 'CHANGES')
    for file_ in files:
        target = join(package_dir, file_)
        shutil.copyfile(target + '.old', target)

    testing.releaserTearDown(test)


def doc_suite(test_dir, setUp=setUp, tearDown=tearDown, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    doctest_dir = os.path.join(package_dir, 'doctests')
    globs['test_dir'] = os.path.dirname(__file__)
    docs = [ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') ]
    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, setUp=setUp, tearDown=tearDown, module_relative=False, checker=renormalizing.RENormalizing([testing.normalize_path])))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')