# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_systemctl_show.py
# Compiled at: 2020-03-25 13:10:41
import doctest, pytest
from insights.parsers import systemctl_show, SkipException, ParseException
from insights.parsers.systemctl_show import SystemctlShowServiceAll, SystemctlShowTarget
from insights.tests import context_wrap
from insights.parsers.systemctl_show import SystemctlShowCinderVolume
from insights.parsers.systemctl_show import SystemctlShowHttpd
from insights.parsers.systemctl_show import SystemctlShowMariaDB
from insights.parsers.systemctl_show import SystemctlShowPulpCelerybeat
from insights.parsers.systemctl_show import SystemctlShowPulpResourceManager
from insights.parsers.systemctl_show import SystemctlShowPulpWorkers
from insights.parsers.systemctl_show import SystemctlShowQpidd
from insights.parsers.systemctl_show import SystemctlShowQdrouterd
from insights.parsers.systemctl_show import SystemctlShowSmartpdc
from insights.parsers.systemctl_show import SystemctlShowNginx
SYSTEMCTL_SHOW_EXAMPLES = '\nWatchdogUSec=0\nWatchdogTimestamp=Thu 2018-01-11 14:22:33 CST\nWatchdogTimestampMonotonic=105028136\nStartLimitInterval=10000000\nStartLimitBurst=5\nStartLimitAction=none\nFailureAction=none\nPermissionsStartOnly=no\nRootDirectoryStartOnly=no\nRemainAfterExit=no\nGuessMainPID=yes\nMainPID=2810\nControlPID=0\nFileDescriptorStoreMax=0\nStatusErrno=0\nResult=success\nExecMainStartTimestamp=Thu 2018-01-11 14:22:33 CST\nExecMainStartTimestampMonotonic=105028117\nExecMainExitTimestampMonotonic=0\nExecMainPID=2811\nLimitNOFILE=4096\n'

