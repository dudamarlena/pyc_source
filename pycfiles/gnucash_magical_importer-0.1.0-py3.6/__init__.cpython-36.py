# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/__init__.py
# Compiled at: 2018-12-13 21:04:34
# Size of source mod 2**32: 543 bytes
import sys
sys.path.append('gnucash_importer')
import os, logging
from gnucash_importer.util import Util
if os.environ.get('DEBUG_TEST', False) in ('TRUE', 'True', 'true', '1', 't', 'y', 'yes'):
    loglevel = logging.DEBUG
    logformat = Util.LOG_FORMAT_DEBUG
    logging.basicConfig(level=loglevel, format=logformat)