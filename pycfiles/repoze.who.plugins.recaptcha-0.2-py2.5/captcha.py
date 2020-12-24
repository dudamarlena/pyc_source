# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/who/plugins/captcha.py
# Compiled at: 2008-09-23 06:19:06
from recaptcha.client import captcha
from paste.httpexceptions import HTTPFound, HTTPUnauthorized
from paste.request import parse_formvars
from zope.interface import implements
from repoze.who.interfaces import IAuthenticator

class RecaptchaPlugin(object):
    implements(IAuthenticator)

    def __init__(self, private_key, form_handler):
        self.private_key = private_key
        self.handler = form_handler

    def authenticate(self, environ, identity):
        log = environ['repoze.who.logger']
        if self.handler:
            if environ['PATH_INFO'] not in self.handler.split():
                log.debug('no recapcha validation needed.')
                return
        form = parse_formvars(environ)
        captcha_challenge = form.get('recaptcha_challenge_field')
        captcha_response = form.get('recaptcha_response_field')
        recaptcha_result = captcha.submit(private_key=self.private_key, remoteip=environ['REMOTE_ADDR'], recaptcha_challenge_field=captcha_challenge, recaptcha_response_field=captcha_response)
        if recaptcha_result.is_valid:
            log.debug('recaptcha is valid.')
            return
        else:
            log.debug('recaptcha failed: ' + recaptcha_result.error_code)
            environ['repoze.who.error'] = recaptcha_result.error_code
            environ['repoze.who.application'] = HTTPUnauthorized()
            return
        return


def make_authentication_plugin(private_key=None, form_handler=None):
    if private_key is None:
        raise ValueError('private_key must be provided for recaptcha API.')
    return RecaptchaPlugin(private_key, form_handler)