# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/projects_base/base/conf.py
# Compiled at: 2020-04-25 05:24:47
# Size of source mod 2**32: 364 bytes
import os, configparser
res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'res', 'config.ini')
config = configparser.ConfigParser()
config.read(res_path)
config.get('BASE', 'static_folder')
config.get('BASE', 'upload_folder')
config.get('BASE', 'db_lock')