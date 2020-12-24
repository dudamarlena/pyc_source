# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/tales.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 2992 bytes
"""PyAMS_i18n.tales module

This module provides a TALES "i18n" expression, as well as a PyAMS TALES extension also called
"i18n"; the first one is the default one used to get a translated attribute value into a chameleon
template, while the second one can be used when you have to handle possible mising attributes
by providing a default value.
"""
from chameleon.astutil import Symbol
from chameleon.tales import StringExpr
from zope.interface import Interface
from pyams_i18n.interfaces import II18n
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.tales import ContextExprMixin
__docformat__ = 'restructuredtext'

def render_i18n_expression(econtext, name):
    """Render an I18n expression

    Value can be given as a single attribute name (for example: "i18n:title"), in which case value
    is extracted from current "context".

    Value can also be given as a dotted name, for example "i18n:local_var.property.title".
    """
    name = name.strip()
    if '.' in name:
        names = name.split('.')
        context = econtext.get(names[0])
        for name in names[1:-1]:
            context = getattr(context, name)

        attr = names[(-1)]
    else:
        context = econtext.get('context')
        attr = name
    request = econtext.get('request')
    return II18n(context).query_attribute(attr, request=request)


class I18nExpr(ContextExprMixin, StringExpr):
    __doc__ = 'i18n:context.attribute TALES expression'
    transform = Symbol(render_i18n_expression)


@adapter_config(name='i18n', context=(Interface, Interface, Interface), provides=ITALESExtension)
class I18NTalesExtension(ContextRequestViewAdapter):
    __doc__ = 'tales:i18n(context, attribute, default=None) TALES extension\n\n    Similar to standard i18n: TALES expression, but provides a default value for missing attributes.\n    Please note that this extension returns default value when applied on a non-existent attribute,\n    not on an attribute with an empty value for selected language!\n    '

    def render(self, context, attribute, default=None):
        """Render TALES extension"""
        try:
            value = II18n(context).query_attribute(attribute, request=self.request)
        except AttributeError:
            value = default

        return value