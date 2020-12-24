# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/responses/redirect.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 276 bytes
from jet_bridge_base.responses.base import Response
from jet_bridge_base.status import HTTP_302_FOUND

class RedirectResponse(Response):

    def __init__(self, url, status=HTTP_302_FOUND):
        self.url = url
        super(RedirectResponse, self).__init__(status=status)