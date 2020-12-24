# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/commands/update.py
# Compiled at: 2018-06-20 17:29:31
# Size of source mod 2**32: 77 bytes
from irk.util.storage import resolv

def update():
    resolv.update_cache()