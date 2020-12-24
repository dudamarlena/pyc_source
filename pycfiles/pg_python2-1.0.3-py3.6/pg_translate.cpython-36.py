# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_translate.py
# Compiled at: 2018-11-30 06:03:49
# Size of source mod 2**32: 1268 bytes
"""
contains various utilities to translate dates
"""
import logging, pg_dates

class Translate(object):
    region = None
    supported_regions = [
     'middle-east',
     'gregorian']

    def __init__(self, region):
        self.region = region
        self._test_region()

    def _help(self):
        logging.info('Supported Regions')
        logging.info('-----------------')
        for item in self.supported_regions:
            logging.info(item)

    def _test_region(self):
        if self.region not in self.supported_regions:
            self._help()
            raise Exception('Region not supported')

    def get_datetime(self, text, **kwargs):
        """
        :param text:
        :param kwargs: dictionary that supports "format" as a key and
        value will be as per the language. Format is a list
        :return:
        """
        if self.region == 'middle-east':
            return pg_dates.middle_east_parsed_date(text, kwargs)
        if self.region == 'gregorian':
            return pg_dates.gregorian_parsed_date(text, kwargs)


if __name__ == '__main__':
    tr = Translate('middle-east')
    td = tr.get_datetime('1397, 8, Dec', format=['%Y', '%m', '%d'])
    print(td)