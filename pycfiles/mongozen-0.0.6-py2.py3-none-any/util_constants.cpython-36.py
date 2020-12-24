# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zencity/clones/mongozen/mongozen/util_constants.py
# Compiled at: 2018-02-11 11:03:45
# Size of source mod 2**32: 739 bytes
"""mongozen constants."""
import os
HOMEDIR = os.path.expanduser('~')
MONGOZEN_DIR_NAME = '.mongozen'
MONGOZEN_DIR_PATH = os.path.join(HOMEDIR, MONGOZEN_DIR_NAME)
os.makedirs(MONGOZEN_DIR_PATH, exist_ok=True)
DATA_DIR_NAME = 'data'
DATA_DIR_PATH = os.path.join(MONGOZEN_DIR_PATH, DATA_DIR_NAME)
os.makedirs(DATA_DIR_PATH, exist_ok=True)
MONGO_CRED_FNAME = 'mongozen_credentials.yml'
MONGO_CRED_FPATH = os.path.abspath(os.path.join(MONGOZEN_DIR_PATH, MONGO_CRED_FNAME))
PERSONAL_MONGO_CFG_FNAME = 'mongozen_cfg.yml'
PERSONAL_MONGO_CFG_FPATH = os.path.abspath(os.path.join(MONGOZEN_DIR_PATH, PERSONAL_MONGO_CFG_FNAME))
CONNECTION_TIMEOUT_IN_MS = 2500
ACCESS_MODES = [
 'reading', 'writing']
MONGODB_BULK_WRITE_LIMIT = 1000