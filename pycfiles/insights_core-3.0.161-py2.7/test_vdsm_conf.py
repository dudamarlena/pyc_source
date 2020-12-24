# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vdsm_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import vdsm_conf
from insights.tests import context_wrap
VDSM_CONF = '\n[vars]\nssl = true\ncpu_affinity = 1\n\n[addresses]\nmanagement_port = 54321\nqq = 345\n'
VDSM_LOGGER_CONF = "\n[loggers]\nkeys=root,vds,storage,virt,ovirt_hosted_engine_ha,ovirt_hosted_engine_ha_config,IOProcess,devel\n\n[handlers]\nkeys=console,syslog,logfile\n\n[formatters]\nkeys=long,simple,none,sysform\n\n[logger_root]\nlevel=DEBUG\nhandlers=syslog,logfile\npropagate=0\n\n[logger_vds]\nlevel=DEBUG\nhandlers=syslog,logfile\nqualname=vds\npropagate=0\n\n[logger_storage]\nlevel=DEBUG\nhandlers=logfile\nqualname=storage\npropagate=0\n\n[logger_ovirt_hosted_engine_ha]\nlevel=DEBUG\nhandlers=\nqualname=ovirt_hosted_engine_ha\npropagate=1\n\n[logger_ovirt_hosted_engine_ha_config]\nlevel=DEBUG\nhandlers=\nqualname=ovirt_hosted_engine_ha.env.config\npropagate=0\n\n[logger_IOProcess]\nlevel=DEBUG\nhandlers=logfile\nqualname=IOProcess\npropagate=0\n\n[logger_virt]\nlevel=DEBUG\nhandlers=logfile\nqualname=virt\npropagate=0\n\n[logger_devel]\nlevel=DEBUG\nhandlers=logfile\nqualname=devel\npropagate=0\n\n[handler_syslog]\nlevel=WARN\nclass=handlers.SysLogHandler\nformatter=sysform\nargs=('/dev/log', handlers.SysLogHandler.LOG_USER)\n\n[handler_logfile]\nclass=vdsm.logUtils.UserGroupEnforcingHandler\nargs=('vdsm', 'kvm', '/var/log/vdsm/vdsm.log',)\nfilters=storage.misc.TracebackRepeatFilter\nlevel=DEBUG\nformatter=long\n\n[handler_console]\nclass: StreamHandler\nargs: []\nformatter: none\n\n[formatter_simple]\nformat: %(asctime)s:%(levelname)s:%(message)s\n\n[formatter_none]\nformat: %(message)s\n\n[formatter_long]\nformat: %(asctime)s %(levelname)-5s (%(threadName)s) [%(name)s] %(message)s (%(module)s:%(lineno)d)\nclass: vdsm.logUtils.TimezoneFormatter\n\n[formatter_sysform]\nformat= vdsm %(name)s %(levelname)s %(message)s\ndatefmt=\n"

def test_vdsm_conf_ini():
    result = vdsm_conf.VDSMConfIni(context_wrap(VDSM_CONF))
    assert sorted(result.sections()) == sorted(['vars', 'addresses'])
    assert result.has_option('vars', 'ssl')
    assert result.getboolean('vars', 'ssl')
    assert result.getint('vars', 'cpu_affinity') == 1
    assert result.getint('addresses', 'management_port') == 54321
    assert result.getint('addresses', 'qq') == 345


def test_vdsm_logger_conf():
    conf = vdsm_conf.VDSMLoggerConf(context_wrap(VDSM_LOGGER_CONF))
    assert len(conf.sections()) == 18
    assert conf.has_option('loggers', 'keys') is True
    assert conf.getboolean('logger_root', 'propagate') is False
    assert conf.get('logger_ovirt_hosted_engine_ha', 'level') == 'DEBUG'
    assert conf.get('formatter_sysform', 'datefmt') == ''
    assert conf.has_option('formatter_long', 'class') is True
    assert conf.items('loggers') == {'keys': 'root,vds,storage,virt,ovirt_hosted_engine_ha,ovirt_hosted_engine_ha_config,IOProcess,devel'}


def test_documentation():
    env = {'conf': vdsm_conf.VDSMConfIni(context_wrap(VDSM_CONF)), 'vdsm_logger_conf': vdsm_conf.VDSMLoggerConf(context_wrap(VDSM_LOGGER_CONF))}
    failed_count, tests = doctest.testmod(vdsm_conf, globs=env)
    assert failed_count == 0