# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/filter.py
# Compiled at: 2015-10-19 17:02:51
from __future__ import unicode_literals
from ..elements.elementbase import LogicElement, Attribute
from ..filter import MoyaFilter, MoyaFilterExpression

class Filter(LogicElement):
    """
    Define a [i]filter[/i], which may be used in expressions.

    Here's an example of a filter:

    [code xml]
    <filter name="repeat">
        <return-str>${str:value * count}</return-str>
    </filter>
    [/code]

    And here is how you might use it in an expression:

    [code xml]
    <echo>${"beetlejuice "|repeat(count=3)}</echo>
    [/code]
    """

    class Help:
        synopsis = b'define a filter'

    name = Attribute(b'Filter name', required=True)
    value = Attribute(b'Value name', default=b'value', required=False)
    expression = Attribute(b'Expression', type=b'function', required=False, default=None)
    missing = Attribute(b'Allow missing values?', type=b'boolean', default=False, required=False)

    def lib_finalize(self, context):
        validator = None
        for signature in self.children(b'signature'):
            validator = signature.get_validator(context)

        expression = self.expression(context)
        value_name = self.value(context)
        allow_missing = self.missing(context)
        if expression is not None:
            _filter = MoyaFilterExpression(expression, value_name, allow_missing=allow_missing)
        else:
            _filter = MoyaFilter(self.lib, self.libid, value_name, allow_missing=allow_missing, validator=validator)
        self.lib.register_filter(self.name(context), _filter)
        return