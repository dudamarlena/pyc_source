# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/data/path.py
# Compiled at: 2019-08-22 02:11:50
# Size of source mod 2**32: 1246 bytes
import os
from os.path import expanduser
from odin.utils import select_path
DEFAULT_BASE_DIR = expanduser('~')
if 'SISUA_DATA' in os.environ:
    DATA_DIR = os.environ['SISUA_DATA']
    os.path.exists(DATA_DIR) or os.mkdir(DATA_DIR)
else:
    if os.path.isfile(DATA_DIR):
        raise RuntimeError("Store data path at '%s' must be a folder" % DATA_DIR)
    else:
        DATA_DIR = select_path((os.path.join(DEFAULT_BASE_DIR, 'bio_data')), create_new=True)
    PREPROCESSED_BASE_DIR = DATA_DIR
    DOWNLOAD_DIR = select_path((os.path.join(DATA_DIR, 'downloads')), create_new=True)
    if 'SISUA_EXP' in os.environ:
        EXP_DIR = os.environ['SISUA_EXP']
        os.path.exists(EXP_DIR) or os.mkdir(EXP_DIR)
    else:
        if os.path.isfile(EXP_DIR):
            raise RuntimeError("Experiment path at '%s' must be a folder" % EXP_DIR)
        else:
            EXP_DIR = select_path((os.path.join(DEFAULT_BASE_DIR, 'bio_log')), create_new=True)