# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adam/Documents/src/Venvs/lsq/lib/python3.7/site-packages/jupyterlab_lsstquery/handlers.py
# Compiled at: 2018-08-02 16:42:36
# Size of source mod 2**32: 2754 bytes
"""
This is a Handler Module with all the individual handlers for LSSTQuery
"""
import json, os
from jinja2 import Template
import notebook.utils as ujoin
from notebook.base.handlers import APIHandler
NBTEMPLATE = '\n{\n "cells": [\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "import os\\n",\n    "token = os.getenv(\\"JUPYTERHUB_API_TOKEN\\")\\n",\n    "print(\\"Placeholder for Butler query \'{{query_id}}\'\\")"\n   ]\n  }\n ],\n "metadata": {\n  "kernelspec": {\n   "display_name": "LSST_Stack (Python 3)",\n   "language": "python",\n   "name": "lsst_stack"\n  },\n  "language_info": {\n   "name": ""\n  }\n },\n "nbformat": 4,\n "nbformat_minor": 2\n}'.strip()

class LSSTQuery_handler(APIHandler):
    __doc__ = '\n    LSSTQuery Parent Handler.\n    '

    @property
    def lsstquery(self):
        return self.settings['lsstquery']

    def post(self):
        """
        POST a queryID and get back a prepopulated notebook.
        """
        self.log.warning(self.request.body)
        post_data = json.loads(self.request.body.decode('utf-8'))
        query_id = post_data['query_id']
        self.log.debug(query_id)
        result = self._substitute_query(query_id)
        self.finish(json.dumps(result))

    def _substitute_query(self, query_id):
        top = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
        root = os.environ.get('HOME')
        fname = self._get_filename(query_id)
        fpath = 'notebooks/queries/' + fname
        os.makedirs((root + '/notebooks/queries'), exist_ok=True)
        filename = root + '/' + fpath
        if os.path.exists(filename):
            with open(filename, 'rb') as (f):
                body = f.read().decode('utf-8')
        else:
            with open(filename, 'wb') as (f):
                templatestr = self._get_template()
                template = Template(templatestr)
                body = template.render(query_id=query_id)
                f.write(bytes(body, 'utf-8'))
        retval = {'status':200, 
         'filename':filename, 
         'path':fpath, 
         'url':top + '/tree/' + fpath, 
         'body':body}
        return retval

    def _get_filename(self, query_id):
        fname = 'query-' + str(query_id) + '.ipynb'
        return fname

    def _get_template(self):
        return NBTEMPLATE


def setup_handlers(web_app):
    """
    Function used to setup all the handlers used.
    """
    host_pattern = '.*$'
    base_url = web_app.settings['base_url']
    handlers = [(ujoin(base_url, '/lsstquery'), LSSTQuery_handler)]
    web_app.add_handlers(host_pattern, handlers)