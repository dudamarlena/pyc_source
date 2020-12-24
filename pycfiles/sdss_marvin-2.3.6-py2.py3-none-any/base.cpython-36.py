# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/api/base.py
# Compiled at: 2018-03-20 20:19:12
# Size of source mod 2**32: 3874 bytes
"""
Licensed under a 3-clause BSD license.

Revision History:
    Initial Version: 2016-02-17 17:46:57
    Last Modified On: 2016-02-17 17:46:57 by Brian

"""
from __future__ import print_function
from __future__ import division
from flask_classful import FlaskView
from flask import request
from brain import bconfig
from brain.core.exceptions import BrainError

def processRequest(request=None, as_dict=None, param=None):
    """Generally process the request for POST or GET, and build a form dict

        Parameters:
            request (request):
                HTTP request object containing POST or GET data
            as_dict (bool):
                Boolean indicating whether to return the data as a standard dict or not
        Returns:
            Dict or ImmutableMultiDict
    """
    if request.method == 'POST':
        if not request.form:
            data = request.get_json()
        else:
            data = request.form
    else:
        if request.method == 'GET':
            data = request.args
        else:
            return {}
        if param:
            if data:
                return data.get(param, None)
        if as_dict:
            if isinstance(data, dict):
                form = data
            else:
                try:
                    form = {key:val if len(val) > 1 else val[0] for key, val in data.iterlists()}
                except AttributeError:
                    form = {key:val if len(val) > 1 else val[0] for key, val in data.lists()}

        else:
            form = data
    return form


class BrainBaseView(FlaskView):
    __doc__ = 'Super Class for all API Views to handle all global API items of interest'

    def __init__(self):
        self.reset_results()
        bconfig.mode = 'local'

    def reset_results(self):
        self.results = {'data':None, 
         'status':-1,  'error':None,  'traceback':None}

    def update_results(self, newresults):
        self.results.update(newresults)

    def reset_status(self):
        self.results['status'] = -1

    def add_config(self):
        pass

    def before_request(self, *args, **kwargs):
        form = processRequest(request=request)
        self._release = form.get('release', None) if form else None
        self._endpoint = request.endpoint
        self.results['inconfig'] = form
        if form:
            for key, val in form.items():
                bconfig.__setattr__(key, val)

        self.add_config()

    def after_request(self, name, response):
        """This performs a reset of the results dict after every request method runs.

        See Flask-Classy for more info on after_request."""
        self.reset_results()
        return response

    def _checkAuth(self):
        """ Checks the API for authentication """
        print('api inconfig', self.results['inconfig'])
        if 'session_id' in self.results['inconfig']:
            session_id = self.results['inconfig'].get('session_id', None)
            if session_id is not None:
                pass
            else:
                if session_id is None or isexpired:
                    pass