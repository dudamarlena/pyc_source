# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/config/start_log.py
# Compiled at: 2016-06-30 06:13:10
from __future__ import print_function
import os, time
startup_debug = os.environ.get('TING_YUN_STARTUP_DEBUG', 'off').lower() in ('on', 'true',
                                                                            '1')
log_file = '/tmp/tingyun_bootstrap.log'
log_file_handler = None

def log_message(text, *args):
    global startup_debug
    if startup_debug:
        text = text % args
        timestamp = time.strftime('%m-%d %T', time.localtime())
        print('TingYun: %s (%d) - %s' % (timestamp, os.getpid(), text))
        return True
    return False


def log_bootstrap(msg, close=False):
    """
    :param msg:
    :return:
    """
    global log_file_handler
    if not startup_debug:
        return
    else:
        if close and log_file_handler is not None:
            log_data = '%s %s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime()), os.getpid(), str(msg))
            log_file_handler.write(log_data)
            log_file_handler.write('close the log file....\n')
            log_file_handler.close()
            log_file_handler = None
            return
        if close and log_file_handler is None:
            log_file_handler = open(log_file, mode='a')
            log_data = '%s %s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime()), os.getpid(), str(msg))
            log_file_handler.write(log_data)
            log_file_handler.write('close the log file....\n')
            log_file_handler.close()
            log_file_handler = None
            return
        if not close and log_file_handler is None:
            log_file_handler = open(log_file, mode='a')
            log_file_handler.write('open the log file....\n')
        log_data = '%s %s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime()), os.getpid(), str(msg))
        log_file_handler.write(log_data)
        return