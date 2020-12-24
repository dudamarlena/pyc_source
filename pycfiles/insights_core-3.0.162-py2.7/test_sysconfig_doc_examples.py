# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_doc_examples.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers import sysconfig
from insights.parsers.sysconfig import ChronydSysconfig, DockerSysconfig, DockerSysconfigStorage
from insights.parsers.sysconfig import HttpdSysconfig, IrqbalanceSysconfig
from insights.parsers.sysconfig import LibvirtGuestsSysconfig, MemcachedSysconfig
from insights.parsers.sysconfig import MongodSysconfig, NtpdSysconfig
from insights.parsers.sysconfig import PrelinkSysconfig, VirtWhoSysconfig
from insights.parsers.sysconfig import SshdSysconfig
from insights.parsers.sysconfig import Up2DateSysconfig, PuppetserverSysconfig
from insights.parsers.sysconfig import NetconsoleSysconfig, ForemanTasksSysconfig
from insights.parsers.sysconfig import DockerStorageSetupSysconfig, DirsrvSysconfig
from insights.parsers.sysconfig import CorosyncSysconfig
from insights.parsers.sysconfig import IfCFGStaticRoute
from insights.parsers.sysconfig import NetworkSysconfig
import doctest
CHRONYDSYSCONFIG = ('\nOPTIONS="-d"\n#HIDE="me"\n').strip()
NTPDSYSCONFIG = ('\nOPTIONS="-x -g"\n#HIDE="me"\n').strip()
DOCKERSYSCONFIG = ('\nOPTIONS="--selinux-enabled"\nDOCKER_CERT_PATH="/etc/docker"\n').strip()
HTTPDSYSCONFIG = ('\nHTTPD=/usr/sbin/httpd.worker\nOPTIONS=\n').strip()
IRQBALANCESYSCONFIG = ('\n#IRQBALANCE_ONESHOT=yes\nIRQBALANCE_BANNED_CPUS=f8\nIRQBALANCE_ARGS="-d"\n').strip()
VIRTWHOSYSCONFIG = ('\n# Register ESX machines using vCenter\n# VIRTWHO_ESX=0\n# Register guests using RHEV-M\nVIRTWHO_RHEVM=1\n# Options for RHEV-M mode\nVIRTWHO_RHEVM_OWNER=\nTEST_OPT="A TEST"\n').strip()
MONGODSYSCONFIG = ('\nOPTIONS="--quiet -f /etc/mongod.conf"\n').strip()
MEMCACHEDSYSCONFIG = ('\nPORT="11211"\nUSER="memcached"\n# max connection 2048\nMAXCONN="2048"\nCACHESIZE="4096"\nOPTIONS="-U 0 -l 127.0.0.1"\n').strip()
LIBVIRTGUESTSSYSCONFIG = ('\nON_BOOT=ignore\n').strip()
PRELINKSYSCONFIG = ('\nPRELINKING=no\nPRELINK_OPTS=-mR\n').strip()
UP2DATESYSCONFIG = ('\nserverURL[comment]=Remote server URL\n#serverURL=https://rhnproxy.glb.tech.markit.partners\nserverURL=https://rhnproxy.glb.tech.markit.partners/XMLRPC\n').strip()
SSHDSYSCONFIG = ('\n# Configuration file for the sshd service.\n\n# The server keys are automatically generated if they are missing.\n# To change the automatic creation, adjust sshd.service options for\n# example using  systemctl enable sshd-keygen@dsa.service  to allow creation\n# of DSA key or  systemctl mask sshd-keygen@rsa.service  to disable RSA key\n# creation.\n\n# System-wide crypto policy:\n# To opt-out, uncomment the following line\n# CRYPTO_POLICY=\nCRYPTO_POLICY=\n').strip()
PUPPETSERVERCONFIG = ('\nUSER="puppet"\nGROUP="puppet"\nINSTALL_DIR="/opt/puppetlabs/server/apps/puppetserver"\nCONFIG="/etc/puppetlabs/puppetserver/conf.d"\nSTART_TIMEOUT=300\n').strip()
NETCONSOLESYSCONFIG = ('\nLOCALPORT=6666\n').strip()
FOREMANTASKSYSCONFG = ('\nFOREMAN_USER=foreman\nBUNDLER_EXT_HOME=/usr/share/foreman\nRAILS_ENV=production\nFOREMAN_LOGGING=warn\n').strip()
DOCKERSTORAGESETUPSYSCONFG = ('\nVG=vgtest\nAUTO_EXTEND_POOL=yes\n##name = mydomain\nPOOL_AUTOEXTEND_THRESHOLD=60\nPOOL_AUTOEXTEND_PERCENT=20\n').strip()
DIRSRVSYSCONFG = ('\n#STARTPID_TIME=10 ; export STARTPID_TIME\n#PID_TIME=600 ; export PID_TIME\nKRB5CCNAME=/tmp/krb5cc_995\nKRB5_KTNAME=/etc/dirsrv/ds.keytab\n').strip()
COROSYNCSYSCONFIG = ('\n# COROSYNC_INIT_TIMEOUT specifies number of seconds to wait for corosync\n# initialization (default is one minute).\nCOROSYNC_INIT_TIMEOUT=60\n# COROSYNC_OPTIONS specifies options passed to corosync command\n# (default is no options).\n# See "man corosync" for detailed descriptions of the options.\nCOROSYNC_OPTIONS=""\n').strip()
CONTEXT_PATH_DEVICE_1 = 'etc/sysconfig/network-scripts/route-test-net'
STATIC_ROUTE_1 = ('\nADDRESS0=10.65.223.0\nNETMASK0=255.255.254.0\nGATEWAY0=10.65.223.1\n').strip()
DOCKER_CONFIG_STORAGE = ('\nDOCKER_STORAGE_OPTIONS="--storage-driver devicemapper --storage-opt dm.fs=xfs --storage-opt dm.thinpooldev=/dev/mapper/dockervg-docker--pool --storage-opt dm.use_deferred_removal=true --storage-opt dm.use_deferred_deletion=true"\n').strip()
NETWORK_SYSCONFIG = ('\nNETWORKING=yes\nHOSTNAME=rhel7-box\nGATEWAY=172.31.0.1\nNM_BOND_VLAN_ENABLED=no\n').strip()

