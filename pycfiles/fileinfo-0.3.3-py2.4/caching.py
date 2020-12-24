# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/caching.py
# Compiled at: 2008-06-08 17:10:55
"""Fileinfo caching.

"""

def writeCache(all):
    """Write file attribute values into one cache file of the containing folder."""
    func = lambda rec: normpath(dirname(rec['path']))
    cacheDict = groupby([ a.__dict__ for a in all ], func)
    for (k, aList) in cacheDict:
        for (i, dic) in enumerate(aList):
            aList[i]['path'] = normpath(aList[i]['path'])

        cachePath = normpath(join(k, '_fileinfoCachePickle.txt'))
        pickle.dump(aList, open(cachePath, 'w'))
        print 'written cache at path:', cachePath
        pp(aList)


def readCaches(paths):
    """Read fileinfo caches for given paths."""
    res = {}
    cache = groupby(paths, lambda x: dirname(x))
    for k in cache.keys():
        cachePath = join(k, '_fileinfoCachePickle.txt')
        if not exists(cachePath):
            continue
        f = open(cachePath, 'r')
        cacheDict = pickle.load(f)
        cacheDict2 = groupby(cacheDict, lambda x: x['path'])
        pp(cacheDict2)
        res.update(cacheDict2)

    for k in res:
        res[k] = res[k][0]

    pp(res)
    return res