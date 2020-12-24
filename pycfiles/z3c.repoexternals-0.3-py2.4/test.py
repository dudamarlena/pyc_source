# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/repoexternals/tests/test.py
# Compiled at: 2007-09-27 04:35:54
import os

def setUp(test):
    import os.path, tempfile, StringIO, logging, pysvn
    test.tmpdir = tempfile.mkdtemp()
    repo = os.path.join(test.tmpdir, 'repo')
    (stdin, stdouterr) = os.popen4('svnadmin create ' + repo)
    assert stdouterr.read() == ''
    assert stdin.close() is None
    assert stdouterr.close() is None
    url = 'file://' + repo
    testdir = os.path.dirname(__file__)
    pysvn.Client().import_(os.path.join(testdir, 'repo'), url, '_')
    template = file(os.path.join(testdir, 'EXTERNALS.txt'))
    (fd, externals_path) = tempfile.mkstemp()
    externals = file(externals_path, 'w')
    externals.write(template.read() % {'tmpdir': test.tmpdir})
    externals.close()
    template.close()
    log = StringIO.StringIO()
    logger = logging.getLogger('repoexternals')
    logger.addHandler(logging.StreamHandler(log))
    script = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'bin', 'repoexternals')
    test.globs.update(script=script, url=url, log=log, externals=externals_path)
    import z3c.repoexternals
    test.globs.update(z3c.repoexternals.__dict__)
    return


def tearDown(test):
    import shutil
    shutil.rmtree(test.tmpdir)
    os.remove(test.globs['externals'])


def test_suite():
    import doctest
    return doctest.DocFileSuite('functional.txt', 'script.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite')