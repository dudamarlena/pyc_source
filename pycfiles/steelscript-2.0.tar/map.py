# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/map.py
# Compiled at: 2016-02-09 09:54:51
from steelscript.appfwk.apps.report.models import Report
import steelscript.appfwk.apps.report.modules.maps as maps, steelscript.appfwk.apps.report.modules.yui3 as yui3
from steelscript.netprofiler.appfwk.datasources.netprofiler import NetProfilerGroupbyTable
report = Report.create('Response Time Map', position=10)
report.add_section()
p = NetProfilerGroupbyTable.create('maploc2', groupby='host_group', duration=60)
p.add_column('group_name', iskey=True, label='Group Name', datatype='string')
p.add_column('response_time', label='Resp Time', units='ms')
p.add_column('network_rtt', label='Net RTT', units='ms')
p.add_column('server_delay', label='Srv Delay', units='ms')
p.add_column('avg_bytes', label='Response Time', units='B/s')
p.add_column('peak_bytes', 'Peak Bytes/s', units='B/s')
p.add_column('avg_bytes_rtx', 'Avg Retrans Bytes/s', units='B/s')
p.add_column('peak_bytes_rtx', 'Peak Retrans Bytes/s', units='B/s')
report.add_widget(maps.MapWidget, p, 'Response Time Map', width=12, height=500)
report.add_widget(yui3.TableWidget, p, 'Locations', width=12)