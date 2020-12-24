# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pathogenseq/logger.py
# Compiled at: 2018-07-14 05:50:46
import json

def log(key, log_file):
    x = json.load(open(log_file))
    x[key] = True
    json.dump(open(log_file, 'w'), x)


def checkpoint(key, log_file):
    x = json.load(open(log_file))
    if key in x:
        return False
    return True