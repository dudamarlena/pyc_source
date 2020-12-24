# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erik997/dev/python/dhooks-lite/venv/lib/python3.5/site-packages/tests/__init__.py
# Compiled at: 2020-03-31 13:14:22
# Size of source mod 2**32: 764 bytes
import logging, os

def set_test_logger(logger_name: str, name: str) -> object:
    """set logger for current test module
    
    Args:
    - logger: current logger object
    - name: name of current module, e.g. __file__
    
    Returns:
    - amended logger
    """
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s')
    f_handler = logging.FileHandler('{}.log'.format(os.path.splitext(name)[0]), 'w+')
    f_handler.setFormatter(f_format)
    logger = logging.getLogger(logger_name)
    logger.level = logging.DEBUG
    logger.addHandler(f_handler)
    logger.propagate = False
    return logger