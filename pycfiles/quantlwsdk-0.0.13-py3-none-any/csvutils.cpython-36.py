# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\utils\csvutils.py
# Compiled at: 2019-06-05 03:26:22
# Size of source mod 2**32: 2505 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import csv, logging, six
from six.moves import xrange
import requests
logging.getLogger('requests').setLevel(logging.ERROR)

class FastDictReader(object):

    def __init__(self, f, fieldnames=None, dialect='excel', *args, **kwargs):
        self._FastDictReader__fieldNames = fieldnames
        self.reader = (csv.reader)(f, dialect, *args, **kwargs)
        if self._FastDictReader__fieldNames is None:
            self._FastDictReader__fieldNames = six.next(self.reader)
        self._FastDictReader__dict = {}

    def _next_impl(self):
        row = six.next(self.reader)
        while row == []:
            row = six.next(self.reader)

        assert len(self._FastDictReader__fieldNames) == len(row), 'Expected columns: %s. Actual columns: %s' % (
         self._FastDictReader__fieldNames, list(row.keys()))
        for i in xrange(len(self._FastDictReader__fieldNames)):
            self._FastDictReader__dict[self._FastDictReader__fieldNames[i]] = row[i]

        return self._FastDictReader__dict

    def __iter__(self):
        return self

    def __next__(self):
        return self._next_impl()

    def next(self):
        return self._next_impl()


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