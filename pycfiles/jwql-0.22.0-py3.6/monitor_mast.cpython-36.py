# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/jwql_monitors/monitor_mast.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 8085 bytes
"""This module is home to a suite of MAST queries that gather bulk
properties of available JWST data for JWQL.

Authors
-------

    Joe Filippazzo

Use
---

    To get an inventory of all JWST files do:
    ::

        from jwql.jwql_monitors import monitor_mast
        inventory, keywords = monitor_mast.jwst_inventory()
"""
import logging, os
from astroquery.mast import Mast
from bokeh.embed import components
from bokeh.io import save, output_file
import pandas as pd
from jwql.utils.constants import JWST_INSTRUMENT_NAMES, JWST_DATAPRODUCTS
from jwql.utils.logging_functions import configure_logging, log_info, log_fail
from jwql.utils.permissions import set_permissions
from jwql.utils.utils import get_config
from jwql.utils.plotting import bar_chart

def instrument_inventory(instrument, dataproduct=JWST_DATAPRODUCTS, add_filters=None, add_requests=None, caom=False, return_data=False):
    """Get the counts for a given instrument and data product

    Parameters
    ----------
    instrument: str
        The instrument name, i.e. one of ['niriss','nircam','nirspec',
        'miri','fgs']
    dataproduct: sequence, str
        The type of data product to search
    add_filters: dict
        The ('paramName':'values') pairs to include in the 'filters'
        argument of the request e.g. add_filters = {'filter':'GR150R'}
    add_requests: dict
        The ('request':'value') pairs to include in the request
        e.g. add_requests = {'pagesize':1, 'page':1}
    caom: bool
        Query CAOM service
    return_data: bool
        Return the actual data instead of counts only

    Returns
    -------
    int, dict
        The number of database records that satisfy the search criteria
        or a dictionary of the data if `return_data=True`
    """
    filters = []
    if isinstance(dataproduct, str):
        dataproduct = [
         dataproduct]
    else:
        if instrument.lower() not in [ins.lower() for ins in JWST_INSTRUMENT_NAMES]:
            raise TypeError('Supported instruments include:', JWST_INSTRUMENT_NAMES)
        if caom:
            service = 'Mast.Caom.Filtered'
            filters += [{'paramName':'obs_collection',  'values':['JWST']},
             {'paramName':'instrument_name', 
              'values':[instrument]},
             {'paramName':'dataproduct_type', 
              'values':dataproduct}]
        else:
            service = 'Mast.Jwst.Filtered.{}'.format(instrument.title())
    if isinstance(add_filters, dict):
        filters += [{'paramName':name,  'values':[val]} for name, val in add_filters.items()]
    params = {'columns':'COUNT_BIG(*)', 
     'filters':filters, 
     'removenullcolumns':True}
    if return_data:
        params['columns'] = '*'
    if isinstance(add_requests, dict):
        params.update(add_requests)
    response = Mast.service_request_async(service, params)
    result = response[0].json()
    if return_data:
        return result
    else:
        return result['data'][0]['Column1']


def instrument_keywords(instrument, caom=False):
    """Get the keywords for a given instrument service

    Parameters
    ----------
    instrument: str
        The instrument name, i.e. one of ['niriss','nircam','nirspec',
        'miri','fgs']
    caom: bool
        Query CAOM service

    Returns
    -------
    pd.DataFrame
        A DataFrame of the keywords
    """
    sample = instrument_inventory(instrument, return_data=True, caom=caom, add_requests={'pagesize':1, 
     'page':1})
    data = [[i['name'], i['type']] for i in sample['fields']]
    keywords = pd.DataFrame(data, columns=('keyword', 'dtype'))
    return keywords


def jwst_inventory(instruments=JWST_INSTRUMENT_NAMES, dataproducts=[
 'image', 'spectrum', 'cube'], caom=False, plot=False):
    """Gather a full inventory of all JWST data in each instrument
    service by instrument/dtype

    Parameters
    ----------
    instruments: sequence
        The list of instruments to count
    dataproducts: sequence
        The types of dataproducts to count
    caom: bool
        Query CAOM service
    plot: bool
        Return a pie chart of the data

    Returns
    -------
    astropy.table.table.Table
        The table of record counts for each instrument and mode
    """
    logging.info('Searching database...')
    inventory, keywords = [], {}
    for instrument in instruments:
        ins = [instrument]
        for dp in dataproducts:
            count = instrument_inventory(instrument, dataproduct=dp, caom=caom)
            ins.append(count)

        ins.append(sum(ins[-3:]))
        inventory.append(ins)
        keywords[instrument] = instrument_keywords(instrument, caom=caom)

    logging.info('Completed database search for {} instruments and {} data products.'.format(instruments, dataproducts))
    all_cols = [
     'instrument'] + dataproducts + ['total']
    table = pd.DataFrame(inventory, columns=all_cols)
    if plot:
        output_dir = get_config()['outputs']
        if caom:
            output_filename = 'database_monitor_caom'
        else:
            output_filename = 'database_monitor_jwst'
        plt = bar_chart(table, 'instrument', dataproducts, title='JWST Inventory')
        html_filename = output_filename + '.html'
        outfile = os.path.join(output_dir, 'monitor_mast', html_filename)
        output_file(outfile)
        save(plt)
        set_permissions(outfile)
        logging.info('Saved Bokeh plots as HTML file: {}'.format(html_filename))
        plt.sizing_mode = 'stretch_both'
        script, div = components(plt)
        div_outfile = os.path.join(output_dir, 'monitor_mast', output_filename + '_component.html')
        with open(div_outfile, 'w') as (f):
            f.write(div)
            f.close()
        set_permissions(div_outfile)
        script_outfile = os.path.join(output_dir, 'monitor_mast', output_filename + '_component.js')
        with open(script_outfile, 'w') as (f):
            f.write(script)
            f.close()
        set_permissions(script_outfile)
        logging.info('Saved Bokeh components files: {}_component.html and {}_component.js'.format(output_filename, output_filename))
    table = pd.melt(table, id_vars=['instrument'], value_vars=dataproducts,
      value_name='files',
      var_name='dataproduct')
    return (
     table, keywords)


@log_fail
@log_info
def monitor_mast():
    """Tabulates the inventory of all JWST data products in the MAST
    archive and generates plots.
    """
    logging.info('Beginning database monitoring.')
    jwst_inventory(instruments=JWST_INSTRUMENT_NAMES, dataproducts=[
     'image', 'spectrum', 'cube'],
      caom=False,
      plot=True)
    jwst_inventory(instruments=JWST_INSTRUMENT_NAMES, dataproducts=[
     'image', 'spectrum', 'cube'],
      caom=True,
      plot=True)


if __name__ == '__main__':
    module = os.path.basename(__file__).strip('.py')
    configure_logging(module)
    monitor_mast()