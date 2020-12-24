# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/RESTinpy/formatters.py
# Compiled at: 2009-04-22 07:30:36
import utils
from xml.sax.saxutils import XMLGenerator
from StringIO import StringIO
DEFAULT_CHARSET = 'utf-8'

class XmlFormatter(object):

    def __init__(self):
        pass

    def format(self, dict):
        self.stream = StringIO()
        self.start_serialization()
        self.ind = 1
        self.start_nodes(dict.itervalues(), self.ind)
        self.end_serialization()
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
        return

    def unformat(self, data):
        pass

    def indent(self, level):
        self.xml.ignorableWhitespace('\n' + '  ' * level)

    def start_serialization(self):
        """
        Start serialization -- open the XML document and the root element.
        """
        self.xml = XMLGenerator(self.stream, encoding=DEFAULT_CHARSET)
        self.xml.startDocument()
        self.xml.startElement('objects', {'version': '1.0', 'xmlns': 'http://rest-in-py.sourceforge.net/ns/', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:schemaLocation': 'http://rest-in-py.sourceforge.net/ns/ http://rest-in-py.sourceforge.net/schema.xsd'})

    def end_serialization(self):
        """
        End serialization -- end the document.
        """
        self.indent(0)
        self.xml.endElement('objects')
        self.xml.endDocument()

    def start_nodes(self, nodes, ind):
        for objects in nodes:
            for obj in objects:
                if self.start_object(obj, ind) is not None:
                    self.end_object(ind)

        return

    def start_object(self, obj, ind):
        """
        Called as each object is handled.
        """
        if obj.has_key('resource'):
            if obj.get('resource') is None:
                return
            else:
                self.indent(ind)
                self.xml.startElement('object', {'resource': obj.get('resource')})
        if obj.has_key('field'):
            self.start_fields(obj.get('field'), ind + 1)
        return not None

    def start_fields(self, value, ind):
        for (k, v) in value.items():
            self.indent(ind)
            if not isinstance(v, dict):
                self.xml.startElement('field', {'property': k})
                self.xml.characters(unicode(v))
                self.xml.endElement('field')
            else:
                v['rel'] = k
                attrs = dict(((k, r) for (k, r) in v.items() if not isinstance(r, list) if r is not None))
                self.xml.startElement('field', attrs)
                children = dict(((k, r) for (k, r) in v.items() if isinstance(r, list)))
                self.start_nodes(children.itervalues(), ind + 1)
                self.xml.endElement('field')

    def end_object(self, ind):
        """
        Called after handling all fields for an object.
        """
        self.indent(ind)
        self.xml.endElement('object')


class JsonFormatter(object):

    def __init__(self):
        pass

    def format(self, obj, fields=None):
        return utils.dumps(obj, ensure_ascii=False)

    def unformat(self, data):
        return simplejson.loads(data)