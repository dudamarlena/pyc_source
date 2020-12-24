# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/rio_grande_do_sul.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 2290 bytes
"""Cities of the Brazilian State of Rio Grande do Sul

The version retrieved here comes from:
https://github.com/sjsrey/rio_grande_do_sul/archive/master.zip
"""
from .base import _fetch, RemoteFileMetadata
RIO = RemoteFileMetadata(filename='master.zip',
  url='https://github.com/sjsrey/rio_grande_do_sul/archive/master.zip',
  checksum='e5629e782e77037912cbfc40d3738f4752e27b5bdfc99a95368b232047b53ff3')
description = '\n\nRio_Grande_do_Sul\n======================\n\nCities of the Brazilian State of Rio Grande do Sul\n-------------------------------------------------------\n\n* 43MUE250GC_SIR.dbf: attribute data (k=2)\n* 43MUE250GC_SIR.shp: Polygon shapefile (n=499)\n* 43MUE250GC_SIR.shx: spatial index\n* 43MUE250GC_SIR.cpg: encoding file \n* 43MUE250GC_SIR.prj: projection information \n* map_RS_BR.dbf: attribute data (k=3)\n* map_RS_BR.shp: Polygon shapefile (no lakes) (n=497)\n* map_RS_BR.prj: projection information\n* map_RS_BR.shx: spatial index\n\n\n\nSource: Renan Xavier Cortes <renanxcortes@gmail.com>\nReference: https://github.com/pysal/pysal/issues/889#issuecomment-396693495\n'

def fetch_rio(meta_data=RIO, dir_name='rio_grande_do_sul', data_home=None, download_if_missing=True, description=description):
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