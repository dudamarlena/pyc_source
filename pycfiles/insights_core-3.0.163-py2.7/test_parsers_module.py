# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_parsers_module.py
# Compiled at: 2019-11-14 13:57:46
import pytest
from collections import OrderedDict
from insights.parsers import split_kv_pairs, unsplit_lines, parse_fixed_table
from insights.parsers import calc_offset, optlist_to_dict, keyword_search
from insights.parsers import parse_delimited_table, ParseException, SkipException
SPLIT_TEST_1 = ('\n# Comment line\n\n  keyword1 = value1   # Inline comments\n\n  # Comment indented\n  keyword3     # Key with no separator\n  keyword2 = value2a=True, value2b=100M\n\n').strip()
SPLIT_TEST_1_OD = OrderedDict([
 ('keyword1', 'value1'),
 ('keyword3', ''),
 ('keyword2', 'value2a=True, value2b=100M')])
SPLIT_TEST_2 = ('\n@ Comment line\n\n  keyword1: value1   @ Inline comments\n  keyword2 : value2a=True, value2b=100M\n\n  @ Comment indented\n  keyword3     @ Key with no separator\n').strip()
OFFSET_CONTENT_1 = ('\n  data 1 line\ndata 2 line\n').strip()
OFFSET_CONTENT_2 = ('\n#\nWarning line\nError line\n    data 1 line\n    data 2 line\nTrailing line\n\nBlank line above\nAnother trailing line\n    Yet another trailing line\n    Yet yet another trailing line\n').strip()

def test_split_kv_pairs():
    kv_pairs = split_kv_pairs(SPLIT_TEST_1.splitlines())
    assert len(kv_pairs) == 2
    assert kv_pairs == {'keyword1': 'value1', 
       'keyword2': 'value2a=True, value2b=100M'}
    kv_pairs = split_kv_pairs(SPLIT_TEST_1.splitlines(), filter_string='value2')
    assert len(kv_pairs) == 1
    assert kv_pairs == {'keyword2': 'value2a=True, value2b=100M'}
    kv_pairs = split_kv_pairs(SPLIT_TEST_1.splitlines(), use_partition=True)
    assert len(kv_pairs) == 3
    assert kv_pairs == {'keyword1': 'value1', 
       'keyword2': 'value2a=True, value2b=100M', 
       'keyword3': ''}
    kv_pairs = split_kv_pairs(SPLIT_TEST_1.splitlines(), use_partition=True, ordered=True)
    assert len(kv_pairs) == 3
    assert kv_pairs == SPLIT_TEST_1_OD
    kv_pairs = split_kv_pairs(SPLIT_TEST_2.splitlines(), comment_char='@', split_on=':')
    assert len(kv_pairs) == 2
    assert kv_pairs == {'keyword1': 'value1', 
       'keyword2': 'value2a=True, value2b=100M'}
    kv_pairs = split_kv_pairs(SPLIT_TEST_2.splitlines(), comment_char='@', split_on=':', filter_string='value2')
    assert len(kv_pairs) == 1
    assert kv_pairs == {'keyword2': 'value2a=True, value2b=100M'}
    kv_pairs = split_kv_pairs(SPLIT_TEST_2.splitlines(), comment_char='@', split_on=':', use_partition=True)
    assert len(kv_pairs) == 3
    assert kv_pairs == {'keyword1': 'value1', 
       'keyword2': 'value2a=True, value2b=100M', 
       'keyword3': ''}


SPLIT_LINES = ('\nLine one\nLine two part 1 \\\n         line two part 2\\\n         line two part 3\nLine three\n').strip()
SPLIT_LINES_2 = ('\nLine one\nLine two part 1 ^\n         line two part 2^\n         line two part 3\nLine three^\n').strip()
SPLIT_LINES_3 = '\nweb.default_taskmaster_tasks = RHN::Task::SessionCleanup, RHN::Task::ErrataQueue,\n    RHN::Task::ErrataEngine,\n    RHN::Task::DailySummary, RHN::Task::SummaryPopulation,\n    RHN::Task::RHNProc,\n    RHN::Task::PackageCleanup\n\ndb_host ='

