# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/cli/init.py
# Compiled at: 2017-01-24 16:17:40
# Size of source mod 2**32: 1140 bytes
from cement.utils.misc import init_defaults
from configparser import NoSectionError
from cli.Mcg import Mcg
from core.db.MongoDB import MongoDB

def main():
    defaults = init_defaults('mcg', 'log.logging')
    defaults['log.logging']['file'] = 'mcg.log'
    with Mcg('mcg', config_defaults=defaults) as (app):
        app.setup()
        try:
            MongoDB({'user': app.config.get('mongodb', 'user'), 
             'password': app.config.get('mongodb', 'password'), 
             'host': app.config.get('mongodb', 'host'), 
             'port': app.config.get('mongodb', 'port'), 
             'db': app.config.get('mongodb', 'db')})
        except NoSectionError:
            print('Configuration File Not Found or [mongodb] Section Not Found (/etc/mcg/mcg.conf)')

        app.run()
        app.close()