# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/oddsman/oddsman.py
# Compiled at: 2017-06-27 10:56:57
# Size of source mod 2**32: 3526 bytes
from bs4 import BeautifulSoup
from urllib import request

class OddsWatcher(object):

    def __get_request_via_get(self, url):
        source = request.urlopen(url)
        return source

    def __find_hid(self, td):
        for link in td.findAll('a'):
            url = link.attrs['href']
            if '/horse/' in link.attrs['href']:
                tmp = url.split('/')
                return tmp[4]

    def __find_rid(self, td):
        for link in td.findAll('a'):
            url = link.attrs['href']
            if '&' in url:
                tmp = url.split('&')
                tmp = tmp[1].split('=')
                return tmp[1][1:]

    def __extract_time(self, text):
        text = text.strip()
        time = text[:5]
        return time

    def __2dict(self, df, time_df):
        if len(df) != len(time_df):
            print('file length is different. void dictionalize')
            return
        dict = {}
        for rid, time in zip(df, time_df):
            dict[time] = rid

        return dict

    def __find_race_time(self, div):
        text = div.text
        time = self._OddsWatcher__extract_time(text)
        if time is not None:
            return time

    def __scrape_race_info(self, source):
        soup = BeautifulSoup(source, 'lxml')
        df = []
        title = soup.find('h1')
        print(title.text)
        self.title = title.text
        table = soup.find(class_='race_table_old nk_tb_common')
        for tr in table.findAll('tr', ''):
            row = []
            for td in tr.findAll('td', ''):
                word = ' '.join(td.text.rsplit())
                row.append(word)
                hid = self._OddsWatcher__find_hid(td)
                if hid is not None:
                    row.append(hid)

            df.append(row)

        return df

    def __scrape_race_id(self, source):
        soup = BeautifulSoup(source, 'lxml')
        df = []
        time_df = []
        body = soup.find(id='race_list_body')
        for col in body.findAll(class_='race_top_hold_list'):
            row = []
            times = []
            for div in col.findAll(class_='racename'):
                rid = self._OddsWatcher__find_rid(div)
                if rid is not None:
                    row.append(rid)

            df.append(row)
            for div in col.findAll(class_='racedata'):
                time = self._OddsWatcher__find_race_time(div)
                if time is not None:
                    times.append(time)

            time_df.append(times)
            dict = self._OddsWatcher__2dict(row, times)
            yield dict

    def get_race_odds(self, race_id):
        url = 'http://race.netkeiba.com/?pid=race_old&id=c' + str(race_id)
        source = self._OddsWatcher__get_request_via_get(url)
        self.df = self._OddsWatcher__scrape_race_info(source)
        odds_list = [x[10] for x in self.df if len(x) > 0]
        return odds_list

    def get_race_ids(self, date):
        url = 'http://race.netkeiba.com/?pid=race_list&id=p' + str(date)
        source = self._OddsWatcher__get_request_via_get(url)
        dict = {}
        for d in self._OddsWatcher__scrape_race_id(source):
            dict.update(d)

        print(dict)