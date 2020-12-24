# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/markitup/widgets.py
# Compiled at: 2011-06-10 23:28:13
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured
if not hasattr(settings, 'MARKITUP_PATH'):
    raise ImproperlyConfigured('You must define the MARKITUP_PATH before using the MarkItUpTextarea.')
if settings.MARKITUP_PATH.endswith('/'):
    settings.MARKITUP_PATH = settings.MARKITUP_PATH[:-1]
settings.MARKITUP_DEFAULT_SET = getattr(settings, 'MARKITUP_DEFAULT_SET', 'default')
settings.MARKITUP_DEFAULT_SKIN = getattr(settings, 'MARKITUP_DEFAULT_SKIN', 'simple')

class MarkItUpTextarea(forms.Textarea):
    """Textarea widget render with `markItUp`
    
    markItUp:
        http://markitup.jaysalvat.com/home/
    """

    def __init__(self, attrs=None, path=None, set=None, skin=None, **kwargs):
        """Constructor of MarkItUpTextarea
        
        Attributes:
            path        - MarkItUp directory URI (DEFAULT = settings.MARKITUP_PATH)
            set         - MarkItUp set name
            skin        - MarkItUp skin name
        
        Example:
            *------------------------------------------*
            + javascript
              + markitup
                + sets
                  + default
                    + set.js
                    + style.css
                + skins
                  + simple
                    + style.css
              + jquery.markitup.js
            *------------------------------------------*
            settings.MARKITUP_PATH = r"javascript/markitup"
            
            markitup = MarkItUpTextarea(
                set='default', skin='simple'
            )
            document = forms.TextField(widget=markitup)
        """
        super(MarkItUpTextarea, self).__init__(attrs=attrs, **kwargs)
        self.path = path or settings.MARKITUP_PATH
        self.set = set or settings.MARKITUP_DEFAULT_SET
        self.skin = skin or settings.MARKITUP_DEFAULT_SKIN

    @property
    def media(self):
        css = {'screen, projection': (
                                '%s/sets/%s/style.css' % (self.path, self.set),
                                '%s/skins/%s/style.css' % (self.path, self.skin))}
        js = (
         '%s/jquery.markitup.js' % self.path,
         '%s/sets/%s/set.js' % (self.path, self.set))
        return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        """Render MarkItUpTextarea"""
        html = super(MarkItUpTextarea, self).render(name, value, attrs)
        code = render_to_string('markitup/javascript.html', {'id': 'id_%s' % name})
        body = '%s\n%s' % (html, code)
        return mark_safe(body)


class AdminMarkItUpTextareaWidget(MarkItUpTextarea, AdminTextareaWidget):
    pass