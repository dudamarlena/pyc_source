# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_ajax_resp/django_ajax_resp.py
# Compiled at: 2014-10-17 05:01:22
"""
Created on Jun 14, 2012

@author: teo
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson

class ResponseItem:

    def __init__(self, target='', action='', message_type='html', template='', render_values={}, js_class='', js_class_action='create'):
        self.target = target
        self.action = action
        self.message_type = message_type
        self.template = template
        self.render_values = render_values
        self.js_class = js_class
        self.js_class_action = js_class_action

    def get_response_item(self, request):
        responseItem = {}
        responseItem['target'] = self.target
        responseItem['action'] = self.action
        responseItem['type'] = self.message_type
        if self.message_type.upper() == 'HTML':
            responseItem['data'] = str(render_to_response(self.template, self.render_values, context_instance=RequestContext(request)))
        elif self.message_type.upper() == 'JAVASCRIPT':
            responseItem['data'] = self.render_values
        else:
            responseItem['data'] = self.render_values
        responseItem['js_class'] = self.js_class
        responseItem['js_class_action'] = self.js_class_action
        return responseItem


class ResponseArray:

    def __init__(self):
        self.response_array = []

    def append(self, to_append):
        self.response_array.append(to_append)

    def generate_response(self, request):
        """SEE ALSO: Django function json_response(x), implementation:
        def json_response(x):
        import json
        return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                            content_type='application/json; charset=UTF-8')
        """
        out_array = []
        for resp_item in self.response_array:
            out_array.append(resp_item.get_response_item(request))

        return HttpResponse(simplejson.dumps(out_array), mimetype='application/json')