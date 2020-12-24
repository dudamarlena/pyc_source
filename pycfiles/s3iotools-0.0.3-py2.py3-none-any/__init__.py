# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: s3iotools/__init__.py
# Compiled at: 2019-05-20 08:43:33
from ._version import __version__
__short_description__ = 'Make S3 file object read/write easier, support raw file, csv, parquet, pandas.DataFrame.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .io.file_object import S3FileObject
except ImportError:
    pass

try:
    from .io.dataframe import S3Dataframe
except ImportError:
    pass

try:
    from .utils.s3_obj_filter import select_from, Filters, filter_constructor
except ImportError:
    pass

try:
    from .utils.s3_url_builder import s3_url_builder
except ImportError:
    pass