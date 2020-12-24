# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/DesktopFiles/PROJECTS/DSVISUALIZER/dataspectra/aefiles/scripts/upload_datasets.py
# Compiled at: 2018-02-15 14:09:14
import webapp2
from google.appengine.ext import ndb
import load_funcs as LF, os

class LocalUploadDatastore(webapp2.RequestHandler):
    """
    Dynamically creates each model separately
    """

    def get(self):
        datasets = LF.json_load_byteified(open('static/datasets.json'))
        numberOfDatasets = len(datasets)
        datasetModelDict = dict()
        for datasetParam in datasets.values():
            datasetModel = type(datasetParam['datasetkey'], (
             ndb.Model,), dict(searchTerm=ndb.StringProperty(), data=ndb.StringProperty(repeated=True, indexed=False)))
            datasetModelDict[datasetParam['datasetkey']] = datasetModel

        for datasetParam in datasets.values():
            datasetModel = datasetModelDict[datasetParam['datasetkey']]
            datasetfile = os.path.join('static', datasetParam['samplefile'])
            searchcol = int(datasetParam['searchcol'])
            with open(datasetfile) as (F):
                for i in range(int(datasetParam['searchrowstart'])):
                    F.readline()

                for i in F:
                    i = i.rstrip().split(',')
                    newEntity = datasetModel(searchTerm=i[(searchcol - 1)], data=i)
                    k = newEntity.put()

        searchLookupDict = LF.json_load_byteified(open('static/search_lookup.json'))
        searchTermModel = type('searchterm', (
         ndb.Model,), dict(searchTerm=ndb.StringProperty(), data=ndb.StringProperty(repeated=True, indexed=False)))
        searchlookupfile = os.path.join('static', searchLookupDict['samplefile'])
        with open(searchlookupfile) as (F):
            for i in F:
                i = i.rstrip().split(',')
                newEntity = searchTermModel(searchTerm=i[0], data=i)
                k = newEntity.put()