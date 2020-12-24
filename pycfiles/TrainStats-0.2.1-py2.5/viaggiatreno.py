# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/viaggiatreno/viaggiatreno.py
# Compiled at: 2009-02-02 06:06:20
import os, pickle
from datetime import date
from siteintf import SiteInterface

class DataUnavailable(Exception):
    pass


class ViaggiaTreno:
    DEFAULT_CACHE_DIR = 'cache'

    def __init__(self, dir=DEFAULT_CACHE_DIR):
        self.dir = dir
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        self._si = SiteInterface()

    def _getFilename(self, tid, date_):
        datef = date_.strftime('%Y%m%d')
        file = '%d-%s.txt' % (tid, datef)
        ret = os.path.join(self.dir, file)
        return ret

    def _getHTMLFilename(self, tid, date_):
        datef = date_.strftime('%Y%m%d')
        file = '%d-%s.html' % (tid, datef)
        ret = os.path.join(self.dir, file)
        return ret

    def haveCacheTxt(self, tid, date_):
        return os.path.isfile(self._getFilename(tid, date_))

    def haveCacheHTML(self, tid, date_):
        return os.path.isfile(self._getHTMLFilename(tid, date_))

    def isCached(self, tid, date_):
        return self.haveCacheTxt(tid, date_) or self.haveCacheHTML(self, tid, date_)

    def get(self, tid, date_):
        if self.haveCacheTxt(tid, date_):
            pkl_file = open(self._getFilename(tid, date_), 'rb')
            data = pickle.load(pkl_file)
            pkl_file.close()
        elif self.haveCacheHTML(tid, date_):
            data = self._si.query(tid, infile=self._getHTMLFilename(tid, date_))
            output = open(self._getFilename(tid, date_), 'wb')
            pickle.dump(data, output)
            output.close()
        elif date_ == date.today():
            data = self._si.query(tid, self._getHTMLFilename(tid, date_))
            output = open(self._getFilename(tid, date_), 'wb')
            pickle.dump(data, output)
            output.close()
        else:
            raise DataUnavailable()
        return data


if __name__ == '__main__':
    import datetime
    vt = ViaggiaTreno()
    data = vt.get(663, datetime.date.today())
    print data