def test_systemctl_show_cinder_volume():
    context = SystemctlShowCinderVolume(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_mariadb():
    context = SystemctlShowMariaDB(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_pulp_workers():
    context = SystemctlShowPulpWorkers(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_pulp_resource_manager():
    context = SystemctlShowPulpResourceManager(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_pulp_celerybeat():
    context = SystemctlShowPulpCelerybeat(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_httpd():
    context = SystemctlShowHttpd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_qpidd():
    context = SystemctlShowQpidd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_qdrouterd():
    context = SystemctlShowQdrouterd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_smartpdc():
    context = SystemctlShowSmartpdc(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


def test_systemctl_show_nginx():
    context = SystemctlShowNginx(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))
    assert context['LimitNOFILE'] == '4096'
    assert len(context.data) == 21


SYSTEMCTL_SHOW_ALL_EXAMPLES = ('\nKillSignal=15\nSendSIGKILL=yes\nSendSIGHUP=no\nId=postfix.service\nNames=postfix.service\nRequires=basic.target\nWants=system.slice\nWantedBy=multi-user.target\nLimitNOFILE=65536\nLimitMEMLOCK=\nLimitLOCKS=18446744073709551615\n\nUser=postgres\nGroup=postgres\nMountFlags=0\nPrivateTmp=no\nPrivateNetwork=no\nPrivateDevices=no\nProtectHome=no\nProtectSystem=no\nSameProcessGroup=no\nIgnoreSIGPIPE=yes\nNoNewPrivileges=no\nSystemCallErrorNumber=0\nRuntimeDirectoryMode=0755\nKillMode=control-group\nKillSignal=15\nSendSIGKILL=yes\nSendSIGHUP=no\nId=postgresql.service\nNames=postgresql.service\nRequires=basic.target\nLimitMSGQUEUE=819200\nLimitNICE=0\nExecStartPre={ path=/usr/bin/postgresql-check-db-dir ; argv[]=/usr/bin/postgresql-check-db-dir ${PGDATA} ; ignore_errors=no ; start_time=[Tue 2019-11-19 23:55:49 EST]\nExecStart={ path=/usr/bin/pg_ctl ; argv[]=/usr/bin/pg_ctl start -D ${PGDATA} -s -o -p ${PGPORT} -w -t 300 ; ignore_errors=no ; start_time=[Tue 2019-11-19 23:55:50 EST]\nExecReload={ path=/usr/bin/pg_ctl ; argv[]=/usr/bin/pg_ctl reload -D ${PGDATA} -s ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; statu\nExecStop={ path=/usr/bin/pg_ctl ; argv[]=/usr/bin/pg_ctl stop -D ${PGDATA} -s -m fast ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; s\nSlice=system.slice\nControlGroup=/system.slice/postgresql.service\n\nId=tuned.service\nNames=tuned.service\nRequires=polkit.service basic.target dbus.service\nWants=system.slice\nWantedBy=multi-user.target\nConflicts=shutdown.target cpupower.service\nBefore=multi-user.target shutdown.target\nAfter=systemd-sysctl.service system.slice network.target systemd-journald.socket\nbasic.target dbus.service\nDocumentation=man:tuned(8) man:tuned.conf(5) man:tuned-adm(8)\nDescription=Dynamic System Tuning Daemon\nLoadState=loaded\nActiveState=active\nSubState=running\nFragmentPath=/usr/lib/systemd/system/tuned.service\nUnitFileState=enabled\nUnitFilePreset=enabled\nInactiveExitTimestamp=Tue 2019-11-19 23:55:50 EST\nInactiveExitTimestampMonotonic=9434667\nActiveEnterTimestamp=Tue 2019-11-19 23:55:53 EST\nActiveEnterTimestampMonotonic=12640144\nActiveExitTimestampMonotonic=0\nInactiveEnterTimestampMonotonic=0\nCanStart=yes\nCanStop=yes\nCanReload=no\nCanIsolate=no\nStopWhenUnneeded=no\nRefuseManualStart=no\nRefuseManualStop=no\nAllowIsolate=no\nDefaultDependencies=yes\nOnFailureJobMode=replace\nIgnoreOnIsolate=no\nIgnoreOnSnapshot=no\nNeedDaemonReload=no\nJobTimeoutUSec=0\nJobTimeoutAction=none\nConditionResult=yes\nAssertResult=yes\nConditionTimestamp=Tue 2019-11-19 23:55:50 EST\nConditionTimestampMonotonic=9429104\nAssertTimestamp=Tue 2019-11-19 23:55:50 EST\nAssertTimestampMonotonic=9429105\nABC=\nTransient=no\n').strip()
SYSTEMCTL_SHOW_ALL_EXP = ('\nKillSignal=15\nSendSIGKILL=yes\nSendSIGHUP=no\nRequires=basic.target\nWants=system.slice\nWantedBy=multi-user.target\nLimitNOFILE=65536\nLimitMEMLOCK=\nLimitLOCKS=18446744073709551615\n\n').strip()
SYSTEMCTL_SHOW_TARGET = ('\nId=network.target\nNames=network.target\nWantedBy=NetworkManager.service\nConflicts=shutdown.target\nBefore=tuned.service network-online.target rhsmcertd.service kdump.service httpd.service rsyslog.service rc-local.service insights-client.timer insights-client.service sshd.service postfix.service\nAfter=firewalld.service network-pre.target network.service NetworkManager.service\nDocumentation=man:systemd.special(7) http://www.freedesktop.org/wiki/Software/systemd/NetworkTarget\nDescription=Network\nLoadState=loaded\nActiveState=active\nSubState=active\nFragmentPath=/usr/lib/systemd/system/network.target\nUnitFileState=static\nUnitFilePreset=disabled\nInactiveExitTimestamp=Tue 2020-02-25 10:39:46 GMT\nInactiveExitTimestampMonotonic=15332468\nActiveEnterTimestamp=Tue 2020-02-25 10:39:46 GMT\nActiveEnterTimestampMonotonic=15332468\nActiveExitTimestampMonotonic=0\nInactiveEnterTimestampMonotonic=0\nCanStart=no\n\nId=swap.target\nNames=swap.target\nRequires=dev-mapper-rhel\\x2dswap.swap\nWantedBy=sysinit.target\nConflicts=shutdown.target\nBefore=sysinit.target tmp.mount\nAfter=dev-disk-by\\x2did-dm\\x2duuid\\x2dLVM\\x2deP73apHGoZ6LcvX230L0BUHQiPDhXceEkTtrOvL6P2biOWacMR3YS7rISVOgnPdc.swap dev-dm\\x2d1.swap dev-rhel-swap.swap dev-disk-by\\x2did-dm\\x2dname\\x2drhel\\x2dswap.swap dev-disk-by\\x2duuid-1ffaf940\\x2de836\\x2d4f08\\x2d9e5f\\x2d4dbe425d787f.swap dev-mapper-rhel\\x2dswap.swap\nDocumentation=man:systemd.special(7)\nDescription=Swap\nLoadState=loaded\nActiveState=active\nSubState=active\nFragmentPath=/usr/lib/systemd/system/swap.target\nUnitFileState=static\nUnitFilePreset=disabled\nInactiveExitTimestamp=Tue 2020-02-25 10:39:35 GMT\nInactiveExitTimestampMonotonic=4692015\nActiveEnterTimestamp=Tue 2020-02-25 10:39:35 GMT\nActiveEnterTimestampMonotonic=4692015\nActiveExitTimestamp=Tue 2020-02-25 10:39:34 GMT\nActiveExitTimestampMonotonic=3432423\n\nId=paths.target\nNames=paths.target\nWantedBy=basic.target\nConflicts=shutdown.target\nBefore=basic.target\nAfter=brandbot.path systemd-ask-password-console.path systemd-ask-password-wall.path\nDocumentation=man:systemd.special(7)\nDescription=Paths\nLoadState=loaded\nActiveState=active\nSubState=active\nFragmentPath=/usr/lib/systemd/system/paths.target\nUnitFileState=static\nUnitFilePreset=disabled\nInactiveExitTimestamp=Tue 2020-02-25 10:39:38 GMT\nInactiveExitTimestampMonotonic=7782864\nActiveEnterTimestamp=Tue 2020-02-25 10:39:38 GMT\nActiveEnterTimestampMonotonic=7782864\nActiveExitTimestamp=Tue 2020-02-25 10:39:34 GMT\nActiveExitTimestampMonotonic=3427228\nInactiveEnterTimestamp=Tue 2020-02-25 10:39:34 GMT\n\nId=sockets.target\nNames=sockets.target\nWants=rpcbind.socket systemd-initctl.socket systemd-udevd-kernel.socket dbus.socket dm-event.socket systemd-udevd-control.socket systemd-journald.socket systemd-shutdownd.socket\nWantedBy=basic.target\nConflicts=shutdown.target\nBefore=basic.target\nAfter=systemd-udevd-kernel.socket systemd-shutdownd.socket sshd.socket systemd-udevd-control.socket systemd-initctl.socket systemd-journald.socket rpcbind.socket syslog.socket dbus.socket\nDocumentation=man:systemd.special(7)\nDescription=Sockets\nLoadState=loaded\nActiveState=active\nSubState=active\nFragmentPath=/usr/lib/systemd/system/sockets.target\nUnitFileState=static\nUnitFilePreset=disabled\nInactiveExitTimestamp=Tue 2020-02-25 10:39:38 GMT\nInactiveExitTimestampMonotonic=7786499\nActiveEnterTimestamp=Tue 2020-02-25 10:39:38 GMT\nActiveEnterTimestampMonotonic=7786499\nActiveExitTimestamp=Tue 2020-02-25 10:39:34 GMT\nActiveExitTimestampMonotonic=3427060\n').strip()

def test_systemctl_show_service_all():
    svc_all = SystemctlShowServiceAll(context_wrap(SYSTEMCTL_SHOW_ALL_EXAMPLES))
    assert len(svc_all) == 3
    assert 'postfix.service' in svc_all
    assert 'LimitMEMLOCK' not in svc_all['postfix.service']
    assert svc_all['postfix.service']['LimitNOFILE'] == '65536'
    assert svc_all['postfix.service']['KillSignal'] == '15'
    assert svc_all['postfix.service']['LimitLOCKS'] == '18446744073709551615'
    assert len(svc_all['postfix.service']) == 10
    assert 'postgresql.service' in svc_all
    assert svc_all['postgresql.service']['User'] == 'postgres'
    assert svc_all['postgresql.service']['ControlGroup'] == '/system.slice/postgresql.service'
    assert len(svc_all['postgresql.service']) == 28
    assert 'tuned.service' in svc_all
    assert svc_all['tuned.service']['Id'] == 'tuned.service'
    assert svc_all['tuned.service']['Transient'] == 'no'
    assert 'ABC' not in svc_all['tuned.service']
    assert len(svc_all['tuned.service']) == 44


def test_systemctl_show_target():
    data = SystemctlShowTarget(context_wrap(SYSTEMCTL_SHOW_TARGET))
    assert 'network.target' in data
    assert data.get('network.target').get('WantedBy', None) == 'NetworkManager.service'
    assert data.get('network.target').get('RequiredBy', None) is None
    return


def test_systemctl_show_service_all_ab():
    with pytest.raises(SkipException):
        SystemctlShowServiceAll(context_wrap(''))
    with pytest.raises(ParseException):
        SystemctlShowServiceAll(context_wrap(SYSTEMCTL_SHOW_ALL_EXP))


def test_systemctl_show_doc_examples():
    env = {'systemctl_show_all': SystemctlShowServiceAll(context_wrap(SYSTEMCTL_SHOW_ALL_EXAMPLES)), 
       'systemctl_show_target': SystemctlShowTarget(context_wrap(SYSTEMCTL_SHOW_TARGET)), 
       'systemctl_show_cinder_volume': SystemctlShowCinderVolume(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_mariadb': SystemctlShowMariaDB(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_pulp_workers': SystemctlShowPulpWorkers(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_pulp_resource_manager': SystemctlShowPulpResourceManager(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_pulp_celerybeat': SystemctlShowPulpCelerybeat(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_httpd': SystemctlShowHttpd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_qpidd': SystemctlShowQpidd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_qdrouterd': SystemctlShowQdrouterd(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_smartpdc': SystemctlShowSmartpdc(context_wrap(SYSTEMCTL_SHOW_EXAMPLES)), 
       'systemctl_show_nginx': SystemctlShowNginx(context_wrap(SYSTEMCTL_SHOW_EXAMPLES))}
    failed, total = doctest.testmod(systemctl_show, globs=env)
    assert failed == 0