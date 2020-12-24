# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/version_info.py
# Compiled at: 2020-04-18 17:55:45
"""
  Copyright (c) 2020 by Rocky Bernstein

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

  NB. This is not a masterpiece of software, but became more like a hack.
  Probably a complete rewrite would be sensefull. hG/2000-12-27
"""
import sys
PYTHON3 = sys.version_info >= (3, 0)
PYTHON_VERSION = sys.version_info[0] + sys.version_info[1] / 10.0
PYTHON_VERSION_STR = '%s.%s' % (sys.version_info[0], sys.version_info[1])
IS_PYPY = '__pypy__' in sys.builtin_module_names