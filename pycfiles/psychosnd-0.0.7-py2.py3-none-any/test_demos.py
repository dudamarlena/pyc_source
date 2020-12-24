# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/tests/test_demos.py
# Compiled at: 2016-09-23 15:30:59
import sys, os, subprocess, unittest

class TestExp(unittest.TestCase):

    def test_gui(self):
        subprocess.call([sys.executable, 'psychopy_ext/demos/run.py'], shell=False)

    def test_exp(self):
        for name in ['main', 'twotasks', 'staircase', 'perclearn']:
            command = '%s psychopy_ext/demos/run.py %s exp run --n --debug --unittest' % (sys.executable, name)
            subprocess.call(command.split(), shell=False)


if __name__ == '__main__':
    unittest.main()