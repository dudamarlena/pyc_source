# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\Documents\PythonWorkSpace\py3\py33_projects\autocompvar-project\autocompvar\helpers.py
# Compiled at: 2017-02-24 14:40:39
# Size of source mod 2**32: 752 bytes
from __future__ import print_function
import os
try:
    from .metadata import gen_code
    from .name_convention import to_variable_name
except:
    from autocompvar.metadata import gen_code
    from autocompvar.name_convention import to_variable_name

def create_data_script(metadata):
    """Create an importable python script stands for the object orientied style
    data visiting.
    
    Warning! This will silently overwrite files. Use this function when you
    fully understand what it does.
    """
    code = gen_code(metadata)
    filename = '%s.py' % to_variable_name(metadata['classname'])
    with open(filename, 'wb') as (f):
        f.write(code.encode('utf-8'))