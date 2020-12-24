# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/utils.py
# Compiled at: 2014-04-26 09:00:59
"""Utilities"""
import sys

def log(message, *args, **kwargs):
    try:
        try:
            output = message.format(*args, **kwargs)
            sys.stderr.write(('{0:s}\n').format(output))
            sys.stderr.flush()
        except Exception as e:
            output = ('ERROR: {0:s}\n').format(e)
            sys.stderr.write(output)
            sys.stderr.flush()

    finally:
        return output