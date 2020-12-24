# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmclaughlin/git/LABHR/octohatrack/octohatrack/utils.py
# Compiled at: 2015-11-21 05:35:59
import os, logging

class AttrDict(dict):
    """Attribute Dictionary (set and access attributes 'pythonically')"""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('no such attribute: %s' % name)

    def __setattr__(self, name, val):
        self[name] = val


def get_logger(name, level=None):
    """Returns logging handler based on name and level (stderr)
        name (str): name of logging handler
        level (str): see logging.LEVEL
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        stderr = logging.StreamHandler()
        stderr.setFormatter(logging.Formatter('%(levelname)s [%(name)s]: %(message)s'))
        logger.addHandler(stderr)
        level = level if level else os.environ.get('OCTOHUB_LOGLEVEL', 'CRITICAL')
        logger.setLevel(getattr(logging, level))
    return logger