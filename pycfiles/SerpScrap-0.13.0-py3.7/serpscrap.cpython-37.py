# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serpscrap\serpscrap.py
# Compiled at: 2018-08-26 07:33:12
# Size of source mod 2**32: 7666 bytes
"""
SerpScrap.SerpScrap
"""
import argparse, os, pprint, shutil
from scrapcore.core import Core
from scrapcore.logger import Logger
from serpscrap.config import Config
from serpscrap.csv_writer import CsvWriter
from serpscrap.chrome_install import ChromeInstall
from serpscrap.phantom_install import PhantomInstall
from serpscrap.urlscrape import UrlScrape
logger = Logger()
logger.setup_logger()
logger = logger.get_logger()

class SerpScrap:
    __doc__ = 'main module to execute the serp and url scrape tasks\n    Attributes:\n        args: list for cli args\n        serp_query: list holds the keywords to query the search engine\n        cli (list): for cli attributes\n        init (dict, str|list): init SerpScarp\n        run (): main method\n        scrap_serps (): scrape serps\n        scrap (): calls GoogleScraper\n        scrap_url(string): calls UrlScrape\n        as_csv(string): scrape serps save as csv\n    '
    args = []
    serp_query = None
    results = []
    related = []

    def cli(self, args=None):
        """method called if executed on command line
        Args:
            args (mixed): args via commandline
        Returns:
            list: dicts of results
        """
        parser = argparse.ArgumentParser(prog='serpscrap')
        parser.add_argument('-k',
          '--keyword',
          help='keyword for scraping',
          nargs='*')
        self.args = parser.parse_args()
        if len(self.args.keyword) > 0:
            keywords = ' '.join(self.args.keyword)
        self.init(config=None, keywords=keywords)
        return self.run()

    def init(self, config=None, keywords=None):
        """init config and serp_query
        Args:
            config (None|dict): override default config
            keywords (str|list): string or list of strings, keywords to scrape
        Raises:
            ValueError:
        """
        if config is not None:
            self.config = config
        else:
            self.config = Config().get()
        if self.config['executable_path'] == '' and self.config['sel_browser'] == 'phantomjs':
            logger.info('preparing phantomjs')
            firstrun = PhantomInstall()
            phantomjs = firstrun.detect_phantomjs()
            if phantomjs is None:
                firstrun.download()
                phantomjs = firstrun.detect_phantomjs()
                if phantomjs is None:
                    raise Exception('\n                        phantomjs binary not found,\n                        provide custom path in config')
            self.config.__setitem__('executable_path', phantomjs)
            logger.info('using ' + str(phantomjs))
        else:
            if self.config['executable_path'] == '':
                if self.config['sel_browser'] == 'chrome':
                    logger.info('preparing chromedriver')
                    firstrun = ChromeInstall()
                    chromedriver = firstrun.detect_chromedriver()
                    if chromedriver is None:
                        firstrun.download()
                        chromedriver = firstrun.detect_chromedriver()
                        if chromedriver is None:
                            raise Exception('\n                        chromedriver binary not found,\n                        provide custom path in config')
                    self.config.__setitem__('executable_path', chromedriver)
                    logger.info('using ' + str(chromedriver))
        if os.path.exists(self.config['dir_screenshot']):
            shutil.rmtree((self.config['dir_screenshot']), ignore_errors=True)
        else:
            screendir = '{}/{}'.format(self.config['dir_screenshot'], self.config['today'])
            if not os.path.exists(screendir):
                os.makedirs(screendir)
            elif isinstance(keywords, str):
                self.serp_query = [
                 keywords]
            else:
                if isinstance(keywords, list) and len(keywords) > 0:
                    self.serp_query = keywords
                else:
                    raise ValueError('no keywords given')

    def run(self):
        """main method to run scrap_serps and scrap_url
        Returns:
            list: dicts with all results
        """
        self.results = []
        if self.serp_query is not None:
            self.results = self.scrap_serps()
        if self.config['scrape_urls']:
            for index, result in enumerate(self.results):
                if 'serp_type' in result and 'serp_url' in result:
                    logger.info('Scraping URL: ' + result['serp_url'])
                    result_url = self.scrap_url(result['serp_url'])
                    if 'status' in result_url:
                        self.results[index].update(result_url)

        if isinstance(self.results, list):
            return self.results
        return [self.results]

    def as_csv(self, file_path):
        writer = CsvWriter()
        self.results = self.run()
        writer.write(file_path + '.csv', self.results)

    def scrap_serps(self):
        """call scrap method and append serp results to list
        Returns
            list: dict of scrape results
        """
        search = self.scrap()
        self.results = []
        if search is not None:
            for serp in search.serps:
                self.related = []
                for related_keyword in serp.related_keywords:
                    self.related.append({'keyword':related_keyword.keyword, 
                     'rank':related_keyword.rank})

                for link in serp.links:
                    self.results.append({'query_num_results_total':serp.num_results_for_query, 
                     'query_num_results_page':serp.num_results, 
                     'query_page_number':serp.page_number, 
                     'query':serp.query, 
                     'serp_rank':link.rank, 
                     'serp_type':link.link_type, 
                     'serp_url':link.link, 
                     'serp_rating':link.rating, 
                     'serp_title':link.title, 
                     'serp_domain':link.domain, 
                     'serp_visible_link':link.visible_link, 
                     'serp_snippet':link.snippet, 
                     'serp_sitelinks':link.sitelinks, 
                     'screenshot':os.path.join('{}/{}/{}_{}-p{}.png'.format(self.config['dir_screenshot'], self.config['today'], 'google', serp.query, str(serp.page_number)))})

            return self.results
        raise Exception('No Results')

    def scrap(self):
        """scrap, method calls GoogleScraper method
        Returns:
            dict: scrape result#
        """
        self.config['keywords'] = self.serp_query if isinstance(self.serp_query, list) else [self.serp_query]
        return Core().run(self.config)

    def scrap_url(self, url):
        """method calls UrlScrape
        Args:
            url (string): url to scrape
        Returns:
            dict: result of url scrape
        """
        urlscrape = UrlScrape(self.config)
        return urlscrape.scrap_url(url)

    def get_related(self):
        return self.related


if __name__ == '__main__':
    res = SerpScrap().cli()
    pprint.pprint(res)