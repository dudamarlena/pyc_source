# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/test_import.py
# Compiled at: 2009-01-14 10:36:41
import mortar, os, unittest

class TestImports(unittest.TestCase):

    def test_imports(self):
        rootdir = os.path.dirname(mortar.__file__)
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            path = dirpath[len(rootdir):]
            segments = path.split(os.sep)
            if '.svn' in segments:
                continue
            base = 'mortar' + ('.').join(segments)
            for filename in filenames:
                if not filename.endswith('.py') or filename.startswith('__init__'):
                    continue
                __import__(base + '.' + filename[:-3])


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(TestImports),))