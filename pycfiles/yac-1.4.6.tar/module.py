# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/module.py
# Compiled at: 2017-12-29 18:03:49
import os, imp
from yac.lib.file import get_localized_script_path

def get_module(module_path_arg, params):
    module_path = get_localized_script_path(module_path_arg, params)
    module_name = 'yac.lib.customizations'
    if module_path and os.path.exists(module_path):
        script_module = imp.load_source(module_name, module_path)
    else:
        script_module = imp.new_module(module_name)
    return script_module