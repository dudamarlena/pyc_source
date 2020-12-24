# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/application/config.py
# Compiled at: 2010-11-21 09:08:50
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import logging, os

def appConfig():
    import aha
    config = aha.Config()
    from aha.dispatch.router import get_router, get_fallback_router
    r = get_router()
    config.initial_user = [
     'test@example.com']
    config.site_root = 'http://your.site'
    config.error_template = '/common/error'
    config.logout_url = '/logout'
    config.page_cache_expire = 14400
    config.query_cache_expire = 7200
    if not hasattr(config, 'site_admin_menus'):
        config.site_admin_menus = [('/style/img/edit_icon.gif', 'Site setting', '/_edit_sitedata')]
    r.connect('/_edit_sitedata', controller='sitedata', action='edit')
    from util.authenticate import admin
    config.admin_auth = admin
    from aha.auth.appengine import AppEngineAuth
    config.auth_obj = AppEngineAuth
    fr = get_fallback_router()
    fr.connect('*url', controller='main', action='index')
    if config.debug:
        config.page_cache_expire = 0
        config.query_cache_expire = 0
        config.site_root = 'http://127.0.0.1:8080'
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()