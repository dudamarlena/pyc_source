# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/nielsen/config.py
# Compiled at: 2019-11-07 22:38:00
# Size of source mod 2**32: 1548 bytes
"""
Config module for Nielsen.
The CONFIG variable from this module should be imported into other modules as
needed.
"""
import configparser
from os import getenv, name, path
CONFIG = configparser.ConfigParser()
CONFIG.add_section('Options')
CONFIG.add_section('Filters')
CONFIG.add_section('IDs')
CONFIG['Options'] = {'User':'', 
 'Group':'', 
 'Mode':'644', 
 'Interactive':'False', 
 'LogFile':'nielsen.log', 
 'LogLevel':'WARNING', 
 'MediaPath':'', 
 'OrganizeFiles':'False', 
 'DryRun':'False', 
 'FetchTitles':'False', 
 'ServiceURI':'http://api.tvmaze.com/'}

def load_config(filename=None):
    """Load config file specified by filename, or check XDG directories for
        configuration files."""
    if filename and path.isfile(filename):
        config_file = filename
    else:
        if name == 'posix':
            config_file = [
             '/etc/xdg/nielsen/nielsen.ini',
             '/etc/nielsen/nielsen.ini',
             path.expanduser('~/.config/nielsen/nielsen.ini')]
        else:
            if name == 'nt':
                config_file = path.join('', getenv('APPDATA'), 'nielsen', 'nielsen.ini')
    return CONFIG.read(config_file)


def update_series_ids(filename=None):
    """Add series_ids to IDs section of filename or default user file."""
    config_files = load_config(filename)
    filename = config_files[(-1)]
    with open(filename, 'w') as (f):
        CONFIG.write(f)