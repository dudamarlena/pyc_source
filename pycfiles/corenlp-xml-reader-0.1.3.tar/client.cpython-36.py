# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1B9074BA60C16502/works/personal/corenlp-webclient/.venv/lib/python3.6/site-packages/corenlp_webclient/client.py
# Compiled at: 2019-03-15 00:33:02
# Size of source mod 2**32: 1419 bytes
import codecs, json
from typing import Iterable, Union
import requests
from .annotators import BaseAnnotator
from .helpers import create_annotator, make_properties
__all__ = [
 'CoreNlpWebClient']

class CoreNlpWebClient:
    DEFAULT_TIMEOUT = 60

    def __init__(self, url: str, session: requests.Session=None, timeout: Union[(int, float)]=None):
        self._url = url
        self._session = session
        self._timeout = timeout

    def api_call(self, text: str, annotators: Union[(Iterable[BaseAnnotator], BaseAnnotator)]=None, timeout: Union[(int, float)]=None):
        text = text.strip()
        if timeout is None:
            if self._timeout is None:
                timeout = self.DEFAULT_TIMEOUT
            else:
                timeout = self._timeout
        else:
            if annotators is None:
                annotators = list()
            else:
                if not isinstance(annotators, Iterable):
                    annotators = (
                     annotators,)
            properties = make_properties(*annotators)
            if self._session:
                sender = self._session
            else:
                sender = requests
        response = sender.post((self._url),
          params={'properties': json.dumps(properties)},
          data=(codecs.encode(text, 'utf-8')),
          timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data