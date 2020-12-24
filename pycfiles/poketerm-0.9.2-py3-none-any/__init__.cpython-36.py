# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\Setup\__init__.py
# Compiled at: 2017-12-09 18:42:10
# Size of source mod 2**32: 656 bytes
from datetime import datetime
import logging, os, sys

def setup_logger(name, loglevel=logging.INFO):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = logging.FileHandler(filename=('logs/{}_{}.log'.format(name, datetime.now().strftime('%m_%d_%y'))))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(level=loglevel,
      format='[%(asctime)s] {%(filename)s:%(lineno)d} (%(funcName)s) %(levelname)s - %(message)s',
      handlers=handlers)
    logger = logging.getLogger(__name__)
    return logger