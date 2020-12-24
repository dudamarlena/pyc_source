# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/options.py
# Compiled at: 2017-12-04 07:19:32
import os
TRUE_VALUES = ('true', '1', 'yes')

def get_boolean_option(option_dict, option_name, env_name):
    return option_name in option_dict and option_dict[option_name][1].lower() in TRUE_VALUES or str(os.getenv(env_name)).lower() in TRUE_VALUES