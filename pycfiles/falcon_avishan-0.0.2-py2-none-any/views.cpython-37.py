# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/route_api/avishan/views.py
# Compiled at: 2020-03-01 13:21:24
# Size of source mod 2**32: 737 bytes
from falcon.request import Request
from falcon.response import Response
from avishan.utils import AvishanRequest, AvishanResponse

class AvishanView:
    url = ''
    request = {}
    response = {}

    def get(self):
        pass

    def post(self):
        pass

    def on_get(self, req: Request, res: Response):
        self.request = AvishanRequest(req=req)
        self.response = AvishanResponse(res=res)
        self.get()
        res.context['response'] = self.response.data

    def on_post(self, req: Request, res: Response):
        self.request = AvishanRequest(req=req)
        self.response = AvishanResponse(res=res)
        self.post()
        res.context['response'] = self.response.data