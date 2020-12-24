# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/utils.py
# Compiled at: 2007-04-17 14:30:43
from zope.testing.cleanup import cleanUp
from zope.publisher.browser import TestRequest

class RESPONSE(object):
    __module__ = __name__

    def __init__(self):
        self.headers = dict()

    def redirect(self, url, lock=None):
        self.status = 302
        self.headers['location'] = url
        self.lock = lock


def new_request(**kwargs):
    request = TestRequest(form=kwargs)
    request.RESPONSE = RESPONSE()
    return request


def setDebugMode(mode):
    """
    Allows manual setting of Five's inspection of debug mode to allow for
    zcml to fail meaningfully
    """
    import Products.Five.fiveconfigure as fc
    fc.debug_mode = mode


def safe_load_site():
    """Load entire component architecture (w/ debug mode on)"""
    cleanUp()
    setDebugMode(1)
    import Products.Five.zcml as zcml
    zcml.load_site()
    setDebugMode(0)


def safe_load_site_wrapper(function):
    """Wrap function with a temporary loading of entire component architecture"""

    def wrapper(*args, **kw):
        safe_load_site()
        value = function(*args, **kw)
        cleanUp()
        import Products.Five.zcml as zcml
        zcml._initialized = 0
        return value

    return wrapper


def monkeyAppAsSite():
    import OFS.Application
    from Products.Five.site.metaconfigure import classSiteHook
    from Products.Five.site.localsite import FiveSite
    from zope.interface import classImplements
    from zope.app.component.interfaces import IPossibleSite, ISite
    classSiteHook(OFS.Application.Application, FiveSite)
    classImplements(OFS.Application.Application, IPossibleSite)


def newuser():
    """ loads up an unrestricted security manager"""
    from AccessControl.SecurityManagement import newSecurityManager
    from AccessControl.User import UnrestrictedUser
    newSecurityManager({}, UnrestrictedUser('debug', 'debug', [], []))