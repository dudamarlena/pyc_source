# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/__init__.py
# Compiled at: 2012-12-24 07:48:49
"""
This module implements the access to KeePass 1.x-databases.
"""
__authors__ = [
 'Hans Lellelid <hans@xmpl.org>']
__copyright__ = 'Copyright (C) 2012 Karsten-Kai König <kkoenig@posteo.de>'
__license__ = '\nkeepassdb is free software: you can redistribute it and/or modify it under the terms\nof the GNU General Public License as published by the Free Software Foundation,\neither version 3 of the License, or at your option) any later version.\n\nkeepassdb is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR\nA PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nkeepassdb.  If not, see <http://www.gnu.org/licenses/>.\n'
from keepassdb.db import LockingDatabase, Database