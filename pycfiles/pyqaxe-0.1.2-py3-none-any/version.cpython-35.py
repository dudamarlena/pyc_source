# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/args/version.py
# Compiled at: 2016-08-02 13:38:32
# Size of source mod 2**32: 2207 bytes
__all__ = [
 'QrVersion']
_ALIGN_START_TABLE = [
 100, 16, 20, 24, 28, 32, 20, 22, 24, 26,
 28, 30, 32, 24, 24, 24, 28, 28, 28, 32,
 26, 24, 28, 26, 30, 28, 32, 24, 28, 24,
 28, 32, 28, 32, 28, 22, 26, 30, 24, 28]
_ALIGN_STEP_TABLE = [
 100, 100, 100, 100, 100, 100, 16, 18, 20, 22,
 24, 26, 28, 20, 22, 24, 24, 26, 28, 28,
 22, 24, 24, 26, 26, 28, 28, 24, 24, 26,
 26, 26, 28, 28, 24, 26, 26, 26, 28, 28]
_VERSION_PATTERN_VALUE_TABLE = [
 0, 0, 0, 0, 0,
 0, 31892, 34236, 39577, 42195,
 48118, 51042, 55367, 58893, 63784,
 68472, 70749, 76311, 79154, 84390,
 87683, 92361, 96236, 102084, 102881,
 110507, 110734, 117786, 119615, 126325,
 127568, 133589, 136944, 141498, 145311,
 150283, 152622, 158308, 161089, 167017]
_CODEWORD_COUNT_TABLE = [
 26, 44, 70, 100, 134, 172, 196, 242, 292, 346,
 404, 466, 532, 581, 655, 733, 815, 901, 991, 1085,
 1156, 1258, 1364, 1474, 1588, 1706, 1828, 1921, 2051, 2185,
 2323, 2465, 2611, 2761, 2876, 3034, 3196, 3362, 3532, 3706]

class QrVersion(object):

    def __init__(self, version_number):
        assert 1 <= version_number <= 40, 'Version must between 1 and 40.'
        self._num = version_number

    @property
    def number(self):
        """
        :return: The number represent of the version, from 1 to 40.
        :rtype: int
        """
        return self._num

    @property
    def size(self):
        return 17 + 4 * self._num

    @property
    def align_start(self):
        return _ALIGN_START_TABLE[(self.number - 1)]

    @property
    def align_step(self):
        return _ALIGN_STEP_TABLE[(self.number - 1)]

    @property
    def version_pattern_value(self):
        return _VERSION_PATTERN_VALUE_TABLE[(self.number - 1)]

    @property
    def cwc(self):
        """
        CodeWord Count
        """
        return _CODEWORD_COUNT_TABLE[(self.number - 1)]