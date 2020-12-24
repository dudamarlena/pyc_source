# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\scraping.py
# Compiled at: 2018-10-10 11:17:25
# Size of source mod 2**32: 9942 bytes
import abc, datetime, logging, random, time
from scrapcore.database import db_Proxy
from scrapcore.parsing import Parsing
from scrapcore.result_writer import ResultWriter
from scrapcore.tools import Proxies
logger = logging.getLogger(__name__)
SEARCH_MODES = 'selenium'

class GoogleSearchError(Exception):
    pass


class InvalidNumberResultsException(GoogleSearchError):
    pass


class MaliciousRequestDetected(GoogleSearchError):
    pass


class SeleniumMisconfigurationError(Exception):
    pass


class SeleniumSearchError(Exception):
    pass


class StopScrapingException(Exception):
    pass


def get_base_search_url_by_search_engine(config, search_engine_name, search_mode):
    """Retrieves the search engine base url for a specific search_engine."""
    assert search_mode in SEARCH_MODES, 'search mode "{}" is not available'.format(search_mode)
    specific_base_url = config.get('{}_search_url'.format(search_engine_name), None)
    return specific_base_url


class SearchEngineScrape(metaclass=abc.ABCMeta):
    __doc__ = 'Abstract base class that represents a search engine scrape.'
    malicious_request_needles = {'google': {'inurl':'/sorry/', 
                'inhtml':'detected unusual traffic'}}

    def __init__(self, config, cache_manager=None, jobs=None, scraper_search=None, session=None, db_lock=None, cache_lock=None, start_page_pos=1, search_engine=None, search_type=None, proxy=None, progress_queue=None):
        """Instantiate an SearchEngineScrape object."""
        self.config = config
        self.cache_manager = cache_manager
        jobs = jobs or {}
        self.search_engine_name = search_engine.lower()
        if not self.search_engine_name:
            raise AssertionError('You need to specify an search_engine')
        else:
            if not search_type:
                self.search_type = self.config.get('search_type', 'normal')
            else:
                self.search_type = search_type
            self.jobs = jobs
            self.missed_keywords = set()
            self.num_keywords = len(self.jobs)
            self.query = ''
            self.pages_per_keyword = [
             1]
            self.search_number = 1
            self.parser = Parsing().get_parser_by_search_engine(self.search_engine_name)(config=(self.config))
            self.num_results_per_page = int(self.config.get('num_results_per_page', 10))
            if start_page_pos:
                self.start_page_pos = 1 if start_page_pos < 1 else start_page_pos
            else:
                self.start_page_pos = int(self.config.get('search_offset', 1))
            self.page_number = self.start_page_pos
            self.proxy = proxy
            if isinstance(proxy, Proxies().Proxy):
                self.set_proxy()
                self.requested_by = self.proxy.host + ':' + self.proxy.port
            else:
                self.requested_by = 'localhost'
        self.scraper_search = scraper_search
        self.scrape_method = ''
        self.startable = True
        self.db_lock = db_lock
        self.cache_lock = cache_lock
        self.progress_queue = progress_queue
        self.session = session
        self.requested_at = None
        self.name = '[{}]'.format(self.search_engine_name) + self.__class__.__name__
        self.sleeping_min = self.config.get('sleeping_min')
        self.sleeping_max = self.config.get('sleeping_max')
        self.timeout = 5
        self.status = 'successful'
        self.html = ''

    @abc.abstractmethod
    def search(self, *args, **kwargs):
        """Send the search request(s) over the transport."""
        pass

    @abc.abstractmethod
    def set_proxy(self):
        """Install a proxy on the communication channel."""
        pass

    @abc.abstractmethod
    def switch_proxy(self, proxy):
        """Switch the proxy on the communication channel."""
        pass

    @abc.abstractmethod
    def proxy_check(self, proxy):
        """Check whether the assigned proxy works correctly and react"""
        pass

    @abc.abstractmethod
    def handle_request_denied(self, status_code):
        """Generic behaviour when search engines detect our scraping.
        Args:
            status_code: The status code of the http response.
        """
        self.status = 'Malicious request detected: {}'.format(status_code)

    def store(self):
        """Store the parsed data in the sqlalchemy scoped session."""
        if not self.session:
            raise AssertionError('No database session.')
        elif self.html:
            self.parser.parse(self.html)
        else:
            self.parser = None
        with self.db_lock:
            serp = Parsing().parse_serp((self.config),
              parser=(self.parser),
              scraper=self,
              query=(self.query))
            self.scraper_search.serps.append(serp)
            self.session.add(serp)
            self.session.commit()
            ResultWriter().store_serp_result(serp, self.config)
            if serp.num_results:
                return True
            return False

    def next_page(self):
        """Increment the page."""
        self.start_page_pos += 1

    def keyword_info(self):
        """Print a short summary"""
        logger.info('\n            {thread_name} {ip} - Keyword: "{keyword}" with {num_pages} pages,\n            slept {delay} seconds before scraping. {done}/{all} already scraped\n            '.format(thread_name=(self.name),
          ip=(self.requested_by),
          keyword=(self.query),
          num_pages=(self.pages_per_keyword),
          delay=(self.current_delay),
          done=(self.search_number),
          all=(self.num_keywords)))

    def instance_creation_info(self, scraper_name):
        """Debug message whenever a scraping worker is created"""
        logger.info('\n        [+] {}[{}][search-type:{}][{}] using search engine "{}".\n        Num keywords={}, num pages for keyword={}\n        '.format(scraper_name, self.requested_by, self.search_type, self.base_search_url, self.search_engine_name, len(self.jobs), self.pages_per_keyword))

    def cache_results(self):
        """Caches the html for the current request."""
        self.cache_manager.cache_results((self.parser),
          (self.query),
          (self.search_engine_name),
          (self.scrape_method),
          (self.page_number),
          db_lock=(self.db_lock))

    def detection_prevention_sleep(self):
        self.current_delay = random.randrange(self.sleeping_min, self.sleeping_max)
        time.sleep(self.current_delay)

    def after_search(self):
        """Store the results and parse em.
        Notify the progress queue if necessary.
        """
        self.search_number += 1
        if not self.store():
            logger.debug('\n            No results to store for keyword: "{}" in search engine: {}\n            '.format(self.query, self.search_engine_name))
        if self.progress_queue:
            self.progress_queue.put(1)
        self.cache_results()

    def before_search(self):
        """before entering the search loop."""
        if self.config.get('check_proxies', True):
            if self.proxy:
                if not self.proxy_check(proxy=(self.proxy)):
                    self.startable = False

    def update_proxy_status(self, status, ipinfo=None, online=True):
        """Sets the proxy status with the results of ipinfo.io
        Args:
            status: A string the describes the status of the proxy.
            ipinfo: The json results from ipinfo.io
            online: Whether the proxy is usable or not.
        """
        ipinfo = ipinfo or {}
        with self.db_lock:
            proxy = self.session.query(db_Proxy).filter(self.proxy.host == db_Proxy.ip).first()
            if proxy:
                for key in ipinfo.keys():
                    setattr(proxy, key, ipinfo[key])

                proxy.checked_at = datetime.datetime.utcnow()
                proxy.status = status
                proxy.online = online
                try:
                    self.session.merge(proxy, load=True)
                    self.session.commit()
                except:
                    pass