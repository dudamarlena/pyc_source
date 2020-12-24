# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/KyunghoonKim/anaconda/lib/python2.7/site-packages/umap/search.py
# Compiled at: 2016-01-20 09:23:30
from vincenty import vincenty
from bson.son import SON

def nearest(database, name, location, maxkm):
    """
    MongoDB GeoSpatial Search
    :param database: db.test
    :param name: field name 'gps'
    :param location: [lat, lon]
    :param maxkm: limit of distance
    :return: count, database
    """
    query = {name: SON([('$near', location),
            (
             '$maxDistance', maxkm / 111.12)])}
    data = database.find(query)
    return (data.count(), data)


def nearest(data, location, dist=10):
    for d in data:
        cand = vincenty(location, d['loc'])
        if dist > cand:
            dist = cand

    return dist


for m in MB:
    maps = db.maps.find({'cat': m})
    for mm in maps:
        location = mm['loc']
        query = {'loc': SON([('$near', location), ('$maxDistance', 0.001 / 111.12)]), 'cat': '시장_쇼핑센터'}
        data = db.maps.find(query)
        count = data.count()
        ite = 1
        while count < 1:
            query = {'loc': SON([('$near', location), ('$maxDistance', (0.001 + 0.1 * ite) / 111.12)]), 'cat': '시장_쇼핑센터'}
            data = db.maps.find(query)
            count = data.count()
            ite += 1

        dist = nearest(data, location)
        db.maps.update({'_id': mm['_id']}, {'$set': {'market': dist}})

    print m