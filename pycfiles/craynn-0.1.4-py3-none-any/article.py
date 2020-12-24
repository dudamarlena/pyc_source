# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/c24b/projets/crawtext/crawtext/newspaper/article.py
# Compiled at: 2014-11-20 05:35:51
__title__ = 'newspaper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
import logging, copy, os, glob
from . import settings
from . import urls
from .cleaners import DocumentCleaner
from .configuration import Configuration
from .extractors import ContentExtractor
from .outputformatters import OutputFormatter
from .utils import URLHelper, encodeValue, RawHelper, extend_config, get_available_languages
from bs4 import BeautifulSoup

class ArticleException(Exception):
    pass


class Article(object):
    """Article objects abstract an online news article page
    """

    def __init__(self, url, depth='', source_url=''):
        """The **kwargs argument may be filled with config values, which
        is added into the config object
        """
        self.config = Configuration()
        self.extractor = ContentExtractor(self.config)
        if source_url == '':
            source_url = urls.get_scheme(url) + '://' + urls.get_domain(url)
        self.source_url = encodeValue(source_url)
        url = encodeValue(url)
        self.url = urls.prepare_url(url, self.source_url)
        self.title = ''
        self.top_img = self.top_image = ''
        self.meta_img = ''
        self.imgs = self.images = []
        self.movies = []
        self.text = ''
        self.keywords = []
        self.meta_keywords = []
        self.tags = set()
        self.authors = []
        self.published_date = ''
        self.summary = ''
        self.html = ''
        self.article_html = ''
        self.is_parsed = False
        self.is_downloaded = False
        self.meta_description = ''
        self.meta_lang = ''
        self.meta_favicon = ''
        self.meta_data = {}
        self.canonical_link = ''
        self.top_node = None
        self.clean_top_node = None
        self.doc = None
        self.clean_doc = None
        self.additional_data = {}
        self.status = True
        if url == None:
            self.status = False
        if url == '':
            self.status = False
        self.links = []
        return

    def parse(self, html):
        self.html = html
        try:
            self.doc = self.config.get_parser().fromstring(self.html)
        except Exception:
            self.msg = 'Parse Error: Unable to load html'
            self.code = '700'

        self.clean_doc = copy.deepcopy(self.doc)
        parse_candidate = self.get_parse_candidate()
        self.link_hash = parse_candidate.link_hash
        try:
            document_cleaner = DocumentCleaner(self.config)
        except Exception:
            self.msg = 'Parse Error: Unable to clean doc'
            self.code = '700'

        try:
            output_formatter = OutputFormatter(self.config)
        except Exception:
            self.msg = 'Parse Error: Unable to output article'
            self.code = '700'

        try:
            title = self.extractor.get_title(self.clean_doc)
            self.set_title(title)
        except Exception:
            self.msg = 'Parse Error: Unable to extract title'
            self.code = '700'
            title = BeautifulSoup(self.html).title

        try:
            self.meta_lang = self.extractor.get_meta_lang(self.clean_doc)
        except Exception as e:
            self.msg = 'Parse Error: Unable to get meta lang ' + str(e)
            self.code = '700'

        if self.config.use_meta_language:
            self.extractor.update_language(self.meta_lang)
            output_formatter.update_language(self.meta_lang)
        try:
            self.canonical_link = self.extractor.get_canonical_link(self.url, self.clean_doc)
        except Exception as e:
            self.msg = 'Parse Error: Unable to get canonical link' + str(e)
            self.code = '700'

        self.tags = self.extractor.extract_tags(self.clean_doc)
        self.meta_data = self.extractor.get_meta_data(self.clean_doc)
        try:
            self.doc = document_cleaner.clean(self.doc)
        except Exception as e:
            self.msg = 'Parse Error: Unable to get document' + str(e)
            self.code = '700'
            return False

        text = ''
        try:
            self.top_node = self.extractor.calculate_best_node(self.doc)
            if self.top_node is not None:
                self.top_node = self.extractor.post_cleanup(self.top_node)
                self.clean_top_node = copy.deepcopy(self.top_node)
                text, article_html = output_formatter.get_formatted(self.top_node)
                self.set_article_html(article_html)
                self.set_text(text)
                self.fetch_links()
                self.status = True
                self.release_resources()
                return True
            try:
                soup = BeautifulSoup(self.html)
                self.text = soup.text
                self.title = soup.title
                self.links = [ n.get('href') for n in soup.findAll('a') ]
                self.status = True
                self.release_resources()
                return True
            except:
                self.msg = 'Parse Error: Unable to calculate best node'
                self.code = '700'

            self.release_resources()
        except Exception as e:
            print 'Parsing', e
            self.msg = 'Error Parsing: %e' % str(e)
            self.code = 900
            self.status = False
            return False

        return

    def fetch_links(self):
        self.links = self.extractor.get_urls(self.doc)
        return self.links

    def fetch_images(self):
        if self.clean_doc is not None:
            meta_img_url = self.extractor.get_meta_img_url(self.url, self.clean_doc)
            self.set_meta_img(meta_img_url)
            imgs = self.extractor.get_img_urls(self.url, self.clean_doc)
            if self.meta_img:
                imgs.add(self.meta_img)
            self.set_imgs(imgs)
        if self.clean_top_node is not None and not self.has_top_image():
            first_img = self.extractor.get_first_img_url(self.url, self.clean_top_node)
            self.set_top_img(first_img)
        if not self.has_top_image():
            self.set_reddit_top_img()
        return

    def has_top_image(self):
        return self.top_img is not None and self.top_img != ''

    def is_valid_url(self):
        """Performs a check on the url of this link to determine if article
        is a real news article or not
        """
        return urls.valid_url(self.url)

    def is_valid_body(self):
        """If the article's body text is long enough to meet
        standard article requirements, keep the article
        """
        if not self.is_parsed:
            raise ArticleException("must parse article before checking                                     if it's body is valid!")
        meta_type = self.extractor.get_meta_type(self.clean_doc)
        wordcount = self.text.split(' ')
        sentcount = self.text.split('.')
        if meta_type == 'article' and wordcount > self.config.MIN_WORD_COUNT:
            return True
        else:
            if not self.is_media_news() and not self.text:
                return False
            if self.title is None or len(self.title.split(' ')) < 2:
                return False
            if len(wordcount) < self.config.MIN_WORD_COUNT:
                return False
            if len(sentcount) < self.config.MIN_SENT_COUNT:
                return False
            if self.html is None or self.html == '':
                return False
            return True

    def is_media_news(self):
        """If the article is related heavily to media:
        gallery, video, big pictures, etc
        """
        safe_urls = [
         '/video', '/slide', '/gallery', '/powerpoint',
         '/fashion', '/glamour', '/cloth']
        for s in safe_urls:
            if s in self.url:
                return True

        return False

    def get_parse_candidate(self):
        """A parse candidate is a wrapper object holding a link hash of this
        article and a final_url of the article
        """
        if self.html:
            return RawHelper.get_parsing_candidate(self.url, self.html)
        return URLHelper.get_parsing_candidate(self.url)

    def build_resource_path(self):
        """Must be called after computing HTML/final URL
        """
        res_path = self.get_resource_path()
        if not os.path.exists(res_path):
            os.mkdir(res_path)

    def get_resource_path(self):
        """Every article object has a special directory to store data in from
        initialization to garbage collection
        """
        res_dir_fn = 'article_resources'
        resource_directory = os.path.join(settings.TOP_DIRECTORY, res_dir_fn)
        if not os.path.exists(resource_directory):
            os.mkdir(resource_directory)
        dir_path = os.path.join(resource_directory, '%s_' % self.link_hash)
        return dir_path

    def release_resources(self):
        path = self.get_resource_path()
        for fname in glob.glob(path):
            try:
                os.remove(fname)
            except OSError:
                pass

    def set_title(self, title):
        if self.title and not title:
            return
        title = title[:self.config.MAX_TITLE]
        title = encodeValue(title)
        if title:
            self.title = title

    def set_text(self, text):
        text = text[:self.config.MAX_TEXT]
        text = encodeValue(text)
        if text:
            self.text = text

    def set_html(self, html):
        """Encode HTML before setting it
        """
        self.is_downloaded = True
        if html:
            self.html = encodeValue(html)

    def set_article_html(self, article_html):
        """Sets the HTML of just the article's `top_node`
        """
        if article_html:
            self.article_html = encodeValue(article_html)

    def is_relevant(self, query):
        indexed = {'title': unicode(self.title), 'content': unicode(self.text)}
        return query.match(indexed)

    def json(self):
        result = {}
        values = [
         'title', 'date', 'depth', 'outlinks', 'inlinks', 'source_url']
        for k, v in self.__dict__.items():
            if k in values and v is not None:
                if type(v) == set:
                    v = list(v)
                result[k] = v

        return result