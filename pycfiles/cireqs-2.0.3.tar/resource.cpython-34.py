# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cirdan/resource.py
# Compiled at: 2015-07-07 15:30:35
# Size of source mod 2**32: 1207 bytes
from __future__ import absolute_import
import cirdan, copy, jinja2
from cirdan.registry import registry
from contextlib import closing

class DocsResource:

    def __init__(self, api):
        self.api = api
        self.body = None

    def build(self):
        with closing(open(cirdan.template_path, 'r')) as (f):
            t = jinja2.Template(f.read())
            payload = {'name': 'Docs', 
             'intro_text': '', 
             'resources': copy.deepcopy(registry.api_to_resources[self.api])}
            if self.api in registry.api_meta:
                for key, value in registry.api_meta[self.api].items():
                    payload[key] = value

            payload['resources'] = [resource for resource in payload['resources'] if not resource.secret]
            for resource in payload['resources']:
                resource.methods = [method for method in resource.methods if not method.secret]

            self.body = t.render(payload)

    def on_get(self, req, resp):
        if self.body is None or not cirdan.cache_template:
            self.build()
        resp.content_type = 'text/html'
        resp.body = self.body