def test_unsplit_lines():
    lines = list(unsplit_lines(SPLIT_LINES.splitlines()))
    assert len(lines) == 3
    assert lines[0] == 'Line one'
    assert lines[1] == 'Line two part 1          line two part 2         line two part 3'
    assert lines[2] == 'Line three'
    lines = list(unsplit_lines(SPLIT_LINES_2.splitlines(), cont_char='^'))
    assert len(lines) == 3
    assert lines[0] == 'Line one'
    assert lines[1] == 'Line two part 1          line two part 2         line two part 3'
    assert lines[2] == 'Line three'
    lines = list(unsplit_lines(SPLIT_LINES_3.splitlines(), cont_char=',', keep_cont_char=True))
    assert len(lines) == 4
    assert lines[0] == ''
    assert lines[1] == 'web.default_taskmaster_tasks = RHN::Task::SessionCleanup, RHN::Task::ErrataQueue,    RHN::Task::ErrataEngine,    RHN::Task::DailySummary, RHN::Task::SummaryPopulation,    RHN::Task::RHNProc,    RHN::Task::PackageCleanup'
    assert lines[2] == ''
    assert lines[3] == 'db_host ='


def test_calc_offset():
    assert calc_offset(OFFSET_CONTENT_1.splitlines(), target=[]) == 0
    assert calc_offset(OFFSET_CONTENT_1.splitlines(), target=[None]) == 0
    assert calc_offset(OFFSET_CONTENT_1.splitlines(), target=['data ']) == 0
    with pytest.raises(ValueError):
        calc_offset(OFFSET_CONTENT_1.splitlines(), target=['xdata '])
    with pytest.raises(ValueError):
        calc_offset(OFFSET_CONTENT_1.splitlines(), target=[
         'data '], invert_search=True)
    assert calc_offset(OFFSET_CONTENT_1.splitlines(), target=[
     'Trailing', 'Blank', 'Another '], invert_search=True) == 0
    assert calc_offset(OFFSET_CONTENT_2.splitlines(), target=[]) == 0
    assert calc_offset(OFFSET_CONTENT_2.splitlines(), target=['data ']) == 3
    assert calc_offset(reversed(OFFSET_CONTENT_2.splitlines()), target=[
     'Trailing', 'Blank', 'Another ', 'Yet'], invert_search=True) == 6
    return


FIXED_CONTENT_1 = ('\nColumn1    Column2    Column3\ndata1      data 2     data   3\n     data4 data5      data6\ndata     7            data   9\n').strip()
FIXED_CONTENT_1A = ('\n    WARNING\n    Column1    Column2    Column3\n    data1      data 2     data   3\n         data4 data5      data6\n    data     7            data   9\n').strip()
FIXED_CONTENT_1B = ('\nColumn1    Column2    Column3\ndata1      data 2\ndata4      data5      data6\n  data   7            data   9\n').strip()
FIXED_CONTENT_2 = ('\nWARNING WARNING WARNING\n Some message\nAnother message\nColumn1    Column2    Column3\ndata1      data 2     data   3\n     data4 data5      data6\ndata     7            data   9\n').strip()
FIXED_CONTENT_3 = ('\nWARNING WARNING WARNING\n Some message\nAnother message\nColumn1    Column2    Column3\ndata1      data 2     data   3\n     data4 data5      data6\ndata     7            data   9\nTrailing non-data line\n Another trailing non-data line\n').strip()
FIXED_CONTENT_4 = ('\nWARNING WARNING WARNING\n Some message\nAnother message\nColumn1    Column 2    Column 3\ndata1      data 2      data   3\n     data4 data5       data6\ndata     7             data   9\ndata10\nTrailing non-data line\n Another trailing non-data line\n').strip()
FIXED_CONTENT_DUP_HEADER_PREFIXES = ('\nNAMESPACE    NAME    LABELS\ndefault      foo     app=superawesome\n').strip()

