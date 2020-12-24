# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/taz.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 1767 bytes
"""Cities of the Brazilian State of Rio Grande do Sul

The version retrieved here comes from:
https://github.com/sjsrey/taz/archive/master.zip
"""
from .base import _fetch, RemoteFileMetadata
TAZ = RemoteFileMetadata(filename='master.zip',
  url='https://github.com/sjsrey/taz/archive/master.zip',
  checksum='1a734670ce8d104beb57a55406ffce497d33d807d5fdf8e63f85f4dff0e39383')
description = '\ntaz\n===\n\nDataset used for regionalization\n--------------------------------\n\n* taz.dbf: attribute data. (k=14)\n* taz.shp: Polygon shapefile. (n=4109)\n* taz.shx: spatial index.\n'

def fetch_taz(meta_data=TAZ, dir_name='taz', data_home=None, download_if_missing=True, description=description):
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