# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/web_module_to_load.py
# Compiled at: 2017-10-27 18:08:28
import os, json, base64
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import app_identity
import lib.cloudstorage as gcs

def basicAuth(func):

    def callf(webappRequest, *args, **kwargs):
        auth_header = webappRequest.request.headers.get('Authorization')
        if auth_header == None:
            webappRequest.response.set_status(401, message='Authorization Required')
            webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="Unsecure Area"'
        else:
            auth_parts = auth_header.split(' ')
            user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
            user_arg = user_pass_parts[0]
            pass_arg = user_pass_parts[1]
            if user_arg != 'guest' or pass_arg != 'barres':
                webappRequest.response.set_status(401, message='Authorization Required')
                webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
            else:
                return func(webappRequest, *args, **kwargs)
        return

    return callf


def _byteify(data, ignore_dicts=False):
    """
    DESCRIPTION:  
    - https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json

    """
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    if isinstance(data, dict) and not ignore_dicts:
        return {_byteify(key, ignore_dicts=True):_byteify(value, ignore_dicts=True) for key, value in data.iteritems()}
    return data


def json_load_byteified(file_handle):
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)


dataFile = open('web/web_data/dataset.data.json')
json_data = json_load_byteified(dataFile)
template_dir = 'web/templates'
gcs.set_default_retry_params(gcs.RetryParams(initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=20, max_retries=1000))

class SearchResult(ndb.Model):
    """
    DESCRIPTION: 
        - This is a class for the noSQL database use to store the locations of the images

    """
    keyName = ndb.StringProperty()
    locationTabbed = ndb.StringProperty()
    urlsTabbed = ndb.StringProperty()


def get_bucketName():
    appId = app_identity.get_application_id()
    bucketName = appId + '.appspot.com'
    return bucketName


def get_web_content(queryTerm, setkey, showImage='NA'):
    nameOfSite = json_data[0]['nameOfSite']
    labLink = json_data[0]['labLink']
    labName = json_data[0]['labName']
    template_values = {'nameOfSite': nameOfSite, 
       'labLink': labLink, 
       'labName': labName}
    if queryTerm == 'NA':
        queryTerm = json_data[0]['defaultTerm']
    if queryTerm != 'NA':
        searchQuery = SearchResult.query(SearchResult.keyName == queryTerm)
        match = searchQuery.fetch(1)
        if len(match) == 0:
            return {}
        match = searchQuery.fetch(1)[0]
        imageLocations = match.locationTabbed.rstrip().split('\t')
        if match.urlsTabbed == 'NA':
            urls = [ images.get_serving_url(None, filename='/gs/' + get_bucketName() + '/' + x) for x in imageLocations ]
            match.urlsTabbed = ('\t').join(urls)
            match.put()
        else:
            urls = match.urlsTabbed.rstrip().split('\t')
        datasetList = [ [json.dumps(json_data[(idx + 1)]), urls[idx] + '=s0', json_data[(idx + 1)]['setKey']] for idx, x in enumerate(imageLocations) ]
        if setkey == 'NA':
            firstPath = [ x[1] for x in datasetList if x[1] != 'NA' ][0]
        else:
            firstPath = [ x[1] for x in datasetList if x[2] == setkey ][0]
        template_values['searchTerm'] = queryTerm
        template_values['datasetList'] = datasetList
        template_values['firstPath'] = firstPath
        template_values['setkey'] = setkey
    print template_values
    print 'YOT'
    return template_values