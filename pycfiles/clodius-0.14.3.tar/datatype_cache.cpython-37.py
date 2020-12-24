# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/datatype_cache.py
# Compiled at: 2019-12-24 22:02:38
# Size of source mod 2**32: 4900 bytes
import os, hashlib
try:
    import cPickle as pickle
except:
    import pickle

from clocwalk.libs.core.exception import DataException
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import paths
from clocwalk.libs.core.http import RequestConnect
from clocwalk.libs.detector.cvecpe import Cpe23Info

class AttribDictCache(dict):
    """AttribDictCache"""

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        self.attribute = attribute
        dict.__init__(self, indict)
        self._AttribDictCache__initialised = True

    def get(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            try:
                md5 = hashlib.md5()
                md5.update(item.encode('utf-8'))
                if not os.path.isdir(paths.CVE_CACHE_PATH):
                    os.makedirs(paths.CVE_CACHE_PATH)
                cache_file = os.path.join(paths.CVE_CACHE_PATH, '{0}.p'.format(md5.hexdigest()))
                if os.path.isfile(cache_file):
                    c = pickle.load(open(cache_file, 'rb'))
                    dict.__setattr__(self, item, c)
                    return c
                cpe_query_set = kb.db.query_cpe_set_by_product(product=item)
                cpe_info_list = []
                for cpe in cpe_query_set:
                    cve_query = kb.db.query_cve_by_cpe23uri(cpe23uri=(cpe.cpe23uri))
                    cpe_info_list.append(Cpe23Info(uri=(cpe.cpe23uri),
                      cve=cve_query,
                      vendor=(cpe.vendor),
                      product=(cpe.product),
                      version=(cpe.version),
                      update=(cpe.update_v)))

                if cpe_info_list:
                    pickle.dump(cpe_info_list, open(cache_file, 'wb'))
                dict.__setattr__(self, item, cpe_info_list)
                return cpe_info_list
            except KeyError as ex:
                try:
                    raise DataException("unable to access item '%s'" % item)
                finally:
                    ex = None
                    del ex

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict


class AttribDictHttpCache(dict):
    """AttribDictHttpCache"""

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        self.attribute = attribute
        dict.__init__(self, indict)
        self._AttribDictHttpCache__initialised = True

    def get(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            try:
                md5 = hashlib.md5()
                md5.update(item.encode('utf-8'))
                if not os.path.isdir(paths.HTTP_CACHE_PATH):
                    os.makedirs(paths.HTTP_CACHE_PATH)
                cache_file = os.path.join(paths.HTTP_CACHE_PATH, '{0}.p'.format(md5.hexdigest()))
                if os.path.isfile(cache_file):
                    c = pickle.load(open(cache_file, 'rb'))
                    dict.__setattr__(self, item, c)
                    return c
                http = RequestConnect()
                html = http.get_data(item)
                if html:
                    pickle.dump(html, open(cache_file, 'wb'))
                dict.__setattr__(self, item, html)
                return html
            except KeyError as ex:
                try:
                    raise DataException("unable to access item '%s'" % item)
                finally:
                    ex = None
                    del ex

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict