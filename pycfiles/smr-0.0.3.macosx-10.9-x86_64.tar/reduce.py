# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/reduce.py
# Compiled at: 2014-07-27 13:01:51
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
from .config import get_config, configure_job

def run(config):
    configure_job(config)
    try:
        try:
            for result in iter(sys.stdin.readline, b''):
                result = result.rstrip()
                config.REDUCE_FUNC(result)

        except (KeyboardInterrupt, SystemExit):
            pass

    finally:
        config.OUTPUT_RESULTS_FUNC()


def main():
    config = get_config()
    run(config)