# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyahooapis\service.py
# Compiled at: 2011-05-16 13:34:50
import os, re, urllib, urllib2
from xml.dom import minidom
import utils
json = utils.import_json()
newline_sub = re.compile('\n').sub
property_match = re.compile('[a-zA-Z].*').match

class Service(object):
    url = 'http://yahoo.co.jp'

    def __init__(self, appid, encoding=None):
        self.appid = appid
        if os.environ.has_key('PYAHOOAPIS_ENCODING'):
            if encoding is not None:
                os.environ['PYAHOOAPIS_ENCODING'] = encoding
        else:
            os.environ['PYAHOOAPIS_ENCODING'] = encoding or 'utf8'
        return

    def _encode_to_utf8(self, text):
        return unicode(text, os.environ['PYAHOOAPIS_ENCODING']).encode('utf8')

    def _get_text(self, node, tagName):
        try:
            return node.getElementsByTagName(tagName)[0].firstChild.nodeValue
        except:
            return

        return

    def _response(self, params):
        return urllib2.urlopen(self.url, data='appid=%s&%s' % (self.appid, urllib.urlencode(params))).read()

    def _setParam(self, params, param, name, split):
        if param is not None:
            params[name] = split.join(map(str, param))
        return

    def _get_dom(self, params):
        params['sentence'] = self._encode_to_utf8(params['sentence'])
        return minidom.parseString(self._remove_newline(self._response(params)))

    def _remove_newline(self, xml):
        return newline_sub('', xml)

    def _binary2list(self, binary, dct):
        return [ dct[key] for key in iter(dct) if binary & key ]

    def _binary2param(self, split, binary, dct):
        return split.join(map(str, self._binary2list(binary, dct)))

    def py2json(self, obj):

        def _py2json(_obj):
            if isinstance(_obj, list):
                return [ _py2json(_o) for _o in _obj ]
            elif isinstance(_obj, BaseObject):
                properties = (p for p in dir(_obj) if property_match(p))
                return dict(((p, _py2json(getattr(_obj, p))) for p in properties))
            else:
                return _obj

        return json.dumps(_py2json(obj), indent=False)


class BaseObject(object):

    def encode(self, text):
        return text.encode(os.environ['PYAHOOAPIS_ENCODING'])