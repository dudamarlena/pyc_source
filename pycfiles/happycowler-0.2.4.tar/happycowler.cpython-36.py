# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pwittek/wrk/python/happycowler/happycowler/happycowler.py
# Compiled at: 2017-06-09 17:55:38
# Size of source mod 2**32: 7008 bytes
"""
Created on Sat Sep 24 18:02:47 2016

@author: pwittek
"""
from __future__ import print_function
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen

import sys
from bs4 import BeautifulSoup
from .file_io import append_results_to_file, write_footer, write_header

def normalize(text):
    processed_text = text.replace('&', '&amp;')
    if sys.version_info.major == 3:
        return processed_text.strip()
    else:
        return processed_text.encode('utf-8').strip()


def get_parsed_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return BeautifulSoup(page, 'html.parser')


def parse_restaurant_page(restaurant_page):
    gmap_link = restaurant_page.find('div', class_='box__map__links').find('a')
    text_link = gmap_link.attrs['href']
    start = text_link.find('q=loc:') + 6
    lat, lon = text_link[start:].split('+')
    return (lat, lon)


class HappyCowler(object):
    __doc__ = 'Class for crawling the HappyCow database\n\n    :param city_url: The URL string for the main page of the city to be\n                     crawled.\n    :type city_url: str.\n    :param target_file: Optional parameter to write the results to a target\n                        file.\n    :type target_file: str.\n\n    :param verbose: Optional parameter for level of verbosity:\n\n                       * 0: quiet (default)\n                       * 1: verbose\n    :type verbose: int.\n    '

    def __init__(self, city_url, target_file=None, verbose=0):
        """Constructor for the class.
        """
        self.city_url = city_url
        self.target_file = target_file
        self.verbose = verbose
        self.coordinates = []
        self.names = []
        self.tags = []
        self.ratings = []
        self.addresses = []
        self.phone_numbers = []
        self.opening_hours = []
        self.cuisines = []
        self.descriptions = []
        self.processed_entries = 0
        self.total_entries = 0

    def _parse_results_page(self, parsed_html, page_no='', deep_crawl=True):
        if self.total_entries == 0:
            h1 = parsed_html.body.find('h1').text.strip()
            self.total_entries = int(h1[h1.index('(') + 1:h1.index(')')])
        else:
            coordinates = []
            names = []
            tags = []
            ratings = []
            addresses = []
            phone_numbers = []
            opening_hours = []
            cuisines = []
            descriptions = []
            for business in parsed_html.body.findAll('div', class_='row venue-list-item'):
                self.processed_entries += 1
                restaurant_url = 'https://www.happycow.net' + business.find('a').get('href')
                if deep_crawl:
                    coordinates.append(parse_restaurant_page(get_parsed_html(restaurant_url)))
                else:
                    coordinates.append(('', ''))
                name = normalize(business.find('a').text)
                if self.verbose > 0:
                    percentage = ' (done: {:.2%}'.format(self.processed_entries / self.total_entries)
                    msg = '\r\x1b[KCurrent entry: ' + name + percentage + ')'
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                names.append(name)
                tags.append(normalize(business.find('span').text))
                stars = business.find('ul', class_='venue-ratings list-inline')
                if stars is None:
                    rating = 'unknown'
                else:
                    rating = str(len(stars.findAll('i', class_='fa fa-star')) + 0.5 * len(stars.findAll('i', class_='fa fa-star-half-o')))
                ratings.append(rating)
                address = None
                for p in business.findAll('p'):
                    if p.find('i', class_='fa fa-map-marker'):
                        address = p.text

                if address is not None:
                    addresses.append(normalize(address))
                else:
                    addresses.append('')
                phone_number = None
                for p in business.findAll('p'):
                    if p.find('i', class_='fa fa-phone'):
                        phone_number = p.text

                if phone_number is not None:
                    phone_numbers.append(normalize(phone_number))
                else:
                    phone_numbers.append('')
                opening_hour = business.find('span', class_='venue-hours-container')
                if opening_hour is not None:
                    opening_hours.append(normalize(opening_hour.attrs['data-summary']))
                else:
                    opening_hours.append('')
                cuisine = None
                for p in business.findAll('p'):
                    if 'uisine' in p.text:
                        cuisine = p.text

                if cuisine is not None:
                    cuisines.append(normalize(cuisine))
                else:
                    cuisines.append('')
                divs = business.findAll('div', class_='col-xs-12')
                description = divs[(-1)].find('p').text
                if description is not None:
                    descriptions.append(normalize(description))
                else:
                    description.append('')

            if self.target_file is not None:
                append_results_to_file(self.target_file, coordinates, names, tags, ratings, addresses, phone_numbers, opening_hours, cuisines, descriptions)
            self.coordinates += coordinates
            self.names += names
            self.tags += tags
            self.ratings += ratings
            self.addresses += addresses
            self.phone_numbers += phone_numbers
            self.opening_hours += opening_hours
            self.cuisines += cuisines
            self.descriptions += descriptions
            pagination = parsed_html.body.find('ul', class_='pagination')
            if pagination is not None:
                for a in pagination.findAll('a'):
                    if 'aria-label' in a.attrs and a.attrs['aria-label'] == 'Next':
                        new_page_no = a.attrs['href']
                        new_page_no = new_page_no[new_page_no.index('?page'):]
                        if page_no != new_page_no:
                            new_page = get_parsed_html(self.city_url + new_page_no)
                            self._parse_results_page(new_page, new_page_no)

            elif self.verbose > 0:
                sys.stdout.write('\n')

    def _estimate_number_of_restaurants(self):
        self.total_entries = 0

    def crawl(self):
        """Process the results page.
        """
        if self.target_file is not None:
            write_header(self.target_file)
        else:
            self._parse_results_page(get_parsed_html(self.city_url))
            if self.verbose > 0:
                sys.stdout.write('\r')
            if self.target_file is not None:
                write_footer(self.target_file)