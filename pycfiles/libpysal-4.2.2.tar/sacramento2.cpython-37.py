# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/sacramento2.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 5118 bytes
"""Zip Code Business Patterns for Sacramento
The version retrieved here comes from:
     https://s3.amazonaws.com/geoda/data/SacramentoMSA2.zip
"""
from .base import _fetch, RemoteFileMetadata
SAC = RemoteFileMetadata(filename='SacramentoMSA2.zip',
  url='https://s3.amazonaws.com/geoda/data/SacramentoMSA2.zip',
  checksum='6446dc044ebb8ce8e63b806bf5202adc80330592f115c8f48d894a706f6481cf')
description = "\nsacramento2\n===========\n\n2000 Census Tract Data for Sacramento MSA\n-----------------------------------------\n\n- Observations = 83\n- Variables = 66\n- Years = 1998, 2001\n- Support = polygon\n\nFiles\n-----\n SacramentoMSA2.gdb       SacramentoMSA2.kml   SacramentoMSA2.shp\n README.md                SacramentoMSA2.mid   SacramentoMSA2.shx\n SacramentoMSA2.csv       SacramentoMSA2.mif   SacramentoMSA2.sqlite\n SacramentoMSA2.dbf       SacramentoMSA2.prj   SacramentoMSA2.xlsx\n SacramentoMSA2.geojson   SacramentoMSA2.sbn  'Variable Info for Zip Code File.pdf'\n SacramentoMSA2.gpkg      SacramentoMSA2.sbx\n\nVariables\n---------\nZIP ZIP code\nPO_NAME \tName of ZIP code area\nSTATE \tSTATE\nMSA \tMSA\nCBSA_CODE \tCBSA code\nMAN98 \t1998 total manufacturing establishments (MSA)\nMAN98_12 \t1998 total manufacturing establishments, 1-9 employees (MSA)\nMAN98_39 \t1998 total manufacturing establishments 10+ employees (MSA)\nMAN01 \t2001 total manufacturing establishments (MSA)\nMAN01_12 \t2001 total manufacturing establishments, 1-9 employees (MSA)\nMAN01_39 \t2001 total manufacturing establishments, 10+ employees (MSA)\nMAN98US \t1998 total manufacturing establishments (US)\nMAN98US12 \t1998 total manufacturing establishments, 1-9 employees (US)\nMAN98US39 \t1998 total manufacturing establishments 10+ employees (US)\nMAN01US \t2001 total manufacturing establishments (US)\nMAN01US_12 \t2001 total manufacturing establishments, 1-9 employees (US)\nMAN01US_39 \t2001 total manufacturing establishments, 10+ employees (US)\nOFF98 \t1998 total office establishments (MSA)\nOFF98_12 \t1998 total office establishments, 1-9 employees (MSA)\nOFF98_39 \t1998 total office establishments, 10+ employees (MSA)\nOFF01 \t2001 total office establishments (MSA)\nOFF01_12 \t2001 total office establishments, 1-9 employees (MSA)\nOFF01_39 \t2001 total office establishments, 10+ employees (MSA)\nOFF98US \t1998 total office establishments (US)\nOFF98US12 \t1998 total office establishments, 1-9 employees (US)\nOFF98US39 \t1998 total office establishments, 10+ employees (US)\nOFF01US \t2001 total office establishments (US)\nOFFUS01_12 \t2001 total office establishments, 1-9 employees (US)\nOFFUS01_39 \t2001 total office establishments, 10+ employees (US)\nINFO98 \t1998 total information establishments (MSA)\nINFO98_12 \t1998 total information establishments, 1-9 employees (MSA)\nINFO98_39 \t1998 total information establishments, 10+ employees (MSA)\nINFO01 \t2001 total information establishments (MSA)\nINFO01_12 \t2001 total information establishments, 1-9 employees (MSA)\nINFO01_39 \t2001 total information establishments, 10+ employees (MSA)\nINFO98US \t1998 total information establishments (US)\nINFO98US12 \t1998 total information establishments, 1-9 employees (US)\nINFO98US39 \t1998 total information establishments, 10+ employees (US)\nINFO01US \t2001 total information establishments (US)\nINFO01US_1 \t2001 total information establishments, 1-9 employees (US)\nINFO01US_3 \t2001 total information establishments, 10+ employees (US)\nINDEX \tIndex\nNUMSEC \tNumber of sectors represented in ZIP code\nEST98 \tTotal establishments in ZIP code, 1998\nEST01 \tTotal establishments in ZIP code, 2001\nPCTNGE \tNational growth effect, percent (N)\nPCTIME \tIndustry mix effect, percent (M)\nPCTCSE \tCompetitive shift effect, percent (S)\nPCTGRO \tPercent growth establishments, 1998-2001 (R)\nID \tUnique ZIP code ID for ID variables in weights matrix creation window\n\nSource: US Census Bureau, 2000 Census (Summary File 3). Extracted from http://factfinder.census.gov in April 2004.\n"

def fetch_sacramento2(meta_data=SAC, dir_name='sacramento2', data_home=None, download_if_missing=True, description=description):
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