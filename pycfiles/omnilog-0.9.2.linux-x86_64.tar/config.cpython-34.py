# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/config.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 441 bytes


class Config(object):
    __doc__ = '\n    This class object serves the configuration readed in the json file to all threads.\n    Here there is no concurrency control, we dont need it.\n    When the config watcher detects configuration changes in config.json, it firstly stops\n    all threads / sub components. After this config object is done, The main module will\n    startup all the threads again.\n    '
    config_dict = None