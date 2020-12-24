# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/templates/SiteBase.py
# Compiled at: 2006-12-13 20:08:51
from Cheetah.Filters import Filter
from Cheetah.Template import Template
from turbogears import url
from cblog.widgets.base import serialize_et
from cblog.utils.formatting import escape

class HSC(Filter):
    """A filter for Cheetah placeholder substitution supporting unicode objects.

    Supports the following arguments:

    encoding  - encode unicode string with the given encoding (default: utf-8).
    escape    - if evaluates to True, escape HTML special chars when
                substituting the placeholder. If escape == 'quote', also
                replace '"' with '&quot;'.
    maxlength - if set to an int > 0, truncate the placeholder substitution at
                max maxlength characters, possibly replacing the end with
                suffix.
    suffix    - when truncating the placeholder to maxlength, replace the last
                len(suffix) characters with suffix (default '...').
    """
    __module__ = __name__

    def filter(self, val, **kw):
        if val is None:
            return ''
        if hasattr(val, 'makeelement'):
            val = serialize_et(val)
        if isinstance(val, unicode):
            val = val.encode(kw.get('encoding', 'utf-8'))
        val = str(val)
        if kw.get('escape', False):
            val = escape(val, kw.get('escape') == 'quote')
        if kw.get('maxlength'):
            try:
                length = int(kw['maxlength'])
            except ValueError:
                pass
            else:
                suffix = kw.get('suffix', '...')
                if len(val) > length and suffix:
                    length -= len(suffix)
                    val = val[:length] + suffix
                else:
                    val = val[:length]
        return val


class SiteBase(Template):
    __module__ = __name__
    image_base = url('/static/images/')
    css_base = url('/static/css/')
    js_base = url('/static/javascript/')
    _js_src_tmpl = '<script type="text/javascript" language="JavaScript%s">\n%s</script>'
    _js_link_tmpl = '<script type="text/javascript" language="JavaScript%s" src="%s"></script>'
    _css_link_tmpl = '<link rel="%s" type="text/css" href="%s" />'

    def __init__(self, *args, **kw):
        """Constructor sets the default filter to use."""
        kw['filter'] = HSC
        super(SiteBase, self).__init__(*args, **kw)

    def js_src(self, relpath, version=''):
        return self._js_src_tmpl % (version, self.js_base + relpath)

    def js_link(self, relpath, version=''):
        return self._js_link_tmpl % (version, self.js_base + relpath)

    def css_link(self, relpath, type='stylesheet'):
        return self._css_link_tmpl % (type, self.css_base + relpath)