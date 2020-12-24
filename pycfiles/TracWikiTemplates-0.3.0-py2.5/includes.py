# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/macros/includes.py
# Compiled at: 2007-11-10 06:34:56
import inspect
from trac.core import *
from trac.wiki.api import IWikiMacroProvider
from trac.wiki.formatter import wiki_to_html
from WikiTemplates.model import WikiTemplate
from WikiTemplates.errors import TemplatesError

class IncludesMacro(Component):
    """Grab a wiki page and include it's full contents inside another.
    To use:
        {{{
        [[Include(WikiPageNameToInclude)]]
        }}}
    [[BR]]
    For more information go to:
        http://wikitemplates.ufsoft.org"""
    implements(IWikiMacroProvider)

    def get_macros(self):
        yield 'Include'

    def get_macro_description(self, name):
        return inspect.getdoc(IncludesMacro)

    def render_macro(self, req, name, content):
        if not content:
            raise TracError, 'Nothing was passed'
        args = [ arg.strip() for arg in content.split('|') ]
        if len(args) != 1:
            self.env.log.debug('ARGS PASSED TO INCLUDE: %r', args)
            return TemplatesError("The 'Include' macro doesn't support arguments.\nIt exists to simply include another wiki page into the current one.\nClick your browser's back button and correct the error, or check the edit box below if present.")
        if args[0].startswith('http://') or args[0].startswith('https://'):
            import urllib
            try:
                webpage = urllib.urlopen(args[0])
                html = webpage.read()
                webpage.close()
                self.env.log.debug('INCLUDE CONTENTS: %r', html)
                return html
            except Exception, e:
                return (
                 TracError, e)

        else:
            contents = WikiTemplate(self.env, args.pop(0), table='wiki')
            return wiki_to_html(contents.text, self.env, req)