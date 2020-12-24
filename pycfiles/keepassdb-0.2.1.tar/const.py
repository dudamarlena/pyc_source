# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/const.py
# Compiled at: 2012-12-24 07:48:49
"""
Some constants used by the application.
"""
__authors__ = [
 'Brett Viren <brett.viren@gmail.com>', 'Hans Lellelid <hans@xmpl.org>']
__license__ = '\nkeepassdb is free software: you can redistribute it and/or modify it under the terms\nof the GNU General Public License as published by the Free Software Foundation,\neither version 3 of the License, or at your option) any later version.\n\nkeepassdb is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR\nA PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nkeepassdb.  If not, see <http://www.gnu.org/licenses/>.\n'
from datetime import datetime
NEVER = datetime(2999, 12, 28, 23, 59, 59)
DB_SIGNATURE1 = 2594363651
DB_SIGNATURE2 = 3041655653
DB_SUPPORTED_VERSION = 196610
DB_SUPPORTED_VERSION_MASK = 4294967040
DB_MAX_CONTENT_LEN = 2147483446