def test_sysconfig_doc():
    env = {'chronyd_syscfg': ChronydSysconfig(context_wrap(CHRONYDSYSCONFIG)), 
       'ntpd_syscfg': NtpdSysconfig(context_wrap(NTPDSYSCONFIG)), 
       'docker_syscfg': DockerSysconfig(context_wrap(DOCKERSYSCONFIG)), 
       'docker_syscfg_storage': DockerSysconfigStorage(context_wrap(DOCKER_CONFIG_STORAGE)), 
       'httpd_syscfg': HttpdSysconfig(context_wrap(HTTPDSYSCONFIG)), 
       'irqb_syscfg': IrqbalanceSysconfig(context_wrap(IRQBALANCESYSCONFIG)), 
       'vwho_syscfg': VirtWhoSysconfig(context_wrap(VIRTWHOSYSCONFIG)), 
       'mongod_syscfg': MongodSysconfig(context_wrap(MONGODSYSCONFIG)), 
       'memcached_syscfg': MemcachedSysconfig(context_wrap(MEMCACHEDSYSCONFIG)), 
       'libvirt_guests_syscfg': LibvirtGuestsSysconfig(context_wrap(LIBVIRTGUESTSSYSCONFIG)), 
       'prelink_syscfg': PrelinkSysconfig(context_wrap(PRELINKSYSCONFIG)), 
       'u2d_syscfg': Up2DateSysconfig(context_wrap(UP2DATESYSCONFIG)), 
       'netcs_syscfg': NetconsoleSysconfig(context_wrap(NETCONSOLESYSCONFIG)), 
       'sshd_syscfg': SshdSysconfig(context_wrap(SSHDSYSCONFIG)), 
       'pps_syscfg': PuppetserverSysconfig(context_wrap(PUPPETSERVERCONFIG)), 
       'ft_syscfg': ForemanTasksSysconfig(context_wrap(FOREMANTASKSYSCONFG)), 
       'dss_syscfg': DockerStorageSetupSysconfig(context_wrap(DOCKERSTORAGESETUPSYSCONFG)), 
       'dirsrv_syscfg': DirsrvSysconfig(context_wrap(DIRSRVSYSCONFG)), 
       'cs_syscfg': CorosyncSysconfig(context_wrap(COROSYNCSYSCONFIG)), 
       'conn_info': IfCFGStaticRoute(context_wrap(STATIC_ROUTE_1, CONTEXT_PATH_DEVICE_1)), 
       'net_syscfg': NetworkSysconfig(context_wrap(NETWORK_SYSCONFIG))}
    failed, total = doctest.testmod(sysconfig, globs=env)
    assert failed == 0