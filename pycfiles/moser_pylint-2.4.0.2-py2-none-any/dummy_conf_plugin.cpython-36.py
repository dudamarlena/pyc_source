# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/regrtest_data/dummy_plugin/dummy_conf_plugin.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 106 bytes


def register(linter):
    pass


def load_configuration(linter):
    linter.config.black_list += ('bin', )