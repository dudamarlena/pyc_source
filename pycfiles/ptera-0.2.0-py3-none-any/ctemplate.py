# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/ptemplate/ctemplate.py
# Compiled at: 2011-08-05 08:06:41
__doc__ = ":mod:`ptemplate.ctemplate` -- ctemplate-like interface\n------------------------------------------------------\n\nThis module implements a templating interface similar Google's `ctemplate\n<http://google-ctemplate.googlecode.com/>`_ with a few important exceptions:\n\n* templates may not change the field delimiter\n* modifiers are marked with '!'\n* comments are marked with '%'\n* the templater does not strip whitespace (except by modifiers)\n* includes are not supported\n* pragmas/macros are not supported\n* separator sections are not supported\n\nLike ctemplate, :class:`CTemplate` expands a string template to match the\nstructure of a dictionary (using :class:`ptemplate.template.Template`). Data dictionaries\nmay contain either lists of other data dictionaries or single values (string,\ninteger, float, etc). Plain variables are substituted according to the usual\nPython string formatting rules (see :pep:`3101`). Sections (fields preceded by\n'#') are expanded once for each data dictionary contained in the corresponding\nlist.\n"
__license__ = 'Copyright (c) 2010 Will Maier <will@m.aier.us>\n\nPermission to use, copy, modify, and distribute this software for any\npurpose with or without fee is hereby granted, provided that the above\ncopyright notice and this permission notice appear in all copies.\n\nTHE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES\nWITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF\nMERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR\nANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES\nWHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN\nACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF\nOR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\n\n'
from ptemplate.template import Template
from ptemplate.util import logger
__all__ = [
 'CTemplate']

class CTemplate(Template):
    """A (somewhat) ctemplate-compatible templater.

    Incompatibilities with Google's ctemplate are documented in
    :mod:`ptemplate.ctemplate`. Construction of a :class:`CTemplate` instance
    is the same as with :class:`ptemplate.template.Template`.
    """
    globals = {'BI_NEWLINE': '\n', 
       'BI_SPACE': ' '}

    def __init__(self, *args, **kwargs):
        super(CTemplate, self).__init__(*args, **kwargs)
        self.log = logger(__name__, self)

    def preprocessor(self, input):
        """Convert Google's ctemplate syntax.

        Since ctemplate and :mod:`ptemplate.template` are quite similar
        internally, a simple translation can make a document (mostly) legible.
        At the moment, the preprocessor only converts the marker indicators
        ('{{' and '}}') and comment character ('!').
        """
        input = input.replace('{', '{{')
        input = input.replace('{{{{', '{')
        input = input.replace('}', '}}')
        input = input.replace('}}}}', '}')
        input = input.replace('{!', '{%')
        return input

    def render(self, data, format='html', fragment=False, template=None):
        """Render the template.

        Here, :class:`CTemplate` adds the :attr:`globals` dictionary to the *data*
        dictionary before calling :meth:`ptemplate.template.Template.render`.
        """
        globals = self.globals.copy()
        globals.update(data)
        return super(CTemplate, self).render(globals)