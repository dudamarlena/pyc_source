# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/pygments.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4924 bytes
"""PyAMS_utils.pygments module

This module is used to provide an URL which allows you to load Pygments CSS files.
It also provides two vocabularies of available lexers and styles.
"""
from fanstatic import get_library_registry
from persistent import Persistent
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer
from pygments.styles import get_all_styles
from pyramid.response import Response
from pyramid.view import view_config
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.fanstatic import ExternalResource
from pyams_utils.interfaces.pygments import IPygmentsCodeConfiguration, PYGMENTS_LEXERS_VOCABULARY_NAME, PYGMENTS_STYLES_VOCABULARY_NAME
from pyams_utils.list import unique_iter
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'
from pyams_utils import _
for library in get_library_registry().values():
    break
else:
    try:
        from pyams_skin import library
    except ImportError:
        try:
            from pyams_default_theme import library
        except ImportError:
            library = None

if library is not None:
    pygments_css = ExternalResource(library, 'get-pygments-style.css', resource_type='css')
else:
    pygments_css = None

@view_config(name='get-pygments-style.css')
def get_pygments_style_view(request):
    """View used to download Pygments style"""
    style = request.params.get('style', 'default')
    styles = HtmlFormatter(linenos='inline', nowrap=False, cssclass='source', style=style).get_style_defs()
    return Response(styles, content_type='text/css')


@vocabulary_config(name=PYGMENTS_LEXERS_VOCABULARY_NAME)
class PygmentsLexersVocabulary(SimpleVocabulary):
    __doc__ = 'Pygments lexers vocabulary'

    def __init__(self, context):
        terms = [
         SimpleTerm('auto', title=_('Automatic detection'))]
        for name, aliases, filetypes, mimetypes in sorted(unique_iter(get_all_lexers(), key=lambda x: x[0].lower()), key=lambda x: x[0].lower()):
            terms.append(SimpleTerm(aliases[0] if len(aliases) > 0 else name, title='{0}{1}'.format(name, ' ({})'.format(', '.join(filetypes)) if filetypes else '')))

        super(PygmentsLexersVocabulary, self).__init__(terms)


@vocabulary_config(name=PYGMENTS_STYLES_VOCABULARY_NAME)
class PygmentsStylesVocabulary(SimpleVocabulary):
    __doc__ = 'Pygments styles vocabulary'

    def __init__(self, context):
        terms = []
        for name in sorted(get_all_styles()):
            terms.append(SimpleTerm(name))

        super(PygmentsStylesVocabulary, self).__init__(terms)


@factory_config(IPygmentsCodeConfiguration)
class PygmentsCodeRendererSettings(Persistent, Contained):
    __doc__ = 'Pygments code renderer settings'
    lexer = FieldProperty(IPygmentsCodeConfiguration['lexer'])
    display_linenos = FieldProperty(IPygmentsCodeConfiguration['display_linenos'])
    disable_wrap = FieldProperty(IPygmentsCodeConfiguration['disable_wrap'])
    style = FieldProperty(IPygmentsCodeConfiguration['style'])


def render_source(code: str, settings: IPygmentsCodeConfiguration):
    """Render source with given settings"""
    if settings.lexer == 'auto':
        lexer = guess_lexer(code)
    else:
        lexer = get_lexer_by_name(settings.lexer)
    if lexer is not None:
        formatter = HtmlFormatter(linenos='inline' if settings.display_linenos else None, nowrap=settings.disable_wrap, cssclass='source', style=settings.style)
        return highlight(code, lexer, formatter)