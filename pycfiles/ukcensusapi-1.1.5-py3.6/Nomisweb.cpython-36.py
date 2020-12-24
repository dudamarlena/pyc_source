# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ukcensusapi/Nomisweb.py
# Compiled at: 2018-07-10 05:40:20
# Size of source mod 2**32: 15215 bytes
"""
Nomisweb API.
"""
import os, json, hashlib, warnings
from pathlib import Path
from collections import OrderedDict
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode
from socket import timeout
import pandas as pd, ukcensusapi.utils as utils

def _get_api_key(cache_dir):
    """
  Look for key in file NOMIS_API_KEY in cache dir, falling back to env var
  """
    filename = cache_dir / 'NOMIS_API_KEY'
    if os.path.isfile(str(filename)):
        with open(str(filename), 'r') as (file):
            content = file.readlines()
            if len(content) == 0:
                return
            else:
                return content[0].replace('\n', '')
    return os.environ.get('NOMIS_API_KEY')


def _shorten(code_list):
    """
  Shortens a list of numeric nomis geo codes into a string format where contiguous values are represented as ranges, e.g.
  1,2,3,6,7,8,9,10 -> "1...3,6,7...10"
  which can drastically reduce the length of the query url
  """
    if not code_list:
        return ''
    else:
        if len(code_list) == 1:
            return str(code_list[0])
        else:
            code_list.sort()
            short_string = ''
            index0 = 0
            index1 = 0
            for index1 in range(1, len(code_list)):
                if code_list[index1] != code_list[(index1 - 1)] + 1:
                    if index0 == index1:
                        short_string += str(code_list[index0]) + ','
                    else:
                        short_string += str(code_list[index0]) + '...' + str(code_list[(index1 - 1)]) + ','
                    index0 = index1

            if index0 == index1:
                short_string += str(code_list[index0])
            else:
                short_string += str(code_list[index0]) + '...' + str(code_list[index1])
        return short_string


