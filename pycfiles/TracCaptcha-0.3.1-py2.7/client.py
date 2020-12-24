# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_recaptcha/client.py
# Compiled at: 2011-02-04 10:53:33
from urllib import urlencode
import urllib2
try:
    from trac_captcha.api import CaptchaFailedError
    from trac_captcha.i18n import _
except ImportError:
    from gettext import gettext as _

    class CaptchaFailedError(Exception):

        def __init__(self, msg, captcha_data=None):
            Exception.__init__(self, msg)
            self.msg = msg
            self.captcha_data = captcha_data or dict()


__all__ = [
 'is_empty', 'reCAPTCHAClient']

def is_string(instance):
    return hasattr(instance, 'strip')


def is_empty(parameter):
    return not is_string(parameter) or parameter.strip() == ''


class reCAPTCHAClient(object):

    def __init__(self, private_key):
        self.private_key = private_key

    def verify_server(self):
        return 'http://www.google.com/recaptcha/api/verify'

    def raise_error(self, error_code, msg=None):
        msg = msg or _('Incorrect captcha input - please try again…')
        raise CaptchaFailedError(msg, dict(error_code=error_code))

    def raise_server_unreachable_error(self):
        self.raise_error('recaptcha-not-reachable')

    def raise_incorrect_solution_error(self, error_code='incorrect-captcha-sol'):
        self.raise_error(error_code)

    def ask_verify_server(self, url, parameters):

        def to_utf8(value):
            return hasattr(value, 'encode') and value.encode('utf-8') or value

        utf8_parameters = dict([ (key, to_utf8(value)) for key, value in parameters.items() ])
        try:
            response = urllib2.urlopen(url, urlencode(utf8_parameters))
            response_content = response.read()
            response.close()
        except IOError:
            self.raise_server_unreachable_error()

        return response_content

    def assert_server_accepted_solution(self, response):
        lines = response.splitlines()
        if len(lines) == 0:
            self.raise_server_unreachable_error()
        if lines[0] == 'true':
            return
        if len(lines) < 2:
            self.raise_server_unreachable_error()
        raise self.raise_incorrect_solution_error(lines[1])

    def no_input_given(self, challenge, response):
        return is_empty(challenge) or is_empty(response)

    def raise_missing_private_key_error(self):
        msg = _('Can not verify captcha because the reCAPTCHA private key is missing. Please add your reCAPTCHA key to your trac.ini ([recaptcha] private_key).')
        self.raise_error('invalid-site-private-key', msg=msg)

    def verify(self, remote_ip, challenge, response, probe=None):
        if self.no_input_given(challenge, response):
            self.raise_incorrect_solution_error()
        if is_empty(self.private_key):
            self.raise_missing_private_key_error()
        parameters = dict(privatekey=self.private_key, remoteip=remote_ip, challenge=challenge, response=response)
        verify_method = probe and probe or self.ask_verify_server
        response = verify_method(self.verify_server(), parameters)
        self.assert_server_accepted_solution(response)