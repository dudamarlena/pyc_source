# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/__init__.py
# Compiled at: 2007-04-18 06:57:54
__version__ = '0.4'

def get_config():
    """Load config file and return configobj containing that information.
    
    Config file is located using 'ECONCONF' environment variable or, if that
    does not exist, looking for a file './etc/econ.conf' (note that this path
    is taken in relation to the current directory.
    """
    import os, ConfigParser
    configFilePath = os.path.abspath('./etc/econ.conf')
    if os.environ.has_key('ECONCONF'):
        configFilePath = os.environ['ECONCONF']
    config = ConfigParser.ConfigParser()
    config.read(configFilePath)
    return config


conf = get_config()