# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/interfaces/Interface.py
# Compiled at: 2016-03-23 14:50:19
from wintx.Fastener import Fastener

class Interface(object):
    """Interface Parent Module"""

    def __init__(self, config_file='/etc/wintx.conf'):
        self.fastener = Fastener(config_file)