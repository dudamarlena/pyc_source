# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/business_hours/business_hours_report_byapp.py
# Compiled at: 2016-12-12 14:11:15
import steelscript.appfwk.apps.report.modules.c3 as c3
from steelscript.appfwk.apps.report.models import Report
import steelscript.appfwk.apps.report.modules.tables as tables, steelscript.appfwk.business_hours.datasource.business_hours_source as bizhours
from steelscript.netprofiler.appfwk.datasources import netprofiler
report = Report.create('Business Hour Reporting - By Application', position=10, field_order=[
 'starttime',
 'endtime',
 'netprofiler_filterexpr',
 'business_hours_start',
 'business_hours_end',
 'business_hours_tzname',
 'business_hours_weekends'], hidden_fields=[
 'duration', 'resolution'])
report.add_section()
basetable = netprofiler.NetProfilerGroupbyTable.create('bh-basetable-byapp', groupby='application', duration=60, resolution=3600, interface=True)
basetable.add_column('app_name', 'Application', iskey=True, datatype='string')
basetable.add_column('network_rtt', 'Network RTT', datatype='integer', units='ms', sortdesc=True)
basetable.add_column('in_avg_bytes', 'Avg Bytes In', units='B')
basetable.add_column('out_avg_bytes', 'Avg Bytes Out', units='B')
biztable = bizhours.BusinessHoursTable.create('bh-biztable-byapp', basetable, aggregate={'network_rtt': 'max', 
   'in_avg_bytes': 'avg', 
   'out_avg_bytes': 'avg'})
report.add_widget(tables.TableWidget, biztable, 'Applications', height=600)
report.add_widget(c3.BarWidget, biztable, 'Applications RTT', height=600, keycols=[
 'app_name'], valuecols=['network_rtt'])
report.add_widget(tables.TableWidget, bizhours.get_timestable(biztable), 'Covered times', width=12, height=200)