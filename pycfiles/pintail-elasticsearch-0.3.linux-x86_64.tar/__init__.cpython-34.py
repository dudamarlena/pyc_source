# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/pintail/elasticsearch/__init__.py
# Compiled at: 2016-07-29 10:39:34
# Size of source mod 2**32: 7236 bytes
import codecs, datetime, os, urllib, uuid, pintail.search, pintail.site, pintail.mallard, elasticsearch

class ElasticSearchPage(pintail.mallard.MallardPage):

    def __init__(self, directory):
        pintail.mallard.MallardPage.__init__(self, directory, 'pintail-elasticsearch.page')

    @property
    def source_path(self):
        return self.stage_path

    @property
    def searchable(self):
        return False

    def stage_page(self):
        pintail.site.Site._makedirs(self.directory.stage_path)
        from pkg_resources import resource_string
        xsl = resource_string(__name__, 'pintail-elasticsearch.page')
        fd = open(self.stage_path, 'w', encoding='utf-8')
        fd.write(codecs.decode(xsl, 'utf-8'))
        fd.close()

    @classmethod
    def get_pages_dir(cls, directory):
        if directory.path == '/':
            return [cls(directory)]
        else:
            return []


class ElasticSearchProvider(pintail.search.SearchProvider, pintail.site.ToolsProvider, pintail.site.XslProvider):
    analyzers = {'ar': 'arabic', 
     'bg': 'bulgarian', 
     'ca': 'catalan', 
     'ckb': 'sorani', 
     'cs': 'czech', 
     'da': 'danish', 
     'de': 'german', 
     'el': 'greek', 
     'en': 'english', 
     'es': 'spanish', 
     'eu': 'basque', 
     'fa': 'persian', 
     'fi': 'finnish', 
     'fr': 'french', 
     'ga': 'irish', 
     'gl': 'galician', 
     'hi': 'hindi', 
     'hu': 'hungarian', 
     'hy': 'armenian', 
     'id': 'indonesian', 
     'it': 'italian', 
     'ja': 'cjk', 
     'ko': 'cjk', 
     'lt': 'lithuanian', 
     'lv': 'latvian', 
     'nb': 'norwegian', 
     'nl': 'dutch', 
     'nn': 'norwegian', 
     'no': 'norwegian', 
     'pt': 'portuguese', 
     'pt-br': 'brazilian', 
     'ro': 'romanian', 
     'ru': 'russian', 
     'sv': 'swedish', 
     'th': 'thai', 
     'tr': 'turkish', 
     'zh': 'cjk'}

    def __init__(self, site):
        pintail.search.SearchProvider.__init__(self, site)
        self.epoch = site.config.get('search_epoch')
        if self.epoch is None:
            self.epoch = datetime.datetime.now().strftime('%Y-%m-%d') + '-' + str(uuid.uuid1())
        elhost = self.site.config.get('search_elastic_host')
        self.elastic = elasticsearch.Elasticsearch([elhost])
        self._indexes = []

    @classmethod
    def get_xsl(cls, site):
        return [os.path.join(site.tools_path, 'pintail-elasticsearch.xsl')]

    @classmethod
    def get_xsl_params(cls, output, obj):
        if not (output == 'html' and isinstance(obj, pintail.site.Page)):
            return []
        if not isinstance(obj.site.search_provider, ElasticSearchProvider):
            return []
        lang = 'en'
        ret = [
         (
          'pintail.elasticsearch.host', obj.site.config.get('search_elastic_host')),
         (
          'pintail.elasticsearch.epoch', obj.site.search_provider.epoch),
         (
          'pintail.elasticsearch.index', obj.site.search_provider.get_index(lang))]
        domains = obj.get_search_domains()
        if domains[0] != 'none':
            ret.append(('pintail.search.domains', ' '.join(domains)))
        return ret

    @classmethod
    def build_tools(cls, site):
        from pkg_resources import resource_string
        xsl = resource_string(__name__, 'pintail-elasticsearch.xsl')
        fd = open(os.path.join(site.tools_path, 'pintail-elasticsearch.xsl'), 'w', encoding='utf-8')
        fd.write(codecs.decode(xsl, 'utf-8'))
        fd.close()

    def get_index(self, lang):
        ix = self.site.config.get('search_elastic_index') or 'pintail@{lang}'
        return ix.format(lang=lang, epoch=self.epoch)

    def get_analyzer(self, lang):
        if lang.lower() in ElasticSearchProvider.analyzers:
            return ElasticSearchProvider.analyzers[lang.lower()]
        if '-' in lang:
            return ElasticSearchProvider.get_analyzer(lang[:lang.rindex('-')])
        return 'english'

    def create_index(self, lang):
        if lang in self._indexes:
            return
        self._indexes.append(lang)
        elindex = self.get_index(lang)
        if self.elastic.indices.exists(elindex):
            pass
        else:
            analyzer = self.get_analyzer(lang)
            self.elastic.indices.create(index=elindex, body={'mappings': {'page': {'properties': {'path': {'type': 'string',  'index': 'not_analyzed'},  'lang': {'type': 'string',  'index': 'not_analyzed'},  'domain': {'type': 'string',  'index': 'not_analyzed'},  'epoch': {'type': 'string',  'index': 'not_analyzed'},  'title': {'type': 'string',  'analyzer': analyzer},  'desc': {'type': 'string',  'analyzer': analyzer},  'keywords': {'type': 'string',  'analyzer': analyzer},  'content': {'type': 'string',  'analyzer': analyzer}}}}})

    def index_page(self, page):
        self.site.log('INDEX', page.site_id)
        lang = 'en'
        self.create_index(lang)
        title = page.get_title(hint='search')
        desc = page.get_desc(hint='search')
        keywords = page.get_keywords(hint='search')
        content = page.get_content(hint='search')
        elid = urllib.parse.quote(page.site_id, safe='') + '@' + self.epoch
        elindex = self.get_index(lang)
        domains = page.get_search_domains()
        self.elastic.index(index=elindex, doc_type='page', id=elid, body={'path': page.site_path, 
         'lang': lang, 
         'domain': domains, 
         'epoch': self.epoch, 
         'title': title, 
         'desc': desc, 
         'keywords': keywords, 
         'content': content})