# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/application.py
# Compiled at: 2015-11-17 11:55:31
from ConfigParser import ConfigParser
from pyramid.config import Configurator
import pkg_resources

def main(global_config, **settings):
    cp = ConfigParser()
    cp.readfp(pkg_resources.resource_stream('springboard', 'defaults.ini'))
    defaults = dict(cp.items('springboard:pyramid'))
    defaults.update(settings)
    config = Configurator(settings=defaults)
    config.include('springboard.config')
    config.add_translation_dirs('springboard:locale/')
    config.configure_celery(global_config['__file__'])
    return config.make_wsgi_app()