# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/restzzz/lib/python2.7/site-packages/restzzz/__init__.py
# Compiled at: 2014-09-11 22:48:19
"""Main entry point
"""
from pyramid.config import Configurator
import yaml, restzzz.views as views

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('cornice')
    with open(config.registry.settings['restzzz.file']) as (fi):
        views.load_sockets(yaml.load(fi.read()))
    config.scan('restzzz.views')
    return config.make_wsgi_app()