# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/serghei/dev/xstatic-jquery-colourpicker/xstatic/pkg/jquery_colourpicker/__init__.py
# Compiled at: 2017-05-19 06:02:57
"""
XStatic resource package

See package 'XStatic' for documentation and basic tools.
"""
DISPLAY_NAME = 'jquery-colourpicker'
PACKAGE_NAME = 'XStatic-%s' % DISPLAY_NAME
NAME = __name__.split('.')[(-1)]
VERSION = '1.0.0'
BUILD = '1'
PACKAGE_VERSION = VERSION + '.' + BUILD
DESCRIPTION = '%s %s (XStatic packaging standard)' % (DISPLAY_NAME, VERSION)
PLATFORMS = 'any'
CLASSIFIERS = []
KEYWORDS = '%s xstatic' % NAME
MAINTAINER = 'Serghei Mihai'
MAINTAINER_EMAIL = 'smihai@entrouvert.com'
HOMEPAGE = 'http://andreaslagerkvist.com/jquery/colour-picker/'
LICENSE = '(same as %s)' % DISPLAY_NAME
from os.path import join, dirname
BASE_DIR = join(dirname(__file__), 'data')
LOCATIONS = {}