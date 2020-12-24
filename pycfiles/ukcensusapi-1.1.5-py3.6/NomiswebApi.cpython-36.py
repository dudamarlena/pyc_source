# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ukcensusapi/NomiswebApi.py
# Compiled at: 2018-07-05 11:46:47
# Size of source mod 2**32: 5798 bytes
import json, hashlib, pandas as pd, numpy as np
from collections import OrderedDict
from urllib import request
import urllib.parse as urlparse
from urllib.parse import urlencode
from socket import timeout
import os

class NomiswebApi:
    url = 'https://www.nomisweb.co.uk/'
    key = os.environ.get('NOMIS_API_KEY')
    Timeout = 30
    LAD = 293
    MSOA = 297
    LSOA = 298
    OA = 299
    England = 2092957699
    EnglandWales = 2092957703
    GB = 2092957698
    UK = 2092957697

    def __init__(self, cacheDir, mappingFile):
        self.cacheDir = cacheDir
        self.mappingFile = mappingFile
        if NomiswebApi.key is None:
            print('Warning - no API key found, downloads may be truncated.\nSet the key value in the environment variable NOMIS_API_KEY.\nRegister at www.nomisweb.co.uk to obtain a key')

    def geoCodes(self, laCodes, type):
        geoCodes = []
        for i in range(0, len(laCodes)):
            path = 'api/v01/dataset/NM_144_1/geography/' + str(laCodes[i]) + 'TYPE' + str(type) + '.def.sdmx.json?'
            rawdata = self._NomiswebApi__fetchJSON(path, {})
            nResults = len(rawdata['structure']['codelists']['codelist'][0]['code'])
            for j in range(0, nResults):
                geoCodes.append(rawdata['structure']['codelists']['codelist'][0]['code'][j]['value'])

        return self._NomiswebApi__shorten(geoCodes)

    def readLADCodes(self, laNames):
        if type(laNames) is not list:
            laNames = [
             laNames]
        geoCodes = pd.read_csv((self.mappingFile), delimiter=',')
        codes = []
        for i in range(0, len(laNames)):
            codes.append(geoCodes[(geoCodes['name'] == laNames[i])]['nomiscode'].tolist()[0])

        return codes

    def getUrl(self, table, queryParams):
        ordered = OrderedDict()
        for key in sorted(queryParams):
            ordered[key] = queryParams[key]

        return NomiswebApi.url + 'api/v01/dataset/' + table + '.data.tsv?' + str(urlencode(ordered))

    def getData(self, table, queryParams):
        queryParams['uid'] = NomiswebApi.key
        queryString = self.getUrl(table, queryParams)
        filename = self.cacheDir + hashlib.md5(queryString.encode()).hexdigest() + '.tsv'
        if not os.path.isfile(self.cacheDir + filename):
            print('Downloading and cacheing data: ' + filename)
            request.urlretrieve(queryString, filename)
            if os.stat(filename).st_size == 0:
                os.remove(filename)
                print('ERROR: Query returned no data. Check table and query parameters')
                return
        else:
            print('Using cached data: ' + filename)
        return pd.read_csv(filename, delimiter='\t')

    def getMetadata(self, tableName):
        path = 'api/v01/dataset/def.sdmx.json?'
        queryParams = {'search': '*' + tableName + '*'}
        data = self._NomiswebApi__fetchJSON(path, queryParams)
        table = data['structure']['keyfamilies']['keyfamily'][0]['id']
        rawfields = data['structure']['keyfamilies']['keyfamily'][0]['components']['dimension']
        fields = {}
        for rawfield in rawfields:
            field = rawfield['conceptref']
            fields[field] = {}
            path = 'api/v01/dataset/' + table + '/' + field + '.def.sdmx.json?'
            try:
                fdata = self._NomiswebApi__fetchJSON(path, {})
            except timeout:
                print('HTTP timeout requesting metadata for ' + tableName)
                return {}
            except:
                print('HTTP error requesting metadata for ' + tableName)
                return {}

            values = fdata['structure']['codelists']['codelist'][0]['code']
            for value in values:
                fields[field][value['value']] = value['description']['value']

        result = {'nomis_table':table, 
         'description':data['structure']['keyfamilies']['keyfamily'][0]['name']['value'], 
         'fields':fields}
        return result

    def __shorten(self, codeList):
        codeList.sort()
        shortString = ''
        i0 = 0
        for i1 in range(1, len(codeList)):
            if codeList[i1] != codeList[(i1 - 1)] + 1:
                if i0 == i1:
                    shortString += str(codeList[i0]) + ','
                else:
                    shortString += str(codeList[i0]) + '...' + str(codeList[(i1 - 1)]) + ','
                i0 = i1

        if i0 == i1:
            shortString += str(codeList[i0])
        else:
            shortString += str(codeList[i0]) + '...' + str(codeList[i1])
        return shortString

    def __fetchJSON(self, path, queryParams):
        queryParams['uid'] = NomiswebApi.key
        queryString = NomiswebApi.url + path + str(urlencode(queryParams))
        response = request.urlopen(queryString, timeout=(NomiswebApi.Timeout))
        return json.loads(response.read().decode('utf-8'))