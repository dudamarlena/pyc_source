# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/business_hours/business_hours_report.py
# Compiled at: 2017-02-22 13:48:01
import steelscript.appfwk.apps.report.modules.c3 as c3, steelscript.appfwk.apps.report.modules.tables as tables, steelscript.appfwk.business_hours.datasource.business_hours_source as bizhours, steelscript.netprofiler.appfwk.libs.profiler_tools as protools
from steelscript.appfwk.apps.report.models import Report
from steelscript.netprofiler.appfwk.datasources import netprofiler
from steelscript.netprofiler.appfwk.datasources import netprofiler_devices
report = Report.create('Business Hour Reporting - NetProfiler Interfaces', position=10, field_order=[
 'starttime',
 'endtime',
 'netprofiler_filterexpr',
 'business_hours_start',
 'business_hours_end',
 'business_hours_tzname',
 'business_hours_weekends'], hidden_fields=[
 'duration', 'resolution'])
report.add_section()
basetable = netprofiler.NetProfilerGroupbyTable.create('bh-basetable', groupby='interface', duration=60, resolution=3600, interface=True)
basetable.add_column('interface_dns', 'Interface', iskey=True, datatype='string')
basetable.add_column('interface_alias', 'Ifalias', iskey=True, datatype='string')
basetable.add_column('avg_util', '% Utilization', units='pct', sortdesc=True)
basetable.add_column('in_avg_util', '% Utilization In', units='pct')
basetable.add_column('out_avg_util', '% Utilization Out', units='pct')
biztable = bizhours.BusinessHoursTable.create('bh-biztable', basetable, aggregate={'avg_util': 'avg', 
   'in_avg_util': 'avg', 
   'out_avg_util': 'avg'})
devtable = netprofiler_devices.NetProfilerDeviceTable.create('devtable')
devtable.add_column('ipaddr', 'Device IP', iskey=True, datatype='string')
devtable.add_column('name', 'Device Name', datatype='string')
devtable.add_column('type', 'Flow Type', datatype='string')
devtable.add_column('version', 'Flow Version', datatype='string')
interfaces = protools.ProfilerMergeIpDeviceTable.create('bh-interfaces', devtable, biztable)
report.add_widget(tables.TableWidget, interfaces, 'Interface', height=600)
report.add_widget(c3.BarWidget, interfaces, 'Interface Utilization', height=600, keycols=['interface_name'], valuecols=[
 'avg_util'])
report.add_widget(tables.TableWidget, bizhours.get_timestable(biztable), 'Covered times', width=12, height=200)