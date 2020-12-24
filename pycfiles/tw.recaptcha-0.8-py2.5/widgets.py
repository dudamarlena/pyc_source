# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/recaptcha/widgets.py
# Compiled at: 2008-06-01 07:07:51
from tw.api import Widget, JSLink, CSSLink
from genshi import HTML
from recaptcha.client.captcha import *
from tw.forms import InputField, FormField, ContainerMixin

class ReCaptchaWidget(InputField):
    engine_name = 'genshi'
    params = [
     'captcha_response', 'public_key', 'server', 'use_ssl', 'error_param']
    template = '<div><script type="text/javascript" src="${server}/challenge?k=${public_key}${error_param}"></script>\n<noscript>\n  <iframe src="${server}/noscript?k=${public_key}${error_param}" height="300" width="500" frameborder="0"></iframe><br />\n  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>\n  <input type=\'hidden\' name=\'recaptcha_response_field\' value=\'manual_challenge\' />\n</noscript></div>\n'

    def __init__(self, id=None, public_key=None, use_ssl=False, error_param=None, parent=None, children=[], **kw):
        """Initialize the widget here. The widget's initial state shall be
        determined solely by the arguments passed to this function; two
        widgets initialized with the same args. should behave in *exactly* the
        same way. You should *not* rely on any external source to determine
        initial state."""
        self.public_key = public_key
        self.error_param = ''
        if error_param:
            self.error_param = '&error=%s' % error_param
        self.server = API_SERVER
        if use_ssl:
            self.server = API_SSL_SERVER
        super(ReCaptchaWidget, self).__init__('recaptcha_response_field', parent, children, **kw)

    def update_params(self, d):
        """This method is called every time the widget is displayed. It's task
        is to prepare all variables that are sent to the template. Those
        variables can accessed as attributes of d."""
        d['captcha_response'] = HTML(displayhtml(self.public_key))
        return super(ReCaptchaWidget, self).update_params(d)