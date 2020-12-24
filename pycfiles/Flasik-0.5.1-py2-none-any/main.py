# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/devlab/new/t1/application/views/main.py
# Compiled at: 2019-08-24 20:38:41
"""
Flasik Views
"""
from flasik import Flasik, set_page_context, get_config, abort, url_for, redirect, models, request, response, functions, utils

class Index(Flasik):

    def index(self):
        set_page_context(title='Hello World', description='Under Construction')

    @response.cors()
    @response.json
    def api(self):
        return {'date': functions.utc_now(), 
           'location': 'NC'}