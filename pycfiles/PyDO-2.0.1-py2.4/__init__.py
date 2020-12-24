# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/__init__.py
# Compiled at: 2007-02-15 13:23:36
"""PyDO (Python Data Objects) is an object-relational wrapper for
relational databases.  It provides a convenient API for retrieving and
manipulating data without constraining in any way how the data is
persisted at the RDBMS level.  Supported databases are:

   * postgresql
   * mysql
   * sqlite
   * mssql
   * oracle

"""
from pydo.exceptions import *
from pydo.field import *
from pydo.guesscache import *
from pydo.base import *
from pydo.operators import *
from pydo.dbi import *
from pydo.dbtypes import *
from pydo.log import *
from pydo.multifetch import *
from pydo.utils import getall
__all__ = getall(('pydo.%s' % m for m in ('exceptions field guesscache base operators dbi dbtypes log multifetch').split()))
del getall
__version__ = '2.0'