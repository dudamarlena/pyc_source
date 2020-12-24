# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bdauvergne/Code/xstatic-leaflet/xstatic/pkg/chart_js/__init__.py
# Compiled at: 2017-01-12 02:20:52
"""
XStatic resource package

See package 'XStatic' for documentation and basic tools.
"""
DISPLAY_NAME = 'Leaflet'
PACKAGE_NAME = 'XStatic-%s' % DISPLAY_NAME
NAME = __name__.split('.')[(-1)]
VERSION = '1.0.2'
BUILD = '1'
PACKAGE_VERSION = VERSION + '.' + BUILD
DESCRIPTION = '%s %s (XStatic packaging standard)' % (DISPLAY_NAME, VERSION)
PLATFORMS = 'any'
CLASSIFIERS = []
KEYWORDS = '%s xstatic' % NAME
MAINTAINER = 'Benjamin Dauvergne'
MAINTAINER_EMAIL = 'bdauvergne@entrouvert.com'
HOMEPAGE = 'http://leaflet.github.io/'
LICENSE = '(same as %s)' % DISPLAY_NAME
from os.path import join, dirname
BASE_DIR = join(dirname(__file__), 'data')
LOCATIONS = {}