# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lpstat.py
# Compiled at: 2019-05-16 13:41:33
"""
Tests for lpstat parser
=======================

Note, that date time is localized (according to LC_TIME).

"""
import pytest
from insights.parsers.lpstat import LpstatPrinters
from insights.tests import context_wrap
LPSTAT_P_OUTPUT = '\nprinter idle_printer is idle.  enabled since Fri 20 Jan 2017 09:55:50 PM CET\nprinter disabled_printer disabled since Wed 15 Feb 2017 12:01:11 PM EST -\n    reason unknown\nprinter processing_printer now printing local_printer-1234.  enabled since Wed 15 Feb 2017 12:01:11 PM EST\n'
LPSTAT_P_OUTPUT_UKNOWN_STATE = '\nprinter unknown_printer may be jammed.  enabled since Fri 20 Jan 2017 09:55:50 PM CET\n'

def test_lpstat_parse():
    lpstat = LpstatPrinters(context_wrap(LPSTAT_P_OUTPUT))
    assert len(lpstat.printers) == 3
    idle_printer = lpstat.printers[0]
    disabled_printer = lpstat.printers[1]
    processing_printer = lpstat.printers[2]
    assert set(idle_printer) == set(['name', 'status']), 'Printer dict should contain (only) "name" and "status" keys'
    assert idle_printer['name'] == 'idle_printer'
    assert idle_printer['status'] == 'IDLE'
    assert set(disabled_printer) == set(['name', 'status']), 'Printer dict should contain (only) "name" and "status" keys'
    assert disabled_printer['name'] == 'disabled_printer'
    assert disabled_printer['status'] == 'DISABLED'
    assert set(processing_printer) == set(['name', 'status']), 'Printer dict should contain (only) "name" and "status" keys'
    assert processing_printer['name'] == 'processing_printer'
    assert processing_printer['status'] == 'PROCESSING'


def test_lpstat_parse_unknown_state():
    lpstat = LpstatPrinters(context_wrap(LPSTAT_P_OUTPUT_UKNOWN_STATE))
    assert len(lpstat.printers) == 1
    unknown_printer = lpstat.printers[0]
    assert set(unknown_printer) == set(['name', 'status']), 'Printer dict should contain (only) "name" and "status" keys'
    assert unknown_printer['name'] == 'unknown_printer'
    assert unknown_printer['status'] == 'UNKNOWN'


@pytest.mark.parametrize('status,expected_name', [
 ('IDLE', 'idle_printer'),
 ('DISABLED', 'disabled_printer'),
 ('PROCESSING', 'processing_printer')])
def test_lpstat_printer_names_by_status(status, expected_name):
    lpstat = LpstatPrinters(context_wrap(LPSTAT_P_OUTPUT))
    names = lpstat.printer_names_by_status(status)
    assert names == [expected_name]