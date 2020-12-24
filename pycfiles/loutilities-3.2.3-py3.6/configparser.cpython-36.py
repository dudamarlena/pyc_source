# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\configparser.py
# Compiled at: 2019-11-25 16:48:03
# Size of source mod 2**32: 1577 bytes
"""
configparser - enhanced ConfigParser
===================================================
uses pypi's configparser.ConfigParser.SafeConfigParser to parse INI file, but preserves case for keys
"""
from collections import OrderedDict
from configparser import ConfigParser
config = ConfigParser()
config.optionxform = lambda option: option

def getitems(filepath, section):
    """
    get items in section
    convert to integer, float, etc., as appropriate
    
    :param filepath: file to read config from
    :param section: section to read items from
    :rtype: OrderedDict containing {key:item, ...} (case is preserved for keys)
    """
    config.readfp(open(filepath))
    thisconfig = config.items(section)
    outdict = OrderedDict()
    for key, value in thisconfig:
        try:
            outdict[key] = eval(value)
        except:
            outdict[key] = value

    return outdict