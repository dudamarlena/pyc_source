# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www-python/django-adminlte-full/demo/adminlte_full/utils.py
# Compiled at: 2016-06-11 10:09:14
# Size of source mod 2**32: 1717 bytes
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.contrib.staticfiles.templatetags.staticfiles import static
import re
from hashlib import md5
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class Html(object):
    _Html__unpaired = [
     'link', 'img']

    @classmethod
    def tag(cls, tag, attrs=None, content=None):
        template = '<{tag}{attrs}>' + ('' if tag in cls._Html__unpaired else '{content}</{tag}>')
        attrs = mark_safe(flatatt(attrs)) if attrs else ''
        content = force_text(content) if content else ''
        return format_html(template, tag=tag, attrs=attrs, content=content)

    @classmethod
    def css_file(cls, url):
        if url:
            return cls.tag('link', {'rel': 'stylesheet', 
             'href': url})
        return ''

    @classmethod
    def js_file(cls, url):
        if url:
            return cls.tag('script', {'src': url})
        return ''

    @classmethod
    def gravatar_url(cls, email, size=200):
        return 'https://www.gravatar.com/avatar/{}?{}'.format(md5(email.lower().encode('utf-8')).hexdigest(), urlencode({'d': cls.static('dist/img/avatar.png'), 
         's': str(size)}))

    @classmethod
    def static(cls, path):
        if not path:
            return ''
        absolute = re.match('^(http|https|//)', path, re.IGNORECASE)
        if absolute:
            return path
        return static(path)