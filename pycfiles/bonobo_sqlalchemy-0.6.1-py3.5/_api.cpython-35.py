# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/_api.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 248 bytes
from bonobo.util.api import ApiHelper
from bonobo_sqlalchemy.readers import Select
from bonobo_sqlalchemy.writers import InsertOrUpdate
__all__ = []
api = ApiHelper(__all__=__all__)
api.register_group(Select)
api.register_group(InsertOrUpdate)