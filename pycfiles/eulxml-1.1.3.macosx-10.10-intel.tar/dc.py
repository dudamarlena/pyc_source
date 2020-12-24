# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/dc.py
# Compiled at: 2016-02-19 17:15:24
from __future__ import unicode_literals
try:
    import rdflib
except ImportError:
    rdflib = None

from eulxml import xmlmap

class _BaseDublinCore(xmlmap.XmlObject):
    """Base Dublin Core class for common namespace declarations"""
    ROOT_NS = b'http://www.openarchives.org/OAI/2.0/oai_dc/'
    ROOT_NAMESPACES = {b'oai_dc': ROOT_NS, b'dc': b'http://purl.org/dc/elements/1.1/'}


class DublinCoreElement(_BaseDublinCore):
    """Generic Dublin Core element with access to element name and value"""
    name = xmlmap.StringField(b'local-name(.)')
    value = xmlmap.StringField(b'.')


class DublinCore(_BaseDublinCore):
    """
    XmlObject for Simple (unqualified) Dublin Core metadata.

    If no node is specified when initialized, a new, empty Dublin Core
    XmlObject will be created.
    """
    ROOT_NAME = b'dc'
    XSD_SCHEMA = b'http://www.openarchives.org/OAI/2.0/oai_dc.xsd'
    contributor = xmlmap.StringField(b'dc:contributor', required=False)
    contributor_list = xmlmap.StringListField(b'dc:contributor', verbose_name=b'Contributors')
    coverage = xmlmap.StringField(b'dc:coverage', required=False)
    coverage_list = xmlmap.StringListField(b'dc:coverage', verbose_name=b'Coverage')
    creator = xmlmap.StringField(b'dc:creator', required=False)
    creator_list = xmlmap.StringListField(b'dc:creator', verbose_name=b'Creators')
    date = xmlmap.StringField(b'dc:date', required=False)
    date_list = xmlmap.StringListField(b'dc:date', verbose_name=b'Dates')
    description = xmlmap.StringField(b'dc:description', required=False)
    description_list = xmlmap.StringListField(b'dc:description', verbose_name=b'Descriptions')
    format = xmlmap.StringField(b'dc:format', required=False)
    format_list = xmlmap.StringListField(b'dc:format', verbose_name=b'Formats')
    identifier = xmlmap.StringField(b'dc:identifier', required=False)
    identifier_list = xmlmap.StringListField(b'dc:identifier', verbose_name=b'Identifiers')
    language = xmlmap.StringField(b'dc:language', required=False)
    language_list = xmlmap.StringListField(b'dc:language', verbose_name=b'Languages')
    publisher = xmlmap.StringField(b'dc:publisher', required=False)
    publisher_list = xmlmap.StringListField(b'dc:publisher', verbose_name=b'Publishers')
    relation = xmlmap.StringField(b'dc:relation', required=False)
    relation_list = xmlmap.StringListField(b'dc:relation', verbose_name=b'Relations')
    rights = xmlmap.StringField(b'dc:rights', required=False)
    rights_list = xmlmap.StringListField(b'dc:rights', verbose_name=b'Rights')
    source = xmlmap.StringField(b'dc:source', required=False)
    source_list = xmlmap.StringListField(b'dc:source', verbose_name=b'Sources')
    subject = xmlmap.StringField(b'dc:subject', required=False)
    subject_list = xmlmap.StringListField(b'dc:subject', verbose_name=b'Subjects')
    title = xmlmap.StringField(b'dc:title', required=False)
    title_list = xmlmap.StringListField(b'dc:title', verbose_name=b'Titles')
    type = xmlmap.StringField(b'dc:type', required=False)
    type_list = xmlmap.StringListField(b'dc:type', verbose_name=b'Types')
    elements = xmlmap.NodeListField(b'dc:*', DublinCoreElement)
    DCMI_TYPES_RDF = b'http://dublincore.org/2010/10/11/dctype.rdf'
    DCMI_TYPE_URI = b'http://purl.org/dc/dcmitype/'
    if rdflib:
        DCMI_TYPE_URI = rdflib.URIRef(DCMI_TYPE_URI)
        _dcmi_types_graph = None

        @property
        def dcmi_types_graph(self):
            """DCMI Types Vocabulary as an :class:`rdflib.Graph`"""
            if self._dcmi_types_graph is None:
                self._dcmi_types_graph = rdflib.Graph()
                self._dcmi_types_graph.parse(self.DCMI_TYPES_RDF)
            return self._dcmi_types_graph

        _dcmi_types = None

        @property
        def dcmi_types(self):
            """DCMI Type Vocabulary (recommended), as documented at
            http://dublincore.org/documents/dcmi-type-vocabulary/"""
            if self._dcmi_types is None:
                self._dcmi_types = []
                items = self.dcmi_types_graph.subjects(rdflib.RDF.type, rdflib.RDFS.Class)
                for item in items:
                    if (item, rdflib.RDFS.isDefinedBy, self.DCMI_TYPE_URI) in self.dcmi_types_graph:
                        self._dcmi_types.append(str(self.dcmi_types_graph.label(subject=item)))

            return self._dcmi_types

    else:
        dcmi_types_graph = None
        dcmi_types = None