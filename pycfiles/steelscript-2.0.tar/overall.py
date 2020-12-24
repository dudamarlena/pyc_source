# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/overall.py
# Compiled at: 2016-12-12 14:33:54
from steelscript.appfwk.apps.report.models import Report
import steelscript.appfwk.apps.report.modules.maps as maps, steelscript.appfwk.apps.report.modules.c3 as c3, steelscript.appfwk.apps.report.modules.tables as tables
from steelscript.netprofiler.appfwk.datasources.netprofiler import NetProfilerGroupbyTable, NetProfilerTimeSeriesTable
from steelscript.netshark.appfwk.datasources.netshark import NetSharkTable
report = Report.create('Overall', position=9, field_order=[
 'endtime', 'netprofiler_filterexpr',
 'netshark_filterexpr'], hidden_fields=[
 'resolution', 'duration'])
report.add_section('Locations', section_keywords=['resolution', 'duration'])
p = NetProfilerGroupbyTable.create('maploc', groupby='host_group', duration=60, resolution='auto')
p.add_column('group_name', label='Group Name', iskey=True, datatype='string')
p.add_column('response_time', label='Resp Time', units='ms', sortdesc=True)
p.add_column('network_rtt', label='Net RTT', units='ms')
p.add_column('server_delay', label='Srv Delay', units='ms')
report.add_widget(c3.BarWidget, p, 'Response Time', width=6, height=300)
report.add_widget(tables.TableWidget, p, 'Locations by Response Time', width=6, info=False, paging=False, searching=False)
report.add_section('NetProfiler Overall', section_keywords=[
 'resolution', 'duration'])
p = NetProfilerTimeSeriesTable.create('ts1', duration=1440, resolution='15min')
p.add_column('time', label='Time', datatype='time', iskey=True)
p.add_column('avg_bytes', label='Avg Bytes/s', units='B/s')
report.add_widget(c3.TimeSeriesWidget, p, 'NetProfiler Overall Traffic', width=6)
section = report.add_section('NetShark Traffic', section_keywords=[
 'resolution', 'duration'])
shark = NetSharkTable.create('Total Traffic Bits', duration=15, resolution='1sec', aggregated=False)
shark.add_column('time', extractor='sample_time', iskey=True, label='Time', datatype='time')
shark.add_column('generic_bits', label='bits', iskey=False, extractor='generic.bits', operation='sum', units='b')
section.add_widget(c3.TimeSeriesWidget, shark, 'Overall Bandwidth (Bits) at (1-second resolution)', width=6)