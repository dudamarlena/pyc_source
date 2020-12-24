# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/query_data.py
# Compiled at: 2018-02-14 01:47:48
from google.appengine.ext import ndb
import os

def extract_data_for_term(searchTerm, datasetsDict, searchLookupDict):
    """

    Step 1: Gets the search term for each dataset. 
    Step 2: Matches the resulting search terms for each 
    
    OUTPUT:
        datasetkey: [     ]

    #DatasetsDict - stores the search term model for each dataset. 
    #

    NOTES:
        - To do: implement asynchronous calls

    The querying process is using the NDB client datastore. 
    -Description is found in Google App Engine Python Standard Environment Documentation. 
    -Note that this is different from the Datastore API - which does not automatically connect with app engine. 

    """
    slmodel = searchLookupDict['datastoremodel']
    query = slmodel.query(slmodel.searchTerm == unicode(searchTerm))
    result = query.fetch(1)
    columns = searchLookupDict['columns']
    if len(result) == 0:
        datasetkeyTermDict = {datasetkey:searchTerm for i, datasetkey in enumerate(columns)}
    else:
        result = result[0]
        datasetkeyTermDict = {datasetkey:result.data[(i + 2)] for i, datasetkey in enumerate(columns)}
    outDict = dict()
    for datasetKey in datasetsDict.keys():
        if datasetKey not in datasetkeyTermDict:
            continue
        datasetSearchTerm = unicode(datasetkeyTermDict[datasetKey])
        query = datasetsDict[datasetKey].query(datasetsDict[datasetKey].searchTerm == datasetSearchTerm)
        result = query.fetch(1)
        if len(result) == 0:
            outDict[datasetKey] = None
        else:
            outDict[datasetKey] = result[0].data

    return outDict


def extract_data_for_term_and_dataset(searchTerm, datasetsDict, datasetKey):
    query = datasetsDict[datasetKey].query(datasetsDict[datasetKey].searchTerm == searchTerm)
    result = query.fetch(1)
    if len(result) == 0:
        return
    else:
        return result[0].data
        return