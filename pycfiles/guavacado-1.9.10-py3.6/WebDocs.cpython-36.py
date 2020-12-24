# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/WebDocs.py
# Compiled at: 2019-06-30 15:56:26
# Size of source mod 2**32: 2092 bytes
from .WebInterface import WebInterface
from .misc import generate_redirect_page
import json

class WebDocs(object):
    __doc__ = 'provides a documentation page for the web server, showing all functions available and their URLs'

    def __init__(self, host, dispatcher_level=None):
        self.host = host
        self.web_interface = WebInterface(host=(self.host), dispatcher_level=dispatcher_level)
        self.resource_list = []

    def connect_funcs(self):
        self.web_interface.connect('/docs/', self.GET_DOCS, 'GET')
        self.web_interface.connect('/docs/json/', self.GET_DOCS_JSON, 'GET')

    def log_connection(self, resource, action, method):
        log_entry = {'docstring':action.__doc__, 
         'function_name':action.__name__, 
         'resource':resource, 
         'method':method}
        self.resource_list.append(log_entry)

    def ROOT_REDIRECT(self):
        """redirects to /static/ directory"""
        return generate_redirect_page('/static/')

    def GET_DOCS(self):
        """return the documentation page in HTML format"""
        resources = ''
        for resource in self.resource_list:
            if resource['docstring'] is None:
                resource['docstring'] = '&lt;No docs provided!&gt;'
            resource_html = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td><a href="{resource}">{resource}</a></td>\n\t\t\t\t\t<td>{method}</td>\n\t\t\t\t\t<td>{function_name}</td>\n\t\t\t\t\t<td>{docstring}</td>\n\t\t\t\t</tr>\n\t\t\t'.format(resource=(resource['resource']),
              method=(resource['method']),
              function_name=(resource['function_name']),
              docstring=(resource['docstring'].replace('\n', '<br />')))
            resources = resources + resource_html

        return '\n\t\t\t<!DOCTYPE html>\n\t\t\t<html>\n\t\t\t\t<head>\n\t\t\t\t\t<title>Guavacado Web Documentation</title>\n\t\t\t\t</head>\n\t\t\t\t<body>\n\t\t\t\t\t<table border="1">\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<th>Resource</th>\n\t\t\t\t\t\t\t<th>Method</th>\n\t\t\t\t\t\t\t<th>Function Name</th>\n\t\t\t\t\t\t\t<th>Docstring</th>\n\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t{resources}\n\t\t\t\t\t</table>\n\t\t\t\t</body>\n\t\t\t</html>\n\t\t'.format(resources=resources)

    def GET_DOCS_JSON(self):
        """return the documentation page in JSON format"""
        return json.dumps(self.resource_list)