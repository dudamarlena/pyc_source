# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/hl7/test_hl7v2.py
# Compiled at: 2013-05-25 04:38:30
import hl7v2
from hl7v2 import *
import os
message = 'MSH|^~\\&|CLINICOM|SHS|BPH-ADT_R|BPH-ADT_R|||ADT^A01|20100606233845315|P|2.3.1||||||8859/1\r'
message += 'EVN|A01|201006062338||||201006062338\r'
message += 'PID|1||0002389^^^CLINICOM||GUIMOND^Alexandre^^^^^L~GUIMOND^Alexandre^^^^^M||19720124|M|||11 rue des pénitents blancs^Appartement 806^TOULOUSE^^31000^F||0952694264|||0||100009873^^^CLINICOM\r'
message += 'PV1|1|I|A7N|R|||||||||||||||100009873^^^CLINICOM|||||||||||||||||||||||||201006062338\r'
message += 'ZFU|||||1701|201006062338\r'

def test_hl7message():
    m = hl7Message(message)
    assert m.is_hl7v2() == True
    assert m.get_segment_by_name('PID').name == 'PID'
    assert m.get_segment_by_name('ZFU').name == 'ZFU'
    assert len(m) == 5
    assert isinstance(m.segments[0], hl7Segment) == True
    assert m.is_multivalue() == True
    assert m.type == 'ADT'
    assert m.event == 'A01'
    assert m.id == '20100606233845315'
    assert m.version == '2.3.1'
    assert m.datetime == ''
    assert m.charset == '8859/1'
    assert str(m[2][0]) == 'PID'
    assert m.is_empty() == False
    assert str(m.get_data('[2][0]')) == 'PID'
    assert str(m.get_data('[1][17]')) == ''
    assert m.get_segmentindex('PID') == 2
    assert m.get_segmentindex('PV1') == 3
    assert str(m.get_data_for_segment('PID', '[0]')) == 'PID'
    assert str(m.get_data_for_segment('EVN', '[1]')) == 'A01'
    assert str(m.get_data_for_segment('EVN', '[17]')) == ''


def test_hl7message_load():
    m = hl7Message()
    assert m.is_empty() == True
    assert m.is_hl7v2() == False
    assert m.load(os.path.join(os.path.dirname(__file__), 'examples/ADT/A01/adt06072.hl7')) == True
    assert m.is_hl7v2() == True
    assert len(m) == 5
    sevn = m.get_segment_by_name('EVN')
    assert str(m[1][1]) == 'A01'
    assert str(sevn.fields[1]) == 'A01'
    assert str(sevn.fields[6]) == '201006062338'
    spid = m.get_segment_by_name('PID')
    assert str(spid.fields[3].values[0].components[0]) == '0002389'
    assert m.is_empty() == False


def test_hl7segments():
    m = hl7Message(message)
    spid = m.get_segment_by_name('PID')
    szfu = m.get_segment_by_name('ZFU')
    assert spid.name == 'PID'
    assert len(spid) == 19
    assert len(szfu) == 7
    assert isinstance(spid.fields[0], hl7Field) == True
    assert spid.is_multivalue() == True
    assert str(szfu) == 'ZFU|||||1701|201006062338'


def test_hl7fields():
    m = hl7Message(message)
    spid = m.get_segment_by_name('PID')
    pidfields = spid.fields
    assert pidfields[3].is_multivalue() == False
    assert len(pidfields[3]) == 1
    assert len(pidfields[5]) == 2
    assert pidfields[5].is_multivalue() == True
    assert isinstance(pidfields[0].values[0], hl7Value) == True


def test_hl7values():
    m = hl7Message(message)
    spid = m.get_segment_by_name('PID')
    pidfields = spid.fields
    pnamevalues = pidfields[5].values
    assert len(pnamevalues[1].components) == 7
    assert str(pnamevalues[1]) == 'GUIMOND^Alexandre^^^^^M'
    assert isinstance(pnamevalues[0].components[0], hl7Component) == True
    assert pnamevalues[0].is_multivalue() == True


def test_hl7components():
    m = hl7Message(message)
    spid = m.get_segment_by_name('PID')
    cnames = spid.fields[5].values[1].components
    assert len(cnames) == 7
    assert str(cnames[0]) == 'GUIMOND'
    assert str(cnames[1]) == 'Alexandre'
    assert str(cnames[6]) == 'M'
    assert cnames[0].is_multivalue() == False


if __name__ == '__main__':
    import doctest, nose
    doctest.testmod(hl7v2)
    nose.main()