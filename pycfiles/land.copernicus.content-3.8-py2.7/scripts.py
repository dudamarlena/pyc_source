# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/browser/scripts.py
# Compiled at: 2018-01-16 07:51:31
from land.copernicus.content.browser.users_statistics import users_statistics_operations_center
from land.copernicus.content.config import ENV_HOST_USERS_STATS
HOST = ENV_HOST_USERS_STATS
PLONE = '/copernicus'

def get_plone_site():
    import Zope2
    app = Zope2.app()
    from Testing.ZopeTestCase import utils
    utils._Z2HOST = HOST
    path = PLONE.split('/')
    app = utils.makerequest(app)
    app.REQUEST['PARENTS'] = [app]
    app.REQUEST.other['VirtualRootPhysicalPath'] = path
    from zope.globalrequest import setRequest
    setRequest(app.REQUEST)
    from AccessControl.SpecialUsers import system as user
    from AccessControl.SecurityManagement import newSecurityManager
    newSecurityManager(None, user)
    _site = app[path[(-1)]]
    site = _site.__of__(app)
    from zope.site.hooks import setSite
    setSite(site)
    return site


def users_stats():
    """ A cron callable script to take care of our users statistics reports
        bin/zeo_client run bin/users_stats
    """
    site = get_plone_site()
    users_statistics_operations_center(site)