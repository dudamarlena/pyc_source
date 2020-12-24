# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/42-kavyarnya/.env/lib/python2.7/site-packages/x_file_accel_redirects/tests/test_views.py
# Compiled at: 2014-03-28 02:58:14
import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from mock import patch
from x_file_accel_redirects.conf import settings

class TestRedirects(TestCase):

    @patch('django.views.static.serve', return_value=HttpResponse())
    def test_accel_redirects(self, serve_mock):
        from x_file_accel_redirects.models import AccelRedirect
        settings.X_FILE_ACCEL = True
        redirect = AccelRedirect(prefix='email_attaches', filename_solver=AccelRedirect.FILENAME_SOLVERS.remainder, internal_path='/protected/attaches/', login_required=False)
        redirect.save()
        filepath = 'hello/world.txt'
        url = reverse('accel_view', kwargs=dict(prefix=redirect.prefix, filepath=filepath))
        response = self.client.get(url)
        file_name = filepath.split('/')[(-1)]
        disposition_header = ('attachment; filename={0}').format(file_name)
        self.assertEqual(response.get('Content-Disposition', None), disposition_header)
        accel_path = os.path.join(redirect.internal_path, filepath)
        self.assertEqual(response.get('X-Accel-Redirect', None), accel_path)
        self.assertFalse(serve_mock.called)
        redirect.login_required = True
        redirect.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        return