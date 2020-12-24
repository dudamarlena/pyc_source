# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_systemd_config.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers.systemd import config
from insights.parsers import SkipException
from insights.tests import context_wrap
from insights.core.plugins import ContentException
import doctest, pytest
SYSTEMD_DOCKER = ("\n[Unit]\nDescription=Docker Application Container Engine\nDocumentation=http://docs.docker.com\nAfter=network.target\nWants=docker-storage-setup.service\nRequires=rhel-push-plugin.socket\n\n[Service]\nType=notify\nNotifyAccess=all\nEnvironmentFile=-/etc/sysconfig/docker\nEnvironmentFile=-/etc/sysconfig/docker-storage\nEnvironmentFile=-/etc/sysconfig/docker-network\nEnvironment=GOTRACEBACK=crash\nExecStart=/bin/sh -c '/usr/bin/docker-current daemon \\\n          --authorization-plugin=rhel-push-plugin \\\n          --exec-opt native.cgroupdriver=systemd \\\n          $OPTIONS \\\n          $DOCKER_STORAGE_OPTIONS \\\n          $DOCKER_NETWORK_OPTIONS \\\n          $ADD_REGISTRY \\\n          $BLOCK_REGISTRY \\\n          $INSECURE_REGISTRY \\\n          2>&1 | /usr/bin/forward-journald -tag docker'\nLimitNOFILE=1048576\nLimitNPROC=1048576\nLimitCORE=infinity\nTimeoutStartSec=0\nMountFlags=slave\nRestart=on-abnormal\nStandardOutput=null\nStandardError=null\n\n[Install]\nWantedBy=multi-user.target\n").strip()
SYSTEMD_DOCKER_EMPTY = ('\nUnit docker.service is not loaded: No such file or directory\n').strip()
SYSTEMD_OPENSHIFT_NODE = ('\n[Unit]\nDescription=Atomic OpenShift Node\nAfter=docker.service\nAfter=openvswitch.service\nWants=docker.service\nDocumentation=https://github.com/openshift/origin\n\n[Service]\nType=notify\nEnvironmentFile=/etc/sysconfig/atomic-openshift-node\nEnvironment=GOTRACEBACK=crash\nExecStart=/usr/bin/openshift start node --config=${CONFIG_FILE} $OPTIONS\nLimitNOFILE=65536\nLimitCORE=infinity\nWorkingDirectory=/var/lib/origin/\nSyslogIdentifier=atomic-openshift-node\nRestart=always\nRestartSec=5s\nOOMScoreAdjust=-999\nExecStartPost=/usr/bin/sleep 10\nExecStartPost=/usr/sbin/sysctl --system\n\n[Install]\nWantedBy=multi-user.target\n\n').strip()
SYSTEMD_LOGIND_CONF = ('\n#  This file is part of systemd.\n#\n#  systemd is free software; you can redistribute it and/or modify it\n#  under the terms of the GNU Lesser General Public License as published by\n#  the Free Software Foundation; either version 2.1 of the License, or\n#  (at your option) any later version.\n#\n# Entries in this file show the compile time defaults.\n# You can change settings by editing this file.\n# Defaults can be restored by simply deleting this file.\n#\n# See logind.conf(5) for details.\n\n[Login]\n#NAutoVTs=6\nReserveVT=6\nKillUserProcesses=Yes\n#KillOnlyUsers=\n#KillExcludeUsers=root\n#InhibitDelayMaxSec=5\n#HandlePowerKey=poweroff\n#HandleSuspendKey=suspend\n#HandleHibernateKey=hibernate\n#HandleLidSwitch=suspend\n#HandleLidSwitchDocked=ignore\n#PowerKeyIgnoreInhibited=no\n#SuspendKeyIgnoreInhibited=no\n#HibernateKeyIgnoreInhibited=no\n#LidSwitchIgnoreInhibited=yes\n#IdleAction=ignore\n#IdleActionSec=30min\nRuntimeDirectorySize=10%\nRemoveIPC=no\n#UserTasksMax=\n').strip()
SYSTEMD_RPCBIND_SOCKET = ("\n[Unit]\nDescription=RPCbind Server Activation Socket\nDefaultDependencies=no\nWants=rpcbind.target\nBefore=rpcbind.target\n\n[Socket]\nListenStream=/run/rpcbind.sock\n\n# RPC netconfig can't handle ipv6/ipv4 dual sockets\nBindIPv6Only=ipv6-only\nListenStream=0.0.0.0:111\nListenDatagram=0.0.0.0:111\nListenStream=[::]:111\nListenDatagram=[::]:111\n\n[Install]\nWantedBy=sockets.target\n").strip()
SYSTEMD_SYSTEM_CONF = ('\n#  This file is part of systemd.\n#\n#  systemd is free software; you can redistribute it and/or modify it\n#  under the terms of the GNU Lesser General Public License as published by\n#  the Free Software Foundation; either version 2.1 of the License, or\n#  (at your option) any later version.\n#\n# Entries in this file show the compile time defaults.\n# You can change settings by editing this file.\n# Defaults can be restored by simply deleting this file.\n#\n# See systemd-system.conf(5) for details.\n\n[Manager]\n#LogLevel=info\n#LogTarget=journal-or-kmsg\n#LogColor=yes\n#LogLocation=no\n#DumpCore=yes\n#CrashShell=no\n#ShowStatus=yes\n#CrashChVT=1\n#CPUAffinity=1 2\n#JoinControllers=cpu,cpuacct net_cls,net_prio\nRuntimeWatchdogSec=0\nShutdownWatchdogSec=10min\n#CapabilityBoundingSet=\n#SystemCallArchitectures=\n#TimerSlackNSec=\n#DefaultTimerAccuracySec=1min\n#DefaultStandardOutput=journal\n#DefaultStandardError=inherit\n#DefaultTimeoutStartSec=90s\n#DefaultTimeoutStopSec=90s\n#DefaultRestartSec=100ms\n#DefaultStartLimitInterval=10s\n#DefaultStartLimitBurst=5\n#DefaultEnvironment=\n#DefaultCPUAccounting=no\n#DefaultBlockIOAccounting=no\n#DefaultMemoryAccounting=no\n#DefaultLimitCPU=\n#DefaultLimitFSIZE=\n#DefaultLimitDATA=\n#DefaultLimitSTACK=\n#DefaultLimitCORE=\n#DefaultLimitRSS=\n#DefaultLimitNOFILE=\n#DefaultLimitAS=\n#DefaultLimitNPROC=\n#DefaultLimitMEMLOCK=\n#DefaultLimitLOCKS=\n#DefaultLimitSIGPENDING=\n#DefaultLimitMSGQUEUE=\n#DefaultLimitNICE=\n#DefaultLimitRTPRIO=\n#DefaultLimitRTTIME=\n').strip()
SYSTEMD_SYSTEM_ORIGIN_ACCOUNTING = ('\n[Manager]\nDefaultCPUAccounting=yes\nDefaultMemoryAccounting=yes\n# systemd v230 or newer\nDefaultIOAccounting=yes\n# Deprecated, remove in future\nDefaultBlockIOAccounting=no\n').strip()

