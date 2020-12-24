# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/software/codegra.fs/env/lib/python3.7/site-packages/codegra_fs/cgfs_types.py
# Compiled at: 2019-02-07 09:15:21
# Size of source mod 2**32: 547 bytes
from mypy_extensions import TypedDict
PartialStat = TypedDict('PartialStat',
  {'st_size':int, 
 'st_atime':float, 
 'st_mtime':float, 
 'st_ctime':float, 
 'st_uid':int, 
 'st_gid':int},
  total=True)

class FullStat(PartialStat, total=True):
    st_nlink: int
    st_mode: int


__APIHandlerResponse = TypedDict('__APIHandlerResponse',
  {'ok': bool},
  total=True)

class APIHandlerResponse(__APIHandlerResponse, total=False):
    error: str
    data: str