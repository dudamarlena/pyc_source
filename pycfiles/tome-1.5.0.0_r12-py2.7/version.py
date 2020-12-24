# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tome\version.py
# Compiled at: 2013-05-16 20:29:57
"""
Copyright 2013 Brian Mearns

This file is part of Tome.

Tome is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Tome is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Tome.  If not, see <http://www.gnu.org/licenses/>.
"""
RELEASE = 12
MAJOR = 1
MINOR = 5
PATCH = 0
SEMANTIC = 0
YEAR = 2013
MONTH = 5
DAY = 15
COPYRIGHT = YEAR
TAG = None
__months = [
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
assert MONTH > 0 and MONTH <= len(__months)

def setuptools_string():
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += '-x-%s' % TAG
    else:
        vstr += '-r%d' % RELEASE
    return vstr


def string():
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += '-%s' % TAG
    else:
        vstr += '-r%d' % RELEASE
    return vstr


def datestr():
    return '%d %s %02d' % (YEAR, __months[(MONTH - 1)], DAY)