# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/compression.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1697 bytes
from tempfile import NamedTemporaryFile
import shutil, gzip, bz2

def uncompress_file(input_file_name, file_extension, dest_dir):
    """
    Uncompress gz and bz2 files
    """
    if file_extension.lower() not in ('.gz', '.bz2'):
        raise NotImplementedError('Received {} format. Only gz and bz2 files can currently be uncompressed.'.format(file_extension))
    if file_extension.lower() == '.gz':
        fmodule = gzip.GzipFile
    else:
        if file_extension.lower() == '.bz2':
            fmodule = bz2.BZ2File
    with fmodule(input_file_name, mode='rb') as (f_compressed):
        with NamedTemporaryFile(dir=dest_dir, mode='wb',
          delete=False) as (f_uncompressed):
            shutil.copyfileobj(f_compressed, f_uncompressed)
    return f_uncompressed.name