# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_scsi.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.scsi import SCSI
from insights.parsers import ParseException
from insights.tests import context_wrap
SCSI_OUTPUT = '\nAttached devices:\nHost: scsi0 Channel: 03 Id: 00 Lun: 00\n  Vendor: HP       Model: P420i            Rev: 3.54\n  Type:   RAID                             ANSI  SCSI revision: 05\nHost: scsi0 Channel: 00 Id: 00 Lun: 00\n  Vendor: HP       Model: LOGICAL VOLUME   Rev: 3.54\n  Type:   Direct-Access                    ANSI  SCSI revision: 05\nHost: scsi0 Channel: 00 Id: 00 Lun: 01\n  Vendor: HP       Model: LOGICAL VOLUME   Rev: 3.54\n  Type:   Direct-Access                    ANSI  SCSI revision: 05\nHost: scsi0 Channel: 00 Id: 00 Lun: 02\n  Vendor: HP       Model: LOGICAL VOLUME   Rev: 3.54\n  Type:   Direct-Access                    ANSI  SCSI revision: 05\nHost: scsi0 Channel: 00 Id: 00 Lun: 03\n  Vendor: HP       Model: LOGICAL VOLUME   Rev: 3.54\n  Type:   Direct-Access                    ANSI  SCSI revision: 05\n'
SCSI_OUTPUT_SINGLE_SPACED_ANSI_SCSI = '\nAttached devices:\nHost: scsi0 Channel: 00 Id: 00 Lun: 00\n  Vendor: VMware   Model: Virtual disk     Rev: 1.0\n  Type:   Direct-Access                    ANSI SCSI revision: 02\nHost: scsi0 Channel: 00 Id: 01 Lun: 00\n  Vendor: VMware   Model: Virtual disk     Rev: 1.0\n  Type:   Direct-Access                    ANSI SCSI revision: 02\nHost: scsi0 Channel: 00 Id: 02 Lun: 00\n  Vendor: VMware   Model: Virtual disk     Rev: 1.0\n  Type:   Direct-Access                    ANSI SCSI revision: 02\nHost: scsi0 Channel: 00 Id: 03 Lun: 00\n  Vendor: VMware   Model: Virtual disk     Rev: 1.0\n  Type:   Direct-Access                    ANSI SCSI revision: 02\n'
SCSI_OUTPUT_MISSING_HEADER = '\nHost: scsi0 Channel: 03 Id: 00 Lun: 00\n  Vendor: HP       Model: P420i            Rev: 3.54\n  Type:   RAID                             ANSI  SCSI revision: 05\n'
SCSI_OUTPUT_INNORMAL_VEMDOR_LINE = '\nAttached devices:\nHost: scsi0 Channel: 03 Id: 00 Lun: 00\n  Vendor: HP       Model: P420i            Rev: 3.:\n  Type:   RAID                             ANSI  SCSI revision: 05\n'
SCSI_OUTPUT_EMPTY = '\n'

def test_parse():
    context = context_wrap(SCSI_OUTPUT)
    result = SCSI(context)
    assert len(result) == 5
    r = result[0]
    assert r.host == 'scsi0'
    assert r.get('host') == 'scsi0'
    assert r.channel == '03'
    assert r.id == '00'
    assert r.lun == '00'
    assert r.vendor == 'HP'
    assert r.model == 'P420i'
    assert r.rev == '3.54'
    assert r.type == 'RAID'
    assert r.ansi__scsi_revision == '05'
    r = result[1]
    assert r.model == 'LOGICAL VOLUME'
    r = result[4]
    assert r.type == 'Direct-Access'
    assert [ disc.vendor for disc in result ] == ['HP'] * 5


def test_single_spaced_ansi_scsi():
    result = SCSI(context_wrap(SCSI_OUTPUT_SINGLE_SPACED_ANSI_SCSI))
    assert len(result) == 4


def test_missing_header():
    with pytest.raises(ParseException) as (excinfo):
        result = SCSI(context_wrap(SCSI_OUTPUT_MISSING_HEADER))
        assert result is None
    assert 'Expected Header: Attached devices:' in str(excinfo.value)
    return


def test_missing_innormal_rev():
    with pytest.raises(ParseException) as (excinfo):
        result = SCSI(context_wrap(SCSI_OUTPUT_INNORMAL_VEMDOR_LINE))
        assert result is None
    assert 'Parse error for current line:' in str(excinfo.value)
    return


def test_empty():
    with pytest.raises(ParseException) as (excinfo):
        result = SCSI(context_wrap(SCSI_OUTPUT_EMPTY))
        assert result is None
    assert 'Empty content of file /proc/scsi/scsi' in str(excinfo.value)
    return