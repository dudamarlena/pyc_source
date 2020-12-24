# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/zoidberg.py
# Compiled at: 2018-03-09 10:11:24
# Size of source mod 2**32: 4060 bytes
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import json, os, pprint
configure_logging({'LOG_FORMAT':'%(levelname)s: %(message)s',  'LOG_LEVEL':'DEBUG'})

class ZoidbergReactor:
    __doc__ = '\n    Start a new CrawlerRunner object for the idealista scrapper\n    '

    def __init__(self, country='es', doctor=None, area=None, illness=None, output='csv', path=None, *args, **kwargs):
        """
        Initialize the CrawlPropertyReactor object
        :param transaction: type of transaction {sale,rent}
        :param property_type: type of property {house,garage,commercial,land,office}
        :param provinces: a list of Spanish provinces to crawl (see idealista scrapper settings for the schema)
        :param args:
        :param kwargs:
        """
        self.stats_dic_list = []
        self.doctor = doctor
        self.area = area
        self.illness = illness
        self.output = output
        self.country = country.lower()
        self.country_db = 'db/' + country + '/' + country + '_db.json'
        if path:
            self.path = path
        else:
            self.path = 'zoigber_output.' + self.output
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {'scraper.pipelines.CleanItemsPipeline': 100, 
         'scraper.pipelines.%sPipeline' % output.capitalize(): 200}, 0)

    @defer.inlineCallbacks
    def conf(self):
        runner = CrawlerRunner(self.settings)
        list_urls = self.get_list_urls(self.area, self.illness)
        doctor_words = self.get_doctor_regex_words(self.doctor)
        for i in range(0, len(list_urls)):
            domain = list_urls[i]['domain']
            urls = list_urls[i]['urls']
            zoidgber_crawler = runner.create_crawler(domain)
            yield runner.crawl(zoidgber_crawler, doctor_regex=doctor_words, urls=urls, path=(self.path))

        reactor.stop()

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()

    def get_doctor_regex_words(self, doctor):
        name_list = [
         doctor, doctor.capitalize(), doctor.upper(), doctor.lower(), doctor.title()]
        regex = ''
        for w in name_list:
            regex += '(\\s' + w + '\\s)|'

        return regex[:-1]

    def get_list_urls(self, area_raw, illness_raw):
        list_urls = []
        data = json.load(open(self.country_db))
        for area in data['area']:
            if area['slug'] == area_raw:
                for illness in area['illness']:
                    if illness['slug'] == illness_raw:
                        list_urls = illness['webs']

        return list_urls

    def get_countries(self):
        return next(os.walk('./db/'))[1]

    def get_domains(self):
        data = json.load(open(self.country_db))
        return data['domains']

    def get_areas(self):
        data = json.load(open(self.country_db))
        return [area['slug'] for area in data['area']]

    def get_illness_for_area(self, area=None):
        data = json.load(open(self.country_db))
        if area not in self.get_areas():
            return 'Please, insert a valid area. use get_areas() function to get a list of valid areas.'
        else:
            return [illness['slug'] for _area in data['area'] if _area['slug'] == area for illness in _area['illness']]


if __name__ == '__main__':
    zoidberg = ZoidbergReactor(country='es', doctor='margalet', area='traumatologia', illness='femoroacetabular', path='aah.csv', output='csv')
    zoidberg.conf()
    zoidberg.run()