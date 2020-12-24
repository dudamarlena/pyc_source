# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/rapl_read.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2070 bytes
""" This module reads intel power measurements"""
from __future__ import absolute_import
import logging, glob, os
from collections import namedtuple
from s_tui.helper_functions import cat
INTER_RAPL_DIR = '/sys/class/powercap/intel-rapl/'
MICRO_JOULE_IN_JOULE = 1000000.0
RaplStats = namedtuple('rapl', ['label', 'current', 'max'])

def rapl_read():
    """ Read power stats and return dictionary"""
    basenames = glob.glob('/sys/class/powercap/intel-rapl:*/')
    basenames = sorted(set({x for x in basenames}))
    pjoin = os.path.join
    ret = list()
    for path in basenames:
        name = None
        try:
            name = cat((pjoin(path, 'name')), fallback=None, binary=False)
        except (IOError, OSError, ValueError) as err:
            try:
                logging.warning('ignoring %r for file %r', (
                 err, path), RuntimeWarning)
                continue
            finally:
                err = None
                del err

        if name:
            try:
                current = cat(pjoin(path, 'energy_uj'))
                max_reading = 0.0
                ret.append(RaplStats(name, float(current), max_reading))
            except (IOError, OSError, ValueError) as err:
                try:
                    logging.warning('ignoring %r for file %r', (
                     err, path), RuntimeWarning)
                finally:
                    err = None
                    del err

    return ret