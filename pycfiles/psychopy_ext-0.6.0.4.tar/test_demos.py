# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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