# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_recaptcha/integration.py
# Compiled at: 2011-03-30 04:21:31
import urlparse
from genshi.builder import tag
from trac.config import BoolOption, Option
from trac.core import Component, implements
from trac.web.href import Href
from trac_captcha.api import ICaptcha
from trac_captcha.controller import TracCaptchaController
from trac_captcha.i18n import _
from trac_recaptcha.client import reCAPTCHAClient, is_empty
from trac_recaptcha.genshi_widget import GenshiReCAPTCHAWidget
__all__ = [
 'reCAPTCHAImplementation']

def trac_hostname(req):

    def host_from_base_url():
        base_url = req.environ.get('trac.base_url')
        if base_url is None:
            return
        else:
            return urlparse.urlsplit(base_url)[1]

    for collector in (host_from_base_url, lambda : req.get_header('host'),
     lambda : req.environ.get('SERVER_NAME')):
        hostname = collector()
        if hostname is not None:
            return hostname

    raise AssertionError('No hostname found!')
    return


class reCAPTCHAImplementation(Component):
    implements(ICaptcha)
    public_key = Option('recaptcha', 'public_key')
    private_key = Option('recaptcha', 'private_key')
    theme = Option('recaptcha', 'theme')
    require_javascript = BoolOption('recaptcha', 'require_javascript', False)

    def genshi_stream(self, req):
        error_xml = self.warn_if_private_key_or_public_key_not_set(req)
        if error_xml is not None:
            return error_xml
        else:
            use_https = req.scheme == 'https'
            error_code = self.error_code_from_request(req)
            widget = GenshiReCAPTCHAWidget(self.public_key, use_https=use_https, error=error_code, js_config=self.js_config(req), log=self.env.log, noscript=not self.require_javascript)
            return widget.xml()

    def assert_captcha_completed(self, req, client_class=None):
        client = self.client(client_class)
        remote_ip = req.remote_addr
        challenge = req.args.get('recaptcha_challenge_field')
        response = req.args.get('recaptcha_response_field')
        client.verify(remote_ip, challenge, response)
        controller = TracCaptchaController(self.env)
        base_message = 'Captcha for %(path)s successfully solved with %(challenge)s/%(response)s and %(arguments)s'
        parameters = dict(path=req.path_info, challenge=repr(challenge), response=repr(response), arguments=repr(req.args))
        controller.debug_log(base_message % parameters)

    def client(self, client_class):
        client_class = client_class and client_class or reCAPTCHAClient
        return client_class(self.private_key)

    def error_code_from_request(self, req):
        if hasattr(req, 'captcha_data'):
            return req.captcha_data.get('error_code')
        else:
            return

    def warn_if_private_key_or_public_key_not_set(self, req):
        if is_empty(self.public_key):
            url_base = Href('http://www.google.com/recaptcha/admin')
            link = tag.a(_('sign up for a reCAPTCHA now'), href=url_base(app='TracCaptcha', domain=trac_hostname(req)))
            return tag.div(_('No public key for reCAPTCHA configured. Please add your reCAPTCHA key to your trac.ini ([recaptcha]/public_key). '), _("If you don't have a key, you can "), link, _('.'))
        else:
            return

    def js_config(self, req):
        config = dict()
        if getattr(req, 'locale', None) is not None:
            config['lang'] = req.locale.language
        if self.theme:
            config['theme'] = self.theme
        return config or None