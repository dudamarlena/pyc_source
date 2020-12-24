# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/controller.py
# Compiled at: 2011-03-25 08:17:14
from genshi import HTML
from genshi.builder import tag
import pkg_resources
from trac.config import ExtensionOption, Option
from trac.core import Component, implements
from trac.perm import IPermissionRequestor
from trac_captcha.api import CaptchaFailedError, ICaptcha
from trac_captcha.cryptobox import CryptoBox
from trac_captcha.i18n import add_domain
from trac_captcha.lib.version import Version
from trac_captcha.trac_version import trac_version
__all__ = [
 'initialize_captcha_data', 'TracCaptchaController']

def initialize_captcha_data(req):
    if not hasattr(req, 'captcha_data'):
        req.captcha_data = dict()


class TracCaptchaController(Component):
    implements(IPermissionRequestor)
    captcha = ExtensionOption('trac-captcha', 'captcha', ICaptcha, 'reCAPTCHAImplementation', 'Name of the component implementing `ICaptcha`, which is used to \n        generate actual captchas.')
    stored_token_key = Option('trac-captcha', 'token_key', None, 'Generated private key which is used to encrypt captcha tokens.')

    def __init__(self):
        super(TracCaptchaController, self).__init__()
        locale_dir = pkg_resources.resource_filename(__name__, 'locale')
        add_domain(self.env.path, locale_dir)

    def get_permission_actions(self):
        permissions = [
         'CAPTCHA_SKIP']
        if Version(major=0, minor=13) <= trac_version:
            permissions.append(('TICKET_ADMIN', ['CAPTCHA_SKIP']))
        return permissions

    def should_skip_captcha(self, req):
        if 'CAPTCHA_SKIP' in req.perm:
            self.debug_log('Skipping CAPTCHA for %(path)s because of CAPTCHA_SKIP' % dict(path=req.path_info))
            return True
        captcha_token = req.args.get('__captcha_token')
        if self.is_token_valid(captcha_token):
            self.debug_log('Skipping CAPTCHA for %(path)s because request has valid token %(token)s' % dict(path=req.path_info, token=repr(captcha_token)))
            self.add_token_for_request(req, captcha_token)
            return True
        return False

    def check_captcha_solution(self, req):
        if self.should_skip_captcha(req):
            return
        else:
            try:
                self.captcha.assert_captcha_completed(req)
            except CaptchaFailedError as e:
                self.debug_log('Wrong CAPTCHA solution for %(path)s: %(arguments)s' % dict(path=req.path_info, arguments=repr(req.args)))
                req.captcha_data = e.captcha_data
                return e.msg

            self.debug_log('Accepted CAPTCHA solution for %(path)s: %(arguments)s' % dict(path=req.path_info, arguments=repr(req.args)))
            self.add_token_for_request(req)
            return

    def captcha_html(self, req):
        return HTML(self.captcha.genshi_stream(req))

    def inject_captcha_into_stream(self, req, stream, transformer):
        initialize_captcha_data(req)
        if 'token' in req.captcha_data:
            return stream | transformer.before(self.captcha_token_tag(req))
        if self.should_skip_captcha(req):
            return stream
        self.debug_log('Displaying captcha for %(path)s' % dict(path=req.path_info))
        return stream | transformer.before(self.captcha_html(req))

    def captcha_token_tag(self, req):
        token = req.captcha_data['token']
        return tag.input(type='hidden', name='__captcha_token', value=token)

    def add_token_for_request(self, req, token=None):
        if token is None:
            token = CryptoBox(self.token_key()).generate_token()
        initialize_captcha_data(req)
        req.captcha_data['token'] = token
        return

    def token_key(self):
        """Return the private token key stored in trac.ini. If no such key was
        set, a new one will be generated."""
        if self.stored_token_key in ('', None):
            new_key = CryptoBox().generate_key()
            self.env.config.set('trac-captcha', 'token_key', new_key)
            self.env.config.save()
        return str(self.stored_token_key)

    def is_token_valid(self, a_token):
        return CryptoBox(self.token_key()).is_token_valid(a_token)

    def debug_log(self, message):
        self.env.log.debug(message)