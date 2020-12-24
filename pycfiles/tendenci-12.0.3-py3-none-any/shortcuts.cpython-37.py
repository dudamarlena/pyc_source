# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/shortcuts.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 1787 bytes
from django.http import HttpResponse
from django.template.loader import get_template, select_template

def _strip_content_above_doctype(html):
    """Strips any content above the doctype declaration out of the
    resulting template. If no doctype declaration, it returns the input.

    This was done because content above the doctype in IE8 triggers the
    browser to go into quirks mode which can break modern HTML5 and CSS3
    elements from the theme.
    """
    try:
        doctype_position = html.index('<!D')
        html = html[doctype_position:]
    except ValueError:
        pass

    return html


def themed_response(request, template_name, context={}, content_type=None, status=None, using=None):
    """
    This is a direct replacement for django.shortcuts.render() which should be
    used in all views by replacing:
    from django.shortcuts import render as render_to_resp
    With:
    from tendenci.apps.theme.shortcuts import themed_response as render_to_resp
    """
    if isinstance(template_name, (list, tuple)):
        template = select_template(template_name, using=using)
    else:
        template = get_template(template_name, using=using)
    context['TEMPLATE_NAME'] = template.origin.template_name
    context['TEMPLATE_THEME'] = getattr(template.origin, 'theme', None)
    rendered = template.render(context=context, request=request)
    rendered = _strip_content_above_doctype(rendered)
    return HttpResponse(rendered, content_type=content_type, status=status)