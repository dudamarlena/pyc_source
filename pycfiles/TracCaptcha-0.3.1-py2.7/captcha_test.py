# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/test_util/captcha_test.py
# Compiled at: 2010-07-03 06:13:49
from trac_captcha.test_util.compat import EnvironmentStub
from trac_captcha.test_util.trac_test import TracTest
from trac_captcha.controller import TracCaptchaController
__all__ = [
 'CaptchaTest']

class CaptchaTest(TracTest):

    def setUp(self):
        self.super()
        self.enable_ticket_subsystem()
        self.enable_captcha_infrastructure()
        self.env = EnvironmentStub(enable=('trac.*', 'trac_captcha.*'))
        self.disable_component('trac.versioncontrol.api.repositorymanager')

    def enable_captcha_infrastructure(self):
        import trac_captcha

    def assert_captcha_is_active(self, captcha):
        self.assert_equals(captcha(self.env), TracCaptchaController(self.env).captcha)

    def enable_captcha(self, captcha_class):
        class_name = str(captcha_class.__name__)
        self.env.config.set('trac-captcha', 'captcha', class_name)
        self.enable_component(captcha_class)
        self.assert_captcha_is_active(captcha_class)

    def is_fake_captcha_visible(self, response):
        return 'fake captcha' in response.html()

    def assert_fake_captcha_is_visible(self, response):
        self.assert_equals(200, response.code())
        self.assert_true(self.is_fake_captcha_visible(response))

    def fake_captcha_error(self):
        return 'Please fill in the CAPTCHA so we know you are not a spammer.'

    def assert_fake_captcha_warning_visible(self, response):
        self.assert_equals([self.fake_captcha_error()], response.trac_warnings())