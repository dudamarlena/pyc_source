# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\core\app.py
# Compiled at: 2020-03-23 11:49:43
# Size of source mod 2**32: 7810 bytes
import logging, os, re, shutil
from urllib.parse import urlparse
from slugify import slugify
from ..binders import available_formats, generate_books
from ..sources import crawler_list
from .novel_search import search_novels
from .downloader import download_chapters
from .novel_info import format_novel, save_metadata
logger = logging.getLogger('APP')

class App:
    __doc__ = 'Bots are based on top of an instance of this app'

    def __init__(self):
        self.progress = 0
        self.user_input = None
        self.crawler_links = None
        self.crawler = None
        self.login_data = ()
        self.search_results = []
        self.output_path = None
        self.pack_by_volume = False
        self.chapters = []
        self.book_cover = None
        self.output_formats = {}
        self.archived_outputs = None
        self.good_file_name = None
        self.no_append_after_filename = False

    def initialize(self):
        logger.info('Initialized App')

    def destroy(self):
        if self.crawler:
            self.crawler.destroy()
        self.chapters.clear()
        logger.info('Destroyed App')

    def init_search(self):
        """Requires: user_input"""
        if not self.user_input:
            raise Exception('User input is not valid')
        elif self.user_input.startswith('http'):
            logger.info('Detected URL input')
            self.init_crawler(self.user_input)
        else:
            logger.info('Detected query input')
            self.crawler_links = [link for link, crawler in crawler_list.items() if 'search_novel' in crawler.__dict__]

    def search_novel(self):
        """Requires: user_input, crawler_links"""
        logger.info('Searching for novels in %d sites...', len(self.crawler_links))
        search_novels(self)
        if len(self.search_results) == 0:
            raise Exception('No results for: %s' % self.user_input)
        logger.info('Total %d novels found from %d sites', len(self.search_results), len(self.crawler_links))

    def init_crawler(self, novel_url):
        """Requires: [user_input]"""
        if not novel_url:
            return
        for home_url, crawler in crawler_list.items():
            if novel_url.startswith(home_url):
                logger.info('Initializing crawler for: %s', home_url)
                self.crawler = crawler()
                self.crawler.novel_url = novel_url
                self.crawler.home_url = home_url.strip('/')
                break

        if not self.crawler:
            raise Exception('No crawlers were found')

    def can_do(self, prop_name):
        return prop_name in self.crawler.__class__.__dict__

    def get_novel_info(self):
        """Requires: crawler, login_data"""
        self.crawler.initialize()
        if self.can_do('login'):
            if self.login_data:
                logger.debug(self.login_data)
                (self.crawler.login)(*self.login_data)
        print('Retrieving novel info...')
        print(self.crawler.novel_url)
        self.crawler.read_novel_info()
        print('NOVEL: %s' % self.crawler.novel_title)
        print('%d volumes and %d chapters found' % (
         len(self.crawler.volumes), len(self.crawler.chapters)))
        format_novel(self.crawler)
        if not self.good_file_name:
            self.good_file_name = slugify((self.crawler.novel_title),
              max_length=50,
              separator=' ',
              lowercase=False,
              word_boundary=True)
        source_name = slugify(urlparse(self.crawler.home_url).netloc)
        self.output_path = os.path.join('Lightnovels', source_name, self.good_file_name)

    def start_download(self):
        """Requires: crawler, chapters, output_path"""
        if not os.path.exists(self.output_path):
            raise Exception('Output path is not defined')
        save_metadata(self.crawler, self.output_path)
        download_chapters(self)
        if self.can_do('logout'):
            self.crawler.logout()

    def bind_books(self):
        """Requires: crawler, chapters, output_path, pack_by_volume, book_cover, output_formats"""
        logger.info('Processing data for binding')
        data = {}
        if self.pack_by_volume:
            for vol in self.crawler.volumes:
                filename_suffix = 'Chapter %d-%d' % (vol['start_chapter'], vol['final_chapter'])
                data[filename_suffix] = [x for x in self.chapters if x['volume'] == vol['id'] if len(x['body']) > 0]

        else:
            first_id = self.chapters[0]['id']
            last_id = self.chapters[(-1)]['id']
            vol = 'c%s-%s' % (first_id, last_id)
            data[vol] = self.chapters
        generate_books(self, data)

    def compress_books(self, archive_singles=False):
        logger.info('Compressing output...')
        path_to_process = []
        for fmt in available_formats:
            root_dir = os.path.join(self.output_path, fmt)
            if os.path.isdir(root_dir):
                path_to_process.append([
                 root_dir,
                 self.good_file_name + ' (' + fmt + ')'])

        self.archived_outputs = []
        for root_dir, output_name in path_to_process:
            file_list = os.listdir(root_dir)
            if len(file_list) == 0:
                logger.info('It has no files: %s', root_dir)
                continue
            archived_file = None
            if len(file_list) == 1 and not archive_singles:
                if not os.path.isdir(os.path.join(root_dir, file_list[0])):
                    logger.info('Not archiving single file inside %s' % root_dir)
                    archived_file = os.path.join(root_dir, file_list[0])
                else:
                    base_path = os.path.join(self.output_path, output_name)
                    logger.info('Compressing %s to %s' % (root_dir, base_path))
                    archived_file = shutil.make_archive(base_path,
                      format='zip',
                      root_dir=root_dir)
                    print('Compressed:', os.path.basename(archived_file))
                if archived_file:
                    self.archived_outputs.append(archived_file)