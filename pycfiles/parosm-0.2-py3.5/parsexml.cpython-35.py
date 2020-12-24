# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parosm/parse/parsexml.py
# Compiled at: 2018-04-09 15:30:09
# Size of source mod 2**32: 5786 bytes
import os.path
from queue import Queue
from defusedxml import sax as defusedxml_sax
from xml.sax.handler import ContentHandler
from parosm.parse.parsebase import BaseParser
from parosm.types import OSM, Node, Way, Relation

class Element:
    __doc__ = '\n    XML element\n    not an osm object!!!\n    '

    def __init__(self, tag, attrib=None):
        self.tag = tag
        self.attrib = dict() if attrib is None else attrib


class OSMContentHandler(ContentHandler):
    __doc__ = '\n    Content Handler for XML data\n    '

    def __init__(self):
        """
        Initialize content handler
        """
        super().__init__()
        self._event_queue = Queue()

    def read_events(self):
        """
        Read the read xml events
        :return: xml parser event
        """
        while not self._event_queue.empty():
            yield self._event_queue.get()

    def startElement(self, name, attrs):
        """
        Callback when an element starts
        Signals the start of an element in non-namespace mode.
        :param name: raw xml name
        :param attrs: Attributes interface object
        """
        attrib = {key:attrs.get(key) for key in attrs.getNames()}
        self._event_queue.put(('start', Element(name, attrib)))

    def endElement(self, name):
        """
        Signals the end of an element in non-namespace mode.
        :param name: raw xml name
        """
        self._event_queue.put(('end', Element(name)))


class XMLParser(BaseParser):
    __doc__ = '\n    XMLParser parses the the osm-xml format\n    '

    def __init__(self, file, callback=None):
        """
        Initialize XMLParser

        The callback-method is called when a osm object is found

        def callback(element):
            pass

        :param file: Path to file
        :param callback: Callback for read osm objects
        """
        super().__init__(file, callback)
        self._XMLParser__file = file
        if not os.path.isfile(file):
            raise Exception('is not a file')
        self._XMLParser__callback = self._XMLParser__default_callback if callback is None else callback
        self._XMLParser__parser = defusedxml_sax.make_parser()
        self._XMLParser__handler = OSMContentHandler()
        self._XMLParser__parser.setContentHandler(self._XMLParser__handler)
        self._XMLParser__in_node = False
        self._XMLParser__in_way = False
        self._XMLParser__in_relation = False
        self._XMLParser__in_osm = False
        self._XMLParser__last_event = None
        self._XMLParser__osm_object = None
        self._XMLParser__current_object = None

    @staticmethod
    def __default_callback(element):
        """
        Default callback when no callback is given in init method
        :param element: osm object
        """
        print(str(element))

    def parse(self):
        """
        Starts the parser
        """
        with open(self._XMLParser__file, 'r') as (f):
            for ln, line in enumerate(f):
                try:
                    self._XMLParser__parse_internal(line)
                except AttributeError as e:
                    print(ln)
                    raise e

    def __parse_internal(self, line):
        """
        Internal osm object orchestration from the file
        :param line: current
        """
        self._XMLParser__parser.feed(line)
        for event, element in self._XMLParser__handler.read_events():
            if element.tag == 'osm' and event == 'start':
                self._XMLParser__in_osm = True
                self._XMLParser__osm_object = OSM(element.attrib['version'])
            elif element.tag == 'osm' and event == 'end':
                self._XMLParser__in_osm = False
                self._XMLParser__callback(self._XMLParser__osm_object)
            elif element.tag == 'tag' and event == 'start':
                key = element.attrib['k']
                value = element.attrib['v']
                self._XMLParser__current_object.add_tag(key, value)
            elif element.tag == 'bounds' and event == 'start':
                self._XMLParser__osm_object.set_bounds(**element.attrib)
            else:
                if element.tag == 'bounds' and event == 'end':
                    continue
                if element.tag == 'node' and event == 'start':
                    attrs = element.attrib
                    self._XMLParser__current_object = Node(identifier=attrs['id'], **attrs)
                    self._XMLParser__in_node = True
                elif element.tag == 'node' and event == 'end':
                    self._XMLParser__callback(self._XMLParser__current_object)
                    self._XMLParser__in_node = False
                    self._XMLParser__current_object = None
                elif element.tag == 'way' and event == 'start':
                    attrs = element.attrib
                    self._XMLParser__current_object = Way(identifier=attrs['id'], **attrs)
                    self._XMLParser__in_way = True
                elif element.tag == 'way' and event == 'end':
                    self._XMLParser__callback(self._XMLParser__current_object)
                    self._XMLParser__in_way = False
                    self._XMLParser__current_object = None
                elif element.tag == 'nd' and event == 'start' and self._XMLParser__in_way:
                    self._XMLParser__current_object.add_node(element.attrib['ref'])
                elif element.tag == 'relation' and event == 'start':
                    attrs = element.attrib
                    self._XMLParser__current_object = Relation(identifier=attrs['id'], **attrs)
                    self._XMLParser__in_relation = True
                else:
                    if element.tag == 'relation' and event == 'end':
                        self._XMLParser__callback(self._XMLParser__current_object)
                        self._XMLParser__in_relation = False
                        self._XMLParser__current_object = None
                    else:
                        if element.tag == 'member' and event == 'start' and self._XMLParser__in_relation:
                            attrs = element.attrib
                            self._XMLParser__current_object.add_member(attrs['ref'], attrs['type'], attrs['role'])
                        elif element.tag == 'member' and event == 'end':
                            pass