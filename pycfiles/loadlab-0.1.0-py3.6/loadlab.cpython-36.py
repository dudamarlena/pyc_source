# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/loadlab/loadlab.py
# Compiled at: 2018-09-08 20:17:23
# Size of source mod 2**32: 1127 bytes
"""Main module."""
import os, requests

class TokenError(BaseException):
    __doc__ = ' No token passed to client '


class Resource:
    __doc__ = ' An Abstract REST Resource '
    PATH = None
    BASE_URL = 'https://api.loadlab.co/v1'

    def __init__(self, token):
        self.headers = {'Authorization':f"Token {token}", 
         'Accept':'application/json'}

    def get(self):
        return requests.get((self.BASE_URL + self.PATH), headers=(self.headers)).json()

    def create(self, **data):
        return requests.post((self.BASE_URL + self.PATH), data=data, headers=(self.headers)).json()


class Plans(Resource):
    PATH = '/plans/'


class Jobs(Resource):
    PATH = '/jobs/'


class Sites(Resource):
    PATH = '/sites/'


class LoadLab:

    def __init__(self, token: str=None):
        self.token = token or os.getenv('LOADLAB_API_TOKEN')
        if not self.token:
            raise TokenError('Missing environment variable `LOADLAB_API_TOKEN`')
        self.jobs = Plans(self.token)
        self.plans = Plans(self.token)
        self.sites = Sites(self.token)