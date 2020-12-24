# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/common/log.py
# Compiled at: 2012-03-02 22:17:19
"""
Convenience functions around the logging module
"""
import logging, os.path

def init_logging(level):
    if level == 2:
        level = logging.DEBUG
    elif level == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('paramiko').setLevel(logging.CRITICAL)
    l = logging.getLogger('globusprovision')
    l.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    l.addHandler(fh)


def set_logging_instance(instance):
    l = logging.getLogger('globusprovision')
    fh = logging.FileHandler(os.path.expanduser('%s/deploy.log' % instance.instance_dir))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    l.addHandler(fh)


def log(msg, func, node):
    if node != None:
        msg = '%s - %s' % (node.id, msg)
    func(msg)
    return


def debug(msg, node=None):
    log(msg, logging.getLogger('globusprovision').debug, node)


def warning(msg, node=None):
    log(msg, logging.getLogger('globusprovision').warning, node)


def info(msg, node=None):
    log(msg, logging.getLogger('globusprovision').info, node)