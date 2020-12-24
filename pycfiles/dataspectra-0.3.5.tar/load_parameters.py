# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/load_parameters.py
# Compiled at: 2018-02-13 11:42:32
"""
 This is where to keep all the commands and variables to be set on instance start. 
"""
import lib.cloudstorage as gcs, load_funcs as LF, jinja2
from google.appengine.ext import ndb
import os
siteJsonData = LF.json_load_byteified(open('static/site.json'))
os.environ['SERVER_SOFTWARE'] = 'Development (remote_api)/1.0'
gcs.set_default_retry_params(gcs.RetryParams(initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=20, max_retries=1000))
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader('web/templates'), extensions=[
 'jinja2.ext.autoescape'], autoescape=True)
datasets = LF.json_load_byteified(open('static/datasets.json'))
datasetModelDict = dict()
for datasetParam in datasets.values():
    datasetModel = type(datasetParam['datasetkey'], (
     ndb.Model,), dict(searchTerm=ndb.StringProperty(), data=ndb.StringProperty(repeated=True, indexed=False)))
    datasetModelDict[datasetParam['datasetkey']] = datasetModel

searchlookupDict = LF.json_load_byteified(open('static/search_lookup.json'))
searchlookupDict['datastoremodel'] = type('searchterm', (
 ndb.Model,), dict(searchTerm=ndb.StringProperty(), data=ndb.StringProperty(repeated=True, indexed=False)))