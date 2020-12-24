# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lust/config.py
# Compiled at: 2013-03-08 10:32:47
from ConfigParser import SafeConfigParser

def load_ini_file(file_name, defaults={}):
    config = SafeConfigParser()
    config.readfp(open(file_name))
    results = {}
    for section in config.sections():
        for key, value in config.items(section):
            results[section + '.' + key] = value

    results.update(defaults)
    return results