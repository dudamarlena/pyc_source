# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/misc.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_metadata.metadata import RootMetadata, registerExtractor
from hachoir_metadata.safe import fault_tolerant
from hachoir_parser.container import SwfFile
from hachoir_parser.misc import TorrentFile, TrueTypeFontFile, OLE2_File, PcfFile
from hachoir_core.field import isString
from hachoir_core.error import warning
from hachoir_parser import guessParser
from hachoir_metadata.setter import normalizeString

class TorrentMetadata(RootMetadata):
    __module__ = __name__
    KEY_TO_ATTR = {'announce': 'url', 'comment': 'comment', 'creation_date': 'creation_date'}
    INFO_TO_ATTR = {'length': 'file_size', 'name': 'filename'}

    def extract(self, torrent):
        for field in torrent[0]:
            self.processRoot(field)

    @fault_tolerant
    def processRoot(self, field):
        if field.name in self.KEY_TO_ATTR:
            key = self.KEY_TO_ATTR[field.name]
            value = field.value
            setattr(self, key, value)
        elif field.name == 'info' and 'value' in field:
            for field in field['value']:
                self.processInfo(field)

    @fault_tolerant
    def processInfo(self, field):
        if field.name in self.INFO_TO_ATTR:
            key = self.INFO_TO_ATTR[field.name]
            value = field.value
            setattr(self, key, value)
        elif field.name == 'piece_length':
            self.comment = 'Piece length: %s' % field.display


class TTF_Metadata(RootMetadata):
    __module__ = __name__
    NAMEID_TO_ATTR = {0: 'copyright', 3: 'title', 5: 'version', 8: 'author', 11: 'url', 14: 'copyright'}

    def extract(self, ttf):
        if 'header' in ttf:
            self.extractHeader(ttf['header'])
        if 'names' in ttf:
            self.extractNames(ttf['names'])

    @fault_tolerant
    def extractHeader(self, header):
        self.creation_date = header['created'].value
        self.last_modification = header['modified'].value
        self.comment = 'Smallest readable size in pixels: %s pixels' % header['lowest'].value
        self.comment = 'Font direction: %s' % header['font_dir'].display

    @fault_tolerant
    def extractNames(self, names):
        offset = names['offset'].value
        for header in names.array('header'):
            key = header['nameID'].value
            foffset = offset + header['offset'].value
            field = names.getFieldByAddress(foffset * 8)
            if not field or not isString(field):
                continue
            value = field.value
            if key not in self.NAMEID_TO_ATTR:
                continue
            key = self.NAMEID_TO_ATTR[key]
            if key == 'version' and value.startswith('Version '):
                value = value[8:]
            setattr(self, key, value)


