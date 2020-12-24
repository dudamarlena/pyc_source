# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/tales.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4460 bytes
"""PyAMS_utils.tales module

This module provides a custom TALES extension engine, which allows you to define custom
TALES expressions which can be used from Chameleon or Zope templates.
"""
import re
from chameleon.astutil import Symbol
from chameleon.codegen import template
from chameleon.tales import StringExpr
from zope.contentprovider.tales import addTALNamespaceData
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

class ContextExprMixin:
    __doc__ = 'Mixin-class for expression compilers'
    transform = None

    def __call__(self, target, engine):
        assignment = super(ContextExprMixin, self).__call__(target, engine)
        transform = template('target = transform(econtext, target)', target=target, transform=self.transform)
        return assignment + transform


FUNCTION_EXPRESSION = re.compile('(.+)\\((.+)\\)', re.MULTILINE | re.DOTALL)
ARGUMENTS_EXPRESSION = re.compile('[^(,)]+')

def render_extension(econtext, name):
    """TALES extension renderer

    See :ref:`tales` for complete description.

    The requested extension can be called with our without arguments, like in
    ${structure:tales:my_expression} or ${structure:tales:my_expression(arg1, arg2)}.
    In the second form, arguments will be passed to the "render" method; arguments can be
    static (like strings or integers), or can be variables defined into current template
    context; other Python expressions including computations or functions calls are actually
    not supported, but dotted syntax is supported to access inner attributes of variables.
    """

    def get_value(econtext, arg):
        """Extract argument value from context

        Extension expression language is quite simple. Values can be given as
        positioned strings, integers or named arguments of the same types.
        """
        arg = arg.strip()
        if arg.startswith('"') or arg.startswith("'"):
            return arg[1:-1]
        if '=' in arg:
            key, value = arg.split('=', 1)
            value = get_value(econtext, value)
            return {key.strip(): value}
        try:
            arg = int(arg)
        except ValueError:
            args = arg.split('.')
            result = econtext.get(args.pop(0))
            for arg in args:
                result = getattr(result, arg)

            return result
        else:
            return arg

    name = name.strip()
    context = econtext.get('context')
    request = econtext.get('request')
    view = econtext.get('view')
    args, kwargs = [], {}
    func_match = FUNCTION_EXPRESSION.match(name)
    if func_match:
        name, arguments = func_match.groups()
        for arg in map(lambda x: get_value(econtext, x), ARGUMENTS_EXPRESSION.findall(arguments)):
            if isinstance(arg, dict):
                kwargs.update(arg)
            else:
                args.append(arg)

    registry = request.registry
    extension = registry.queryMultiAdapter((context, request, view), ITALESExtension, name=name)
    if extension is None:
        extension = registry.queryMultiAdapter((context, request), ITALESExtension, name=name)
    if extension is None:
        extension = registry.queryAdapter(context, ITALESExtension, name=name)
    if extension is None:
        return ''
    addTALNamespaceData(extension, econtext)
    return extension.render(*args, **kwargs)


class ExtensionExpr(ContextExprMixin, StringExpr):
    __doc__ = 'tales: TALES expression\n\n    This expression can be used to call a custom named adapter providing ITALESExtension interface.\n    '
    transform = Symbol(render_extension)