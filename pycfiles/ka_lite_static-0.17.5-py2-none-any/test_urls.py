# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/tests/test_urls.py
# Compiled at: 2018-07-11 18:15:31
import sys
from copy import copy
from django.conf.urls import include, patterns, url
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]


else:

    def u(x):
        return x


def dummy_view(*args, **kwargs):
    pass


basic_patterns = patterns('', url('^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'), url('^test_no_url_args/$', dummy_view, name='test_no_url_args'), url('^test_one_url_args/(?P<arg_one>[-\\w]+)/$', dummy_view, name='test_one_url_args'), url('^test_two_url_args/(?P<arg_one>[-\\w]+)-(?P<arg_two>[-\\w]+)/$', dummy_view, name='test_two_url_args'), url('^test_optional_url_arg/(?:1_(?P<arg_one>[-\\w]+)-)?2_(?P<arg_two>[-\\w]+)/$', dummy_view, name='test_optional_url_arg'), url('^test_unicode_url_name/$', dummy_view, name=u('test_unicode_url_name')), url('^test_duplicate_name/(?P<arg_one>[-\\w]+)/$', dummy_view, name='test_duplicate_name'), url('^test_duplicate_name/(?P<arg_one>[-\\w]+)-(?P<arg_two>[-\\w]+)/$', dummy_view, name='test_duplicate_name'))
urlpatterns = copy(basic_patterns)
urlexclude = patterns('', url('^test_exclude_namespace/$', dummy_view, name='test_exclude_namespace_url1'))
pattern_ns_1 = patterns('', url('', include(basic_patterns)))
pattern_ns_2 = patterns('', url('', include(basic_patterns)))
pattern_ns_arg = patterns('', url('', include(basic_patterns)))
pattern_nested_ns = patterns('', url('^ns1/', include(pattern_ns_1, namespace='ns1')))
urlpatterns += patterns('', url('^ns1/', include(pattern_ns_1, namespace='ns1')), url('^ns2/', include(pattern_ns_2, namespace='ns2')), url('^ns_ex/', include(urlexclude, namespace='exclude_namespace')), url('^ns(?P<ns_arg>[^/]*)/', include(pattern_ns_arg, namespace='ns_arg')), url('^nestedns/', include(pattern_nested_ns, namespace='nestedns')))