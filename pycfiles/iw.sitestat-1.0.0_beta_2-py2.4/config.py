# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/config.py
# Compiled at: 2008-10-10 10:14:00
"""
iw.sitestat globals
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
PRODUCTNAME = 'iw.sitestat'
I18N_DOMAIN = 'iw.sitestat'
ANNOTATIONS_KEY = 'iw.sitestat'
PROPERTYSHEET = 'iwsitestat_properties'
PDF_MIMETYPES = ('application/pdf', 'application/x-pdf')
BLACKLISTED_LABELS = ('agent', 'availscreen', 'colordepth', 'cookie', 'corporate',
                      'day', 'full_loading_time', 'html_loading_time', 'HttpReferer',
                      'innersize', 'ip', 'java', 'lang', 'mimetypes', 'name', 'newcookie',
                      'NewCookie', 'offset', 'or', 'outersize', 'p', 'pie', 'plugins',
                      'referrer', 'screen', 'site', '_t', 'time', 'type', 'url',
                      'ver')
BLACKLISTED_CHARS = ' &=<>'
import os
PACKAGE_HOME = os.path.dirname(os.path.abspath(__file__))
del os
ZOPETESTCASE = False
try:
    import Products.PloneArticle
except ImportError, e:
    HAVE_PLONEARTICLE = False
else:
    HAVE_PLONEARTICLE = True

try:
    import Products.Collage
except ImportError, e:
    HAVE_COLLAGE = False
else:
    HAVE_COLLAGE = True

try:
    import Products.SimpleAlias
except ImportError, e:
    HAVE_SIMPLEALIAS = False
else:
    HAVE_SIMPLEALIAS = True