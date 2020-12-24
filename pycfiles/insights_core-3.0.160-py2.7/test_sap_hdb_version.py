# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sap_hdb_version.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import SkipException, sap_hdb_version
from insights.parsers.sap_hdb_version import HDBVersion
from insights.tests import context_wrap
import pytest, doctest
HDB_VER_1 = ('\nHDB version info:\n  version:             2.00.030.00.1522210459\n  branch:              hanaws\n  machine config:      linuxx86_64\n  git hash:            bb2ff6b25b8eab5ab382c170a43dc95ae6ce298f\n  git merge time:      2018-03-28 06:14:19\n  weekstone:           2018.13.0\n  cloud edition:       0000.00.00\n  compile date:        2018-03-28 06:19:13\n  compile host:        ld2221\n  compile type:        rel\n').strip()
HDB_VER_2 = ('\nHDB version info:\n  version:             2.00.020.00.1500920972\n  branch:              fa/hana2sp02\n  git hash:            7f63b0aa11dca2ea54d450aa302319302c2eeaca\n  git merge time:      2017-07-24 20:29:32\n  weekstone:           0000.00.0\n  compile date:        2017-07-24 20:35:12\n  compile host:        ld4551\n  compile type:        rel\n').strip()
HDB_VER_NG_1 = ('\nsu: user hxeadm does not exist\n').strip()
HDB_VER_NG_2 = ('\nHDB version info:\n  version:             2.00.020.1500920972\n  branch:              fa/hana2sp02\n  git hash:            7f63b0aa11dca2ea54d450aa302319302c2eeaca\n  git merge time:      2017-07-24 20:29:32\n  weekstone:           0000.00.0\n  compile date:        2017-07-24 20:35:12\n  compile host:        ld4551\n').strip()
CMD_PATH = 'insights_commands/sudo_-iu_sr1adm_HDB_version'

def test_HDBVersion_doc():
    env = {'hdb_ver': HDBVersion(context_wrap(HDB_VER_1, path=CMD_PATH))}
    failed, total = doctest.testmod(sap_hdb_version, globs=env)
    assert failed == 0


def test_HDBVersion_ng():
    with pytest.raises(SkipException) as (e_info):
        HDBVersion(context_wrap(HDB_VER_NG_1))
    assert 'Incorrect content.' in str(e_info.value)
    with pytest.raises(SkipException) as (e_info):
        HDBVersion(context_wrap(HDB_VER_NG_2))
    assert 'Incorrect HDB version: 2.00.020.1500920972' in str(e_info.value)


def test_HDBVersion_1():
    hdb_ver = HDBVersion(context_wrap(HDB_VER_1, path=CMD_PATH))
    assert hdb_ver['branch'] == 'hanaws'
    assert hdb_ver['compile type'] == 'rel'
    assert hdb_ver['weekstone'] == '2018.13.0'


def test_HDBVersion_2():
    hdb_ver = HDBVersion(context_wrap(HDB_VER_2, path=CMD_PATH))
    assert hdb_ver['branch'] == 'fa/hana2sp02'
    assert hdb_ver['compile host'] == 'ld4551'
    assert 'compile_type' not in hdb_ver
    assert hdb_ver['weekstone'] == '0000.00.0'
    assert hdb_ver.major == '2'
    assert hdb_ver.revision == '020'
    assert hdb_ver.sid == 'sr1'