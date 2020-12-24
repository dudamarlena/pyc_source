# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/example.py
# Compiled at: 2017-05-12 18:03:48
# Size of source mod 2**32: 2354 bytes
import re
from typing import Match
from django.conf import settings
from django.utils.safestring import SafeString
from django.utils.module_loading import import_string
from django.urls import reverse
from .render_source import render_template_source, render_python_source

def add_links_to_docs(text: str) -> str:
    """
    This somewhat hacky function takes a string of documentation and
    adds Sphinx documentation hyperlinks to anything that looks like a
    reference to a uswds_forms object.

    Note that it's assumed the text passed in is trusted.
    """

    def hyperlink(match: Match) -> str:
        end_text = ''
        objname = match.group(0)
        if objname.endswith('.'):
            end_text = objname[(-1)]
            objname = objname[:-1]
        _, short_objname = objname.split('.', 1)
        import_string(objname)
        return '<a href="{}reference.html#{}"><code>{}</code></a>{}'.format(settings.DOCS_URL, objname, short_objname, end_text)

    text = re.sub('uswds_forms\\.([a-zA-Z0-9_.]+)', hyperlink, text)
    return text


class Example:

    def __init__(self, basename):
        self.basename = basename
        self.view = import_string('app.examples.' + basename + '.view')
        docstr = import_string('app.examples.' + basename + '.__doc__')
        self.name, description = docstr.split('\n\n', 1)
        self.description = SafeString(add_links_to_docs(description))
        self.python_source = render_python_source(basename + '.py')

    @property
    def template_source(self):
        return render_template_source(self.basename + '.html')

    @property
    def url(self):
        return reverse('example', args=(self.basename,))

    def render(self, request):
        return SafeString(self.view(request).content.decode('utf-8'))