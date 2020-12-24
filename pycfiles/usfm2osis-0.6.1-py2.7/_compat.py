# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/usfm2osis/_compat.py
# Compiled at: 2015-05-07 19:39:13
"""usfm2osis._compat

Copyright 2012-2015 by Christopher C. Little

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full text of the GNU General Public License is available at:
<http://www.gnu.org/licenses/gpl-3.0.txt>.
"""
from __future__ import unicode_literals
import sys
if sys.version_info[0] == 3:
    _range = range
    _unicode = str
    _unichr = chr
else:
    _range = xrange
    _unicode = unicode
    _unichr = unichr