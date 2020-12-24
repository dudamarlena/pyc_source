# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default\presets_default.py
# Compiled at: 2013-09-26 17:04:23
from __future__ import division, absolute_import, print_function, unicode_literals
import os
__rev__ = 20130918
handler = os.path.basename(os.path.dirname(__file__))
handler_path = None
db_default = {b'dbtype': b'sqlite', 
   b'dbname': os.path.expanduser(b'~/default.sqlite')}
profiles = dict()
profiles[(b'Example list ({0})').format(handler)] = {b'handler': handler, 
   b'rev': __rev__, 
   b'db': db_default}
profiles[(b'Example tree ({0})').format(handler)] = {b'handler': handler, 
   b'rev': __rev__, 
   b'treeview': b'tree', 
   b'db': db_default}