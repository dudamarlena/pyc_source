# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_docker_storage_setup.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import DockerStorageSetupSysconfig
from insights.tests import context_wrap
DOCKER_STORAGE_SETUP1 = ('\n# Edit this file to override any configuration options specified in\n# /usr/lib/docker-storage-setup/docker-storage-setup.\n#\n# For more details refer to "man docker-storage-setup"\nVG=vgtest\nAUTO_EXTEND_POOL=yes\n##name = mydomain\nPOOL_AUTOEXTEND_THRESHOLD=60\nPOOL_AUTOEXTEND_PERCENT=20\n').strip()
DOCKER_STORAGE_SETUP2 = ('\n#comment\n# comment\n# comment = comment\n# comment = comment = comment\n#comment=comment\n#comment=comment=comment\noption_a=value_a\noption_b = value_b\noption_c= value_c\noption_d =value_d\nbroken_option_e = value_e = value_2_e\nbroken_option_f=value_f=value_2_f\nbroken_option_g\noption_h = value_h # some comment\noption_i = value_i # this must be accessible, even after all these errors\n').strip()

def test_docker_storage_setup():
    context = context_wrap(DOCKER_STORAGE_SETUP1)
    result = DockerStorageSetupSysconfig(context)
    assert 'POOL_AUTOEXTEND_THRESHOLD' in result
    assert '20' == result['POOL_AUTOEXTEND_PERCENT']
    assert 'name' not in result
    assert '##name' not in result
    assert 'vgtest' == result['VG']
    context = context_wrap(DOCKER_STORAGE_SETUP2)
    result = DockerStorageSetupSysconfig(context)
    assert 'comment' not in result
    assert 'broken_option_g' not in result
    assert 'option_i' not in result