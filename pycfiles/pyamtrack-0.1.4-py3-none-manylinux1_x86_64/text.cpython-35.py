# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/text.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 9467 bytes
__doc__ = 'PyAMS_utils.text module\n\nThis module provides text manipulation and conversion functions, as well as a set of TALES\nextensions (see :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`).\n'
import html, docutils.core
from markdown import markdown
from pyramid.interfaces import IRequest
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_utils.adapter import ContextRequestAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.interfaces.text import IHTMLRenderer
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'
from pyams_utils import _

def get_text_start(text, length, maxlen=0):
    """Get first words of given text with maximum given length

    Text is always truncated between words; if *maxlen* is specified, text is shortened only if
    remaining text is longer this value.

    :param str text: initial text
    :param integer length: maximum length of resulting text
    :param integer maxlen: if > 0, *text* is shortened only if remaining text is longer than max

    >>> from pyams_utils.text import get_text_start

    Setting text length higher than original text size returns original string:

    >>> get_text_start('This is a long string', 30)
    'This is a long string'

    Otherwise, text is truncated:

    >>> get_text_start('This is a long string', 10)
    'This is a&#133;'
    >>> get_text_start('This is a long string', 20)
    'This is a long&#133;'
    >>> get_text_start('This is a long string', 20, 7)
    'This is a long string'
    """
    result = text or ''
    if length > len(result):
        return result
    index = length - 1
    text_length = len(result)
    while index > 0 and result[index] != ' ':
        index -= 1

    if index > 0 and text_length > index + maxlen:
        return result[:index] + '&#133;'
    return text


@adapter_config(name='truncate', context=(Interface, Interface, Interface), provides=ITALESExtension)
class TruncateCharsTalesExtension(ContextRequestViewAdapter):
    """TruncateCharsTalesExtension"""

    @staticmethod
    def render(value, length=50, maxlen=0):
        """Render TALES extension;
        see :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if not value:
            return ''
        return get_text_start(value, length, maxlen=maxlen)


@adapter_config(name='raw', context=(str, IRequest), provides=IHTMLRenderer)
class BaseHTMLRenderer(ContextRequestAdapter):
    """BaseHTMLRenderer"""

    def render(self, **kwargs):
        """Convert raw code as HTML"""
        return self.context


@adapter_config(name='text', context=(str, IRequest), provides=IHTMLRenderer)
class TextRenderer(BaseHTMLRenderer):
    """TextRenderer"""
    label = _('Simple text')

    def render(self, **kwargs):
        return html.escape(self.context).replace('\n', '<br />\n')


@adapter_config(name='js', context=(str, IRequest), provides=IHTMLRenderer)
class JsRenderer(BaseHTMLRenderer):
    """JsRenderer"""

    def render(self, **kwargs):
        return self.context.replace("'", "\\'")


@adapter_config(name='rest', context=(str, IRequest), provides=IHTMLRenderer)
class ReStructuredTextRenderer(BaseHTMLRenderer):
    """ReStructuredTextRenderer"""
    label = _('ReStructured text')

    def render(self, **kwargs):
        """Render reStructuredText to HTML"""
        overrides = {'halt_level': 6, 
         'input_encoding': 'unicode', 
         'output_encoding': 'unicode', 
         'initial_header_level': 3}
        if 'settings' in kwargs:
            overrides.update(kwargs['settings'])
        parts = docutils.core.publish_parts(self.context, writer_name='html', settings_overrides=overrides)
        return ''.join((parts['body_pre_docinfo'], parts['docinfo'], parts['body']))


@adapter_config(name='markdown', context=(str, IRequest), provides=IHTMLRenderer)
class MarkdownTextRenderer(BaseHTMLRenderer):
    """MarkdownTextRenderer"""
    label = _('Markdown text')

    def render(self, **kwargs):
        """Render Markdown code to HTML"""
        return markdown(self.context)


def text_to_html(text, renderer='text'):
    """Convert text to HTML using the given renderer

    Renderer name can be any registered HTML renderer adapter.

    You can provide several renderers by giving their names separated by semicolon; renderers
    will then act as in a pipe, each renderer transforming output of the previous one.
    """
    request = check_request()
    registry = request.registry
    for renderer_name in renderer.split(';'):
        renderer = registry.queryMultiAdapter((text, request), IHTMLRenderer, name=renderer_name)
        if renderer is not None:
            text = renderer.render() or text

    return text


EMPTY_MARKER = object()

@adapter_config(name='html', context=(Interface, Interface, Interface), provides=ITALESExtension)
class HTMLTalesExtension(ContextRequestViewAdapter):
    """HTMLTalesExtension"""

    def render(self, context=EMPTY_MARKER, renderer='text'):
        """Render TALES extension;
        see :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if context is EMPTY_MARKER:
            context = self.context
        if not context:
            return ''
        registry = self.request.registry
        adapter = registry.queryMultiAdapter((context, self.request, self.view), IHTMLRenderer)
        if adapter is None:
            adapter = registry.queryMultiAdapter((context, self.request), IHTMLRenderer)
        if adapter is not None:
            return adapter.render()
        if isinstance(context, str):
            return text_to_html(context, renderer)
        return str(context)


PYAMS_HTML_RENDERERS_VOCABULARY = 'PyAMS HTML renderers'

@vocabulary_config(name=PYAMS_HTML_RENDERERS_VOCABULARY)
class RenderersVocabulary(SimpleVocabulary):
    """RenderersVocabulary"""

    def __init__(self, context=None):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        terms = []
        append = terms.append
        for name, adapter in registry.getAdapters(('', request), IHTMLRenderer):
            if hasattr(adapter, 'label'):
                append(SimpleTerm(name, title=translate(adapter.label)))

        super(RenderersVocabulary, self).__init__(terms)


@adapter_config(name='br', context=(Interface, Interface, Interface), provides=ITALESExtension)
class BrTalesExtension(ContextRequestViewAdapter):
    """BrTalesExtension"""

    @staticmethod
    def render(value, css_class='', character='|', start_tag=None, end_tag=None):
        """Render TALES extension;
        see :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if not value:
            return ''
        br_tag = '<br {0} />'.format('class="{0}"'.format(css_class) if css_class else '')
        elements = value.split(character)
        if start_tag:
            elements[0] = '<{0}>{1}</{0}>'.format(start_tag, elements[0])
        if end_tag:
            elements[-1] = '<{0}>{1}</{0}>'.format(end_tag, elements[(-1)])
        return br_tag.join(elements)