# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/settings.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 121 bytes
import dotenv, os

def load_settings_from_env(root_path):
    dotenv.load_dotenv(os.path.join(root_path, '.env'))