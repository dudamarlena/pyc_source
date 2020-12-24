# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\version.py
# Compiled at: 2013-07-26 13:15:12
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.
"""
MAJOR = 1
MINOR = 2
PATCH = 0
SEMANTIC = 0
YEAR = 2013
MONTH = 7
DAY = 26
COPYRIGHT = YEAR
TAG = None
__months = [
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
assert MONTH > 0 and MONTH <= len(__months)

def setuptools_string():
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += '-p-%s' % TAG
    return vstr


def string():
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += '-%s' % TAG
    return vstr


def datestr():
    return '%d %s %02d' % (YEAR, __months[(MONTH - 1)], DAY)