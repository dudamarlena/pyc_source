# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: craigslist/base.py
# Compiled at: 2019-12-12 18:28:26
import logging
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from threading import Thread
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from six import iteritems
from six.moves import range
from .utils import bs, requests_get, get_all_sites, get_list_filters
ALL_SITES = get_all_sites()
RESULTS_PER_REQUEST = 100

class CraigslistBase(object):
    """ Base class for all Craiglist wrappers. """
    url_templates = {'base': 'http://%(site)s.craigslist.org', 
       'no_area': 'http://%(site)s.craigslist.org/search/%(category)s', 
       'area': 'http://%(site)s.craigslist.org/search/%(area)s/%(category)s'}
    default_site = 'sfbay'
    default_category = None
    base_filters = {'query': {'url_key': 'query', 'value': None}, 'search_titles': {'url_key': 'srchType', 'value': 'T'}, 'has_image': {'url_key': 'hasPic', 'value': 1}, 'posted_today': {'url_key': 'postedToday', 'value': 1}, 'bundle_duplicates': {'url_key': 'bundleDuplicates', 'value': 1}, 'search_distance': {'url_key': 'search_distance', 'value': None}, 'zip_code': {'url_key': 'postal', 'value': None}}
    extra_filters = {}
    __list_filters = {}
    custom_result_fields = False
    sort_by_options = {'newest': 'date', 
       'price_asc': 'priceasc', 
       'price_desc': 'pricedsc'}

    def __init__(self, site=None, area=None, category=None, filters=None, log_level=logging.WARNING):
        self.set_logger(log_level, init=True)
        self.site = site or self.default_site
        if self.site not in ALL_SITES:
            msg = "'%s' is not a valid site" % self.site
            self.logger.error(msg)
            raise ValueError(msg)
        if area:
            if not self.is_valid_area(area):
                msg = "'%s' is not a valid area for site '%s'" % (area, site)
                self.logger.error(msg)
                raise ValueError(msg)
        self.area = area
        self.category = category or self.default_category
        url_template = self.url_templates[('area' if area else 'no_area')]
        self.url = url_template % {'site': self.site, 'area': self.area, 'category': self.category}
        self.filters = self.get_filters(filters)

    def get_filters(self, filters):
        """Parses filters passed by the user into GET parameters."""
        list_filters = self.get_list_filters(self.url)
        parsed_filters = {'searchNearby': 1}
        for key, value in iteritems(filters or {}):
            try:
                filter_ = self.base_filters.get(key) or self.extra_filters.get(key) or list_filters[key]
                if filter_['value'] is None:
                    parsed_filters[filter_['url_key']] = value
                elif isinstance(filter_['value'], list):
                    valid_options = filter_['value']
                    if not hasattr(value, '__iter__'):
                        value = [
                         value]
                    options = []
                    for opt in value:
                        try:
                            options.append(valid_options.index(opt) + 1)
                        except ValueError:
                            self.logger.warning("'%s' is not a valid option for %s" % (
                             opt, key))

                    parsed_filters[filter_['url_key']] = options
                elif value:
                    parsed_filters[filter_['url_key']] = filter_['value']
            except KeyError:
                self.logger.warning("'%s' is not a valid filter", key)

        return parsed_filters

    def set_logger(self, log_level, init=False):
        if init:
            self.logger = logging.getLogger('python-craiglist')
            self.handler = logging.StreamHandler()
            self.logger.addHandler(self.handler)
        self.logger.setLevel(log_level)
        self.handler.setLevel(log_level)

    def is_valid_area(self, area):
        base_url = self.url_templates['base']
        response = requests_get(base_url % {'site': self.site}, logger=self.logger)
        soup = bs(response.content)
        sublinks = soup.find('ul', {'class': 'sublinks'})
        return sublinks and sublinks.find('a', text=area) is not None

    def get_results(self, limit=None, start=0, sort_by=None, geotagged=False, include_details=False):
        """
        Gets results from Craigslist based on the specified filters.

        If geotagged=True, the results will include the (lat, lng) in the
        'geotag' attrib (this will make the process a little bit longer).
        """
        if sort_by:
            try:
                self.filters['sort'] = self.sort_by_options[sort_by]
            except KeyError:
                msg = "'%s' is not a valid sort_by option, use: 'newest', 'price_asc' or 'price_desc'" % sort_by
                self.logger.error(msg)
                raise ValueError(msg)

        total_so_far = start
        results_yielded = 0
        total = 0
        while True:
            self.filters['s'] = start
            response = requests_get(self.url, params=self.filters, logger=self.logger)
            self.logger.info('GET %s', response.url)
            self.logger.info('Response code: %s', response.status_code)
            response.raise_for_status()
            soup = bs(response.content)
            if not total:
                totalcount = soup.find('span', {'class': 'totalcount'})
                total = int(totalcount.text) if totalcount else 0
            rows = soup.find('ul', {'class': 'rows'})
            for row in rows.find_all('li', {'class': 'result-row'}, recursive=False):
                if limit is not None and results_yielded >= limit:
                    break
                self.logger.debug('Processing %s of %s results ...', total_so_far + 1, total)
                yield self.process_row(row, geotagged, include_details)
                results_yielded += 1
                total_so_far += 1

            if results_yielded == limit:
                break
            if total_so_far - start < RESULTS_PER_REQUEST:
                break
            start = total_so_far

        return

    def process_row(self, row, geotagged=False, include_details=False):
        id = row.attrs['data-pid']
        repost_of = row.attrs.get('data-repost-of')
        link = row.find('a', {'class': 'hdrlnk'})
        name = link.text
        url = urljoin(self.url, link.attrs['href'])
        time = row.find('time')
        if time:
            datetime = time.attrs['datetime']
        else:
            pl = row.find('span', {'class': 'pl'})
            datetime = pl.text.split(':')[0].strip() if pl else None
        price = row.find('span', {'class': 'result-price'})
        where = row.find('span', {'class': 'result-hood'})
        if where:
            where = where.text.strip()[1:-1]
        tags_span = row.find('span', {'class': 'result-tags'})
        tags = tags_span.text if tags_span else ''
        result = {'id': id, 'repost_of': repost_of, 
           'name': name, 
           'url': url, 
           'datetime': datetime, 
           'last_updated': datetime, 
           'price': price.text if price else None, 
           'where': where, 
           'has_image': 'pic' in tags, 
           'geotag': None}
        if geotagged or include_details:
            detail_soup = self.fetch_content(result['url'])
            if geotagged:
                self.geotag_result(result, detail_soup)
            if include_details:
                self.include_details(result, detail_soup)
        if self.custom_result_fields:
            self.customize_result(result)
        return result

    def customize_result(self, result):
        """ Adds custom/delete/alter fields to result. """
        pass

    def geotag_result(self, result, soup):
        """ Adds (lat, lng) to result. """
        self.logger.debug('Geotagging result ...')
        map = soup.find('div', {'id': 'map'})
        if map:
            result['geotag'] = (
             float(map.attrs['data-latitude']),
             float(map.attrs['data-longitude']))
        return result

    def include_details(self, result, soup):
        """ Adds description, images to result """
        self.logger.debug('Adding details to result...')
        body = soup.find('section', id='postingbody')
        body_text = (getattr(e, 'text', e) for e in body if not getattr(e, 'attrs', None))
        result['body'] = ('').join(body_text).strip()
        postinginfos = soup.find('div', {'class': 'postinginfos'})
        for p in postinginfos.find_all('p'):
            if 'posted' in p.text:
                time = p.find('time')
                if time:
                    created = time.attrs['datetime'].replace('T', ' ')
                    result['created'] = created.rsplit(':', 1)[0]

        image_tags = soup.find_all('img')
        image_tags = image_tags[1:] if len(image_tags) > 1 else image_tags
        images = []
        for img in image_tags:
            if 'src' not in img:
                continue
            img_link = img['src'].replace('50x50c', '600x450')
            images.append(img_link)

        result['images'] = images
        attrgroups = soup.find_all('p', {'class': 'attrgroup'})
        attrs = []
        for attrgroup in attrgroups:
            for attr in attrgroup.find_all('span'):
                attr_text = attr.text.strip()
                if attr_text:
                    attrs.append(attr_text)

        result['attrs'] = attrs
        if attrs:
            self.parse_attrs(result)

    def parse_attrs(self, result):
        """Parses raw attributes into structured fields in the result dict."""
        attrs = set(attr.lower() for attr in result['attrs'])
        for key, options in iteritems(self.extra_filters):
            if options['value'] != 1:
                continue
            if options.get('attr', '') in attrs:
                result[key] = True

        attrs_after_colon = set(attr.split(': ', 1)[(-1)] for attr in result['attrs'])
        for key, options in iteritems(self.get_list_filters(self.url)):
            for option in options['value']:
                if option in attrs_after_colon:
                    result[key] = option
                    break

    def fetch_content(self, url):
        response = requests_get(url, logger=self.logger)
        self.logger.info('GET %s', response.url)
        self.logger.info('Response code: %s', response.status_code)
        if response.ok:
            return bs(response.content)
        else:
            return

    def geotag_results(self, results, workers=8):
        """
        Adds (lat, lng) to each result. This process is done using N threads,
        where N is the amount of workers defined (default: 8).
        """
        results = list(results)
        queue = Queue()
        for result in results:
            queue.put(result)

        def geotagger():
            while not queue.empty():
                self.logger.debug('%s results left to geotag ...', queue.qsize())
                self.geotag_result(queue.get())
                queue.task_done()

        threads = []
        for _ in range(workers):
            thread = Thread(target=geotagger)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return results

    @classmethod
    def get_list_filters(cls, url):
        if cls.__list_filters.get(url) is None:
            cls.__list_filters[url] = get_list_filters(url)
        return cls.__list_filters[url]

    @classmethod
    def show_filters(cls, category=None):
        print 'Base filters:'
        for key, options in iteritems(cls.base_filters):
            value_as_str = '...' if options['value'] is None else 'True/False'
            print '* %s = %s' % (key, value_as_str)

        print 'Section specific filters:'
        for key, options in iteritems(cls.extra_filters):
            value_as_str = '...' if options['value'] is None else 'True/False'
            print '* %s = %s' % (key, value_as_str)

        url = cls.url_templates['no_area'] % {'site': cls.default_site, 
           'category': category or cls.default_category}
        list_filters = cls.get_list_filters(url)
        for key, options in iteritems(list_filters):
            value_as_str = (', ').join([ repr(opt) for opt in options['value'] ])
            print '* %s = %s' % (key, value_as_str)

        return