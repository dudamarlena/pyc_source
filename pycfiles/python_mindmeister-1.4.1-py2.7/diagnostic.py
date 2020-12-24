# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mindmeister/diagnostic.py
# Compiled at: 2012-04-07 16:32:49
"""
Copyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>

This file is part of PythonMindmeister.

PythonMindmeister is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PythonMindmeister is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PythonMindmeister.  If not, see <http://www.gnu.org/licenses/>.

This file implement MindException class,  which is used for error handling within
PythonMindmeister library.

This product uses the MindMeister API but is not endorsed or certified
by MindMeister.
"""

class MindException(Exception):
    """
  This class implements Exception class used for PythonMindmeister errors
  caused by error responses from mindmeister.org.
  """

    def __init__(self, method, data):
        """
    Create new exception from mindmeister error response.

    Arguments:
    method -- name of the failed method
    data -- xml tree of the response
    """
        self.method = method
        self.message = data.attrib['msg']
        self.code = data.attrib['code']

    def __str__(self):
        """
    Convert object to string.
    """
        return str(self.method) + ' failed: ' + str(self.message) + ' (code ' + str(self.code) + ')'