# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/microne/config.py
# Compiled at: 2011-03-30 02:43:33
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import logging, os, sys

def initConfig(basedir):
    """
    Initialize config object
    """
    sys.path = [
     basedir,
     os.path.join(basedir, 'application'),
     os.path.join(basedir, 'lib')] + sys.path
    import aha
    config = aha.Config()
    config.template_dirs = [
     os.path.join(basedir, 'template'),
     'plugin']
    import dispatcher
    config.dispatcher = dispatcher
    config.debug = False
    config.useappstatus = False
    if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
        config.debug = True
    from aha.controller import makocontroller
    makocontroller.get_lookup()
    config.template_lookup = makocontroller.tlookup
    config.error_template = ''
    config.page_cache_expire = 14400
    config.query_cache_expire = 7200
    config.debug = os.environ.get('SERVER_SOFTWARE', '').lower().startswith('dev')
    if config.debug:
        config.page_cache_expire = 0
        config.query_cache_expire = 0
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    from application import *
    if not hasattr(config, 'auth_obj'):
        from aha.auth.appengine import AppEngineAuth
        config.auth_obj = AppEngineAuth
    if not hasattr(config, 'controller_class'):
        from aha.controller.makocontroller import MakoTemplateController
        config.controller_class = MakoTemplateController
    return config


if __name__ == '__main__':
    main()