class OLE2_Metadata(RootMetadata):
    __module__ = __name__
    SUMMARY_ID_TO_ATTR = {2: 'title', 3: 'title', 4: 'author', 6: 'comment', 8: 'author', 12: 'creation_date', 13: 'last_modification', 14: 'nb_page', 18: 'producer'}
    IGNORE_SUMMARY = set((1, ))
    DOC_SUMMARY_ID_TO_ATTR = {3: 'title', 14: 'author'}
    IGNORE_DOC_SUMMARY = set((1, ))

    def extract(self, ole2):
        self._extract(ole2)

    def _extract(self, fieldset, main_document=True):
        if main_document:
            fieldset._feedAll()
            if 'root[0]' in fieldset:
                self.useRoot(fieldset['root[0]'])
        doc_summary = self.getField(fieldset, main_document, 'doc_summary[0]')
        if doc_summary:
            self.useSummary(doc_summary, True)
        word_doc = self.getField(fieldset, main_document, 'word_doc[0]')
        if word_doc:
            self.useWordDocument(word_doc)
        summary = self.getField(fieldset, main_document, 'summary[0]')
        if summary:
            self.useSummary(summary, False)

    @fault_tolerant
    def useRoot(self, root):
        stream = root.getSubIStream()
        ministream = guessParser(stream)
        if not ministream:
            warning('Unable to create the OLE2 mini stream parser!')
            return
        self._extract(ministream, main_document=False)

    def getField(self, fieldset, main_document, name):
        if name not in fieldset:
            return
        fieldset._feedAll()
        field = fieldset[name]
        if main_document:
            stream = field.getSubIStream()
            field = guessParser(stream)
            if not field:
                warning('Unable to create the OLE2 parser for %s!' % name)
                return
        return field

    @fault_tolerant
    def useSummary(self, summary, is_doc_summary):
        if 'os' in summary:
            self.os = summary['os'].display
        if 'section[0]' not in summary:
            return
        summary = summary['section[0]']
        for property in summary.array('property_index'):
            self.useProperty(summary, property, is_doc_summary)

    @fault_tolerant
    def useWordDocument(self, doc):
        self.comment = 'Encrypted: %s' % doc['fEncrypted'].value

    @fault_tolerant
    def useProperty(self, summary, property, is_doc_summary):
        field = summary.getFieldByAddress(property['offset'].value * 8)
        if not field or 'value' not in field:
            return
        field = field['value']
        if not field.hasValue():
            return
        value = field.value
        if isinstance(value, (str, unicode)):
            value = normalizeString(value)
            if not value:
                return
        prop_id = property['id'].value
        if is_doc_summary:
            id_to_attr = self.DOC_SUMMARY_ID_TO_ATTR
            ignore = self.IGNORE_DOC_SUMMARY
        else:
            id_to_attr = self.SUMMARY_ID_TO_ATTR
            ignore = self.IGNORE_SUMMARY
        if prop_id in ignore:
            return
        try:
            key = id_to_attr[prop_id]
            use_prefix = False
        except LookupError:
            key = 'comment'
            use_prefix = True

        if use_prefix:
            prefix = property['id'].display
            if prefix in ('TotalEditingTime', 'LastPrinted') and not field:
                return
            value = '%s: %s' % (prefix, value)
        elif key == 'last_modification' and not field:
            return
        setattr(self, key, value)


class PcfMetadata(RootMetadata):
    __module__ = __name__
    PROP_TO_KEY = {'CHARSET_REGISTRY': 'charset', 'COPYRIGHT': 'copyright', 'WEIGHT_NAME': 'font_weight', 'FOUNDRY': 'author', 'FONT': 'title', '_XMBDFED_INFO': 'producer'}

    def extract(self, pcf):
        if 'properties' in pcf:
            self.useProperties(pcf['properties'])

    def useProperties(self, properties):
        last = properties['total_str_length']
        offset0 = last.address + last.size
        for index in properties.array('property'):
            value = properties.getFieldByAddress(offset0 + index['value_offset'].value * 8)
            if not value:
                continue
            value = value.value
            if not value:
                continue
            name = properties.getFieldByAddress(offset0 + index['name_offset'].value * 8)
            if not name:
                continue
            name = name.value
            if name not in self.PROP_TO_KEY:
                warning('Skip %s=%r' % (name, value))
                continue
            key = self.PROP_TO_KEY[name]
            setattr(self, key, value)


class SwfMetadata(RootMetadata):
    __module__ = __name__

    def extract(self, swf):
        self.height = swf['rect/ymax'].value
        self.width = swf['rect/xmax'].value
        self.format_version = 'flash version %s' % swf['version'].value
        self.frame_rate = swf['frame_rate'].value
        self.comment = 'Frame count: %s' % swf['frame_count'].value


registerExtractor(TorrentFile, TorrentMetadata)
registerExtractor(TrueTypeFontFile, TTF_Metadata)
registerExtractor(OLE2_File, OLE2_Metadata)
registerExtractor(PcfFile, PcfMetadata)
registerExtractor(SwfFile, SwfMetadata)