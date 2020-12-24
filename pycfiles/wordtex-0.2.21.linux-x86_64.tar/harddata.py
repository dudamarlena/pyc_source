# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/harddata.py
# Compiled at: 2013-11-12 16:48:22
import time, math, cPickle, tempfiles, logtools
logtools.setup_logger(logtools.logging.DEBUG)
LOG = logtools.get_logger(__name__)

def harddata_base(object):
    MIN_KEEP_TIME = 0.5

    def __init__(self, data):
        self._data = data
        self._last_accessed = time.time()
        self._access_counter = 1
        self._THREAD_hold = False
        self._datafile = None
        self._get_tempfile()
        return

    def _get_tempfile(self):
        assert self._datafile == None
        self._datafile = tempfiles.get_temp_file()
        return

    def _getdata(self):
        """The primary magic that stores the data"""
        self._last_accessed = time.time()
        self._access_counter += 1
        try:
            return self._data
        except AttributeError:
            self._data = self._load_data()
            return self._data

    def _load_data(self):
        """loads the data from temp file"""
        self._data = cPickle.load(self._datafile)

    def _store_data(self):
        """Stores the data. Hasn't been accessed for a while"""
        self._access_counter = 0
        cPickle.dump(self._data, self._datafile, protocol=cPickle.HIGHEST_PROTOCOL)
        del self._data

    def _check(self):
        """checks to see if it's data needs to be stored"""
        now = time.time()
        sroot = int(math.sqrt(self._access_counter)) + 1
        self._access_counter = sroot
        if now - self._last_accessed < self.MIN_KEEP_TIME:
            return
        if sroot > 100:
            return
        self._store_data()