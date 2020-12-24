# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/as/recipe/filetemplate/tests.py
# Compiled at: 2013-05-03 05:51:32
import doctest, os, time, zc.buildout.testing, zc.buildout.tests

def update_file(dir, *args):
    """Update a file.

    Make sure that the mtime of the file is updated so that buildout notices
    the changes.  The resolution of mtime is system dependent, so we keep
    trying to write until mtime has actually changed."""
    path = os.path.join(dir, *args[:-1])
    original = os.stat(path).st_mtime
    while True:
        f = open(path, 'w')
        f.write(args[(-1)])
        f.flush()
        if os.stat(path).st_mtime != original:
            break
        time.sleep(0.2)


def setUp(test):
    zc.buildout.tests.easy_install_SetUp(test)
    test.globs['update_file'] = update_file
    zc.buildout.testing.install_develop('as.recipe.filetemplate', test)


def test_suite():
    return doctest.DocFileSuite('README.txt', 'tests.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=doctest.NORMALIZE_WHITESPACE)