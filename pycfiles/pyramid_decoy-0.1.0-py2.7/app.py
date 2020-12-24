# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_decoy/app.py
# Compiled at: 2014-12-20 15:40:48
"""pyramid_decoy's pyramid app definition."""
from pyramid.config import Configurator

def main(global_config, **settings):
    """Build a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    return config.make_wsgi_app()