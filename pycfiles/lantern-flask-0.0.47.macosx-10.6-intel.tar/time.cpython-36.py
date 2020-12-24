# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/utils/time.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 200 bytes
import datetime

def current_ts(tz=datetime.timezone.utc):
    """ returns the current timestamp for the specified timezone """
    return int(datetime.datetime.now(tz).timestamp() * 1000)