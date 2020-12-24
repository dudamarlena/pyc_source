# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ntp_sources.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.core.dr import SkipComponent
from insights.parsers.ntp_sources import ChronycSources, NtpqPn, NtpqLeap
from insights.tests import context_wrap
chrony_output = ('\n210 Number of sources = 3\nMS Name/IP address Stratum Poll Reach LastRx Last sample\n===============================================================================\n#* GPS0            0        4    377   11  -479ns[ -621ns]  +/- 134ns\n^? a.b.c 2 6 377 23 -923us[ -924us] +/- 43ms\n^+ d.e.f 1 6 377 21 -2629us[-2619us] +/- 86ms\n').strip()
ntpq_leap_output = ('\nleap=00\n').strip()
ntpq_leap_output_2 = ('\nassID=0 status=06f4 leap_none, sync_ntp, 15 events, event_peer/strat_chg,\nleap=00\n').strip()
ntpd_output = ('\n     remote           refid      st t when poll reach   delay   offset  jitter\n==============================================================================\n*ntp103.cm4.tbsi 10.225.208.100   2 u  225  256  377    0.464    0.149   0.019\n+ntp104.cm4.tbsi 10.228.209.150   2 u  163  256  377    0.459   -0.234   0.05\n').strip()
ntpd_qn = '\n     remote           refid      st t when poll reach   delay   offset  jitter\n==============================================================================\n 202.118.1.81    .INIT.          16 u    - 1024    0    0.000    0.000   0.000\n'
ntp_connection_issue = ('\n/usr/sbin/ntpq: read: Connection refused\n').strip()

def test_get_chrony_sources():
    parser_result = ChronycSources(context_wrap(chrony_output))
    assert parser_result.data[1].get('source') == 'a.b.c'
    assert parser_result.data[2].get('state') == '+'
    assert parser_result.data[2].get('mode') == '^'


def test_get_ntpq_leap():
    parser_result = NtpqLeap(context_wrap(ntpq_leap_output))
    assert parser_result.leap == '00'
    parser_result = NtpqLeap(context_wrap(ntpq_leap_output_2))
    assert parser_result.leap == '00'
    with pytest.raises(SkipComponent) as (e):
        NtpqLeap(context_wrap(ntp_connection_issue))
    assert 'NTP service is down' in str(e)


def test_get_ntpd_sources():
    parser_result = NtpqPn(context_wrap(ntpd_output))
    assert parser_result.data[0].get('source') == 'ntp103.cm4.tbsi'
    assert parser_result.data[1].get('flag') == '+'
    assert parser_result.data[1].get('source') == 'ntp104.cm4.tbsi'
    parser_result2 = NtpqPn(context_wrap(ntpd_qn))
    assert parser_result2.data[0].get('source') == '202.118.1.81'
    assert parser_result2.data[0].get('flag') == ' '
    with pytest.raises(SkipComponent) as (e):
        NtpqPn(context_wrap(ntp_connection_issue))
    assert 'NTP service is down' in str(e)