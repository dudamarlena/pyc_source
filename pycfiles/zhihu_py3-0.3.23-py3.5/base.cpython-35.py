# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zhihu/base.py
# Compiled at: 2016-04-21 06:36:55
# Size of source mod 2**32: 1631 bytes
from .common import BeautifulSoup
from requests import Response
import json

class BaseZhihu:

    def _gen_soup(self, content):
        self.soup = BeautifulSoup(content)

    def _get_content(self):
        url = self._url if hasattr(self, '_url') else self.url
        if url.endswith('/'):
            resp = self._session.get(url[:-1])
        else:
            resp = self._session.get(url)
        class_name = self.__class__.__name__
        if class_name == 'Answer':
            if 'answer' in resp.url:
                self._deleted = False
            else:
                self._deleted = True
        elif class_name == 'Question':
            self._deleted = resp.status_code == 404
        return resp.content

    def _make_soup(self):
        if self.url and not self.soup:
            self._gen_soup(self._get_content())

    def refresh(self):
        self._gen_soup(self._get_content())

    @classmethod
    def from_html(cls, content):
        obj = cls(url=None)
        obj._gen_soup(content)
        return obj


class JsonAsSoupMixin:

    def _gen_soup(self, content):
        if isinstance(content, bytes):
            r = Response()
            r._content = content
            soup = r.json()
            self.soup = soup
        else:
            if isinstance(content, str):
                self.soup = json.loads(content)
            else:
                self.soup = content