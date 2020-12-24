# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/util.py
# Compiled at: 2017-04-30 08:25:08
# Size of source mod 2**32: 2835 bytes
import json, flask
from .models.error_model import ErrorModel

class Error(Exception, ErrorModel):

    def __init__(self, status=400, title=None, type=None, instance=None, headers=None, detail=None):
        Exception.__init__(self)
        ErrorModel.__init__(self, status, type, title, detail, instance)
        self._detail = detail
        self.headers = headers

    def __str__(self):
        return self._detail

    def to_problem(self):
        flask.current_app.logger.error('{url} {type} {error}'.format(url=(flask.request.url), type=(self.type),
          error=(self.__str__())))
        problem_response = {'type':self.type,  'title':self.title, 
         'detail':self.detail, 
         'status':self.status, 
         'instance':self.instance}
        body = [json.dumps(problem_response, indent=2), '\n']
        response = flask.current_app.response_class(body, mimetype='application/problem+json', status=(self.status))
        if self.headers:
            response.headers.extend(headers)
        return response


class NotFoundUserError(Error):

    def __init__(self, detail=''):
        Error.__init__(self, status=404,
          title='Not Found User',
          type='RG-001',
          detail=detail)

    def __str__(self):
        return '%s user not found' % self._detail


class AlreadyExistUserError(Error):

    def __init__(self, detail=''):
        Error.__init__(self, status=404,
          title='User Already Exist',
          type='RG-002',
          detail=detail)

    def __str__(self):
        return '%s user exist' % self._detail


class EchecAuthentification(Error):

    def __init__(self, detail=''):
        Error.__init__(self, status=404,
          title='Echec Authentification',
          type='RG-002',
          detail=detail)

    def __str__(self):
        return '%s user echec authentification' % self._detail


class Unauthorized(Error):

    def __init__(self):
        Error.__init__(self, status=401,
          title='Unauthorized',
          type='',
          detail='')

    def __str__(self):
        return 'Authorization Required'


def to_json(fn):

    def _request_fn(*args, **kw):
        try:
            fn_exec = fn(*args, **kw)
            return json.dumps(fn_exec)
        except Error as e:
            return e.to_problem()

        return Error(status=500, title='Error System', type='UNKNOW', detail=(e.__str__())).to_problem()

    return _request_fn