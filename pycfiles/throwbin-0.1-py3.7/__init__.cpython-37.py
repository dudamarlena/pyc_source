# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\throwbin\__init__.py
# Compiled at: 2020-01-25 11:10:03
# Size of source mod 2**32: 689 bytes
from .constants import AVAILABLE_SYNTAXES
from .exceptions import ThrowBinException
from .PasteModel import PasteModel
import requests

class ThrowBin:

    def __init__(self):
        self.url = 'https://api.throwbin.io/v1'
        self.session = requests.session()

    def post(self, title, text, syntax) -> PasteModel:
        if syntax not in AVAILABLE_SYNTAXES:
            raise ThrowBinException(f"Unknown syntax: '{syntax}'")
        response = self.session.put(f"{self.url}/store",
          data={'title':title, 
         'id':None,  'paste':text,  'syntax':syntax}).json()
        return PasteModel(response['status'], response['id'])