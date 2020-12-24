# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/teimap.py
# Compiled at: 2016-06-01 14:16:48
from __future__ import unicode_literals
from eulxml import xmlmap
TEI_NAMESPACE = b'http://www.tei-c.org/ns/1.0'

class _TeiBase(xmlmap.XmlObject):
    """Common TEI namespace declarations, for use by all TEI XmlObject instances."""
    ROOT_NS = TEI_NAMESPACE
    ROOT_NAME = b'tei'
    ROOT_NAMESPACES = {b'tei': ROOT_NS, 
       b'xml': b'http://www.w3.org/XML/1998/namespace'}


class TeiLine(_TeiBase):
    rend = xmlmap.StringField(b'@rend')

    def indent(self):
        if self.rend.startswith(b'indent'):
            indentation = self.rend[len(b'indent'):]
            if indentation:
                return int(indentation)
            return 0


class TeiLineGroup(_TeiBase):
    head = xmlmap.StringField(b'tei:head')
    linegroup = xmlmap.NodeListField(b'tei:lg', b'self')
    line = xmlmap.NodeListField(b'tei:l', TeiLine)


class TeiQuote(_TeiBase):
    line = xmlmap.NodeListField(b'tei:l', TeiLine)
    linegroup = xmlmap.NodeListField(b'tei:lg', TeiLineGroup)


class TeiEpigraph(_TeiBase):
    quote = xmlmap.NodeListField(b'tei:q|tei:quote|tei:cit/tei:q|tei:cit/tei:quote', TeiQuote)
    bibl = xmlmap.StringField(b'tei:bibl')


class TeiDiv(_TeiBase):
    id = xmlmap.StringField(b'@xml:id')
    type = xmlmap.StringField(b'@type')
    author = xmlmap.StringField(b'tei:docAuthor/tei:name/tei:choice/tei:sic')
    docauthor = xmlmap.StringField(b'tei:docAuthor')
    title = xmlmap.StringField(b'tei:head[1]')
    title_list = xmlmap.StringListField(b'tei:head')
    text = xmlmap.StringField(b'.')
    linegroup = xmlmap.NodeListField(b'tei:lg', TeiLineGroup)
    div = xmlmap.NodeListField(b'tei:div', b'self')
    byline = xmlmap.StringField(b'tei:byline')
    epigraph = xmlmap.NodeListField(b'tei:epigraph', TeiEpigraph)
    p = xmlmap.StringListField(b'tei:p')
    q = xmlmap.StringListField(b'tei:q')
    quote = xmlmap.StringListField(b'tei:quote')
    floatingText = xmlmap.NodeListField(b'tei:floatingText/tei:body/tei:div', b'self')


class TeiFloatingText(_TeiBase):
    head = xmlmap.StringField(b'./tei:body/tei:head')
    line_group = xmlmap.NodeListField(b'.//tei:lg', TeiLineGroup)
    line = xmlmap.NodeListField(b'.//tei:l', TeiLine)


class TeiFigure(_TeiBase):
    ana = xmlmap.StringField(b'@ana')
    head = xmlmap.StringField(b'tei:head')
    description = xmlmap.StringField(b'tei:figDesc')
    entity = xmlmap.StringField(b'tei:graphic/@url')
    floatingText = xmlmap.NodeListField(b'tei:floatingText', TeiFloatingText)


class TeiInterp(_TeiBase):
    ROOT_NAME = b'interp'
    id = xmlmap.StringField(b'@xml:id')
    value = xmlmap.StringField(b'.')


class TeiSection(_TeiBase):
    div = xmlmap.NodeListField(b'tei:div', TeiDiv)
    all_figures = xmlmap.NodeListField(b'.//tei:figure', TeiFigure)


class TeiInterpGroup(_TeiBase):
    ROOT_NAME = b'interpGrp'
    type = xmlmap.StringField(b'@type')
    interp = xmlmap.NodeListField(b'tei:interp', TeiInterp)


class TeiName(_TeiBase):
    type = xmlmap.StringField(b'@person')
    reg = xmlmap.StringField(b'tei:choice/tei:reg')
    value = xmlmap.StringField(b'tei:choice/tei:sic')


class TeiHeader(_TeiBase):
    """xmlmap object for a TEI (Text Encoding Initiative) header"""
    title = xmlmap.StringField(b'tei:fileDesc/tei:titleStmt/tei:title')
    author_list = xmlmap.NodeListField(b'tei:fileDesc/tei:titleStmt/tei:author/tei:name', TeiName)
    editor_list = xmlmap.NodeListField(b'tei:fileDesc/tei:titleStmt/tei:editor/tei:name', TeiName)
    publisher = xmlmap.StringField(b'tei:fileDesc/tei:publicationStmt/tei:publisher')
    publication_date = xmlmap.StringField(b'tei:fileDesc/tei:publicationStmt/tei:date')
    availability = xmlmap.StringField(b'tei:fileDesc/tei:publicationStmt/tei:availability')
    source_description = xmlmap.StringField(b'tei:fileDesc/tei:sourceDesc')
    series_statement = xmlmap.StringField(b'tei:fileDesc/tei:seriesStmt')


class Tei(_TeiBase):
    """xmlmap object for a TEI (Text Encoding Initiative) XML document """
    id = xmlmap.StringField(b'@xml:id')
    title = xmlmap.StringField(b'tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title')
    author = xmlmap.StringField(b'tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:name/tei:choice/tei:sic')
    editor = xmlmap.StringField(b'tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:editor/tei:name/tei:choice/tei:sic')
    header = xmlmap.NodeField(b'tei:teiHeader', TeiHeader)
    front = xmlmap.NodeField(b'tei:text/tei:front', TeiSection)
    body = xmlmap.NodeField(b'tei:text/tei:body', TeiSection)
    back = xmlmap.NodeField(b'tei:text/tei:back', TeiSection)