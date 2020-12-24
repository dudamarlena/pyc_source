# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/config.py
# Compiled at: 2008-10-06 10:31:06
try:
    import Products.CMFPlone.migrations.v3_0
    HAS_PLONE3 = True
except ImportError:
    HAS_PLONE3 = False

import icsemantic.langfallback
PACKAGE = icsemantic.langfallback
PROJECTNAME = 'icsemantic.langfallback'
PACKAGENAME = 'icsemantic.langfallback'
DEPENDENCIES = [
 'LinguaPlone', 'icsemantic.core']
if HAS_PLONE3:
    DEPENDENCIES.insert(0, 'plone.browserlayer')
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
GLOBALS = globals()