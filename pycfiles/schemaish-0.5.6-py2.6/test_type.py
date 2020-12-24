# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schemaish/tests/test_type.py
# Compiled at: 2010-03-01 05:17:17
import unittest

class FileTests(unittest.TestCase):

    def _makeOne(self, *arg, **kw):
        from schemaish.type import File
        return File(*arg, **kw)

    def test_ctor(self):
        f = self._makeOne('file', 'filename', 'mimetype')
        self.assertEqual(f.file, 'file')
        self.assertEqual(f.filename, 'filename')
        self.assertEqual(f.mimetype, 'mimetype')
        self.assertEqual(f.metadata, {})

    def test_repr_with_file(self):
        f = self._makeOne('file', 'filename', 'mimetype')
        result = repr(f)
        self.failUnless(result.startswith('<schemaish.type.File file="\'file\'" filename="filename"'))
        self.failUnless(result.endswith('mimetype="mimetype", metadata="{}" >'))