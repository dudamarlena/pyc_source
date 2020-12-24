# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/databrowse/sites.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django import http
from django.db import models
from django.contrib.databrowse.datastructures import EasyModel
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class DatabrowsePlugin(object):

    def urls(self, plugin_name, easy_instance_field):
        """
        Given an EasyInstanceField object, returns a list of URLs for this
        plugin's views of this object. These URLs should be absolute.

        Returns None if the EasyInstanceField object doesn't get a
        list of plugin-specific URLs.
        """
        return

    def model_index_html(self, request, model, site):
        """
        Returns a snippet of HTML to include on the model index page.
        """
        return b''

    def model_view(self, request, model_databrowse, url):
        """
        Handles main URL routing for a plugin's model-specific pages.
        """
        raise NotImplementedError


class ModelDatabrowse(object):
    plugins = {}

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'objects/3'.
        """
        if url is None:
            return self.main_view(request)
        else:
            try:
                plugin_name, rest_of_url = url.split(b'/', 1)
            except ValueError:
                plugin_name, rest_of_url = url, None

            try:
                plugin = self.plugins[plugin_name]
            except KeyError:
                raise http.Http404(b'A plugin with the requested name does not exist.')

            return plugin.model_view(request, self, rest_of_url)

    def main_view(self, request):
        easy_model = EasyModel(self.site, self.model)
        html_snippets = mark_safe((b'\n').join([ p.model_index_html(request, self.model, self.site) for p in self.plugins.values() ]))
        return render_to_response(b'databrowse/model_detail.html', {b'model': easy_model, 
           b'root_url': self.site.root_url, 
           b'plugin_html': html_snippets})


class DatabrowseSite(object):

    def __init__(self):
        self.registry = {}
        self.root_url = None
        return

    def register(self, *model_list, **options):
        """
        Registers the given model(s) with the given databrowse site.

        The model(s) should be Model classes, not instances.

        If a databrowse class isn't given, it will use DefaultModelDatabrowse
        (the default databrowse options).

        If a model is already registered, this will raise AlreadyRegistered.
        """
        databrowse_class = options.pop(b'databrowse_class', DefaultModelDatabrowse)
        for model in model_list:
            if model in self.registry:
                raise AlreadyRegistered(b'The model %s is already registered' % model.__name__)
            self.registry[model] = databrowse_class

    def unregister(self, *model_list):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        for model in model_list:
            if model not in self.registry:
                raise NotRegistered(b'The model %s is not registered' % model.__name__)
            del self.registry[model]

    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'comments/comment/'.
        """
        self.root_url = request.path[:len(request.path) - len(url)]
        url = url.rstrip(b'/')
        if url == b'':
            return self.index(request)
        if b'/' in url:
            return self.model_page(request, *url.split(b'/', 2))
        raise http.Http404(b'The requested databrowse page does not exist.')

    def index(self, request):
        m_list = [ EasyModel(self, m) for m in self.registry.keys() ]
        return render_to_response(b'databrowse/homepage.html', {b'model_list': m_list, b'root_url': self.root_url})

    def model_page(self, request, app_label, model_name, rest_of_url=None):
        """
        Handles the model-specific functionality of the databrowse site, delegating
        to the appropriate ModelDatabrowse class.
        """
        model = models.get_model(app_label, model_name)
        if model is None:
            raise http.Http404(b'App %r, model %r, not found.' % (app_label, model_name))
        try:
            databrowse_class = self.registry[model]
        except KeyError:
            raise http.Http404(b'This model exists but has not been registered with databrowse.')

        return databrowse_class(model, self).root(request, rest_of_url)


site = DatabrowseSite()
from django.contrib.databrowse.plugins.calendars import CalendarPlugin
from django.contrib.databrowse.plugins.objects import ObjectDetailPlugin
from django.contrib.databrowse.plugins.fieldchoices import FieldChoicePlugin

class DefaultModelDatabrowse(ModelDatabrowse):
    plugins = {b'objects': ObjectDetailPlugin(), b'calendars': CalendarPlugin(), b'fields': FieldChoicePlugin()}