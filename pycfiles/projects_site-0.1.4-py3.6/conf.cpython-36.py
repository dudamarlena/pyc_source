# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/projects_base/base/conf.py
# Compiled at: 2020-04-23 05:23:02
# Size of source mod 2**32: 364 bytes
import os, configparser
res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'res', 'config.ini')
config = configparser.ConfigParser()
config.read(res_path)
config.get('BASE', 'static_folder')
config.get('BASE', 'upload_folder')
config.get('BASE', 'db_lock')