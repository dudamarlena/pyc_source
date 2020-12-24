# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/ptemplate/template.py
# Compiled at: 2011-08-05 08:36:38
__doc__ = ':mod:`ptemplate.template` -- advanced string templating\n-------------------------------------------------------\n\n:mod:`ptemplate.template` provides a :class:`Template`, a thin interface on top\n:mod:`ptemplate.formatter` that is more useful for typical templating tasks.\n'
__license__ = 'Copyright (c) 2010 Will Maier <will@m.aier.us>\n\nPermission to use, copy, modify, and distribute this software for any\npurpose with or without fee is hereby granted, provided that the above\ncopyright notice and this permission notice appear in all copies.\n\nTHE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES\nWITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF\nMERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR\nANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES\nWHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN\nACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF\nOR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\n\n'
from ptemplate.formatter import Formatter
from ptemplate.util import logger
__all__ = [
 'Template']

class Template(object):
    """A templater.

    :class:`Template` wraps :class:`ptemplate.formatter.Formatter` with a
    _`Buffet`-compatible _`interface`. In addition to the standard Buffet
    arguments (*extra_vars_func*, *options*), the constructor accepts a
    *template* string. This string is the template that will be rendered later
    (by a call to :meth:`render`).

    .. _Buffet:     http://pypi.python.org/pypi/Buffet/
    .. _interface:  http://docs.turbogears.org/1.0/TemplatePlugins
    """
    options = {}
    preprocessor = None
    converters = {}

    def __init__(self, extra_vars_func=None, options=None, template=''):
        self.log = logger(__name__, self)
        self.options = options
        self.template = template
        self.formatter = Formatter()
        self.formatter.converters.update(self.converters)

    def render(self, data, format='html', fragment=False, template=None):
        """Render the template using *data*.

        The *format*, *fragment* and *template* arguments are ignored. Instead,
        :class:`Template` uses :attr:`template` as the template, passing it to
        :attr:`preprocessor` if necessary. It then expands the template (using
        :attr:`formatter`) and returns the result as a string.
        """
        template = self.template
        preprocessor = getattr(self, 'preprocessor', None)
        if callable(preprocessor):
            template = preprocessor(template)
        self.formatter.converters.update(self.converters)
        return self.formatter.format(template, **data)

    def transform(self, info, template):
        """Render the output to Elements.

        Required by Buffet; not supported.
        """
        raise NotImplementedError

    def load_template(self, templatename):
        """Find a template specified in Python 'dot' notation.

        Required by Buffet; not supported.
        """
        raise NotImplementedError