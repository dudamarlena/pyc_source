# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/include.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2615 bytes
"""PyAMS_utils.include module

This module is used for Pyramid integration
"""
import os.path
from chameleon import PageTemplateFile
from persistent import IPersistent
from zope.annotation import IAttributeAnnotatable, IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.keyreference.interfaces import IKeyReference
from zope.keyreference.persistent import KeyReferenceToPersistent
import pyams_utils
from pyams_utils.container import ParentSelector
from pyams_utils.context import ContextSelector
from pyams_utils.i18n import set_locales
from pyams_utils.request import RequestSelector, get_annotations, get_debug, get_display_context
from pyams_utils.tales import ExtensionExpr
from pyams_utils.traversing import NamespaceTraverser
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_utils:locales')
    set_locales(config.registry.settings)
    config.add_request_method(get_annotations, 'annotations', reify=True)
    config.add_request_method(get_debug, 'debug', reify=True)
    config.add_request_method(get_display_context, 'display_context', property=True)
    config.add_traverser(NamespaceTraverser)
    config.add_subscriber_predicate('context_selector', ContextSelector)
    config.add_subscriber_predicate('parent_selector', ParentSelector)
    config.add_subscriber_predicate('request_selector', RequestSelector)
    config.registry.registerAdapter(AttributeAnnotations, (IAttributeAnnotatable,), IAnnotations)
    config.registry.registerAdapter(KeyReferenceToPersistent, (IPersistent,), IKeyReference)
    config.scan()
    if hasattr(config, 'load_zcml') and os.path.exists(os.path.join(pyams_utils.__path__[0], 'configure.zcml')):
        config.load_zcml('configure.zcml')
    PageTemplateFile.expression_types['tales'] = ExtensionExpr