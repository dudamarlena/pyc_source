# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/grouping/strategies/template.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.grouping.component import GroupingComponent
from sentry.grouping.strategies.base import strategy

@strategy(id='template:v1', interfaces=['template'], variants=['default'], score=1100)
def template_v1(template, **meta):
    filename_component = GroupingComponent(id='filename')
    if template.filename is not None:
        filename_component.update(values=[template.filename])
    context_line_component = GroupingComponent(id='context-line')
    if template.context_line is not None:
        context_line_component.update(values=[template.context_line])
    return GroupingComponent(id='template', values=[filename_component, context_line_component])