def test_parse_fixed_table():
    data = parse_fixed_table(FIXED_CONTENT_1.splitlines())
    assert len(data) == 3
    assert data[0] == {'Column1': 'data1', 'Column2': 'data 2', 'Column3': 'data   3'}
    assert data[1] == {'Column1': 'data4', 'Column2': 'data5', 'Column3': 'data6'}
    assert data[2] == {'Column1': 'data     7', 'Column2': '', 'Column3': 'data   9'}
    data = parse_fixed_table(FIXED_CONTENT_1A.splitlines(), heading_ignore=['Column1 '])
    assert len(data) == 3
    assert data[0] == {'Column1': 'data1', 'Column2': 'data 2', 'Column3': 'data   3'}
    assert data[1] == {'Column1': 'data4', 'Column2': 'data5', 'Column3': 'data6'}
    assert data[2] == {'Column1': 'data     7', 'Column2': '', 'Column3': 'data   9'}
    data = parse_fixed_table(FIXED_CONTENT_1B.splitlines())
    assert len(data) == 3
    assert data[0] == {'Column1': 'data1', 'Column2': 'data 2', 'Column3': ''}
    assert data[1] == {'Column1': 'data4', 'Column2': 'data5', 'Column3': 'data6'}
    assert data[2] == {'Column1': 'data   7', 'Column2': '', 'Column3': 'data   9'}
    data = parse_fixed_table(FIXED_CONTENT_2.splitlines(), heading_ignore=['Column1 '])
    assert len(data) == 3
    assert data[0] == {'Column1': 'data1', 'Column2': 'data 2', 'Column3': 'data   3'}
    assert data[1] == {'Column1': 'data4', 'Column2': 'data5', 'Column3': 'data6'}
    assert data[2] == {'Column1': 'data     7', 'Column2': '', 'Column3': 'data   9'}
    data = parse_fixed_table(FIXED_CONTENT_3.splitlines(), heading_ignore=[
     'Column1 '], trailing_ignore=[
     'Trailing', 'Another'])
    assert len(data) == 3
    assert data[0] == {'Column1': 'data1', 'Column2': 'data 2', 'Column3': 'data   3'}
    assert data[1] == {'Column1': 'data4', 'Column2': 'data5', 'Column3': 'data6'}
    assert data[2] == {'Column1': 'data     7', 'Column2': '', 'Column3': 'data   9'}
    data = parse_fixed_table(FIXED_CONTENT_4.splitlines(), heading_ignore=[
     'Column1 '], header_substitute=[
     ('Column 2', 'Column_2'), ('Column 3', 'Column_3')], trailing_ignore=[
     'Trailing', 'Another'])
    assert len(data) == 4
    assert data[0] == {'Column1': 'data1', 'Column_2': 'data 2', 'Column_3': 'data   3'}
    assert data[1] == {'Column1': 'data4', 'Column_2': 'data5', 'Column_3': 'data6'}
    assert data[2] == {'Column1': 'data     7', 'Column_2': '', 'Column_3': 'data   9'}
    assert data[3] == {'Column1': 'data10', 'Column_2': '', 'Column_3': ''}
    data = parse_fixed_table([ 'foo' + line for line in FIXED_CONTENT_4.splitlines() ], heading_ignore=[
     'fooColumn1 '], header_substitute=[
     ('fooColumn1', 'Column1'), ('Column 2', 'Column_2'), ('Column 3', 'Column_3')], trailing_ignore=[
     'foo'])
    assert len(data) == 6
    assert data[4] == {'Column1': 'fooTrailing', 'Column_2': 'non-data li', 'Column_3': 'ne'}
    assert data[5] == {'Column1': 'foo Another', 'Column_2': 'trailing no', 'Column_3': 'n-data line'}
    data = parse_fixed_table(FIXED_CONTENT_DUP_HEADER_PREFIXES.splitlines())
    assert data[0] == {'NAMESPACE': 'default', 'NAME': 'foo', 'LABELS': 'app=superawesome'}


def test_parse_fixed_table_empty_exception():
    with pytest.raises(ParseException) as (pe):
        parse_fixed_table(FIXED_CONTENT_1B.splitlines(), empty_exception=True)
    assert 'Incorrect line:' in str(pe.value)


def test_optlist_standard():
    d = optlist_to_dict('key1,key2=val2,key1=val1,key3')
    assert sorted(d.keys()) == sorted(['key1', 'key2', 'key3'])
    assert d['key1'] == 'val1'
    assert d['key2'] == 'val2'
    assert d['key3'] is True


def test_optlist_no_vals():
    d = optlist_to_dict('key1,key2=val2,key1=val1,key3', kv_sep=None)
    assert sorted(d.keys()) == sorted(['key1', 'key1=val1', 'key2=val2', 'key3'])
    assert d['key1'] is True
    assert d['key1=val1'] is True
    assert d['key2=val2'] is True
    assert d['key3'] is True
    return


