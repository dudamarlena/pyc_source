# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/confighelper.py
# Compiled at: 2018-06-19 09:05:36
# Size of source mod 2**32: 762 bytes


class ConfigHelper(object):

    @staticmethod
    def bool_to_config_str(input_val: bool) -> str:
        if input_val:
            return 'yes'
        else:
            return 'no'