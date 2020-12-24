# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/nyc_bikes.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 1997 bytes
"""NYC Bike trips

The version retrieved here comes from:
https://github.com/sjsrey/nyc_bikes/archive/master.zip
"""
from .base import _fetch, RemoteFileMetadata
BIKE = RemoteFileMetadata(filename='master.zip',
  url='https://github.com/sjsrey/nyc_bikes/archive/master.zip',
  checksum='159b430476d53cdd6891832c18c575c10cee25e401da96ce7f7aeb049fccd387')
description = '\nNYC Bike Data\n=============\n\n\n- observations: 14042 origin-desination flows\n- variables: 27\n- support: polygon\n\n\nFiles\n-----\nnyc_bikes_ct.csv\nnyct2010.dbf\nnyct2010.prj\nnyct2010.shp\nnyct2010.shp.xml\nnyct2010.shx\n\n\nVariables\n--------\n\ncount\tnumber of trips\nd_cap   destination tract cap\nd_tract destination tract\ndistance distance\nend station latitutde\nend station longitude\no_cap   origin tract cap\no_tract origin tract\n'

def fetch_bikes(meta_data=BIKE, dir_name='nyc_bikes', data_home=None, download_if_missing=True, description=description):
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