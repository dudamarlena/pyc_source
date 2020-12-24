# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/templatetags/djblets_deco.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django import template
from django.template.loader import render_to_string
from djblets.util.decorators import blocktag
register = template.Library()

@register.tag
@blocktag
def box(context, nodelist, classname=None):
    """
    Displays a box container around content, with an optional class name.
    """
    return render_to_string(b'deco/box.html', {b'classname': classname or b'', 
       b'content': nodelist.render(context)})


@register.tag
@blocktag
def errorbox(context, nodelist, box_id=None):
    """
    Displays an error box around content, with an optional ID.
    """
    return render_to_string(b'deco/errorbox.html', {b'box_id': box_id or b'', 
       b'content': nodelist.render(context)})