# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/config.py
# Compiled at: 2017-10-20 16:05:59
import pkg_resources
PROJECTNAME = 'sc.photogallery'
JS_RESOURCES = ('++resource++collective.js.cycle2/jquery.cycle2.min.js', '++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js',
                '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js')
HAS_ZIPEXPORT = True
try:
    pkg_resources.get_distribution('ftw.zipexport')
except pkg_resources.DistributionNotFound:
    HAS_ZIPEXPORT = False