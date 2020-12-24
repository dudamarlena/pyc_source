# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/utils/conf_utils.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 910 bytes
import os
from arch.api.utils import file_utils

def get_base_config(key, default=None):
    base_config = file_utils.load_yaml_conf(os.path.join(file_utils.get_project_base_directory(), 'arch/conf/base_conf.yaml')) or dict()
    return base_config.get(key, default)