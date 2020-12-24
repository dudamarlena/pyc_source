# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiform\form.py
# Compiled at: 2006-12-10 14:54:21
"""WSGI middleware for validating form submissions and parsing them into
dictionaries, individual WSGI 'environ' dictionary entries, cgi.FieldStorage
instances, or keyword arguments passed to a WSGI application. Supports
automatically escaping and sterilizing form submissions.
"""
import cgi, urllib
from StringIO import StringIO
from wsgiform.util import escapeform, hyperform, sterileform, getinput
__all__ = [
 'WsgiForm', 'form']

def _errorapp(environ, start_response):
    """Default error handler for form validation errors.

    Replace with custom handler.
    """
    start_response('200 OK', ('Content-type', 'text/plain'))
    return ['Data in field(s) %s was invalid.' % (' ').join(environ['wsgiform.error'])]


def validate(qdict, validators, environ, strict=False):
    """Validates form data.

    qdict Dictionary of validators where the key is a form field
    environ A WSGI environment dictionary
    validators An iterable with validators
    strict Keys w/out validators are form errors (default: False)
    """
    errors = []
    for (key, value) in qdict.iteritems():
        try:
            if not validators[key](value):
                errors.append(key)
        except KeyError:
            if strict:
                errors.append(key)

    if errors:
        environ['wsgiform.error'] = errors
        return False
    return True


def form(**kw):
    """Decorator for form parsing."""

    def decorator(application):
        return WsgiForm(application, **kw)

    return decorator


class WsgiForm(object):
    """Class that parses form data into dictionaries, individual 'environ'
    entries, FieldStorage instances, or keyword arguments that can be passed to
    WSGI applications in the environ dictionary.
    """
    __module__ = __name__
    environ = None
    keys = {'fieldstorage': 'wsgiform.fieldstorage', 'dict': 'wsgiform.dict', 'kwargs': 'wsgize.kwargs', 'environ': 'wsgiform.%s', 'routing_args': 'wsgiorg.routing_args'}
    funclist = {'escape': escapeform, 'hyperescape': hyperform, 'sterilize': sterileform}

    def __init__(self, application, **kw):
        self.application = application
        self.style = kw.get('style', 'dict')
        self.key = self.keys.get(self.style)
        self.validators = kw.get('validators', {})
        self.validate = kw.get('validfunc', validate)
        self.handler = kw.get('errapp', _errorapp)
        self.strict = kw.get('strict', False)
        self.func = self.funclist[kw.get('func', 'escape')]

    def __call__(self, env, start_response):
        qdict = self.func(env, self.strict)
        if self.validators:
            if not self.validate(qdict, self.validators, env, self.strict):
                return self.handler(env, start_response)
        if self.style == 'fieldstorage':
            cginput = StringIO(urllib.urlencode(qdict))
            qdict = cgi.FieldStorage(fp=cginput, environ=env)
        if self.style == 'environ':
            for (k, v) in qdict.iteritems():
                env[self.key % k] = v

        elif self.style == 'routing_args':
            (args, kwargs) = env.get(self.key, ((), {}))
            env[self.key] = (args, kwargs.update(qdict))
        else:
            env[self.key] = qdict
        return self.application(env, start_response)