# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_recaptcha/genshi_widget.py
# Compiled at: 2011-03-30 04:14:40
from urllib import urlencode
from genshi.builder import tag
from trac_captcha.compat import json
__all__ = [
 'GenshiReCAPTCHAWidget']

class NullLog(object):

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass


class GenshiReCAPTCHAWidget(object):

    def __init__(self, public_key, use_https=False, error=None, log=None, js_config=None, noscript=True):
        self.public_key = public_key
        self.use_https = use_https
        self.error = error
        self.log = log or NullLog()
        self.js_config = js_config
        self.noscript = noscript

    def recaptcha_domain(self):
        if self.use_https:
            return 'https://www.google.com/recaptcha/api'
        return 'http://www.google.com/recaptcha/api'

    def challenge_url(self):
        url_path = '%(domain)s/challenge?' % dict(domain=self.recaptcha_domain())
        parameters = dict(k=self.public_key)
        if self.error is not None:
            parameters['error'] = self.error
        return url_path + urlencode(parameters)

    def noscript_url(self):
        url_path = '%(domain)s/noscript?' % dict(domain=self.recaptcha_domain())
        parameters = dict(k=self.public_key)
        if self.error is not None:
            parameters['error'] = self.error
        return url_path + urlencode(parameters)

    def widget_tag(self):
        return tag.script(src=self.challenge_url(), type='text/javascript')

    def noscript_fallback_tag(self):
        return tag.noscript(tag.iframe(src=self.noscript_url(), height=300, width=500, frameborder=0), tag.br(), tag.textarea(name='recaptcha_challenge_field', rows=3, cols=40), tag.input(type='hidden', name='recaptcha_response_field', value='manual_challenge'))

    def jsconfig_tag(self):
        if self.js_config is None:
            return
        else:
            if json is None:
                if 'theme' in self.js_config:
                    msg = 'simplejson is not available, can not set reCAPTCHA ' + 'theme. Please install simplejson.'
                    self.log.error(msg)
                else:
                    msg = 'simplejson is not available so the reCAPTCHA widget ' + "can not switch to the user's language."
                    self.log.debug(msg)
                return
            js_string = 'RecaptchaOptions = %s;' % json.dumps(self.js_config)
            return tag.script(js_string, type='text/javascript')

    def xml(self):
        tags = [self.jsconfig_tag(), self.widget_tag()]
        if self.noscript:
            tags.append(self.noscript_fallback_tag())
        return tag.span(*tags)