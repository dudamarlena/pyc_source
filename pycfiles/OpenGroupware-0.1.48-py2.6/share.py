# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/horde/apis/share.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from api import HordeAPI

class HordeShareAPI(HordeAPI):

    def api_share_getsharelist(self, args):
        import pprint
        pprint.pprint(args)
        return []