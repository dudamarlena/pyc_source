# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_tuned_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import tuned_conf
from insights.parsers.tuned_conf import TunedConfIni
from insights.tests import context_wrap
from insights.contrib.ConfigParser import NoSectionError, NoOptionError
TUNED_CONF = ('\n#\n# tuned configuration main service\n#\n\n[main]\n# Interval for monitoring and tuning. Default is 10s.\ninterval=10\n\n#\n# Disk monitoring section\n#\n[DiskMonitor]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\n# enabled=False\n\n#\n# Disk tuning section\n#\n[DiskTuning]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\n# enabled=False\n#hdparm=False\nalpm=False\n\n#\n# Net monitoring section\n#\n[NetMonitor]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\n enabled=\n\n#\n# Net tuning section\n#\n[NetTuning]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\nenabled=False\n\n#\n# CPU monitoring section\n#\n[CPUMonitor]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\nenabled=False\n\n#\n# CPU tuning section\n#\n[CPUTuning]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\nenabled=False\n').strip()
TUNED_CONF_DOCS = ('\n#\n# Net tuning section\n#\n[NetTuning]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\n enabled=False\n\n#\n# CPU monitoring section\n#\n[CPUMonitor]\n# Enabled or disable the plugin. Default is True. Any other value\n# disables it.\n# enabled=False\n').strip()

def test_documentation():
    env = {'tuned_obj': tuned_conf.TunedConfIni(context_wrap(TUNED_CONF_DOCS))}
    failed_count, tests = doctest.testmod(tuned_conf, globs=env)
    assert failed_count == 0


def test_tuned_conf():
    result = tuned_conf.TunedConfIni(context_wrap(TUNED_CONF))
    assert sorted(result.sections()) == sorted(['CPUMonitor', 'CPUTuning', 'DiskMonitor', 'DiskTuning', 'NetMonitor', 'NetTuning', 'main'])
    with pytest.raises(NoSectionError) as (exc):
        tuned_obj = TunedConfIni(context_wrap(TUNED_CONF))
        assert not tuned_obj.get('Xyz', 'Abc')
    assert "No section: 'Xyz'" in str(exc)
    with pytest.raises(NoOptionError) as (exc):
        tuned_obj = TunedConfIni(context_wrap(TUNED_CONF))
        assert not tuned_obj.get('NetTuning', 'Abc')
    assert "No option 'Abc' in section: 'NetTuning'" in str(exc)
    with pytest.raises(ValueError) as (exc):
        tuned_obj = TunedConfIni(context_wrap(TUNED_CONF))
        assert not tuned_obj.getboolean('main', 'interval')
    assert 'Not a boolean: 10' in str(exc)
    assert tuned_obj.get('CPUMonitor', 'enabled') == 'False'
    assert tuned_obj.getboolean('CPUMonitor', 'enabled') is False
    assert tuned_obj.get('NetMonitor', 'enabled') == ''