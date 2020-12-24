# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Outputs/Ros2Cpp/Tests/test_Ros2Cpp.py
# Compiled at: 2019-09-09 15:48:17
import unittest
from RoboticsLanguage.Outputs.Ros2Cpp import Output

class TestRos2Cpp(unittest.TestCase):

    def test_template(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()