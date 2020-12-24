# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/papydvd/run.py
# Compiled at: 2010-12-19 17:09:00
from repoze.bfg.configuration import Configurator
from paste.deploy.converters import asbool
from papydvd.models import initialize_sql

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    settings['default_locale_name'] = 'it'
    config = Configurator(settings=settings)
    config.begin()
    config.load_zcml(zcml_file)
    config.end()
    return config.make_wsgi_app()