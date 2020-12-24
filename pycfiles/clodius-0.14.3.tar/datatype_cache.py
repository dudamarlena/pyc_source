# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/datatype_cache.py
# Compiled at: 2019-12-10 07:07:29
import copy, types, os, hashlib
try:
    import cPickle as pickle
except:
    import pickle

from clocwalk.libs.core.exception import DataException
from clocwalk.libs.core.settings import CACHE_PATH
from clocwalk.libs.core.data import db

class AttribDictCache(dict):
    """
    This class defines the object, inheriting from Python data
    type dictionary.

    >>> foo = AttribDictCache()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True
        return

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
                if not os.path.isdir(CACHE_PATH):
                    os.makedirs(CACHE_PATH)
                cache_file = os.path.join(CACHE_PATH, ('{0}.p').format(md5.hexdigest()))
                if os.path.isfile(cache_file):
                    c = pickle.load(open(cache_file, 'rb'))
                    dict.__setattr__(self, item, c)
                    return c
                cpe_query_set = db.query_cpe_set_by_product(product=item)
                cve_cpe23uri_list = []
                cve_list = {}
                for item in cpe_query_set:
                    if item.cpe23uri not in cve_cpe23uri_list:
                        cve_cpe23uri_list.append(item.cpe23uri)
                        cve_query_set = db.query_cve_set_by_cpe23uri(cpe23uri=item.cpe23uri)
                        for c in cve_query_set:
                            if c.cve not in cve_list:
                                cve_list[c.cve] = c

                info = {'cve': cve_list, 
                   'cpe': cpe_query_set}
                pickle.dump(info, open(cache_file, 'wb'))
                dict.__setattr__(self, item, info)
                return info
            except Exception as ex:
                raise DataException("unable to access item '%s'" % item)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal