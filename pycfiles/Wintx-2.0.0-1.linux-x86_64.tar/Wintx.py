# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/Wintx.py
# Compiled at: 2016-03-31 11:14:28
import wintx
from errors import WintxFunctionNotImplemented
from interfaces import Query, Importer
from Fastener import Fastener

class Wintx(object):
    """Wintx Class
     Ensures compatibility with 1.x.x versions of Wintx
  """

    def __init__(self, config_file='/etc/wintx.conf'):
        self.query_instance = Query(config_file=config_file)
        self.importer_instance = Importer(config_file=config_file)
        self.fastener_instance = Fastener(config_file)

    def __getattr__(self, name):
        try:
            return getattr(self.fastener_instance, name)
        except WintxFunctionNotImplemented, err:
            if name == 'shard_groups':
                return []
            if name == '__setGlobalConnectionProperty__' or name == '__setLocalConnectionGroupProperty__':
                return lambda *args, **kwargs: None
            raise err

    def __getTime__(self, timestamp):
        return wintx.getTime(timestamp)

    def __getTimestamp__(self, time):
        return wintx.getTimestamp(time)

    def getWintxDict(self):
        wintx.getWintxDict()

    def getWintxIndexesDict(self):
        wintx.getWintxIndexesDict()

    def checkQueryDict(self, query, restricted_columns=None):
        self.query_instance.checkQueryDict(query, restricted_columns)

    def compareDictFromQuery(self, value, comparedict):
        self.import_instance.__compareDictFromQuery__(value, comparedict)

    def checkRecordDict(self, record):
        self.import_instance.checkRecordDict(record)

    def query(self, query_dict, sort_column=None):
        return self.query_instance.query(query_dict, sort_column)

    def queryWithin(self, polygon, query_dict, reverse_points=False, sort_column=None):
        return self.query_instance.queryWithin(polygon, query_dict, reverse_points, sort_column)

    def insertBulk(self, records, clear_cache=False):
        return self.fastener_instance.insertRecords(records)

    def importGrib(self, gribFile, datatype, parameters=None, ignore_unknowns=False, longitude_convert_east=False):
        pass

    def getTimes(self):
        return self.query_instance.getTimes()

    def getVariables(self):
        return self.query_instance.getVariables()

    def getLevels(self):
        return self.query_instance.getLevels()

    def getLocationCorners(self):
        return self.query_instance.getLocationCorners()

    def getDatabaseStats(self):
        return self.query_instance.getDatabaseStats()

    def getVarnamesAtTime(self, time, time_end=None):
        return self.query_instance.getVarnamesAtTime(time, time_end)