# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/route_api/avishan/stage.py
# Compiled at: 2020-02-26 08:29:06
# Size of source mod 2**32: 614 bytes
import falcon
from avishan.middlewares import JSONTranslator
from avishan.utils import all_subclasses
from avishan.views import AvishanView

class AvishanFalconStage:

    def __init__(self, middlewares: list=()):
        self.app = self.create_app(middlewares=middlewares)
        for view in all_subclasses(AvishanView):
            url = view.url
            if not url.startswith('/'):
                url = '/' + url
            self.app.add_route(url, view())

    @staticmethod
    def create_app(middlewares: list=()):
        return falcon.API(middleware=([JSONTranslator()] + list(middlewares)))