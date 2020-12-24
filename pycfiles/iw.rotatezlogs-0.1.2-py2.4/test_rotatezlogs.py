# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/rotatezlogs/tests/test_rotatezlogs.py
# Compiled at: 2008-07-29 13:25:22
"""Testing rotatezlogs

$Id: test_rotatezlogs.py 5751 2006-06-05 19:40:05Z glenfant $
"""
import unittest, tempfile, logging, os, sys
from ZConfig.components.logger.tests import test_logger
from ZConfig import ConfigurationSyntaxError
from iw.rotatezlogs import LogHandlers as lhs

class TestRotatelogConfig(test_logger.TestConfig):
    """Note that we run all original tests too for regression purpose
    to check if our config doesn't screw up standard config.  See base
    class to see how we create new tests """
    __module__ = __name__
    _schematext = '\n      <schema>\n      <import package="ZConfig.components.logger"/>\n        <import package="iw.rotatezlogs"/>\n        <section type="eventlog" name="*" attribute="eventlog"/>\n      </schema>\n      '

    def test_with_rotatelog1(self):
        """With rotatezlog, no path"""
        logger_def = '<eventlog>\n  <rotatelogfile>\n  </rotatelogfile>\n</eventlog>'
        self.failUnlessRaises(ConfigurationSyntaxError, self.check_simple_logger, logger_def)

    def test_with_rotatelog2(self):
        """With rotatezlog with path but no max-bytes"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n  </rotatelogfile>\n</eventlog>' % fn
        self.failUnlessRaises(ConfigurationSyntaxError, self.check_simple_logger, logger_def)

    def test_with_rotatelog3(self):
        """With rotatezlog with path, max-bytes, no backup-count"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n    max-bytes 100KB\n  </rotatelogfile>\n</eventlog>' % fn
        self.failUnlessRaises(ConfigurationSyntaxError, self.check_simple_logger, logger_def)

    def test_with_rotatelog4(self):
        """With rotatezlog with path, max-bytes, backup-count, invalid compression"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n    max-bytes 100KB\n    backup-count 5\n    compression invalid\n  </rotatelogfile>\n</eventlog>' % fn
        self.failUnlessRaises(ConfigurationSyntaxError, self.check_simple_logger, logger_def)

    def test_with_rotatelog5(self):
        """With rotatezlog with all options set, default compression"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n    max-bytes 100KB\n    backup-count 5\n    level warning\n  </rotatelogfile>\n</eventlog>' % fn
        logger = self.check_simple_logger(logger_def)
        handler = logger.handlers[0]
        self.failUnless(isinstance(handler, lhs.RotateFileHandler))
        self.assertEqual(handler.maxBytes, 100 * 1024)
        self.assertEqual(handler.backupCount, 5)
        self.assertEqual(handler.level, logging.WARNING)
        self.failUnless(isinstance(handler.compressor, lhs.NoneCompressor))
        handler.close()
        os.remove(fn)

    def test_compressor_zip(self):
        """Selection of zip compression"""
        self._test_compressor_select('zip', lhs.ZipCompressor)

    def test_compressor_gzip(self):
        """Selection of gzip compression"""
        self._test_compressor_select('gzip', lhs.GzipCompressor)

    def test_compressor_bzip2(self):
        """Selection of bzip2 compression"""
        self._test_compressor_select('bzip2', lhs.Bzip2Compressor)

    def _test_compressor_select(self, compression_mode, compressor_klass):
        """Generic test for the compressor selection"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n    max-bytes 100KB\n    backup-count 5\n    compression %s\n    level warning\n  </rotatelogfile>\n</eventlog>' % (fn, compression_mode)
        logger = self.check_simple_logger(logger_def)
        handler = logger.handlers[0]
        self.failUnless(isinstance(handler, lhs.RotateFileHandler))
        self.assertEqual(handler.maxBytes, 100 * 1024)
        self.assertEqual(handler.backupCount, 5)
        self.assertEqual(handler.level, logging.WARNING)
        self.failUnless(isinstance(handler.compressor, compressor_klass))
        handler.close()
        os.remove(fn)

    def test_file_rotation1(self):
        """We'll try to fill and rotate some logs, no compression"""
        self._test_rotated_files('none', '.%d')

    def test_file_rotation2(self):
        """We'll try to fill and rotate some logs, zip compression"""
        self._test_rotated_files('zip', '.%d.zip')

    def test_file_rotation3(self):
        """We'll try to fill and rotate some logs, gzip compression"""
        self._test_rotated_files('gzip', '.%d.gz')

    def test_file_rotation4(self):
        """We'll try to fill and rotate some logs, bzip2 compression"""
        try:
            import bz2
            self._test_rotated_files('bzip2', '.%d.bz2')
        except ImportError, e:
            self._test_rotated_files('bzip2', '.%d')

    def _test_rotated_files(self, compression_mode, ext_template):
        """Common method for checking files"""
        fn = tempfile.mktemp()
        logger_def = '<eventlog>\n  <rotatelogfile>\n    path %s\n    max-bytes 2KB\n    backup-count 2\n    compression %s\n    level warning\n  </rotatelogfile>\n</eventlog>' % (fn, compression_mode)
        logger = self.check_simple_logger(logger_def)
        handler = logger.handlers[0]
        for i in xrange(1000):
            logger.error('Houston, we got a problem')

        basename = os.path.basename(fn)
        dirname = os.path.dirname(fn)
        for i in xrange(1, handler.backupCount + 1):
            ext = ext_template % i
            rot_log_path = os.path.join(dirname, basename + ext)
            self.failUnless(os.path.exists(rot_log_path))
            os.remove(rot_log_path)

        handler.close()
        os.remove(fn)


def test_suite():
    return unittest.makeSuite(TestRotatelogConfig)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')