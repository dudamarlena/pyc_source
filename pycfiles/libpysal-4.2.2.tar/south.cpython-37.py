# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/south.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 3350 bytes
"""Southern NCOVR dataset.

The version retrieved here comes from:
     https://s3.amazonaws.com/geoda/data/south.zip
"""
from .base import _fetch, RemoteFileMetadata
SOUTH = RemoteFileMetadata(filename='south.zip',
  url='https://s3.amazonaws.com/geoda/data/south.zip',
  checksum='8f151d99c643b187aad37cfb5c3212353e1bc82804a4399a63de369490e56a7a')
description = '\nsouth\n=====\n\nHomicides and selected socio-economic characteristics for Southern U.S. counties.\n---------------------------------------------------------------------------------\n\n- Observations = 1,412\n- Variables = 69\n- Years = 1960-90s\n- Support = polygon\n\nFiles\n-----\nsouth.gdb     README.md  south.dbf      south.gpkg  south.kml  south.mif  south.shp  south.sqlite\ncodebook.pdf  south.csv  south.geojson  south.html  south.mid  south.prj  south.shx  south.xlsx\n\nVariables\n---------\nNAME \tcounty name\nSTATE_NAME \tstate name\nSTATE_FIPS \tstate fips code (character)\nCNTY_FIPS \tcounty fips code (character)\nFIPS \tcombined state and county fips code (character)\nSTFIPS \tstate fips code (numeric)\nCOFIPS \tcounty fips code (numeric)\nFIPSNO \tfips code as numeric variable\nSOUTH \tdummy variable for Southern counties (South = 1)\nHR** \thomicide rate per 100,000 (1960, 1970, 1980, 1990)\nHC** \thomicide count, three year average centered on 1960, 1970, 1980, 1990\nPO** \tcounty population, 1960, 1970, 1980, 1990\nRD** \tresource deprivation 1960, 1970, 1980, 1990 (principal component, see Codebook for details)\nPS** \tpopulation structure 1960, 1970, 1980, 1990 (principal component, see Codebook for details)\nUE** \tunemployment rate 1960, 1970, 1980, 1990\nDV** \tdivorce rate 1960, 1970, 1980, 1990 (% males over 14 divorced)\nMA** \tmedian age 1960, 1970, 1980, 1990\nPOL** \tlog of population 1960, 1970, 1980, 1990\nDNL** \tlog of population density 1960, 1970, 1980, 1990\nMFIL** \tlog of median family income 1960, 1970, 1980, 1990\nFP** \t% families below poverty 1960, 1970, 1980, 1990 (see Codebook for details)\nBLK** \t% black 1960, 1970, 1980, 1990\nGI** \tGini index of family income inequality 1960, 1970, 1980, 1990\nFH** \t% female headed households 1960, 1970, 1980, 1990\n'

def fetch_south(meta_data=SOUTH, dir_name='south', data_home=None, download_if_missing=True, description=description):
    """Download the south data-set.

    Download it if necessary - will check if it has been fetched already.

    Parameters
    ----------

    meta_data: RemoteFileMetadata
            fields of remote archive
             - filename
             - url
             - checksum

    dir_name: string
            the name of the dataset directory under the examples parent directory

    description: string
            Contents of the README.md file for the example dataset.

    data_home : option, default: None
        Specify another download and cache folder for the datasets. By default
        all libpysal data is stored in ~/pysal_data' subfolders

    download_if_missing : optional, True by default
       If False, raise a IOError if the data is not locally available instead
       of trying to download the data from the source site.

    """
    _fetch(meta_data,
      dir_name,
      description,
      data_home=data_home,
      download_if_missing=download_if_missing)