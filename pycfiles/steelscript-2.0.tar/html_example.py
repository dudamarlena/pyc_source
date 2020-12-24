# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/html_example.py
# Compiled at: 2016-02-09 09:54:51
import logging
from django.core.urlresolvers import reverse
from steelscript.appfwk.apps.datasource.modules.html import HTMLTable
from steelscript.appfwk.apps.report.models import Report
import steelscript.appfwk.apps.report.modules.raw as raw
logger = logging.getLogger(__name__)
report = Report.create('HTML Example', position=11)
report.add_section('Raw HTML')
imgurl = 'http://radar.weather.gov/Conus/Loop/NatLoop_Small.gif'
markup = '<img src="%s" alt="Doppler Radar National Mosaic Loop">' % imgurl
table = HTMLTable.create('Weather Image', html=markup)
report.add_widget(raw.TableWidget, table, 'weather image')
lines = []
reports = Report.objects.all().order_by('position')
for r in reports:
    kwargs = {'report_slug': r.slug, 'namespace': r.namespace}
    url = reverse('report-view', kwargs=kwargs)
    line = '<li><a href="%s" target="_blank">%s</a></li>' % (url, r.title)
    lines.append(line)

markup = '\n<ul>\n%s\n</ul>\n' % ('\n').join(lines)
table = HTMLTable.create('Report Links', html=markup)
report.add_widget(raw.TableWidget, table, 'report table')