# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/ping_chem.py
# Compiled at: 2012-05-05 17:30:19
from mrpump.chem import Chem

class PingChem(Chem):

    def appliesTo(self, text):
        return text.lower().strip().startswith('ping')

    def __call__(self, sender_screen_name, text, reply):
        reply('pong')