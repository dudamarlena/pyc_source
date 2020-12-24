# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sc/__init__.py
# Compiled at: 2009-12-29 13:58:42
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

try:
    from zopeskel.localcommands.plone import *
    from zopeskel.localcommands.archetype import *
    ArchetypeSubTemplate.parent_templates.append('sc_plone_app')
    PloneSubTemplate.parent_templates.append('sc_plone_app')
except ImportError:
    pass