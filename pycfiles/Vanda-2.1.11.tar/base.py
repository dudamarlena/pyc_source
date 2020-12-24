# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/dashboard/widgets/base.py
# Compiled at: 2013-01-07 03:52:15
import json
from django.template.loader import get_template
from django.template import Template, Context
from django.conf.urls import patterns, url
from django.http import HttpResponse

class Widget(object):
    """
    Base class for all widgets.
    """
    title = ''
    name = ''
    display = True
    template = None
    html = ''
    dashboard = None
    _request = None

    @property
    def url_patterns(self):
        return []

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        url_patterns = self.url_patterns
        url_patterns.extend([
         url('^$', self.widget_html)])
        urlpatterns = patterns('', *url_patterns)
        return urlpatterns

    def set_dashboard_instance(self, dashboard):
        self.dashboard = dashboard

    def get_html(self):
        if self.template:
            return get_template(self.template)
        else:
            if self.html:
                return Template(self.html)
            return Template()

    def render(self):
        """
        Render the widget html code using widgets htmls.
        """
        html = self.get_html()
        return html.render(Context({'self': self}))

    def from_json(self, jsonstr):
        self.from_dict(json.loads(jsonstr))

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'title': self.title, 'name': self.name, 
           'display': self.display}

    def from_dict(self, dict_):
        for i in dict_:
            setattr(self, i, dict_[i])

    def get_element_id(self):
        if hasattr(self, 'css_id'):
            if self.css_id:
                return self.css_id
        return 'id_%s' % self.name

    def widget_html(self, request):
        self._request = request
        html = self.get_html()
        return HttpResponse(html.render(Context({'self': self})))

    @property
    def request(self):
        if self._request:
            return self._request
        if self.dashboard:
            return self.dashboard.request

    @classmethod
    def load(cls, data):
        obj = cls().from_json(data)
        return obj