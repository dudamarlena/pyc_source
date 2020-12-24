# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\Documents\PythonWorkSpace\py3\py33_projects\autocompvar-project\autocompvar\__init__.py
# Compiled at: 2017-02-24 14:47:31
# Size of source mod 2**32: 347 bytes
__version__ = '0.0.3'
__short_description__ = 'make your data importable'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
try:
    from .helpers import create_data_script
    from .metadata import gen_code
    from .name_convention import to_variable_name
except ImportError:
    pass