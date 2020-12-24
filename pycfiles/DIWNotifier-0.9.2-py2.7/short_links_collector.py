# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/utils/short_links_collector/short_links_collector.py
# Compiled at: 2014-01-29 20:12:07
import os, logging
module_logger = logging.getLogger('utils.utils.shor_links_collector')

class ShortLinksCollector(object):

    def __init__(self, file_name):
        self.import_check()
        self.bitly_shortener = tiny4py.getShortener(tiny4py.BITLY_ID)
        self.bitly_shortener.setApi('tiny4py', 'R_b69f9ca899f8e7ef59fd5c27272ec26c')
        self.links = {}
        self.file_name = file_name
        self.entry_count_onload = -1

    @staticmethod
    def import_check():
        global tiny4py
        try:
            import tiny4py
        except ImportError:
            tiny4py = None
            module_logger.error('Please install tiny4py python module first, see https://code.google.com/p/tiny4py/')
            raise ImportError('Please install tiny4py python module first, see https://code.google.com/p/tiny4py/')

        return

    def load(self):
        if os.path.getsize(self.file_name) > 10:
            with open(self.file_name, 'r') as (f):
                data = f.readlines()
                for line in data:
                    entry = line.split()
                    self.links[entry[0]] = entry[1]

        self.entry_count_onload = len(self.links)

    def save(self):
        if self.entry_count_onload != len(self.links) and len(self.links) > 0:
            with open(self.file_name, 'w+') as (f):
                for link, short_link in self.links.items():
                    f.write(link + ' ' + short_link + '\n')

    def match(self, new_link):
        for link, short_link in self.links.items():
            if link == new_link or short_link == new_link:
                return True

        return False

    def add(self, link):
        if not self.match(link):
            self.links[link] = self.bitly_shortener.getShorturl(link)
        return self.links[link]

    def mirror(self, new_link):
        if new_link[0:14] == 'http://bit.ly/' and len(new_link) == 21:
            for key in self.links.keys():
                if self.links[key] == new_link:
                    return key

        else:
            for link in self.links.items():
                if link == new_link:
                    return self.links[link]

        return 'http://clandiw.it/index.php?app=core&module=search&do=viewNewContent&search_app=forums&sid=2a4e1257c3e3566f5f623a86709fa4f8&search_app_filters[forums][searchInKey]=&change=1&period=week&userMode=all&followedItemsOnly=0'