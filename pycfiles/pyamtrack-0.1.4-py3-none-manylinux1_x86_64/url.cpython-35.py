# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/url.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 8538 bytes
__doc__ = 'PyAMS_utils.url module\n\nThis module provides several functions, adapters and TALES extensions which can be used to\ngenerate object\'s URLs.\n\nThree kinds of URLs can be used:\n - an absolute URL, which is the standard way to access an object via it\'s physical path\n - a canonical URL; this URL is the "preferred" one used to access an object, and is typically\n   used by search engines to index contents\n - a relative URL; some contents can use this kind of URL to get access to an object from another\n   context.\n'
from pyramid.encode import url_quote, urlencode
from pyramid.url import QUERY_SAFE, resource_url
from zope.interface import Interface
from pyams_utils.adapter import ContextRequestAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.interfaces.url import ICanonicalURL, IRelativeURL
from pyams_utils.unicode import translate_string
__docformat__ = 'restructuredtext'

def generate_url(title, min_word_length=2):
    """Generate an SEO-friendly content URL from it's title

    The original title is translated to remove accents, converted to lowercase, and words
    shorter than three characters (by default) are removed; terms are joined by hyphens.

    :param title: the input text
    :param min_word_length: minimum length of words to keep

    >>> from pyams_utils.url import generate_url
    >>> generate_url('This is my test')
    'this-is-my-test'

    Single letters are removed from generated URLs:

    >>> generate_url('This word has a single a')
    'this-word-has-single'

    But you can define the minimum length of word:

    >>> generate_url('This word has a single a', min_word_length=4)
    'this-word-single'

    If input text contains slashes, they are replaced with hyphens:

    >>> generate_url('This string contains/slash')
    'this-string-contains-slash'

    Punctation and special characters are completely removed:

    >>> generate_url('This is a string with a point. And why not?')
    'this-is-string-with-point-and-why-not'
    """
    return '-'.join(filter(lambda x: len(x) >= min_word_length, translate_string(title.replace('/', '-'), escape_slashes=False, force_lower=True, spaces='-', remove_punctuation=True, keep_chars='-').split('-')))


def get_display_context(request):
    """Get current display context

    The display context can be used when we generate a page to display an object in the context
    of another one; PyAMS_content package is using this feature to display "shared" contents as
    is they were located inside another site or folder...
    """
    return request.annotations.get(DISPLAY_CONTEXT_KEY_NAME, request.context)


def absolute_url(context, request, view_name=None, query=None):
    """Get resource absolute_url

    :param object context: the persistent object for which absolute URL is required
    :param request: the request on which URL is based
    :param str view_name: an optional view name to add to URL
    :param str/dict query: an optional URL arguments string or mapping

    This absolute URL function is based on default Pyramid's :py:func:`resource_url` function, but
    add checks to remove some double slashes, and add control on view name when it begins with a '#'
    character which is used by MyAMS.js framework.
    """
    if isinstance(context, str):
        return context
    result = resource_url(context, request).replace('//', '/').replace(':/', '://')
    if result.endswith('/'):
        result = result[:-1]
    if view_name:
        if view_name.startswith('#'):
            result += view_name
        else:
            result += '/' + view_name
        if query:
            qstr = ''
            if isinstance(query, str):
                qstr = '?' + url_quote(query, QUERY_SAFE)
    else:
        if query:
            qstr = '?' + urlencode(query, doseq=True)
        result += qstr
    return result


@adapter_config(name='absolute_url', context=(Interface, Interface, Interface), provides=ITALESExtension)
class AbsoluteUrlTalesExtension(ContextRequestViewAdapter):
    """AbsoluteUrlTalesExtension"""

    def render(self, context=None, view_name=None):
        """Extension rendering; see
        :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if context is None:
            context = self.context
        return absolute_url(context, self.request, view_name)


def canonical_url(context, request, view_name=None, query=None):
    """Get resource canonical URL

    We look for an :py:class:`ICanonicalURL <pyams_utils.interfaces.url.ICanonicalURL>` adapter;
    if none is found, we use the absolute_url.
    """
    if isinstance(context, str):
        return context
    url_adapter = request.registry.queryMultiAdapter((context, request), ICanonicalURL)
    if url_adapter is None:
        url_adapter = request.registry.queryAdapter(context, ICanonicalURL)
    if url_adapter is not None:
        return url_adapter.get_url(view_name, query)
    return absolute_url(context, request, view_name, query)


@adapter_config(name='canonical_url', context=(Interface, Interface, Interface), provides=ITALESExtension)
class CanonicalUrlTalesExtension(ContextRequestViewAdapter):
    """CanonicalUrlTalesExtension"""

    def render(self, context=None, view_name=None):
        """Render TALES extension; see
        :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if context is None:
            context = self.context
        return canonical_url(context, self.request, view_name)


@adapter_config(context=(Interface, Interface), provides=IRelativeURL)
class DefaultRelativeURLAdapter(ContextRequestAdapter):
    """DefaultRelativeURLAdapter"""

    def get_url(self, display_context=None, view_name=None, query=None):
        """Default adapter returns absolute URL"""
        return absolute_url(self.context, self.request, view_name, query)


def relative_url(context, request, display_context=None, view_name=None, query=None):
    """Get resource URL relative to given context"""
    if display_context is None:
        display_context = request.annotations.get(DISPLAY_CONTEXT_KEY_NAME, request.context)
    adapter = request.registry.getMultiAdapter((context, request), IRelativeURL)
    return adapter.get_url(display_context, view_name, query)


@adapter_config(name='relative_url', context=(Interface, Interface, Interface), provides=ITALESExtension)
class RelativeUrlTalesExtension(ContextRequestViewAdapter):
    """RelativeUrlTalesExtension"""

    def render(self, context=None, view_name=None, query=None):
        """Rander TALES extension;
        see :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        """
        if context is None:
            context = self.context
        return relative_url(context, self.request, view_name=view_name, query=query)