class Nomisweb:
    __doc__ = '\n  Nomisweb API methods and data.\n  '
    URL = 'https://www.nomisweb.co.uk/'
    Timeout = 15
    GeoCodeLookup = {'LAD':'TYPE464', 
     'MSOA11':'TYPE297', 
     'LSOA11':'TYPE298', 
     'OA11':'TYPE299', 
     'MSOA01':'TYPE305', 
     'LSOA01':'TYPE304', 
     'OA01':'TYPE310', 
     'England':'2092957699', 
     'EnglandWales':'2092957703', 
     'GB':'2092957698', 
     'UK':'2092957697'}

    def __init__(self, cache_dir, verbose=False):
        """Constructor.
    Args:
        cache_dir: cache directory
    Returns:
        an instance.
    """
        self.cache_dir = utils.init_cache_dir(cache_dir)
        self.verbose = verbose
        self.key = _get_api_key(self.cache_dir)
        if self.key is None:
            raise RuntimeError('No API key found. Whilst downloads still work, they may be truncated,\ncausing potentially unforseen problems in any modelling/analysis.\nSet the key value in the environment variable NOMIS_API_KEY.\nRegister at www.nomisweb.co.uk to obtain a key')
        if self.verbose:
            print('Cache directory: ', self.cache_dir)
        try:
            request.urlopen((self.URL), timeout=(Nomisweb.Timeout))
        except (HTTPError, URLError, timeout) as error:
            print('ERROR: ', error, ' accessing', self.URL)

        Nomisweb.cached_lad_codes = self._Nomisweb__cache_lad_codes()

    def get_geo_codes(self, la_codes, code_type):
        """Get nomis geographical codes.

    Args:
        la_codes: local authority codes for the region
        code_type: enumeration specifying the geographical resolution
    Returns:
        a string representation of the codes.
    """
        if not isinstance(la_codes, list):
            la_codes = [
             la_codes]
        geo_codes = []
        for i in range(0, len(la_codes)):
            path = 'api/v01/dataset/NM_144_1/geography/' + str(la_codes[i]) + code_type + '.def.sdmx.json?'
            rawdata = self._Nomisweb__fetch_json(path, {})
            try:
                n_results = len(rawdata['structure']['codelists']['codelist'][0]['code'])
                for j in range(0, n_results):
                    geo_codes.append(rawdata['structure']['codelists']['codelist'][0]['code'][j]['value'])

            except (KeyError, ValueError):
                print(la_codes[i], ' does not appear to be a valid LA code')

        return _shorten(geo_codes)

    def get_lad_codes(self, la_names):
        """Convert local autority name(s) to nomisweb codes.
    Args:
        la_names: one or more local authorities (specify either the name or the ONS code)
    Returns:
        codes.
    """
        if not isinstance(la_names, list):
            la_names = [
             la_names]
        codes = []
        for la_name in la_names:
            if la_name in Nomisweb.cached_lad_codes:
                codes.append(Nomisweb.cached_lad_codes[la_name])

        return codes

    def get_url(self, table_internal, query_params):
        """Constructs a query url given a nomisweb table code and a query.
    Args:
        table_internal: nomis table code. This can be found in the table metadata
        query_params: a dictionary of parameters and values
    Returns:
        the url that can be used to download the data
    """
        ordered = OrderedDict()
        for key in sorted(query_params):
            ordered[key] = query_params[key]

        return Nomisweb.URL + 'api/v01/dataset/' + table_internal + '.data.tsv?' + str(urlencode(ordered))

    def get_data(self, table, query_params, r_compat=False):
        """Downloads or retrieves data given a table and query parameters.
    Args:
       table: ONS table name, or nomisweb table code if no explicit ONS name 
       query_params: table query parameters
    Returns:
        a dataframe containing the data. If downloaded, the data is also cached to a file
    """
        metadata = self.load_metadata(table)
        query_params['uid'] = self.key
        query_string = self.get_url(metadata['nomis_table'], query_params)
        filename = self.cache_dir / (table + '_' + hashlib.md5(query_string.encode()).hexdigest() + '.tsv')
        if not os.path.isfile(str(filename)):
            if self.verbose:
                print('Downloading and cacheing data: ' + str(filename))
            request.urlretrieve(query_string, str(filename))
            if os.stat(str(filename)).st_size == 0:
                os.remove(str(filename))
                errormsg = 'ERROR: Query returned no data. Check table and query parameters'
                if r_compat:
                    return errormsg
                else:
                    print(errormsg)
                    return
        else:
            if self.verbose:
                print('Using cached data: ' + str(filename))
        if r_compat:
            return str(filename)
        else:
            data = pd.read_csv((str(filename)), delimiter='\t')
            if len(data) == 1000000:
                warnings.warn("Data download has reached nomisweb's single-query row limit. Truncation is extremely likely")
            return data

    def get_metadata(self, table_name):
        """Downloads census table metadata.
    Args:
      table_name: the (ONS) table name, e.g. KS4402EW
    Returns:
      a dictionary containing information about the table contents including categories and category values.
    """
        if not table_name.startswith('NM_'):
            path = 'api/v01/dataset/def.sdmx.json?'
            query_params = {'search': '*' + table_name + '*'}
        else:
            path = 'api/v01/' + table_name + '.def.sdmx.json?'
            query_params = {}
        data = self._Nomisweb__fetch_json(path, query_params)
        if not data['structure']['keyfamilies']:
            return
        table = data['structure']['keyfamilies']['keyfamily'][0]['id']
        rawfields = data['structure']['keyfamilies']['keyfamily'][0]['components']['dimension']
        fields = {}
        for rawfield in rawfields:
            field = rawfield['conceptref']
            fields[field] = {}
            if not field.upper() == 'CURRENTLY_RESIDING_IN':
                if field.upper() == 'PLACE_OF_WORK':
                    pass
                else:
                    path = 'api/v01/dataset/' + table + '/' + field + '.def.sdmx.json?'
                    try:
                        fdata = self._Nomisweb__fetch_json(path, {})
                    except timeout:
                        print('HTTP timeout requesting metadata for ' + table_name)
                        return {}
                    except (HTTPError, URLError):
                        print('HTTP error requesting metadata for ' + table_name)
                        return {}
                    else:
                        values = fdata['structure']['codelists']['codelist'][0]['code']
                        for value in values:
                            fields[field][value['value']] = value['description']['value']

        geogs = {}
        path = 'api/v01/dataset/' + table + '/geography/TYPE.def.sdmx.json?'
        try:
            fdata = self._Nomisweb__fetch_json(path, {})
        except timeout:
            print('HTTP timeout requesting geography metadata for ' + table_name)
        except (HTTPError, URLError):
            print('HTTP error requesting geography metadata for ' + table_name)
        else:
            if fdata['structure']['codelists']:
                values = fdata['structure']['codelists']['codelist'][0]['code']
                for value in values:
                    geogs[str(value['value'])] = value['description']['value']

            result = {'nomis_table':table, 
             'description':data['structure']['keyfamilies']['keyfamily'][0]['name']['value'], 
             'fields':fields, 
             'geographies':geogs}
            self.write_metadata(table_name, result)
            return result

    def load_metadata(self, table_name):
        """Retrieves cached, or downloads census table metadata. Use this in preference to get_metadata.
    Args:
      table_name: the (ONS) table name, e.g. KS4402EW
    Returns:
      a dictionary containing information about the table contents including categories and category values.
    """
        filename = self.cache_dir / (table_name + '_metadata.json')
        if not os.path.isfile(str(filename)):
            if self.verbose:
                print(filename, 'not found, downloading...')
            return self.get_metadata(table_name)
        else:
            if self.verbose:
                print(filename, 'found, using cached metadata...')
            with open(str(filename)) as (metafile):
                meta = json.load(metafile)
            return meta

    def __cache_lad_codes(self):
        filename = self.cache_dir / 'lad_codes.json'
        if not os.path.isfile(str(filename)):
            if self.verbose:
                print(filename, 'not found, downloading LAD codes...')
            else:
                data = self._Nomisweb__fetch_json('api/v01/dataset/NM_144_1/geography/' + str(Nomisweb.GeoCodeLookup['EnglandWales']) + Nomisweb.GeoCodeLookup['LAD'] + '.def.sdmx.json?', {})
                if data == {}:
                    return []
                rawfields = data['structure']['codelists']['codelist'][0]['code']
                codes = {}
                for rawfield in rawfields:
                    codes[rawfield['description']['value']] = rawfield['value']
                    codes[rawfield['annotations']['annotation'][2]['annotationtext']] = rawfield['value']

                if self.verbose:
                    print('Writing LAD codes to ', filename)
            with open(str(filename), 'w') as (metafile):
                json.dump(codes, metafile, indent=2)
        else:
            if self.verbose:
                print('using cached LAD codes:', filename)
            with open(str(filename)) as (cached_ladcodes):
                codes = json.load(cached_ladcodes)
        return codes

    def __fetch_json(self, path, query_params):
        query_params['uid'] = self.key
        query_string = Nomisweb.URL + path + str(urlencode(query_params))
        reply = {}
        try:
            response = request.urlopen(query_string, timeout=(Nomisweb.Timeout))
        except (HTTPError, URLError) as error:
            print('ERROR: ', error, '\n', query_string)
        except timeout:
            print('ERROR: request timed out\n', query_string)
        else:
            reply = json.loads(response.read().decode('utf-8'))
        return reply

    def write_metadata(self, table, meta):
        """method.
    Args:
        arg: argument
        ...
    Returns:
        a return value.
    """
        filename = self.cache_dir / (table + '_metadata.json')
        if self.verbose:
            print('Writing metadata to ', str(filename))
        with open(str(filename), 'w') as (metafile):
            json.dump(meta, metafile, indent=2)

    def contextify(self, table_name, column, table):
        """Adds context to a column in a table, as a separate column containing the meanings of each numerical value
    Args:
        table_name: name of census table
        column: name of column within the table (containing numeric values)
        table:
    Returns:
        a new table containing an extra column with descriptions of the numeric values.
    """
        metadata = self.load_metadata(table_name)
        if column not in metadata['fields']:
            print(column, ' is not in metadata')
            return
        if column not in table.columns:
            print(column, ' is not in table')
            return
        lookup = {int(k):v for k, v in metadata['fields'][column].items()}
        table[column + '_NAME'] = table[column].map(lookup)