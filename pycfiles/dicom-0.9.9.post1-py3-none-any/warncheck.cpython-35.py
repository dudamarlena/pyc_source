# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\warncheck.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 1357 bytes
import warnings, unittest
from dicom.test.version_dep import capture_warnings

def assertWarns(self, warn_msg, function, *func_args, **func_kwargs):
    """
    Check that the function generates the expected warning
    with the arguments given.

    warn_msg -- part of the warning string, any warnings should contain this
    function -- the function to call (expected to issue a warning)
    func_args -- positional arguments to the function
    func_kwargs -- keyword arguments to the function

    Return the function return value.
    """
    result, all_warnings = capture_warnings(function, *func_args, **func_kwargs)
    msg = 'Expected one warning; got {0:d}'
    self.assertTrue(len(all_warnings) == 1, msg.format(len(all_warnings)))
    msg = "Expected warning message '{0:s}...'; got '{1:s}'"
    self.assertTrue(warn_msg in all_warnings[0], msg.format(warn_msg, all_warnings[0]))
    return result


def test_warning(the_warning):
    if the_warning:
        warnings.warn(the_warning)


class WarnTests(unittest.TestCase):

    def testWarn(self):
        """Test that assertWarns works as expected"""
        assertWarns(self, 'Look', test_warning, 'Look out')


if __name__ == '__main__':
    unittest.main()