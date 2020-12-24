# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/debug.py
# Compiled at: 2013-01-25 20:24:52
import os, logging, settings
use_debugging = False
f_name = os.path.join(settings.config_directory, 'lyrics.log')
logging.basicConfig(filename=f_name, level=logging.DEBUG)

def debug(msg, *args):
    if use_debugging:
        logging.debug(_format_msg(msg, *args))


def warning(msg, *args):
    logging.warning(_format_msg(msg, *args))


def _format_msg(msg, *args):
    if args:
        msg = '%s: ' % msg + (', ').join(str(a) for a in args)
    return msg