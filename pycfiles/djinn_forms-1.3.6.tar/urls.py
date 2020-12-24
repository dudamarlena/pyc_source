# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/urls.py
# Compiled at: 2014-12-08 04:48:47
from django.conf.urls import url, patterns
from pgsearch.views import ModalSearchView
from pgsearch.forms import PGSearchForm, DocumentFilterSearchForm
from djinn_forms.views.fileupload import UploadView
from djinn_forms.views.relate import RelateSearch
from djinn_forms.views.keywords import Keywords
from djinn_forms.views.contentimages import ContentImages
from django.views.decorators.csrf import csrf_exempt
urlpatterns = patterns('', url('^fileupload$', csrf_exempt(UploadView.as_view()), name='djinn_forms_fileupload'), url('^searchrelate$', RelateSearch.as_view(), name='djinn_forms_relatesearch'), url('^contentimages/(?P<ctype>[\\w]+)/(?P<pk>[\\d]+)$', ContentImages.as_view(), name='djinn_forms_contentimages'), url('^contentlinks/', ModalSearchView(load_all=False, form_class=PGSearchForm, template='djinn_forms/snippets/contentlinks.html'), name='haystack_link_popup'), url('^document_search/', ModalSearchView(load_all=False, form_class=DocumentFilterSearchForm, template='djinn_forms/snippets/documentsearch.html'), name='djinn_forms_relate_popup'), url('^content_search/', ModalSearchView(load_all=False, form_class=PGSearchForm, template='djinn_forms/snippets/contentsearch.html'), name='djinn_forms_relate_popup'), url('^contentlinks_search/', ModalSearchView(load_all=False, form_class=PGSearchForm), name='haystack_link_search'), url('^keywords/?$', Keywords.as_view(), name='djinn_forms_keywords'))