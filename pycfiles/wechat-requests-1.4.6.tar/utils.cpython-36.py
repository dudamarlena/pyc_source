# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\utils.py
# Compiled at: 2018-05-15 22:46:28
# Size of source mod 2**32: 1917 bytes
from six import iteritems
from .compat import json, str, bytes
from .__version__ import __version__, __name__
__all__ = [
 'build_user_agent', 'serialize_dict_to_xml']
_USER_AGENT = None

def build_user_agent():
    global _USER_AGENT
    if _USER_AGENT is None:
        _USER_AGENT = '{}{}'.format(__name__, __version__)
    return _USER_AGENT


class Node(object):

    def __init__(self):
        pass

    def prettify(self):
        raise NotImplementedError('implement prettify in sub class')


class Root(Node):
    PRETTIFY_INDENT = '  '

    def __init__(self):
        self._kvnodes = []

    def append(self, child):
        self._kvnodes.append(child)
        return self

    def prettify(self):
        out = [
         '<xml>']
        for child in self._kvnodes:
            out.append('{}{}'.format(self.PRETTIFY_INDENT, child.prettify()))

        out.append('</xml>')
        return '\n'.join(out)


class KVNode(Node):

    def __init__(self, key, value):
        self.key = key
        if type(value) in (dict, list):
            _value_str = json.dumps(value, ensure_ascii=False)
            self._pretty_value = '<![CDATA[{}]]>'.format(_value_str)
        else:
            if not isinstance(value, bytes):
                self._pretty_value = str(value)
            else:
                self._pretty_value = value
        if type(self._pretty_value) is bytes:
            self._pretty_value = self._pretty_value.decode('utf-8')

    def prettify(self):
        return '<{key}>{value}</{key}>'.format(key=(self.key),
          value=(self._pretty_value))


def serialize_dict_to_xml(**kwargs):
    root = Root()
    for k, v in iteritems(kwargs):
        if v is None:
            pass
        else:
            root.append(KVNode(k, v))

    return root.prettify()