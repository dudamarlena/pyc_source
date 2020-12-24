# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/markdown_utils.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import warnings, pymdownx.emoji
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.html import escape
from djblets import markdown as djblets_markdown
from djblets.siteconfig.models import SiteConfiguration
from markdown import markdown
from reviewboard.deprecation import RemovedInReviewBoard40Warning
MARKDOWN_KWARGS = {b'enable_attributes': False, 
   b'output_format': b'xhtml1', 
   b'lazy_ol': False, 
   b'extensions': [
                 b'markdown.extensions.fenced_code',
                 b'markdown.extensions.codehilite',
                 b'markdown.extensions.sane_lists',
                 b'markdown.extensions.smart_strong',
                 b'markdown.extensions.tables',
                 b'markdown.extensions.nl2br',
                 b'pymdownx.tilde',
                 b'pymdownx.emoji',
                 b'djblets.markdown.extensions.escape_html',
                 b'djblets.markdown.extensions.wysiwyg'], 
   b'extension_configs': {b'markdown.extensions.codehilite': {b'guess_lang': False}, 
                          b'pymdownx.emoji': {b'emoji_index': pymdownx.emoji.gemoji, 
                                              b'options': {b'classes': b'emoji', 
                                                           b'image_path': b'https://github.githubassets.com/images/icons/emoji/unicode/', 
                                                           b'non_standard_image_path': b'https://github.githubassets.com/images/icons/emoji/'}}}}

def markdown_escape(text):
    """Escapes text for use in Markdown.

    This will escape the provided text so that none of the characters will
    be rendered specially by Markdown.

    This is deprecated. Please use djblets.markdown.markdown_escape instead.
    """
    warnings.warn(b'reviewboard.reviews.markdown_utils.markdown_escape is deprecated. Please use djblets.markdown.markdown_escape.', RemovedInReviewBoard40Warning)
    return djblets_markdown.markdown_escape(text)


def markdown_unescape(escaped_text):
    """Unescapes Markdown-escaped text.

    This will unescape the provided Markdown-formatted text so that any
    escaped characters will be unescaped.

    This is deprecated. Please use djblets.markdown.markdown_unescape instead.
    """
    warnings.warn(b'reviewboard.reviews.markdown_utils.markdown_unescape is deprecated. Please use djblets.markdown.markdown_unescape.', RemovedInReviewBoard40Warning)
    return djblets_markdown.markdown_unescape(escaped_text)


def markdown_escape_field(obj, field_name):
    """Escapes Markdown text in a model or dictionary's field.

    This is a convenience around markdown_escape to escape the contents of
    a particular field in a model or dictionary.
    """
    if isinstance(obj, Model):
        setattr(obj, field_name, djblets_markdown.markdown_escape(getattr(obj, field_name)))
    elif isinstance(obj, dict):
        obj[field_name] = djblets_markdown.markdown_escape(obj[field_name])
    else:
        raise TypeError(b'Unexpected type %r passed to markdown_escape_field' % obj)


def markdown_unescape_field(obj, field_name):
    """Unescapes Markdown text in a model or dictionary's field.

    This is a convenience around markdown_unescape to unescape the contents of
    a particular field in a model or dictionary.
    """
    if isinstance(obj, Model):
        setattr(obj, field_name, markdown_unescape(getattr(obj, field_name)))
    elif isinstance(obj, dict):
        obj[field_name] = markdown_unescape(obj[field_name])
    else:
        raise TypeError(b'Unexpected type %r passed to markdown_unescape_field' % obj)


def normalize_text_for_edit(user, text, rich_text, escape_html=True):
    """Normalizes text, converting it for editing.

    This will normalize text for editing based on the rich_text flag and
    the user settings.

    If the text is not in Markdown and the user edits in Markdown by default,
    this will return the text escaped for edit. Otherwise, the text is
    returned as-is.
    """
    if text is None:
        return b''
    else:
        if not rich_text and is_rich_text_default_for_user(user):
            text = djblets_markdown.markdown_escape(text)
        if escape_html:
            text = escape(text)
        return text


def markdown_render_conditional(text, rich_text):
    """Return the escaped HTML content based on the rich_text flag."""
    if rich_text:
        return render_markdown(text)
    else:
        return escape(text)


def is_rich_text_default_for_user(user):
    """Returns whether the user edits in Markdown by default."""
    if user.is_authenticated():
        try:
            return user.get_profile().should_use_rich_text
        except ObjectDoesNotExist:
            pass

    siteconfig = SiteConfiguration.objects.get_current()
    return siteconfig.get(b'default_use_rich_text')


def markdown_set_field_escaped(obj, field, escaped):
    """Escapes or unescapes the specified field in a model or dictionary."""
    if escaped:
        markdown_escape_field(obj, field)
    else:
        markdown_unescape_field(obj, field)


def iter_markdown_lines(markdown_html):
    """Iterates over lines of Markdown, normalizing for individual display.

    Generated Markdown HTML cannot by itself be handled on a per-line-basis.
    Code blocks, for example, will consist of multiple lines of content
    contained within a <pre> tag. Likewise, lists will be a bunch of
    <li> tags inside a <ul> tag, and individually do not form valid lists.

    This function iterates through the Markdown tree and generates
    self-contained lines of HTML that can be rendered individually.

    This is deprecated. Please use djblets.markdown.iter_markdown_lines
    instead.
    """
    warnings.warn(b'reviewboard.reviews.markdown_utils.iter_markdown_lines is deprecated. Please use djblets.markdown.iter_markdown_lines.', RemovedInReviewBoard40Warning)
    return djblets_markdown.iter_markdown_lines(markdown_html)


def get_markdown_element_tree(markdown_html):
    """Returns an XML element tree for Markdown-generated HTML.

    This will build the tree and return all nodes representing the rendered
    Markdown content.

    This is deprecated. Please use djblets.markdown.get_markdown_element_tree
    instead.
    """
    warnings.warn(b'reviewboard.reviews.markdown_utils.get_markdown_element_tree is deprecated. Please use djblets.markdown.get_markdown_element_tree.', RemovedInReviewBoard40Warning)
    return djblets_markdown.get_markdown_element_tree(markdown_html)


def sanitize_illegal_chars_for_xml(s):
    """Sanitize a string, removing characters illegal in XML.

    This will remove a number of characters that would break the  XML parser.
    They may be in the string due to a copy/paste.

    This code is courtesy of the XmlRpcPlugin developers, as documented
    here: http://stackoverflow.com/a/22273639

    This is deprecated. Please use
    djblets.markdown.sanitize_illegal_chars_for_xml instead.
    """
    warnings.warn(b'reviewboard.reviews.markdown_utils.sanitize_illegal_chars_for_xml is deprecated. Please use djblets.markdown.sanitize_illegal_chars_for_xml.', RemovedInReviewBoard40Warning)
    return djblets_markdown.sanitize_illegal_chars_for_xml(s)


def render_markdown(text):
    """Renders Markdown text to HTML.

    The Markdown text will be sanitized to prevent injecting custom HTML.
    It will also enable a few plugins for code highlighting and sane lists.
    """
    if isinstance(text, bytes):
        text = text.decode(b'utf-8')
    return markdown(text, **MARKDOWN_KWARGS)


def render_markdown_from_file(f):
    """Renders Markdown text to HTML.

    The Markdown text will be sanitized to prevent injecting custom HTML.
    It will also enable a few plugins for code highlighting and sane lists.
    """
    return djblets_markdown.render_markdown_from_file(f, **MARKDOWN_KWARGS)