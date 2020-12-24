# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/utils/log.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 1601 bytes
import os, logging
logger = logging.getLogger(__name__)

def configure_logging(process_name):
    """
    Configure all logging to a log file
    ===
    %(asctime)s Human-readable time
    %(name)s Name of the logger used to log the call.
    """
    logs_folder_path = os.path.join(os.environ['WORKDIR_PATH'], os.environ['LOGS_DIR_PATH'])
    logging.basicConfig(level=(logging.DEBUG),
      format='%(asctime)s %(name)s %(levelname)s %(message)s',
      datefmt='%d-%b-%y %H:%M:%S',
      filename=('{}/process_name_{}.log'.format(logs_folder_path, process_name)))