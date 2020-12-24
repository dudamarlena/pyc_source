# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/readjson.py
# Compiled at: 2012-10-12 07:02:39
import base64, json, StringIO
from lxml import etree
from xml.sax.saxutils import escape, unescape
from coils.core import *
from coils.core.logic import ActionCommand

def fix_key(key):
    if key[0:1].isdigit():
        key = 'key' + key
    return key


def describe_key_value(key, value):
    key = fix_key(key)
    if value is None:
        return ('<{0}/>').format(key)
    else:
        if isinstance(value, dict):
            return ('<{0} dataType="complex">{1}</{0}>').format(key, describe_dict(value))
        else:
            if isinstance(value, list):
                return ('<{0} dataType="list">{1}</{0}>').format(key, describe_list(value))
            return ('<{0}>{1}</{0}>').format(key, escape(str(value)))
        return


def describe_list(values):
    stream = StringIO.StringIO()
    for value in values:
        if value is None:
            stream.write('<value/>')
        elif isinstance(value, dict):
            stream.write(('<value dataType="complex">{0}</value>').format(describe_dict(value)))
        elif isinstance(value, list):
            stream.write(('<value dataType="list">{0}</value>').format(describe_list(value)))
        else:
            stream.write(('<value>{0}</value>').format(escape(str(value))))

    payload = stream.getvalue()
    stream.close()
    return payload


def describe_dict(collection):
    stream = StringIO.StringIO()
    for key in collection:
        value = collection[key]
        key = fix_key(key)
        if value is None:
            stream.write(('<{0}/>').format(key))
        elif isinstance(value, dict):
            stream.write(('<{0} dataType="complex">{1}</{0}>').format(key, describe_dict(value)))
        elif isinstance(value, list):
            stream.write(('<{0} dataType="list">{1}</{0}>').format(key, describe_list(value)))
        else:
            stream.write(('<{0}>{1}</{0}>').format(key, escape(str(value))))

    payload = stream.getvalue()
    stream.close()
    return payload


class ReadJSONAction(ActionCommand):
    """ ReadJSONActon accepts JSON data as its input message and transforms it to StandardXML. """
    __domain__ = 'action'
    __operation__ = 'read-json'
    __aliases__ = ['readJSON', 'readJSONAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def parse_action_parameters(self):
        self._xpath = self.action_parameters.get('xpath', None)
        self._b64 = self.action_parameters.get('isBase64', 'NO').upper()
        return

    def do_action(self):
        if self._xpath is None:
            self.log.debug('Starting JSON decoding')
            data = json.load(self.rfile)
            self.log.debug('JSON data decoded')
            self.wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
            self.wfile.write('<json>')
            if isinstance(data, dict):
                self.wfile.write(('<value dataType="complex">{0}</value>').format(describe_dict(data)))
            elif isinstance(data, list):
                self.wfile.write(('<value dataType="list">{0}</value>').format(describe_list(data)))
            else:
                self.wfile.write(('<value>{1}</value>').format(escape(str(value))))
            self.wfile.write('</json>')
        else:
            doc = etree.parse(self.rfile)
            jsondata = doc.xpath(self._xpath)[0]
            text = jsondata.text
            data = json.loads(text)
            if isinstance(data, dict):
                text = ('<json><value dataType="complex">{0}</value></json>').format(describe_dict(data))
            elif isinstance(data, list):
                text = ('<json><value dataType="list">{0}</value></json>').format(describe_list(data))
            else:
                text = ('<json><value>{0}</value></json>').format(escape(str(value)))
            xml = etree.fromstring(text)
            text = None
            doc.getroot().replace(jsondata, xml)
            self.wfile.write(etree.tostring(doc))
            doc = None
            xml = None
            jsondata = None
        return

    def do_epilogue(self):
        pass