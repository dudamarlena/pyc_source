# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/nat.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 3202 bytes
"""National NCOVR dataset.

The version retrieved here comes from:
     https://s3.amazonaws.com/geoda/data/ncovr.zip
"""
from .base import _fetch, RemoteFileMetadata
NAT = RemoteFileMetadata(filename='ncovr.zip',
  url='https://s3.amazonaws.com/geoda/data/ncovr.zip',
  checksum='e8cb04e6da634c6cd21808bd8cfe4dad6e295b22e8d40cc628e666887719cfe9')
description = '\nnat\n===\n\nUS county homicides 1960-1990\n-----------------------------\n\n- Observations = 3,085\n- Variables = 69\n- Years = 1960-90s\n- Support = polygon\n\nFiles\n-----\nncovr.gdb     NAT.csv  NAT.geojson  NAT.kml  NAT.mif  NAT.shp  NAT.sqlite  ncovr.html\ncodebook.pdf  NAT.dbf  NAT.gpkg     NAT.mid  NAT.prj  NAT.shx  NAT.xlsx    README.md\n\nVariables\n--------\nNAME \tcounty name\nSTATE_NAME \tstate name\nSTATE_FIPS \tstate fips code (character)\nCNTY_FIPS \tcounty fips code (character)\nFIPS \tcombined state and county fips code (character)\nSTFIPS \tstate fips code (numeric)\nCOFIPS \tcounty fips code (numeric)\nFIPSNO \tfips code as numeric variable\nSOUTH \tdummy variable for Southern counties (South = 1)\nHR** \thomicide rate per 100,000 (1960, 1970, 1980, 1990)\nHC** \thomicide count, three year average centered on 1960, 1970, 1980, 1990\nPO** \tcounty population, 1960, 1970, 1980, 1990\nRD** \tresource deprivation 1960, 1970, 1980, 1990 (principal component, see Codebook for details)\nPS** \tpopulation structure 1960, 1970, 1980, 1990 (principal component, see Codebook for details)\nUE** \tunemployment rate 1960, 1970, 1980, 1990\nDV** \tdivorce rate 1960, 1970, 1980, 1990 (% males over 14 divorced)\nMA** \tmedian age 1960, 1970, 1980, 1990\nPOL** \tlog of population 1960, 1970, 1980, 1990\nDNL** \tlog of population density 1960, 1970, 1980, 1990\nMFIL** \tlog of median family income 1960, 1970, 1980, 1990\nFP** \t% families below poverty 1960, 1970, 1980, 1990 (see Codebook for details)\nBLK** \t% black 1960, 1970, 1980, 1990\nGI** \tGini index of family income inequality 1960, 1970, 1980, 1990\nFH** \t% female headed households 1960, 1970, 1980, 1990\n'

def fetch_nat(meta_data=NAT, dir_name='nat', data_home=None, download_if_missing=True, description=description):
    """Download the nat data-set.

    Download it if necessary - will check if it has already been fetched.

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
        all libpysal data is stored in ~/libpysal_data' subfolders

    download_if_missing : optional, True by default
       If False, raise a IOError if the data is not locally available instead
       of trying to download the data from the source site.

    """
    _fetch(meta_data,
      dir_name,
      description,
      data_home=data_home,
      download_if_missing=download_if_missing)