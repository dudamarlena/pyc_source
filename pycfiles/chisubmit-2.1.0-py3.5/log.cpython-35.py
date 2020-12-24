# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/common/log.py
# Compiled at: 2014-09-17 12:26:15
# Size of source mod 2**32: 2333 bytes
import logging

def init_logging(verbose=False, debug=False):
    if verbose:
        level = logging.INFO
    else:
        if debug:
            level = logging.DEBUG
        else:
            level = logging.WARNING
    l = logging.getLogger('chisubmit')
    l.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    l.addHandler(fh)


def log(msg, func):
    func(msg)


def debug(msg):
    log(msg, logging.getLogger('chisubmit').debug)


def warning(msg):
    log(msg, logging.getLogger('chisubmit').warning)


def info(msg):
    log(msg, logging.getLogger('chisubmit').info)