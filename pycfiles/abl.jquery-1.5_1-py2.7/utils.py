# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/abl/jquery/core/utils.py
# Compiled at: 2013-08-29 10:09:25
from tg import override_template, request
from tg import tmpl_context as c

def partial_action(action, widget, data, **kwargs):
    """
    This can be use inside of a TG2 action that uses paging.
    It returns a partial content
    @action: the TG2 action
    @param widget: the widget that is paginated
    @param data: the data that should be returned, typically a list like object
    @kwargs: the kwargs of the action. That may contain 'partial'
    """
    name = widget.id
    page = '%s_page' % name
    if kwargs.get('partial') and request.GET.has_key(page):
        override_template(action, 'genshi:abl.jquery.core.templates.widget_container')
        c.widget = widget
        return {name: data}