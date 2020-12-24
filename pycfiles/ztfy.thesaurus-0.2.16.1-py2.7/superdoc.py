# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/loader/superdoc.py
# Compiled at: 2013-10-03 05:22:54
import chardet
from datetime import datetime
from lxml import etree
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from ztfy.thesaurus.loader import BaseThesaurusLoader, XMLThesaurusLoaderHandler, BaseThesaurusExporter, XMLThesaurusExporterHandler, ThesaurusLoaderDescription, ThesaurusLoaderTerm
INM = '{http://www.inmagic.com/webpublisher/query}'

class SuperdocThesaurusLoaderHandler(XMLThesaurusLoaderHandler):
    """SuperDoc format thesaurus load handler"""

    def read(self, data, configuration=None):
        terms = {}
        if configuration is None:
            configuration = self.configuration
        encoding = None
        if configuration and configuration.encoding:
            encoding = configuration.encoding
        if not encoding and isinstance(data, (str, unicode)):
            encoding = chardet.detect(data[:1000]).get('encoding', 'utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding=encoding)
        xml = etree.parse(data, parser=parser)
        root = xml.getroot()
        description = ThesaurusLoaderDescription()
        for records in root.findall(INM + 'Recordset'):
            for record in records.findall(INM + 'Record'):
                key = None
                label = None
                alt = None
                definition = None
                note = None
                generic = None
                specifics = []
                associations = []
                usage = None
                used_for = []
                created = None
                modified = None
                for element in record.getchildren():
                    if element.text:
                        if element.tag == INM + 'Terme':
                            key = label = unicode(element.text)
                        elif element.tag == INM + 'NA':
                            definition = unicode(element.text)
                        elif element.tag == INM + 'TS':
                            specifics.append(unicode(element.text))
                        elif element.tag == INM + 'TG':
                            generic = unicode(element.text)
                        elif element.tag == INM + 'TA':
                            associations.append(unicode(element.text))
                        elif element.tag == INM + 'EM':
                            if configuration.import_synonyms:
                                usage = unicode(element.text)
                        elif element.tag == INM + 'EP':
                            if configuration.import_synonyms:
                                used_for.append(unicode(element.text))
                        elif element.tag == INM + 'Notes':
                            note = unicode(element.text)
                        elif element.tag == INM + 'DateCreation':
                            created = datetime.strptime(element.text, '%d/%m/%Y')
                        elif element.tag == INM + 'DateModification':
                            modified = datetime.strptime(element.text, '%d/%m/%Y')

                if key:
                    terms[key] = ThesaurusLoaderTerm(label, alt, definition, note, generic, specifics, associations, usage, used_for, created, modified)

        return (
         description, terms)


class SuperdocThesaurusLoader(BaseThesaurusLoader):
    """SuperDoc export format thesaurus loader"""
    handler = SuperdocThesaurusLoaderHandler


class SuperdocThesaurusExporterHandler(XMLThesaurusExporterHandler):
    """SuperDoc format thesaurus export handler"""

    def _write(self, thesaurus, configuration=None):
        intids = getUtility(IIntIds)
        xml = etree.Element('Results', nsmap={None: INM[1:-1]}, productTitle='ONF Thesaurus Manager', productVersion='0.1')
        doc = etree.ElementTree(xml)
        extract = configuration and configuration.extract or None
        if extract:
            terms = [ term for term in thesaurus.terms.itervalues() if extract in (term.extracts or set()) ]
        else:
            terms = thesaurus.terms
        rs = etree.SubElement(xml, 'Recordset', setCount=str(len(terms)))
        for index, term in enumerate(thesaurus.terms.itervalues()):
            if extract and extract not in (term.extracts or set()):
                continue
            rec = etree.SubElement(rs, 'Record', setEntry=str(index))
            etree.SubElement(rec, 'ID').text = str(intids.queryId(term))
            etree.SubElement(rec, 'Terme').text = term.label
            etree.SubElement(rec, 'NA').text = term.note
            added_subterms = False
            if term.specifics:
                for subterm in term.specifics:
                    if extract and extract not in (subterm.extracts or ()):
                        continue
                    etree.SubElement(rec, 'TS').text = subterm.label
                    added_subterms = True

            if not added_subterms:
                etree.SubElement(rec, 'TS')
            sub = etree.SubElement(rec, 'TG')
            if term.generic:
                sub.text = term.generic.label
            added_subterms = False
            if term.associations:
                for subterm in term.associations:
                    if extract and extract not in (subterm.extracts or ()):
                        continue
                    etree.SubElement(rec, 'TA').text = subterm.label
                    added_subterms = True

            if not added_subterms:
                etree.SubElement(rec, 'TA')
            sub = etree.SubElement(rec, 'EM')
            if term.usage:
                sub.text = term.usage.label
            added_subterms = False
            if term.used_for:
                for subterm in term.used_for:
                    if extract and extract not in (subterm.extracts or ()):
                        continue
                    etree.SubElement(rec, 'EP').text = subterm.label
                    added_subterms = True

            if not added_subterms:
                etree.SubElement(rec, 'EP')
            etree.SubElement(rec, 'Notes').text = term.definition
            etree.SubElement(rec, 'Status').text = term.status
            etree.SubElement(rec, 'DateCreation').text = term.created and term.created.strftime('%d/%m/%Y') or ''
            etree.SubElement(rec, 'DateModification').text = term.modified and term.modified.strftime('%d/%m/%Y') or ''
            etree.SubElement(rec, 'Niveau').text = str(term.level)
            etree.SubElement(rec, 'MicroThes').text = term.micro_thesaurus and 'OUI' or 'NON'
            etree.SubElement(rec, 'Terme0').text = term.parent is None and term.label or term.parent.label

        return doc


class SuperdocThesaurusExporter(BaseThesaurusExporter):
    """SuperDoc format thesaurus exporter"""
    handler = SuperdocThesaurusExporterHandler