# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/reports/appresponse/appresponse.py
# Compiled at: 2017-08-09 11:44:29
from steelscript.appfwk.apps.report.models import Report
import steelscript.appfwk.apps.report.modules.c3 as c3, steelscript.appfwk.apps.report.modules.tables as tables
from steelscript.appresponse.appfwk.datasources.appresponse import AppResponseTable
report = Report.create('AppResponse Report')
report.add_section()
p = AppResponseTable.create('network_traffic', include_files=True)
p.add_column('time', 'Time', datatype='time', iskey=True, extractor='start_time')
p.add_column('network_traffic', 'Network Traffic', datatype='integer', extractor='sum_traffic.network_bytes')
report.add_widget(c3.TimeSeriesWidget, p, 'Network Traffic (Bytes)', width=12)
p = AppResponseTable.create('Traffic by TCP/UDP', include_files=True)
p.add_column('time', 'Time', datatype='time', iskey=True, extractor='start_time')
p.add_column('tcp_traffic', 'TCP Traffic', datatype='integer', extractor='sum_tcp.total_bytes')
p.add_column('udp_traffic', 'UDP Traffic', datatype='integer', extractor='sum_udp.total_bytes')
report.add_widget(c3.TimeSeriesWidget, p, 'Traffic By Type (Bytes)', width=12)
p = AppResponseTable.create(name='Packet Traffic', rows=100)
p.add_column('ip_src', label='Source IP', iskey=True, extractor='src_ip.addr', datatype='string')
p.add_column('ip_dst', label='Dest IP', iskey=True, extractor='dst_ip.addr', datatype='string')
p.add_column('network_traffic', 'Network Traffic (Bytes)', datatype='integer', extractor='sum_traffic.network_bytes')
p.add_column('network_packets', 'Network Traffic (Packets)', datatype='integer', extractor='sum_traffic.packets', sortdesc=True)
report.add_widget(tables.TableWidget, p, 'Top 100 Conversations', width=12)