# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ukcensusapi/NRScotland.py
# Compiled at: 2018-11-02 08:14:28
# Size of source mod 2**32: 8844 bytes
"""
Data scraper for Scottish 2011 census Data
"""
import os.path
from pathlib import Path
import urllib.parse, zipfile, pandas as pd, requests, ukcensusapi.utils as utils

def _coverage_type(code):
    if isinstance(code, list):
        code = code[0]
    else:
        if code == 'S92000003':
            return 'ALL'
        else:
            if code[:3] == 'S12':
                return 'LAD'
            if code[:3] == 'S02':
                return 'MSOA11'
            if code[:3] == 'S01':
                return 'LSOA11'
        if code[:3] == 'S00':
            return 'OA11'
    raise ValueError('Invalid code: {}'.format(code))


class NRScotland:
    __doc__ = '\n  NRScotland web data scraper.\n  '
    URL = 'https://www.scotlandscensus.gov.uk/ods-web/download/getDownloadFile.html'
    data_sources = [
     'Council Area blk', 'SNS Data Zone 2011 blk', 'Output Area blk']
    GeoCodeLookup = {'LAD':0, 
     'LSOA11':1, 
     'OA11':2}

    def __init__(self, cache_dir):
        """Constructor.
    Args:
        cache_dir: cache directory
    Returns:
        an instance.
    """
        self.cache_dir = utils.init_cache_dir(cache_dir)
        lookup_file = self.cache_dir / 'sc_lookup.csv'
        if not os.path.isfile(str(lookup_file)):
            lookup_url = 'https://www2.gov.scot/Resource/0046/00462936.csv'
            response = requests.get(lookup_url)
            with open(str(lookup_file), 'wb') as (fd):
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

        self.area_lookup = pd.read_csv(str(self.cache_dir / 'sc_lookup.csv'))
        self.area_lookup.columns = [
         'OA11', 'LSOA11', 'MSOA11', 'LAD']

    def get_geog(self, coverage, resolution):
        """
    Returns all areas at resolution in coverage
    """
        coverage_type = _coverage_type(coverage)
        if coverage_type == 'ALL':
            return self.area_lookup[resolution].unique()
        else:
            if isinstance(coverage, str):
                coverage = [
                 coverage]
            return self.area_lookup[self.area_lookup[coverage_type].isin(coverage)][resolution].unique()

    def get_metadata(self, table, resolution):
        """
    Returns the table metadata
    """
        return self._NRScotland__get_rawdata(table, resolution)[0]

    def __get_rawdata(self, table, resolution):
        """
    Gets the raw csv data and metadata
    """
        z = zipfile.ZipFile(str(self._NRScotland__source_to_zip(NRScotland.data_sources[NRScotland.GeoCodeLookup[resolution]])))
        raw_data = pd.read_csv(z.open(table + '.csv'))
        if raw_data.shape == (2, 1):
            raise ValueError('Table {}: data not available at {} resolution.'.format(table, resolution))
        raw_cols = raw_data.columns.tolist()
        fields = {}
        col_index = 1
        while raw_cols[col_index][:8] == 'Unnamed:':
            fields[table + '_' + str(col_index) + '_CODE'] = raw_data[raw_cols[col_index]].unique().tolist()
            col_index = col_index + 1

        fields[table + '_0_CODE'] = raw_data.columns.tolist()[col_index:]
        meta = {'table':table, 
         'description':'', 
         'geography':resolution, 
         'fields':fields}
        return (
         meta, raw_data)

    def get_data(self, table, coverage, resolution, category_filters={}, r_compat=False):
        """
    Returns a table with categories in columns, filtered by geography and (optionally) category values
    If r_compat==True, instead of returning a pandas dataframe it returns a dict raw value data and column names
    that can be converted into an R data.frame 
    """
        msoa_workaround = False
        if resolution == 'MSOA11':
            msoa_workaround = True
            resolution = 'LSOA11'
        geography = self.get_geog(coverage, resolution)
        meta, raw_data = self._NRScotland__get_rawdata(table, resolution)
        raw_data.replace('-', 0, inplace=True)
        raw_data.replace(',', '', inplace=True, regex=True)
        lookup = raw_data.columns.tolist()[len(meta['fields']):]
        id_vars = [
         'GEOGRAPHY_CODE']
        for i in range(1, len(meta['fields'])):
            id_vars.append(table + '_' + str(i) + '_CODE')

        cols = id_vars.copy()
        cols.extend(list(range(0, len(lookup))))
        raw_data.columns = cols
        raw_data = raw_data.melt(id_vars=id_vars)
        id_vars.extend([table + '_0_CODE', 'OBS_VALUE'])
        raw_data.columns = id_vars
        raw_data['OBS_VALUE'] = pd.to_numeric(raw_data['OBS_VALUE'])
        for i in range(1, len(meta['fields'])):
            category_name = raw_data.columns[i]
            category_values = meta['fields'][category_name]
            assert len(category_values) == len(raw_data[category_name].unique())
            category_map = {k:v for v, k in enumerate(category_values)}
            raw_data[category_name] = raw_data[category_name].map(category_map)

        if isinstance(geography, str):
            geography = [
             geography]
        data = raw_data[raw_data.GEOGRAPHY_CODE.isin(geography)]
        if msoa_workaround:
            data = data.reset_index(drop=True)
            lookup = self.area_lookup[self.area_lookup.LSOA11.isin(data.GEOGRAPHY_CODE)]
            lookup = pd.Series((lookup.MSOA11.values), index=(lookup.LSOA11)).to_dict()
            data.GEOGRAPHY_CODE = data.GEOGRAPHY_CODE.map(lookup)
            cols = list(data.columns[:-1])
            data = data.groupby(cols).sum().reset_index()
        for category in category_filters:
            filter = category_filters[category]
            if isinstance(filter, int):
                filter = [
                 filter]
            data = data[data[category].isin(filter)]

        data = data.reset_index(drop=True)
        if r_compat:
            return {'columns':data.columns.values,  'values':data.values}
        else:
            return data

    def contextify(self, table, meta, colname):
        """
    Replaces the numeric category codes with the descriptive strings from the metadata
    """
        lookup = meta['fields'][colname]
        mapping = {k:v for k, v in enumerate(lookup)}
        category_name = colname.replace('_CODE', '_NAME')
        table[category_name] = table[colname].map(mapping)
        return table

    def __source_to_zip(self, source_name):
        """
    Downloads if necessary and returns the name of the locally cached zip file of the source data (replacing spaces with _)
    """
        zip = self.cache_dir / (source_name.replace(' ', '_') + '.zip')
        if not os.path.isfile(str(zip)):
            scotland_src = NRScotland.URL + '?downloadFileIds=' + urllib.parse.quote(source_name)
            print(scotland_src, ' -> ', (self.cache_dir / zip), '...', end='')
            response = requests.get(scotland_src, verify=False)
            with open(str(zip), 'wb') as (fd):
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

            print('OK')
        return zip