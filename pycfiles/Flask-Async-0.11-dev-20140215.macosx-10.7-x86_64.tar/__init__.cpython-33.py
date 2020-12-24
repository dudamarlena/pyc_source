# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/__init__.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 7210 bytes
"""
    werkzeug
    ~~~~~~~~

    Werkzeug is the Swiss Army knife of Python web development.

    It provides useful classes and functions for any WSGI application to make
    the life of a python web developer much easier.  All of the provided
    classes are independent from each other so you can mix it with any other
    library.

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from types import ModuleType
import sys
from werkzeug._compat import iteritems
__version__ = '0.9.4'
all_by_module = {'werkzeug.debug': [
                    'DebuggedApplication'], 
 'werkzeug.local': [
                    'Local', 'LocalManager', 'LocalProxy',
                    'LocalStack', 'release_local'], 
 'werkzeug.serving': [
                      'run_simple'], 
 'werkzeug.test': [
                   'Client', 'EnvironBuilder', 'create_environ',
                   'run_wsgi_app'], 
 'werkzeug.testapp': [
                      'test_app'], 
 'werkzeug.exceptions': [
                         'abort', 'Aborter'], 
 'werkzeug.urls': [
                   'url_decode', 'url_encode', 'url_quote',
                   'url_quote_plus', 'url_unquote',
                   'url_unquote_plus', 'url_fix', 'Href',
                   'iri_to_uri', 'uri_to_iri'], 
 'werkzeug.formparser': [
                         'parse_form_data'], 
 'werkzeug.utils': [
                    'escape', 'environ_property',
                    'append_slash_redirect', 'redirect',
                    'cached_property', 'import_string',
                    'dump_cookie', 'parse_cookie', 'unescape',
                    'format_string', 'find_modules', 'header_property',
                    'html', 'xhtml', 'HTMLBuilder',
                    'validate_arguments', 'ArgumentValidationError',
                    'bind_arguments', 'secure_filename'], 
 'werkzeug.wsgi': [
                   'get_current_url', 'get_host', 'pop_path_info',
                   'peek_path_info', 'SharedDataMiddleware',
                   'DispatcherMiddleware', 'ClosingIterator',
                   'FileWrapper', 'make_line_iter', 'LimitedStream',
                   'responder', 'wrap_file', 'extract_path_info'], 
 'werkzeug.datastructures': [
                             'MultiDict', 'CombinedMultiDict', 'Headers',
                             'EnvironHeaders', 'ImmutableList',
                             'ImmutableDict', 'ImmutableMultiDict',
                             'TypeConversionDict', 'ImmutableTypeConversionDict',
                             'Accept', 'MIMEAccept', 'CharsetAccept',
                             'LanguageAccept', 'RequestCacheControl',
                             'ResponseCacheControl', 'ETags', 'HeaderSet',
                             'WWWAuthenticate', 'Authorization',
                             'FileMultiDict', 'CallbackDict', 'FileStorage',
                             'OrderedMultiDict', 'ImmutableOrderedMultiDict'], 
 'werkzeug.useragents': [
                         'UserAgent'], 
 'werkzeug.http': [
                   'parse_etags', 'parse_date', 'http_date',
                   'cookie_date', 'parse_cache_control_header',
                   'is_resource_modified', 'parse_accept_header',
                   'parse_set_header', 'quote_etag', 'unquote_etag',
                   'generate_etag', 'dump_header',
                   'parse_list_header', 'parse_dict_header',
                   'parse_authorization_header',
                   'parse_www_authenticate_header',
                   'remove_entity_headers', 'is_entity_header',
                   'remove_hop_by_hop_headers', 'parse_options_header',
                   'dump_options_header', 'is_hop_by_hop_header',
                   'unquote_header_value',
                   'quote_header_value', 'HTTP_STATUS_CODES'], 
 'werkzeug.wrappers': [
                       'BaseResponse', 'BaseRequest', 'Request',
                       'Response', 'AcceptMixin', 'ETagRequestMixin',
                       'ETagResponseMixin', 'ResponseStreamMixin',
                       'CommonResponseDescriptorsMixin',
                       'UserAgentMixin', 'AuthorizationMixin',
                       'WWWAuthenticateMixin',
                       'CommonRequestDescriptorsMixin'], 
 'werkzeug.security': [
                       'generate_password_hash', 'check_password_hash'], 
 'werkzeug._internal': [
                        '_easteregg']}
attribute_modules = frozenset(['exceptions', 'routing', 'script'])
object_origins = {}
for module, items in iteritems(all_by_module):
    for item in items:
        object_origins[item] = module

class module(ModuleType):
    __doc__ = 'Automatically import objects from the modules.'

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))

            return getattr(module, name)
        else:
            if name in attribute_modules:
                __import__('werkzeug.' + name)
            return ModuleType.__getattribute__(self, name)

    def __dir__(self):
        """Just show what we want to show."""
        result = list(new_module.__all__)
        result.extend(('__file__', '__path__', '__doc__', '__all__', '__docformat__',
                       '__name__', '__path__', '__package__', '__version__'))
        return result


old_module = sys.modules['werkzeug']
new_module = sys.modules['werkzeug'] = module('werkzeug')
new_module.__dict__.update({'__file__': __file__, 
 '__package__': 'werkzeug', 
 '__path__': __path__, 
 '__doc__': __doc__, 
 '__version__': __version__, 
 '__all__': tuple(object_origins) + tuple(attribute_modules), 
 '__docformat__': 'restructuredtext en'})
__import__('werkzeug.exceptions')