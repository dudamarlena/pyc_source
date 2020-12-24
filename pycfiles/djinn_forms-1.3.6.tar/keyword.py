# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/widgets/keyword.py
# Compiled at: 2015-08-26 18:03:23
from django.forms.widgets import Widget
from django.forms import Media
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
TPL = 'djinn_forms/snippets/keywordwidget.html'

class KeywordWidget(Widget):
    """ Widget for handling user keywords. Supported attributes:
      * search_url Specify the url to use for searching suggestions
    """

    def _media(self):
        """ Add JS for TinyMCE """
        return Media(js=('js/djinn_forms_keyword.js', ), css={'all': ('css/djinn_forms_keyword.css', )})

    media = property(_media)

    def render(self, name, value, attrs=None):
        url = self.attrs.get('search_url', reverse('djinn_forms_keywords'))
        context = {'name': name, 'hint': self.attrs.get('hint', ''), 
           'value': (',').join(value), 
           'keywords': value, 
           'maxkeywords': self.attrs.get('maxkeywords', 10), 
           'search_minlength': self.attrs.get('search_minlength', 2), 
           'search_url': url}
        html = render_to_string(TPL, context)
        return mark_safe(('').join(html))