# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/eggproxy/config.py
# Compiled at: 2008-09-22 04:57:28
from ConfigParser import ConfigParser
CONFIG_FILE = '/etc/apache2/eggproxy.conf'
config = ConfigParser()
config.add_section('default')
config.set('default', 'eggs_directory', '/var/www')
config.set('default', 'index', 'http://pypi.python.org/simple')
config.set('default', 'update_interval', 24)
config.readfp(open(CONFIG_FILE))
EGGS_DIR = config.get('default', 'eggs_directory')