def test_systemd_docker():
    docker_service = config.SystemdDocker(context_wrap(SYSTEMD_DOCKER))
    assert docker_service.data['Unit']['After'] == 'network.target'
    assert docker_service.data['Service']['NotifyAccess'] == 'all'
    assert docker_service.data['Service']['Environment'] == 'GOTRACEBACK=crash'
    assert docker_service.data['Install']['WantedBy'] == 'multi-user.target'
    assert list(docker_service.data['Install'].keys()) == ['WantedBy']
    assert docker_service.data['Service']['ExecStart'] == "/bin/sh -c '/usr/bin/docker-current daemon --authorization-plugin=rhel-push-plugin --exec-opt native.cgroupdriver=systemd $OPTIONS $DOCKER_STORAGE_OPTIONS $DOCKER_NETWORK_OPTIONS $ADD_REGISTRY $BLOCK_REGISTRY $INSECURE_REGISTRY 2>&1 | /usr/bin/forward-journald -tag docker'"


def test_systemd_docker_empty():
    with pytest.raises(ContentException):
        config.SystemdDocker(context_wrap(SYSTEMD_DOCKER_EMPTY))


def test_systemd_openshift_node():
    openshift_node_service = config.SystemdOpenshiftNode(context_wrap(SYSTEMD_OPENSHIFT_NODE))
    assert openshift_node_service.data['Unit']['Wants'] == 'docker.service'
    assert openshift_node_service.data['Unit']['After'] == ['docker.service', 'openvswitch.service']


def test_systemd_system_conf():
    common_conf_info = config.SystemdSystemConf(context_wrap(SYSTEMD_SYSTEM_CONF))
    assert 'Manager' in common_conf_info
    print common_conf_info.doc
    assert common_conf_info['Manager']['RuntimeWatchdogSec'] == '0'
    assert common_conf_info['Manager']['ShutdownWatchdogSec'] == '10min'


def test_systemd_system_origin_accounting():
    common_system_origin_accounting = config.SystemdOriginAccounting(context_wrap(SYSTEMD_SYSTEM_ORIGIN_ACCOUNTING))
    assert 'Manager' in common_system_origin_accounting
    assert common_system_origin_accounting['Manager']['DefaultCPUAccounting'] == 'True'
    assert common_system_origin_accounting['Manager']['DefaultBlockIOAccounting'] == 'False'


def test_systemd_logind_conf():
    logind_conf = config.SystemdLogindConf(context_wrap(SYSTEMD_LOGIND_CONF))
    assert 'Login' in logind_conf
    assert logind_conf['Login']['RemoveIPC'] == 'False'
    assert logind_conf['Login']['RuntimeDirectorySize'] == '10%'


def test_systemd_rpcbind_socket_conf():
    rpcbind_socket = config.SystemdRpcbindSocketConf(context_wrap(SYSTEMD_RPCBIND_SOCKET))
    assert 'Socket' in rpcbind_socket
    assert rpcbind_socket['Socket']['ListenStream'] == ['/run/rpcbind.sock', '0.0.0.0:111', '[::]:111']
    assert rpcbind_socket['Socket']['ListenDatagram'] == ['0.0.0.0:111', '[::]:111']


def test_systemd_empty():
    with pytest.raises(SkipException):
        assert config.SystemdLogindConf(context_wrap('')) is None
    return


def test_doc_examples():
    env = {'docker_service': config.SystemdDocker(context_wrap(SYSTEMD_DOCKER)), 
       'system_conf': config.SystemdSystemConf(context_wrap(SYSTEMD_SYSTEM_CONF)), 
       'system_origin_accounting': config.SystemdOriginAccounting(context_wrap(SYSTEMD_SYSTEM_ORIGIN_ACCOUNTING)), 
       'openshift_node_service': config.SystemdOpenshiftNode(context_wrap(SYSTEMD_OPENSHIFT_NODE)), 
       'logind_conf': config.SystemdLogindConf(context_wrap(SYSTEMD_LOGIND_CONF)), 
       'rpcbind_socket': config.SystemdRpcbindSocketConf(context_wrap(SYSTEMD_RPCBIND_SOCKET))}
    failed, total = doctest.testmod(config, globs=env)
    assert failed == 0