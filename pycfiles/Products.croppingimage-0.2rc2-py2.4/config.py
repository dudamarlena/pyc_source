# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/croppingimage/config.py
# Compiled at: 2008-07-23 09:49:01
DESIRED_WIDTH = 600
DESIRED_HEIGHT = 450
CROPPING_IMAGE_TYPE = 'CroppingImage'
LONG_NAME = 'Cropping Image'
PROJECTNAME = 'croppingimage'
SKINS_DIR = 'skins'
GLOBALS = globals()
from Globals import package_home
_product_dir = package_home(GLOBALS)
f = file('%s/version.txt' % _product_dir, 'r')
VERSION = f.read().strip()
f.close()
del f
del package_home
del _product_dir