def test_optlist_strip_quotes():
    d = optlist_to_dict('key1="foo",key2=\'bar\',key3="mismatched quotes\',key4="inner\'quotes"', strip_quotes=True)
    assert sorted(d.keys()) == sorted(['key1', 'key2', 'key3', 'key4'])
    assert d['key1'] == 'foo'
    assert d['key2'] == 'bar'
    assert d['key3'] == '"mismatched quotes\''
    assert d['key4'] == "inner'quotes"


def test_optlist_with_spaces():
    d = optlist_to_dict('key1=foo,  key2=bar')
    assert 'key1' in d
    assert 'key2' in d


PS_AUX_TEST = '\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.0  0.0  19356  1544 ?        Ss   May31   0:01 /sbin/init\nroot      1821  0.0  0.0      0     0 ?        S    May31   0:25 [kondemand/0]\nroot      1864  0.0  0.0  18244   668 ?        Ss   May31   0:05 irqbalance --pid=/var/run/irqbalance.pid\nuser1    20160  0.0  0.0 108472  1896 pts/3    Ss   10:09   0:00 bash\nroot     20357  0.0  0.0   9120   760 ?        Ss   10:09   0:00 /sbin/dhclient -1 -q -lf /var/lib/dhclient/dhclient-extbr0.leases -pf /var/run/dhclient-extbr0.pid extbr0\nqemu     22673  0.8 10.2 1618556 805636 ?      Sl   11:38   1:07 /usr/libexec/qemu-kvm -name rhel7 -S -M rhel6.5.0 -enable-kvm -m 1024 -smp 2,sockets=2,cores=1,threads=1 -uuid 13798ffc-bc1e-d437-4f3f-2e0fa6c923ad\n'
MISSING_DATA_TEST = '\n  WARNING: Locking disabled. Be careful! This could corrupt your metadata.\nLVM2_PV_FMT|LVM2_PV_UUID|LVM2_DEV_SIZE|LVM2_PV_NAME|LVM2_PV_MAJOR|LVM2_PV_MINOR|LVM2_PV_MDA_FREE|LVM2_PV_MDA_SIZE|LVM2_PV_EXT_VSN|LVM2_PE_START|LVM2_PV_SIZE|LVM2_PV_FREE|LVM2_PV_USED|LVM2_PV_ATTR|LVM2_PV_ALLOCATABLE|LVM2_PV_EXPORTED|LVM2_PV_MISSING|LVM2_PV_PE_COUNT|LVM2_PV_PE_ALLOC_COUNT|LVM2_PV_TAGS|LVM2_PV_MDA_COUNT|LVM2_PV_MDA_USED_COUNT|LVM2_PV_BA_START|LVM2_PV_BA_SIZE|LVM2_PV_IN_USE|LVM2_PV_DUPLICATE|LVM2_VG_NAME\n  WARNING: Locking disabled. Be careful! This could corrupt your metadata.\n'
SUBSTITUTE_HEADERS_TEST = ('\naddress,port,state,read-only\n0.0.0.0,3000,LISTEN,N\n10.76.19.184,37500,ESTAB,Y\n').strip()
POSTGRESQL_LOG = ('\n schema |             table              |   rows\n public | rhnsnapshotpackage             | 47428950\n public | rhnpackagefile                 | 32174333\n public | rhnpackagecapability           | 12934215\n public | rhnpackagechangelogrec         | 11269933\n public | rhnchecksum                    | 10129746\n public | rhnactionconfigrevision        |  2894957\n public | rhnpackageprovides             |  2712442\n public | rhnpackagerequires             |  2532861\n public | rhn_command_target             |  1009152\n public | rhnconfigfilename              |        0\n public | rhnxccdfidentsystem            |        0\n public | rhndistchannelmap              |        0\n public | rhnactionvirtshutdown          |        0\n public | rhnpublicchannelfamily         |        0\n (402 rows)\n').strip()
TABLE2 = [
 'SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE',
 'HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe',
 'HA2|  22|       D22|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe']
