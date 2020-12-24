# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cedricporter/git/funcat/funcat/__init__.py
# Compiled at: 2017-04-19 07:07:20
import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()
version_info = tuple((int(v) if v.isdigit() else v) for v in __version__.split('.'))
__main_version__ = '%s.%s.x' % (version_info[0], version_info[1])
del pkgutil
from .api import *
from .indicators import *
from .data.tushare_backend import TushareDataBackend
from .context import ExecutionContext as funcat_execution_context
funcat_execution_context(date=20170104, order_book_id='000001.XSHG', data_backend=TushareDataBackend())._push()