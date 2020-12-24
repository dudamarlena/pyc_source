# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/berg/git/django-amp-tools/tests/test_base.py
# Compiled at: 2018-12-13 10:52:34
from __future__ import unicode_literals
import threading
from django.test import TestCase, override_settings
from django.template import Template, RequestContext
from mock import MagicMock, Mock, patch, call
from amp_tools import get_amp_detect
from amp_tools.middleware import AMPDetectionMiddleware
from amp_tools.settings import settings as amp_setting
from amp_tools.templatetags.amp_tags import amp_img, amp_safe

def _reset():
    """
    Reset the thread local.
    """
    import amp_tools
    del amp_tools._local
    amp_tools._local = threading.local()


class BaseTestCase(TestCase):

    def setUp(self):
        _reset()

    def tearDown(self):
        _reset()


class DetectAMPMiddlewareTests(BaseTestCase):

    def setUp(self):
        self.amp_get_parameter = amp_setting.AMP_TOOLS_GET_PARAMETER
        self.amp_get_value = amp_setting.AMP_TOOLS_GET_VALUE

    def test_default_page(self):
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(get_amp_detect(), b'')

    @patch(b'amp_tools.middleware.set_amp_detect')
    def test_set_amp_detect_through_get_parameter(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {b'amp-content': b'amp'}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    def test_tamplate_tags(self):
        request = Mock()
        request.META = MagicMock()
        request.GET = {b'amp-content': b'amp'}
        template = Template(b'{% load amp_tags %}{% amp_link "/path/" %}')
        context = RequestContext(request, {})
        rendered = template.render(context)
        self.assertEqual(rendered, b'/path/?%s=%s' % (self.amp_get_parameter, self.amp_get_value))
        html_content = b'\n            <html><body>\n                <img alt="alternate text" src="/media/uploads/img.png" width="800" height="600" style="width: 100%;">\n                <img alt="alternate text2" src="/media/uploads/img2.png" style="width: 100%;" />\n            </body></html>\n        '
        amp_content = amp_img(html_content)
        self.assertNotEqual(amp_content, html_content)
        self.assertEqual(amp_content, b'\n            <html><body>\n                <amp-img alt="alternate text" src="/media/uploads/img.png" width="800" height="600" style="width: 100%;" layout="responsive"></amp-img>\n                <amp-img alt="alternate text2" src="/media/uploads/img2.png" style="width: 100%;"  layout="responsive" width="1.33" height="1"></amp-img>\n            </body></html>\n        ')
        amp_content = amp_safe(html_content)
        self.assertNotEqual(amp_content, html_content)
        self.assertEqual(amp_content, b'\n            <html><body>\n                <amp-img alt="alternate text" src="/media/uploads/img.png" width="800" height="600"  layout="responsive"></amp-img>\n                <amp-img alt="alternate text2" src="/media/uploads/img2.png"   layout="responsive" width="1.33" height="1"></amp-img>\n            </body></html>\n        ')

    @patch(b'amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=[b'^/$'])
    def test_set_amp_not_set_url_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {b'amp-content': b'amp'}
        request.path_info = b'/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    @patch(b'amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=[b'^/$'])
    def test_set_amp_not_set_url_not_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {b'amp-content': b'amp'}
        request.path_info = b'/not-amp-url/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(0, len(set_amp_detect.call_args_list))