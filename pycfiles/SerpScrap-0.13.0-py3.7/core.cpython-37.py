# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\core.py
# Compiled at: 2017-09-21 11:30:01
# Size of source mod 2**32: 6596 bytes
import datetime, queue, threading
from random import shuffle
from scrapcore.cachemanager import CacheManager
from scrapcore.database import ScraperSearch
from scrapcore.database import get_session, fixtures
from scrapcore.logger import Logger
from scrapcore.result_writer import ResultWriter
from scrapcore.scraper.scrape_worker_factory import ScrapeWorkerFactory
from scrapcore.tools import Proxies
from scrapcore.tools import ScrapeJobGenerator
from scrapcore.tools import ShowProgressQueue
from scrapcore.validator_config import ValidatorConfig

class Core:
    logger = None

    def run(self, config):
        """run with the dict in config."""
        validator = ValidatorConfig()
        validator.validate(config)
        return self.main(return_results=True, config=config)

    def main(self, return_results=False, config=None):
        """the main method"""
        logger = Logger()
        logger.setup_logger(level=(config.get('log_level').upper()))
        self.logger = logger.get_logger()
        keywords = set(config.get('keywords', []))
        proxy_file = config.get('proxy_file', '')
        search_engines = config.get('search_engines', ['google'])
        if not isinstance(search_engines, list):
            if search_engines == '*':
                search_engines = config.get('supported_search_engines')
            else:
                search_engines = search_engines.split(',')
        search_engines = set(search_engines)
        num_search_engines = len(search_engines)
        num_workers = int(config.get('num_workers'))
        scrape_method = config.get('scrape_method')
        pages = int(config.get('num_pages_for_keyword', 1))
        method = config.get('scrape_method', 'selenium')
        result_writer = ResultWriter()
        result_writer.init_outfile(config, force_reload=True)
        cache_manager = CacheManager(config, self.logger, result_writer)
        scrape_jobs = {}
        if not scrape_jobs:
            scrape_jobs = ScrapeJobGenerator().get(keywords, search_engines, scrape_method, pages)
        scrape_jobs = list(scrape_jobs)
        proxies = []
        if config.get('use_own_ip'):
            proxies.append(None)
        else:
            if proxy_file:
                proxies = Proxies().parse_proxy_file(proxy_file)
            elif not proxies:
                raise Exception('No proxies available. Turning down.')
            else:
                shuffle(proxies)
                session_cls = get_session(config, scoped=True)
                session = session_cls()
                fixtures(config, session)
                Proxies().add_proxies_to_db(proxies, session)
                scraper_search = ScraperSearch(number_search_engines_used=num_search_engines,
                  number_proxies_used=(len(proxies)),
                  number_search_queries=(len(keywords)),
                  started_searching=(datetime.datetime.utcnow()),
                  used_search_engines=(','.join(search_engines)))
                if config.get('do_caching'):
                    scrape_jobs = cache_manager.filter_scrape_jobs(scrape_jobs, session, scraper_search)
                if scrape_jobs:
                    db_lock = threading.Lock()
                    cache_lock = threading.Lock()
                    captcha_lock = threading.Lock()
                    self.logger.info('\n                Going to scrape {num_keywords} keywords with {num_proxies}\n                proxies by using {num_threads} threads.'.format(num_keywords=(len(list(scrape_jobs))),
                      num_proxies=(len(proxies)),
                      num_threads=num_search_engines))
                    progress_thread = None
                    q = queue.Queue()
                    progress_thread = ShowProgressQueue(config, q, len(scrape_jobs))
                    progress_thread.start()
                    workers = queue.Queue()
                    num_worker = 0
                    for search_engine in search_engines:
                        for proxy in proxies:
                            for worker in range(num_workers):
                                num_worker += 1
                                workers.put(ScrapeWorkerFactory(config,
                                  cache_manager=cache_manager,
                                  mode=method,
                                  proxy=proxy,
                                  search_engine=search_engine,
                                  session=session,
                                  db_lock=db_lock,
                                  cache_lock=cache_lock,
                                  scraper_search=scraper_search,
                                  captcha_lock=captcha_lock,
                                  progress_queue=q,
                                  browser_num=num_worker))

                    for job in scrape_jobs:
                        while True:
                            worker = workers.get()
                            workers.put(worker)
                            if worker.is_suitabe(job):
                                worker.add_job(job)
                                break

                    threads = []
                    while not workers.empty():
                        worker = workers.get()
                        thread = worker.get_worker()
                        if thread:
                            threads.append(thread)

                    for t in threads:
                        t.start()

                    for t in threads:
                        t.join()

                    q.put('done')
                    progress_thread.join()
                result_writer.close_outfile()
                scraper_search.stopped_searching = datetime.datetime.utcnow()
                try:
                    session.add(scraper_search)
                    session.commit()
                except Exception:
                    pass

            if return_results:
                return scraper_search