TABLE3 = ('\nTHIS | IS | A | HEADER\nthis ^ is ^ some ^ content\nThis ^ is ^ more ^ content\n').strip()

def test_parse_delimited_table():
    assert parse_delimited_table([]) == []
    tbl = parse_delimited_table(PS_AUX_TEST.splitlines(), max_splits=10, heading_ignore=['USER'])
    assert tbl
    assert isinstance(tbl, list)
    assert len(tbl) == 6
    assert isinstance(tbl[0], dict)
    assert tbl[0] == {'%MEM': '0.0', 
       'TTY': '?', 'VSZ': '19356', 'PID': '1', '%CPU': '0.0', 'START': 'May31', 
       'COMMAND': '/sbin/init', 'USER': 'root', 'STAT': 'Ss', 
       'TIME': '0:01', 'RSS': '1544'}
    assert tbl[5]['COMMAND'] == '/usr/libexec/qemu-kvm -name rhel7 -S -M rhel6.5.0 -enable-kvm -m 1024 -smp 2,sockets=2,cores=1,threads=1 -uuid 13798ffc-bc1e-d437-4f3f-2e0fa6c923ad'
    tbl = parse_delimited_table(MISSING_DATA_TEST.splitlines(), delim='|', heading_ignore=[
     'LVM2_PV_FMT'], trailing_ignore=[
     'WARNING', 'ERROR', 'Cannot get lock'])
    assert isinstance(tbl, list)
    assert len(tbl) == 0
    tbl = parse_delimited_table(SUBSTITUTE_HEADERS_TEST.splitlines(), delim=',', strip=False, header_substitute=[
     ('read-only', 'read_only')])
    assert tbl
    assert isinstance(tbl, list)
    assert len(tbl) == 2
    assert isinstance(tbl[1], dict)
    assert tbl[1] == {'address': '10.76.19.184', 
       'port': '37500', 'state': 'ESTAB', 'read_only': 'Y'}
    tbl = parse_delimited_table(POSTGRESQL_LOG.splitlines(), delim='|', trailing_ignore=['('])
    assert isinstance(tbl, list)
    assert len(tbl) == 14
    assert isinstance(tbl[0], dict)
    assert tbl[0] == {'schema': 'public', 
       'table': 'rhnsnapshotpackage', 'rows': '47428950'}
    result = parse_delimited_table(TABLE3.splitlines(), delim='^', header_delim='|')
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)
    expected = [{'THIS': 'this', 'IS': 'is', 'A': 'some', 'HEADER': 'content'}, {'THIS': 'This', 'IS': 'is', 'A': 'more', 'HEADER': 'content'}]
    assert expected == result
    result = parse_delimited_table(TABLE2, delim='|', header_delim=None)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)
    expected = [
     {'SID': 'HA2', 'Nr': '16', 'Instance': 'D16', 'SAPLOCALHOST': 'lu0417', 'Version': '749, patch 10, changelist 1698137', 
        'DIR_EXECUTABLE': '/usr/sap/HA2/D16/exe'},
     {'SID': 'HA2', 'Nr': '22', 'Instance': 'D22', 'SAPLOCALHOST': 'lu0417', 'Version': '749, patch 10, changelist 1698137', 
        'DIR_EXECUTABLE': '/usr/sap/HA2/D22/exe'}]
    assert expected == result
    return


