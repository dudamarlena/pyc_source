# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/elasticsearch/magic.py
# Compiled at: 2017-12-19 17:11:32
# Size of source mod 2**32: 2187 bytes
"""Elasticearch IPython magic."""
from __future__ import absolute_import, print_function
import json, os, urllib.parse
from IPython.core.magic import Magics, magics_class, line_cell_magic
import requests
from . import notebook as nb

@magics_class
class ElasticsearchMagics(Magics):

    def __init__(self, **kwargs):
        self._base_url = 'http://localhost:9200/'
        nb.output_notebook()
        (super().__init__)(**kwargs)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value
        print('Using: {}'.format(self.base_url))

    @line_cell_magic
    def elasticsearch(self, line, cell=None):
        """elasticsearch line magic"""
        cell_base_url = line if line else self.base_url
        if not cell:
            self.base_url = cell_base_url
        else:
            line1 = (cell + os.linesep).find(os.linesep)
            method, path = cell[:line1].split(None, 1)
            body = cell[line1:].strip()
            request_args = {}
            if body:
                request_args['data'] = body
                request_args['headers'] = {'Content-Type': 'application/json'}
            session = requests.Session()
            rsp = session.send((requests.Request)(method=method, url=urllib.parse.urljoin(cell_base_url, path), **request_args).prepare())
            try:
                nb.output_cell(rsp.json())
            except json.JSONDecodeError:
                print(rsp.content.decode('UTF-8'))

            return rsp


def load_ipython_extension(ipy):
    ipy.register_magics(ElasticsearchMagics)