# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/xml2obj.py
# Compiled at: 2011-12-23 04:19:50
import re, xml.sax.handler

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """
    non_id_char = re.compile('[^_0-9a-zA-Z]')

    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):

        def __init__(self):
            self._attrs = {}
            self.data = None
            return

        def __len__(self):
            return 1

        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key, None)
            else:
                return [
                 self][key]
                return

        def __contains__(self, name):
            return self._attrs.has_key(name)

        def __nonzero__(self):
            return bool(self._attrs or self.data)

        def __getattr__(self, name):
            if name.startswith('__'):
                raise AttributeError(name)
            return self._attrs.get(name, None)

        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [
                     children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value

        def __str__(self):
            return self.data or ''

        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return '{%s}' % (', ').join([ '%s:%s' % (k, repr(v)) for k, v in items ])

    class TreeBuilder(xml.sax.handler.ContentHandler):

        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []

        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)

        def endElement(self, name):
            text = ('').join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)

        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src, basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]