DATA_LIST = [{'name': 'test 1', 'role': 'server', 'memory_gb': 16, 'ssd': True}, {'name': 'test 2', 'role': 'server', 'memory_gb': 256, 'ssd': False}, {'name': 'test 3', 'role': 'server', 'memory_gb': 16, 'ssd': False}, {'name': 'test 4', 'role': 'embedded', 'memory_gb': 1, 'ssd': False}, {'name': 'test 5', 'role': 'workstation', 'memory_gb': 16, 'ssd': True}]
CERT_LIST = [
 {'status': 'MONITORING', 
    'stuck': 'no', 
    'key pair storage': "type=NSSDB,location='/etc/dirsrv/slapd-LDAP-EXAMPLE-COM',nickname='Server-Cert',token='NSS Certificate DB',pinfile='/etc/dirsrv/slapd-LDAP-EXAMPLE-COM/pwdfile.txt'", 
    'certificate': {'type': 'NSSDB', 
                    'location': '/etc/dirsrv/slapd-LDAP-EXAMPLE-COM', 
                    'nickname': 'Server-Cert', 
                    'token': 'NSS Certificate DB'}, 
    'CA': 'IPA', 
    'issuer': 'CN=Certificate Authority,O=LDAP.EXAMPLE.COM', 
    'subject': 'CN=master.LDAP.EXAMPLE.COM,O=LDAP.EXAMPLE.COM', 
    'expires': '2017-06-28 12:52:12 UTC', 
    'eku': 'id-kp-serverAuth,id-kp-clientAuth', 
    'pre-save command': '', 
    'post-save command': '/usr/lib64/ipa/certmonger/restart_dirsrv LDAP-EXAMPLE-COM', 
    'track': 'yes', 
    'auto-renew': 'yes'},
 {'status': 'MONITORING', 
    'stuck': 'no', 
    'key pair storage': "type=NSSDB,location='/etc/dirsrv/slapd-PKI-IPA',nickname='Server-Cert',token='NSS Certificate DB',pinfile='/etc/dirsrv/slapd-PKI-IPA/pwdfile.txt'", 
    'certificate': {'type': 'NSSDB', 
                    'location': '/etc/dirsrv/slapd-PKI-IPA', 
                    'nickname': 'Server-Cert', 
                    'token': 'NSS Certificate DB'}, 
    'CA': 'IPA', 
    'issuer': 'CN=Certificate Authority,O=EXAMPLE.COM', 
    'subject': 'CN=ldap.EXAMPLE.COM,O=EXAMPLE.COM', 
    'expires': '2017-06-28 12:52:13 UTC', 
    'eku': 'id-kp-serverAuth,id-kp-clientAuth', 
    'pre-save command': '', 
    'post-save command': '/usr/lib64/ipa/certmonger/restart_dirsrv PKI-IPA', 
    'track': 'yes', 
    'auto-renew': 'yes', 
    'dash- space': 'tested'}]

def test_keyword_search():
    assert len(keyword_search(DATA_LIST)) == 0
    assert keyword_search(DATA_LIST, cpu_count=4) == []
    assert keyword_search(DATA_LIST, memory_gb=8) == []
    results = keyword_search(DATA_LIST, role='embedded')
    assert len(results) == 1
    assert results[0] == DATA_LIST[3]
    results = keyword_search(DATA_LIST, memory_gb=16)
    assert len(results) == 3
    assert results == [ DATA_LIST[i] for i in (0, 2, 4) ]
    results = keyword_search(DATA_LIST, ssd=False)
    assert len(results) == 3
    assert results == [ DATA_LIST[i] for i in (1, 2, 3) ]
    assert len(keyword_search([], role='server')) == 0
    results = keyword_search(DATA_LIST, role__contains='e')
    assert len(results) == 4
    assert results == [ DATA_LIST[i] for i in (0, 1, 2, 3) ]
    results = keyword_search(DATA_LIST, role__startswith='e')
    assert len(results) == 1
    assert results[0] == DATA_LIST[3]
    results = keyword_search(CERT_LIST, pre_save_command='', key_pair_storage__startswith="type=NSSDB,location='/etc/dirsrv/slapd-PKI-IPA'")
    assert len(results) == 1
    assert results[0] == CERT_LIST[1]
    results = keyword_search(CERT_LIST, post_save_command__contains='PKI-IPA')
    assert len(results) == 1
    assert results[0] == CERT_LIST[1]
    results = keyword_search(CERT_LIST, status__lower_value='Monitoring')
    assert len(results) == 2
    assert results == CERT_LIST
    results = keyword_search(CERT_LIST, dash__space='tested')
    assert len(results) == 1
    assert results[0] == CERT_LIST[1]
    results = keyword_search(CERT_LIST, certificate__contains='type')
    assert len(results) == 2
    assert results == CERT_LIST
    assert keyword_search(CERT_LIST, certificate__contains='encryption') == []


def test_parse_exception():
    with pytest.raises(ParseException) as (e_info):
        raise ParseException('This is a parse exception')
    assert 'This is a parse exception' == str(e_info.value)


def test_skip_exception():
    with pytest.raises(SkipException) as (e_info):
        raise SkipException('This is a skip exception')
    assert 'This is a skip exception' == str(e_info.value)