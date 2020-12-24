# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/config.py
# Compiled at: 2008-10-06 10:31:13
import iccommunity.mediawiki
PROJECTNAME = 'iccommunity.mediawiki'
PACKAGE = iccommunity.mediawiki
PACKAGENAME = 'iccommunity.mediawiki'
DEPENDENCIES = ['iccommunity.core']
try:
    import Products.CMFPlone.migrations.v3_0
    HAS_PLONE3 = True
except ImportError:
    HAS_PLONE3 = False