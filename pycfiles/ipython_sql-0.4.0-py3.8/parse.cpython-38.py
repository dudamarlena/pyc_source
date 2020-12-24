# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sql/parse.py
# Compiled at: 2020-05-02 10:55:12
# Size of source mod 2**32: 2011 bytes
import json, re
from os.path import expandvars
import six
import six.moves as CP
from sqlalchemy.engine.url import URL

def connection_from_dsn_section(section, config):
    parser = CP.ConfigParser()
    parser.read(config.dsn_filename)
    cfg_dict = dict(parser.items(section))
    return str(URL(**cfg_dict))


def _connection_string(s):
    s = expandvars(s)
    if '@' in s or '://' in s:
        return s
    if s.startswith('['):
        if s.endswith(']'):
            section = s.lstrip('[').rstrip(']')
            parser = CP.ConfigParser()
            parser.read(config.dsn_filename)
            cfg_dict = dict(parser.items(section))
            return str(URL(**cfg_dict))
    return ''


def parse(cell, config):
    """Extract connection info and result variable from SQL
    
    Please don't add any more syntax requiring 
    special parsing.  
    Instead, add @arguments to SqlMagic.execute.
    
    We're grandfathering the 
    connection string and `<<` operator in.
    """
    result = {'connection':'', 
     'sql':'',  'result_var':None}
    pieces = cell.split(None, 3)
    if not pieces:
        return result
    result['connection'] = _connection_string(pieces[0])
    if result['connection']:
        pieces.pop(0)
    if len(pieces) > 1:
        if pieces[1] == '<<':
            result['result_var'] = pieces.pop(0)
            pieces.pop(0)
    result['sql'] = ' '.join(pieces).strip()
    return result