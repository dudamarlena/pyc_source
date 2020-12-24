# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/__init__.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 752 bytes
from __future__ import absolute_import, division, print_function
import os, sys, logging
BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(level=(logging.WARN))
logger = logging.getLogger()
log_path = os.path.join(BASE_DIR, 'logs')
print('Will log to: {}'.format(log_path))
if not os.path.exists(log_path):
    os.mkdir(log_path)
fileHandler = logging.FileHandler('{0}/{1}.log'.format(log_path, 'dj-dna-streaming-python'))
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)