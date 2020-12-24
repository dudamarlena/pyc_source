# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redlink/analysis.py
# Compiled at: 2015-11-07 08:21:00
import logging, json
from xml.dom import minidom
from rdflib.graph import Graph
from .client import RedlinkClient
from .format import from_mimetype, Format

class RedlinkAnalysis(RedlinkClient):
    """
    Redlink Analysis Client
    """
    path = 'analysis'
    enhance_path = 'enhance'

    def __init__(self, key):
        """
        @type key: str
        @param key: api key
        """
        super(RedlinkAnalysis, self).__init__(key)

    def enhance(self, content, input=Format.TEXT, output=Format.JSON):
        """
        Enhance the content

        @type content: str
        @param content: target content

        @type input: C{FormatDef}
        @param input: input type

        @type output: C{FormatDef}
        @param output: output type

        @return: enhancements
        """
        analysis = self.status['analyses'][0]
        params = {self.param_in: input.name, 
           self.param_out: output.name}
        resource = self._build_url('/%s/%s/%s' % (self.path, analysis, self.enhance_path), params)
        logging.debug('Making request to %s' % resource)
        response = self._post(resource, content, input.mimetype, output.mimetype)
        if response.status_code != 200:
            logging.error('Enhance request returned %d: %s' % (response.status_code, response.reason))
            return response.text
        else:
            content_type = from_mimetype(response.headers['Content-Type'])
            if content_type == Format.JSON or content_type == Format.REDLINKJSON:
                return json.loads(response.text)
            if content_type == Format.XML or content_type == Format.REDLINKXML:
                return minidom.parse(response.text)
            if content_type.rdflibMapping:
                g = Graph()
                g.parse(data=response.text, format=content_type.rdflibMapping)
                return g
            logging.warn('Handler not found for %s, so returning raw text response...' % content_type.mimetype)
            return response.text