# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/utils/csvutils.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import csv, requests, logging
logging.getLogger('requests').setLevel(logging.ERROR)

class FastDictReader(object):

    def __init__(self, f, fieldnames=None, dialect='excel', *args, **kwargs):
        self.__fieldNames = fieldnames
        self.reader = csv.reader(f, dialect, *args, **kwargs)
        if self.__fieldNames is None:
            self.__fieldNames = self.reader.next()
        self.__dict = {}
        return

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        while row == []:
            row = self.reader.next()

        assert len(self.__fieldNames) == len(row)
        for i in xrange(len(self.__fieldNames)):
            self.__dict[self.__fieldNames[i]] = row[i]

        return self.__dict


def download_csv(url, url_params=None, content_type='text/csv'):
    response = requests.get(url, params=url_params)
    response.raise_for_status()
    response_content_type = response.headers['content-type']
    if response_content_type != content_type:
        raise Exception('Invalid content-type: %s' % response_content_type)
    ret = response.text
    while not ret[0].isalnum():
        ret = ret[1:]

    return ret


def float_or_string(value):
    try:
        ret = float(value)
    except Exception:
        ret = value

    return ret