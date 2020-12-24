# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bdauvergne/Code/xstatic-chart-js/xstatic/pkg/chart_js/__init__.py
# Compiled at: 2015-11-26 05:58:33
"""
XStatic resource package

See package 'XStatic' for documentation and basic tools.
"""
DISPLAY_NAME = 'Chart.js'
PACKAGE_NAME = 'XStatic-%s' % DISPLAY_NAME
NAME = __name__.split('.')[(-1)]
VERSION = '1.0.2'
BUILD = '2'
PACKAGE_VERSION = VERSION + '.' + BUILD
DESCRIPTION = '%s %s (XStatic packaging standard)' % (DISPLAY_NAME, VERSION)
PLATFORMS = 'any'
CLASSIFIERS = []
KEYWORDS = '%s xstatic' % NAME
MAINTAINER = 'Benjamin Dauvergne'
MAINTAINER_EMAIL = 'bdauvergne@entrouvert.com'
HOMEPAGE = 'https://github.com/nnnick/Chart.js'
LICENSE = '(same as %s)' % DISPLAY_NAME
from os.path import join, dirname
BASE_DIR = join(dirname(__file__), 'data')
LOCATIONS = {}