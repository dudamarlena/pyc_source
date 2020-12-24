# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pacemaker_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.pacemaker_log import PacemakerLog
from insights.tests import context_wrap
from datetime import datetime
PACEMAKER_LOG = "\nAug 21 12:58:32 [11661] example.redhat.com       crmd:     info: crm_timer_popped: \tPEngine Recheck Timer (I_PE_CALC) just popped (900000ms)\nAug 21 12:58:32 [11661] example.redhat.com       crmd:   notice: do_state_transition: \tState transition S_IDLE -> S_POLICY_ENGINE [ input=I_PE_CALC cause=C_TIMER_POPPED origin=crm_timer_popped ]\nAug 21 12:58:32 [11661] example.redhat.com       crmd:     info: do_state_transition: \tProgressed to state S_POLICY_ENGINE after C_TIMER_POPPED\nAug 21 12:58:32 [11656] example.redhat.com        cib:     info: cib_process_request: \tCompleted cib_query operation for section 'all': OK (rc=0, origin=local/crmd/262, version=0.10.3)\nAug 21 12:58:32 [11660] example.redhat.com    pengine:   notice: unpack_config: \tOn loss of CCM Quorum: Ignore\nAug 21 12:58:32 [11660] example.redhat.com    pengine:     info: determine_online_status: \tNode d-d9ckmw1 is online\nAug 21 12:58:32 [11660] example.redhat.com    pengine:     info: determine_online_status: \tNode d-gqynnw1 is online\nAug 21 12:58:32 [11660] example.redhat.com    pengine:   notice: stage6: \tDelaying fencing operations until there are resources to manage\nAug 21 12:58:32 [11660] example.redhat.com    pengine:   notice: process_pe_message: \tCalculated Transition 125: /var/lib/pacemaker/pengine/pe-input-14.bz2\nAug 21 12:58:33 [11661] example.redhat.com       crmd:     info: do_state_transition: \tState transition S_POLICY_ENGINE -> S_TRANSITION_ENGINE [ input=I_PE_SUCCESS\n"

def test_pacemaker_log():
    pacemaker = PacemakerLog(context_wrap(PACEMAKER_LOG))
    assert 'Progressed to state S_POLICY_ENGINE after C_TIMER_POPPED' in pacemaker
    assert len(list(pacemaker.get_after(datetime(2017, 8, 21, 12, 58, 30)))) == 10