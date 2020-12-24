# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/analyze.py
# Compiled at: 2020-01-02 09:34:26
# Size of source mod 2**32: 1126 bytes
from base64 import b64encode
from .model import Model
from ..endpoints import API_PATH

class Analyze(Model):

    def domain(self, domain):
        """Request the PhishDetect Node to statically analyze a domain name.
        :param domain: Domain to analyze.
        """
        return self._phishdetect.post((API_PATH['analyze_domain']), json={'url': domain})

    def link(self, url):
        """Request the PhishDetect Node to dynamically analyze a URL.
        :param url: URL to analyze.
        """
        return self._phishdetect.post((API_PATH['analyze_link']), json={'url': url})

    def html(self, url, html):
        """Request the PhishDetect Node to statically analyze an HTML page.
        :param url: URL of the HTML page.
        :param html: HTML of the page to analyze.
        """
        json = {'url':url, 
         'html':b64encode(html.encode()).decode()}
        return self._phishdetect.post((API_PATH['analyze_html']), json=json)