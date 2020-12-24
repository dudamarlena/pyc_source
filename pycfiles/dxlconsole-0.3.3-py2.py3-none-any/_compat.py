# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opendxl/viji/opendxl-console/dxlconsole/_compat.py
# Compiled at: 2019-06-07 18:26:01
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def read_file(config_parser, file_like_obj):
    config_parser.optionxform = str
    if hasattr(config_parser, 'read_file'):
        return config_parser.read_file(file_like_obj)
    return config_parser.readfp(file_like_obj)