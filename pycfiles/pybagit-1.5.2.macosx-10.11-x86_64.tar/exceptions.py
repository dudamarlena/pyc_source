# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pybagit/exceptions.py
# Compiled at: 2014-11-17 11:44:18
__author__ = 'Andrew Hankinson (andrew.hankinson@mail.mcgill.ca)'
__version__ = '1.5'
__date__ = '2011'
__copyright__ = 'Creative Commons Attribution'
__license__ = 'The MIT License\n\n                Permission is hereby granted, free of charge, to any person obtaining a copy\n                of this software and associated documentation files (the "Software"), to deal\n                in the Software without restriction, including without limitation the rights\n                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n                copies of the Software, and to permit persons to whom the Software is\n                furnished to do so, subject to the following conditions:\n\n                The above copyright notice and this permission notice shall be included in\n                all copies or substantial portions of the Software.\n\n                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n                IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n                FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n                LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n                THE SOFTWARE.'

class BagError(Exception):
    """ BagIt Errors """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BagDoesNotExistError(BagError):
    pass


class BagIsNotValidError(BagError):
    pass


class BagCouldNotBeCreatedError(BagError):
    pass


class BagFormatNotRecognized(BagError):
    pass


class BagCheckSumNotValid(BagError):
    pass


class BagFileDownloadError(BagError):
    pass