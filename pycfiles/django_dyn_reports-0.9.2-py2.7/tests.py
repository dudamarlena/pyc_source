# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_reports/tests.py
# Compiled at: 2017-09-01 05:57:44
import time
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_reports.models import Report

class ReportTest(TestCase):

    def setUp(self):
        r1 = Report.objects.create(name='Test Report 1', source_code='\nfrom django_reports.models import Report\nfrom django_reports.highcharts import PieChartReportQuery\n\nclass TestQuery1(PieChartReportQuery):\n        \n    def get_series_data(self, **kwargs):\n        return [{"name":r.name, "y":1} for r in Report.objects.all()]\n    \n    def get_series_name(self, **kwargs):\n        return "Reports"\n    \n    def get_title(self, **kwargs):\n        return "Reports"\n    \n    def get_form(parameter_name):\n        pass\n\nquery = TestQuery1()\n')

    def test_reports(self):
        r = Report.objects.get(name='Test Report 1')
        r.compile()
        print r.eval()

    def test_call_view_loads(self):
        response = self.client.get(reverse('report_view'))
        print response
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('report_view'), data={'get': 'values', 'report': 'Test Report 1'})
        print response
        self.assertEqual(response.status_code, 200)