# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ukcensusapi/NISRA.py
# Compiled at: 2018-07-10 05:40:20
# Size of source mod 2**32: 9659 bytes
"""
Northern Ireland
"""
import os.path
from pathlib import Path
import urllib.parse, zipfile, pandas as pd, requests, ukcensusapi.utils as utils

def _coverage_type(code):
    if isinstance(code, list):
        code = code[0]
    else:
        if code == 'N92000002':
            return 'ALL'
        else:
            if len(code) == 4:
                return 'LGD'
            if len(code) == 6:
                return 'WARD'
            if len(code) == 8:
                return 'SOA'
        if code[:3] == 'N00':
            return 'OA'
    raise ValueError('Invalid code: {}'.format(code))


class NISRA:
    __doc__ = '\n  Scrapes and refomats NI 2011 census data from NISRA website\n  '
    URL = 'http://www.ninis2.nisra.gov.uk/Download/Census%202011/'
    Timeout = 15
    data_sources = [
     'Detailed Characteristics Tables (statistical geographies).zip',
     'Key Statistics Tables (statistical geographies).zip',
     'Local Characteristic Tables (statistical geographies).zip',
     'Quick Statistics Tables (statistical geographies).zip']
    GeoCodeLookup = {'LAD':0, 
     'MSOA11':1, 
     'LSOA11':2, 
     'OA11':3}
    NIGeoCodes = [
     'LGD', 'WARD', 'SOA', 'SA']
    source_map = {'LC':2, 
     'DC':0,  'KS':1,  'QS':3}
    res_map = {'SA':'SMALL AREAS', 
     'SOA':'SUPER OUTPUT AREAS'}
    LADs = {'95AA':'Antrim', 
     '95BB':'Ards', 
     '95CC':'Armagh', 
     '95DD':'Ballymena', 
     '95EE':'Ballymoney', 
     '95FF':'Banbridge', 
     '95GG':'Belfast', 
     '95HH':'Carrickfergus', 
     '95II':'Castlereagh', 
     '95JJ':'Coleraine', 
     '95KK':'Cookstown', 
     '95LL':'Craigavon', 
     '95MM':'Derry', 
     '95NN':'Down', 
     '95OO':'Dungannon', 
     '95PP':'Fermanagh', 
     '95QQ':'Larne', 
     '95RR':'Limavady', 
     '95SS':'Lisburn', 
     '95TT':'Magherafelt', 
     '95UU':'Moyle', 
     '95VV':'Newry and Mourne', 
     '95WW':'Newtownabbey', 
     '95XX':'North Down', 
     '95YY':'Omagh', 
     '95ZZ':'Strabane'}

    def __init__(self, cache_dir):
        """Constructor.
    Args:
        cache_dir: cache directory
    Returns:
        an instance.
    """
        self.cache_dir = utils.init_cache_dir(cache_dir)
        lookup_file = self.cache_dir / 'ni_lookup.csv'
        if not os.path.isfile(str(lookup_file)):
            z = zipfile.ZipFile(str(self._NISRA__source_to_zip(NISRA.data_sources[2])))
            pd.read_csv(z.open('All_Geographies_Code_Files/NI_HIERARCHY.csv')).drop([
             'NUTS3', 'HSCT', 'ELB', 'COUNTRY'],
              axis=1).to_csv((str(lookup_file)),
              index=False)
        self.area_lookup = pd.read_csv(str(lookup_file))

    def get_geog(self, coverage, resolution):
        """
    Returns all areas at resolution in coverage
    """
        resolution = _ni_resolution(resolution)
        coverage_type = _coverage_type(coverage)
        if coverage_type == 'ALL':
            return self.area_lookup[resolution].unique()
        else:
            if isinstance(coverage, str):
                coverage = [
                 coverage]
            return self.area_lookup[self.area_lookup[coverage_type].isin(coverage)][resolution].unique()

    def get_metadata(self, table, resolution):
        return self._NISRA__get_metadata_impl(table, resolution)[0]

    def __get_metadata_impl(self, table, resolution):
        resolution = _ni_resolution(resolution)
        if resolution == 'LGD' or resolution == 'WARD':
            resolution = 'SOA'
        else:
            z = zipfile.ZipFile(str(self._NISRA__source_to_zip(NISRA.data_sources[NISRA.source_map[table[:2]]])))
            raw_meta = pd.read_csv(z.open(NISRA.res_map[resolution] + '/' + table + 'DESC0.CSV')).drop([
             'ColumnVariableMeasurementUnit', 'ColumnVariableStatisticalUnit'],
              axis=1)
            commas = raw_meta['ColumnVariableDescription'].str.count(',').unique()
            min_categories = min(commas)
            if len(commas) > 1:
                if min_categories > 0:
                    print('WARNING: it apprears that {} is multivariate and some category descriptions appear to contain a comma. '.format(table) + 'This makes the individual category names ambiguous. Be aware that category names may have been be incorrectly interpreted.')
            if min_categories > 0:
                raw_meta = pd.concat([raw_meta['ColumnVariableCode'], raw_meta['ColumnVariableDescription'].str.split(', ', n=min_categories, expand=True)], axis=1)
            else:
                raw_meta.rename({'ColumnVariableDescription': 0}, axis=1, inplace=True)
        raw_meta = raw_meta.set_index('ColumnVariableCode', drop=True)
        meta = {'table':table, 
         'description':'', 
         'geography':resolution, 
         'fields':{}}
        text_columns = range(0, len(raw_meta.columns))
        for text_column in text_columns:
            raw_meta[text_column] = raw_meta[text_column].astype('category')
            code_column = table + '_' + str(text_column) + '_CODE'
            raw_meta[code_column] = raw_meta[text_column].cat.codes
            meta['fields'][code_column] = dict(enumerate(raw_meta[text_column].cat.categories))

        raw_meta.drop(text_columns, axis=1, inplace=True)
        return (
         meta, raw_meta)

    def get_data(self, table, region, resolution, category_filters={}, r_compat=False):
        resolution = _ni_resolution(resolution)
        agg_workaround = False
        if resolution == 'LGD' or resolution == 'WARD':
            agg_workaround = True
            actual_resolution = resolution
            resolution = 'SOA'
        meta, raw_meta = self._NISRA__get_metadata_impl(table, resolution)
        area_codes = self.get_geog(region, resolution)
        z = zipfile.ZipFile(str(self._NISRA__source_to_zip(NISRA.data_sources[NISRA.source_map[table[:2]]])))
        id_vars = ['GeographyCode']
        raw_data = pd.read_csv(z.open(NISRA.res_map[resolution] + '/' + table + 'DATA0.CSV')).melt(id_vars=id_vars)
        raw_data.columns = ['GEOGRAPHY_CODE', table, 'OBS_VALUE']
        raw_data = raw_data[raw_data['GEOGRAPHY_CODE'].isin(area_codes)]
        data = raw_data.join(raw_meta, on=table).drop([table], axis=1)
        if agg_workaround:
            data = data.reset_index(drop=True)
            lookup = self.area_lookup[self.area_lookup[resolution].isin(data.GEOGRAPHY_CODE)]
            lookup = pd.Series((lookup[actual_resolution].values), index=(lookup[resolution])).to_dict()
            data.GEOGRAPHY_CODE = data.GEOGRAPHY_CODE.map(lookup)
            cols = list(data.columns)
            cols.remove('OBS_VALUE')
            print(cols)
            data = data.groupby(cols).sum().reset_index()
        for category in category_filters:
            filter = category_filters[category]
            if isinstance(filter, int):
                filter = [
                 filter]
            data = data[data[category].isin(filter)]

        data.reset_index(drop=True, inplace=True)
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
        zipfile = self.cache_dir / source_name.replace(' ', '_')
        if not os.path.isfile(str(zipfile)):
            ni_src = NISRA.URL + source_name.replace(' ', '%20')
            print(ni_src, ' -> ', zipfile, '...', end='')
            response = requests.get(ni_src)
            with open(str(zipfile), 'wb') as (fd):
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

            print('OK')
        return zipfile


def _ni_resolution(resolution):
    """
  Maps E&W statistical geography codes to their closest NI equvalents
  """
    if resolution in NISRA.NIGeoCodes:
        return resolution
    else:
        if resolution not in NISRA.GeoCodeLookup:
            raise ValueError("resolution '{}' is not available".format(resolution))
        return NISRA.NIGeoCodes[NISRA.GeoCodeLookup[resolution]]