# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/urls.py
# Compiled at: 2017-11-02 04:35:21
# Size of source mod 2**32: 1935 bytes
from django.conf.urls import url
from moneta.views import public_check, index, check, add_element, add_element_post, add_element_signature, get_signature, modify_repository, delete_repository, delete_element, search_package, compare_states, private_check, test_upload, get_file_p, get_checksum_p, get_signature_p, get_file, get_checksum, show_file
__author__ = 'flanker'
urlpatterns = [
 url('^p/$', public_check, name='public_check'),
 url('^p/get/(?P<eid>\\d+)/(?P<name>.*)$', get_file_p, name='get_file_p'),
 url('^p/check/(?P<eid>\\d+)/(?P<value>sha1|sha256|md5)$', get_checksum_p, name='get_checksum_p'),
 url('^p/signature/(?P<eid>\\d+)/(?P<sid>\\d+)/$', get_signature_p, name='get_signature_p'),
 url('^a/get/(?P<eid>\\d+)/(?P<name>.*)$', get_file, name='get_file'),
 url('^a/check/(?P<eid>\\d+)/(?P<value>sha1|sha256|md5)$', get_checksum, name='get_checksum'),
 url('^a/file/(?P<eid>\\d+)/$', show_file, name='show_file'),
 url('^a/add_package/(?P<rid>\\d+)/$', add_element, name='add_element'),
 url('^a/post/(?P<rid>\\d+)/$', add_element_post, name='add_element_post'),
 url('^a/sign/(?P<rid>\\d+)/$', add_element_signature, name='add_element_signature'),
 url('^a/signature/(?P<eid>\\d+)/(?P<sid>\\d+)/$', get_signature, name='get_signature'),
 url('^a/modify/(?P<rid>\\d+)/$', modify_repository, name='modify_repository'),
 url('^a/delete/(?P<rid>\\d+)/$', delete_repository, name='delete_repository'),
 url('^a/delete/(?P<rid>\\d+)/(?P<eid>\\d+)/$', delete_element, name='delete_element'),
 url('^a/search/(?P<rid>\\d+)/$', search_package, name='search_package'),
 url('^a/compare/(?P<rid>\\d+)/$', compare_states, name='compare_states'),
 url('^a/index/$', index, name='index'),
 url('^a/$', private_check, name='private_check'),
 url('^a/check/$', check, name='check'),
 url('^test/$', test_upload, name='test_upload')]
app_name = 'moneta'