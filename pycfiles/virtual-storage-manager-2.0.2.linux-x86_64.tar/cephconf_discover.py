# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/agent/cephconf_discover.py
# Compiled at: 2016-06-13 14:11:03
"""Crush map parser..

Parse crush map in json format, and identify storage groups from ruleset.

"""
import json, operator
from vsm import utils
from vsm import exception
from vsm.openstack.common import log as logging
from vsm import flags
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class cephconf_discover:

    def __init__(self, json_file=None, keyring=None):
        self._keyring = keyring
        if json_file:
            with open(json_file, 'r') as (fh):
                ceph_report = json.load(fh)
        else:
            ceph_report = self._get_report()
        self._osds = {}
        self._mons = {}
        self.ceph_report = ceph_report
        if ceph_report:
            self._osds = ceph_report['osd_metadata']
            self._mons = ceph_report['monmap']['mons']

    def _get_report(self):
        report = ''
        stderr = ''
        try:
            if self._keyring:
                report, stderr = utils.execute('ceph', 'report', '--keyring', self._keyring, run_as_root=True)
            else:
                report, stderr = utils.execute('ceph', 'report', run_as_root=True)
            return json.loads(report)
        except exception.ProcessExecutionError:
            LOG.warn('Fail to get report from ceph: %s' % stderr)

    def get_osds(self):
        return self._osds

    def get_osd(self, id=0):
        if id >= 0:
            if id < len(self._osds):
                return self._osds[id]

    def fixup_osd_settings(self):
        osd_settings = '\n'
        for osd in self.get_osds():
            osd_settings += '[osd.%s]\n' % osd['id']
            osd_settings += 'host = %s\n' % osd['hostname']
            osd_settings += 'devs = %s\n' % osd['osd_data']
            osd_settings += 'osd journal = %s\n' % osd['osd_journal']
            osd_settings += 'cluster addr = %s\n' % osd['back_addr']
            osd_settings += 'public addr = %s\n\n' % osd['front_addr']

        return osd_settings

    def get_mons(self):
        return self._mons

    def get_mon(self, id=0):
        if id >= 0:
            if id < len(self._mons):
                return self._mons[id]

    def fixup_mon_settings(self):
        mon_settings = '\n'
        for mon in self.get_mons():
            mon_settings += '[mon.%s]\n' % mon['rank']
            mon_settings += 'host = %s\n' % mon['name']
            mon_settings += 'mon addr = %s\n\n' % mon['addr']

        return mon_settings

    def detect_ceph_conf(self):
        global_value_dict = {'heartbeat_interval': 10, 'osd_pool_default_size': self.ceph_report['osdmap']['pools'][0]['size'], 
           'osd_heartbeat_grace': 10, 
           'fsid': self.ceph_report['osdmap']['fsid']}
        global_settings = '\n[global]\nheartbeat interval = %(heartbeat_interval)s\nosd pool default size = %(osd_pool_default_size)s\nosd heartbeat grace = %(osd_heartbeat_grace)s\nkeyring = /etc/ceph/keyring.admin\nfsid = %(fsid)s\nauth supported = cephx\n        ' % global_value_dict
        osd_header_settings = '\n[osd]\nosd mount options xfs = rw,noatime,inode64,logbsize=256k,delaylog\nosd crush update on start = false\nfilestore xattr use omap = true\nkeyring = /etc/ceph/keyring.$name\nosd mkfs type = %(mkfs_type)s\nosd data = /var/lib/ceph/osd/osd$id\nosd heartbeat interval = 10\nosd heartbeat grace = 10\nosd mkfs options xfs = -f\nosd journal size = 0\n        ' % {'mkfs_type': self.ceph_report['osd_metadata'][0].get('filestore_backend', 'xfs')}
        mon_header_settings = '\n[mon]\nmon osd full ratio = .90\nmon data = /var/lib/ceph/mon/mon$id\nmon osd nearfull ratio = .75\nmon clock drift allowed = .200\n        '
        osd_settings = self.fixup_osd_settings()
        mon_settings = self.fixup_mon_settings()
        cephconf = global_settings + '\n' + osd_header_settings + '\n' + osd_settings + '\n' + mon_header_settings + '\n' + mon_settings + '\n'
        return cephconf


if __name__ == '__main__':
    discover = cephconf_discover('./report.json')
    print 'osds=%s' % discover.get_osds()
    print 'osd.0=%s' % discover.get_osd(1)
    osd_settings = discover.fixup_osd_settings()
    print osd_settings
    mon_settings = discover.fixup_mon_settings()
    print mon_settings