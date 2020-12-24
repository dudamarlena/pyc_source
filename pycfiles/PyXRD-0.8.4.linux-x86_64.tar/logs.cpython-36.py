# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/logs.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2058 bytes
import os, queue, logging
from logging.handlers import QueueHandler, QueueListener

def setup_logging(basic=False, prefix=None):
    """
        Setup logging module.
    """
    from pyxrd.data import settings
    debug = settings.DEBUG
    log_file = settings.LOG_FILENAME
    basic = not settings.GUI_MODE
    fmt = '%(name)s - %(levelname)s: %(message)s'
    if prefix is not None:
        fmt = prefix + ' ' + fmt
    if log_file is not None:
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
    if not basic:
        file_handler = logging.FileHandler(log_file, 'w')
        disk_fmt = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-40s %(message)s',
          datefmt='%m-%d %H:%M')
        file_handler.setFormatter(disk_fmt)
        log_handler = logging.StreamHandler()
        full = logging.Formatter(fmt)
        log_handler.setFormatter(full)
        log_que = queue.Queue(-1)
        queue_handler = QueueHandler(log_que)
        queue_listener = QueueListener(log_que, file_handler, log_handler, respect_handler_level=True)
        queue_listener.start()
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        logger.addHandler(queue_handler)
    else:
        logging.basicConfig(format=fmt)
        logger = logging.getLogger('')
        logger.addHandler(queue_handler)
    settings.FINALIZERS.append(queue_listener.stop)