# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/databrowse/plugins/objects.py
# Compiled at: 2018-07-11 18:15:30
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django import http
from django.contrib.databrowse.datastructures import EasyModel
from django.contrib.databrowse.sites import DatabrowsePlugin
from django.shortcuts import render_to_response

class ObjectDetailPlugin(DatabrowsePlugin):

    def model_view(self, request, model_databrowse, url):
        if url is None:
            return http.HttpResponseRedirect(urljoin(request.path, '../'))
        else:
            easy_model = EasyModel(model_databrowse.site, model_databrowse.model)
            obj = easy_model.object_by_pk(url)
            return render_to_response('databrowse/object_detail.html', {'object': obj, 'root_url': model_databrowse.site.root_url})