# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/test/test_config.py
# Compiled at: 2009-02-06 08:14:35
"""
Тесты на L{spamfighter.utils.config}.
"""
import os.path, inspect, unittest
from spamfighter.utils.config import _load_file

class ConfigTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.config}.
    """

    def testLoadFile(self):
        config = _load_file(os.path.join(os.path.dirname(inspect.getfile(ConfigTestCase)), 'test_config.xml'))
        self.assertEquals('34', config.aaaa.bbb)
        self.assertEquals(3, config.aaaa.ccc)
        self.assertEquals('c', config.override.nooverride)
        self.assertEquals('B', config.override.doit)
        self.assertEquals('3', config.override.nextlevel)
        self.assertEquals('10', config.override.thirdlevel)
        self.assertEquals('A', config.included)