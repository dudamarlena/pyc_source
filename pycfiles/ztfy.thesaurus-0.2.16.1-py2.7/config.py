# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/loader/config.py
# Compiled at: 2013-09-04 09:38:38
from ztfy.thesaurus.interfaces.loader import IThesaurusLoaderConfiguration, IThesaurusUpdaterConfiguration, IThesaurusExporterConfiguration
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

class ThesaurusLoaderConfiguration(object):
    """Thesaurus loader configuration"""
    implements(IThesaurusLoaderConfiguration)
    name = FieldProperty(IThesaurusLoaderConfiguration['name'])
    data = FieldProperty(IThesaurusLoaderConfiguration['data'])
    format = FieldProperty(IThesaurusLoaderConfiguration['format'])
    import_synonyms = FieldProperty(IThesaurusLoaderConfiguration['import_synonyms'])
    language = FieldProperty(IThesaurusLoaderConfiguration['language'])
    encoding = FieldProperty(IThesaurusLoaderConfiguration['encoding'])

    def __init__(self, data={}):
        if data:
            name = data.get('name')
            if name:
                self.name = name
            self.data = data.get('data')
            self.format = data.get('format')
            self.import_synonyms = data.get('import_synonyms')
            self.language = data.get('language')
            self.encoding = data.get('encoding')


class ThesaurusUpdaterConfiguration(ThesaurusLoaderConfiguration):
    """Thesaurus updater configuration"""
    implements(IThesaurusUpdaterConfiguration)
    clear = FieldProperty(IThesaurusUpdaterConfiguration['clear'])
    conflict_suffix = FieldProperty(IThesaurusUpdaterConfiguration['conflict_suffix'])

    def __init__(self, data={}):
        super(ThesaurusUpdaterConfiguration, self).__init__(data)
        if data:
            self.clear = data.get('clear')
            self.conflict_suffix = data.get('conflict_suffix')


class ThesaurusExporterConfiguration(object):
    """Thesaurus exporter configuration"""
    implements(IThesaurusExporterConfiguration)
    filename = FieldProperty(IThesaurusExporterConfiguration['filename'])
    format = FieldProperty(IThesaurusExporterConfiguration['format'])
    extract = FieldProperty(IThesaurusExporterConfiguration['extract'])

    def __init__(self, data={}):
        if data:
            self.filename = data.get('filename')
            self.format = data.get('format')
            self.extract = data.get('extract')