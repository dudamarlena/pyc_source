# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_processing.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 617 bytes
from mediagoblin import processing

class TestProcessing(object):

    def run_fill(self, input, format, output=None):
        builder = processing.FilenameBuilder(input)
        result = builder.fill(format)
        if output is None:
            return result
        assert output == result

    def test_easy_filename_fill(self):
        self.run_fill('/home/user/foo.TXT', '{basename}bar{ext}', 'foobar.txt')

    def test_long_filename_fill(self):
        self.run_fill('{0}.png'.format('A' * 300), 'image-{basename}{ext}', 'image-{0}.png'.format('A' * 245))