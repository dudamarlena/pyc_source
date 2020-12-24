# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/services/localdisk_service.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 15608 bytes
"""LVM based local disk management service."""
import math, errno, logging, os, re, subprocess
from .. import cgroups
from .. import exc
from .. import fs
from .. import logcontext as lc
from .. import lvm
from .. import sysinfo
from .. import utils
from .. import subproc
from ._base_service import BaseResourceServiceImpl
_LOGGER = lc.ContainerAdapter(logging.getLogger(__name__))
TREADMILL_MIN_VG_SIZE = utils.size_to_bytes('100M')
TREADMILL_IMG = 'treadmill.img'

class LocalDiskResourceService(BaseResourceServiceImpl):
    __doc__ = 'LocalDisk service implementation.\n    '
    __slots__ = ('_block_dev', '_default_read_bps', '_default_read_iops', '_default_write_bps',
                 '_default_write_iops', '_img_location', '_pending', '_reserve',
                 '_status', '_volumes')
    PAYLOAD_SCHEMA = (
     (
      'size', True, str),)
    TREADMILL_VG = 'treadmill'

    def __init__(self, block_dev=None, img_location=None, reserve='2G', default_read_bps='20M', default_write_bps='20M', default_read_iops=100, default_write_iops=100):
        super(LocalDiskResourceService, self).__init__()
        assert bool(block_dev is None) ^ bool(img_location is None)
        if block_dev is not None:
            self._block_dev = block_dev
            self._reserve = None
            self._img_location = None
        else:
            if img_location is not None:
                self._reserve = reserve
                self._img_location = os.path.realpath(img_location)
                self._block_dev = None
            else:
                raise ValueError('Need to provide either a block device or an image location.')
        self._status = {}
        self._volumes = {}
        self._pending = []
        self._default_read_bps = default_read_bps
        self._default_write_bps = default_write_bps
        self._default_read_iops = default_read_iops
        self._default_write_iops = default_write_iops

    def initialize(self, service_dir):
        super(LocalDiskResourceService, self).initialize(service_dir)
        need_init = False
        try:
            lvm.vgactivate(group=self.TREADMILL_VG)
        except subprocess.CalledProcessError:
            need_init = True

        if need_init:
            _LOGGER.info('Initialiazing Volume Group')
            if self._block_dev is None:
                self._block_dev = _init_block_dev(self._img_location, self._reserve)
            _init_vg(self.TREADMILL_VG, self._block_dev)
        lvs_info = lvm.lvsdisplay(group=self.TREADMILL_VG)
        for lv in lvs_info:
            lv['stale'] = True
            if lv['open_count']:
                _LOGGER.warning('Logical volume in use: %r', lv['block_dev'])
                continue

        volumes = {lv['name']:{k:lv[k] for k in ['name', 'block_dev', 'dev_major', 'dev_minor', 'stale']} for lv in lvs_info}
        self._volumes = volumes
        self._status = _refresh_vg_status(self.TREADMILL_VG)

    def synchronize(self):
        """Make sure that all stale volumes are removed.
        """
        modified = False
        for uniqueid in self._volumes.keys():
            if not self._volumes[uniqueid].get('stale', False):
                continue
            modified = True
            self._destroy_volume(uniqueid)

        if not modified:
            return
        for pending_id in self._pending:
            self._retry_request(pending_id)

        self._pending = []
        self._status = _refresh_vg_status(self.TREADMILL_VG)

    def report_status(self):
        return self._status

    def on_create_request(self, rsrc_id, rsrc_data):
        app_unique_name = rsrc_id
        size = rsrc_data['size']
        read_bps = self._default_read_bps
        write_bps = self._default_write_bps
        read_iops = self._default_read_iops
        write_iops = self._default_write_iops
        with lc.LogContext(_LOGGER, rsrc_id) as (log):
            log.logger.info('Processing request')
            size_in_bytes = utils.size_to_bytes(size)
            _, uniqueid = app_unique_name.rsplit('-', 1)
            existing_volume = uniqueid in self._volumes
            if not existing_volume:
                needed = math.ceil(size_in_bytes / self._status['extent_size'])
                if needed > self._status['extent_free']:
                    log.logger.info('Delaying request %r until %d extents are free', rsrc_id, needed)
                    self._pending.append(rsrc_id)
                    return
                lvm.lvcreate(volume=uniqueid, group=self.TREADMILL_VG, size_in_bytes=size_in_bytes)
                self._status = _refresh_vg_status(self.TREADMILL_VG)
            lv_info = lvm.lvdisplay(volume=uniqueid, group=self.TREADMILL_VG)
            cgrp = os.path.join('treadmill', 'apps', app_unique_name)
            cgroups.create('blkio', cgrp)
            major, minor = lv_info['dev_major'], lv_info['dev_minor']
            cgroups.set_value('blkio', cgrp, 'blkio.throttle.write_bps_device', '{major}:{minor} {bps}'.format(major=major, minor=minor, bps=utils.size_to_bytes(write_bps)))
            cgroups.set_value('blkio', cgrp, 'blkio.throttle.read_bps_device', '{major}:{minor} {bps}'.format(major=major, minor=minor, bps=utils.size_to_bytes(read_bps)))
            cgroups.set_value('blkio', cgrp, 'blkio.throttle.write_iops_device', '{major}:{minor} {iops}'.format(major=major, minor=minor, iops=write_iops))
            cgroups.set_value('blkio', cgrp, 'blkio.throttle.read_iops_device', '{major}:{minor} {iops}'.format(major=major, minor=minor, iops=read_iops))
            volume_data = {k:lv_info[k] for k in ['name', 'block_dev', 'dev_major', 'dev_minor']}
            self._volumes[lv_info['name']] = volume_data
        return volume_data

    def on_delete_request(self, rsrc_id):
        app_unique_name = rsrc_id
        with lc.LogContext(_LOGGER, rsrc_id):
            _, uniqueid = app_unique_name.rsplit('-', 1)
            if not self._destroy_volume(uniqueid):
                return
            for pending_id in self._pending:
                self._retry_request(pending_id)

            self._pending = []
            self._status = _refresh_vg_status(self.TREADMILL_VG)
        return True

    def _destroy_volume(self, uniqueid):
        """Try destroy a volume from LVM.
        """
        self._volumes.pop(uniqueid, None)
        try:
            lvm.lvremove(uniqueid, group=self.TREADMILL_VG)
        except subprocess.CalledProcessError:
            _LOGGER.warning('Ignoring unknow volume %r', uniqueid)
            return False

        _LOGGER.info('Destroyed volume %r', uniqueid)
        return True

    def _retry_request(self, rsrc_id):
        """Force re-evaluation of a request.
        """
        request_lnk = os.path.join(self._service_rsrc_dir, rsrc_id)
        _LOGGER.debug('Updating %r', rsrc_id)
        try:
            os.lchown(request_lnk, os.getuid(), os.getgid())
        except OSError as err:
            if err.errno != errno.ENOENT:
                raise


def _refresh_vg_status(group):
    """Query LVM for the current volume group status.
    """
    vg_info = lvm.vgdisplay(group=group)
    status = {'name': vg_info['name'], 
     'extent_size': utils.size_to_bytes('{kb}k'.format(kb=vg_info['extent_size'])), 
     'extent_free': vg_info['extent_free'], 
     'extent_nb': vg_info['extent_nb'], 
     'size': utils.size_to_bytes('{kb}k'.format(kb=vg_info['extent_nb'] * vg_info['extent_size']))}
    _LOGGER.info('Group %r available space: %s (bytes)', group, status['size'])
    return status


def _init_vg(group, block_dev):
    """Initialize the 'treadmill' volume group.

    :param group:
        Name of the LVM Volume Group.
    :type group:
        ``str``
    :param block_dev:
        LVM Physical Volume device backing the Volume Group
    :type block_dev:
        ``str``
    """
    try:
        lvm.vgactivate(group)
        return
    except subprocess.CalledProcessError:
        pass

    lvm.pvcreate(device=block_dev)
    lvm.vgcreate(group, device=block_dev)
    lvm.vgactivate(group)


def _init_block_dev(img_location, reserve='2G'):
    """Initialize a block_dev suitable to back the Treadmill Volume Group.

    The physical volume size will be auto-size based on the available capacity
    minus the reserved size.

    :param img_location:
        Path name to the file which is going to back the new volume group.
    :type img_location:
        ``str``
    :param reserved:
        Reserved amount of free filesystem space to leave to the OS, in bytes
        or using a literal qualifier (e.g. "2G").
    :type size:
        ``int`` or ``str``
    """
    filename = os.path.join(img_location, TREADMILL_IMG)
    _init_loopback_devices()
    try:
        loop_dev = _loop_dev_for(filename)
    except subprocess.CalledProcessError:
        loop_dev = None
        _create_image(TREADMILL_IMG, img_location, reserve)

    if loop_dev is None:
        subproc.check_call([
         'losetup',
         '-f',
         filename])
        loop_dev = _loop_dev_for(filename)
    if loop_dev is None:
        raise exc.NodeSetupError('Unable to find /dev/loop device')
    _LOGGER.info('Using %r as backing for the physical volume group', loop_dev)
    return loop_dev


def _create_image(img_name, img_location, reserve):
    """Create a sparse file of the appropriate size.
    """
    fs.mkdir_safe(img_location)
    filename = os.path.join(img_location, img_name)
    retries = 10
    while retries > 0:
        retries -= 1
        try:
            stats = os.stat(filename)
            os.unlink(filename)
            _LOGGER.info('Disk image found and unlinked: %r; stat: %r', filename, stats)
        except OSError as err:
            if err.errno == errno.ENOENT:
                pass
            else:
                raise

        available_size = sysinfo.disk_usage(img_location)
        reserved_size = utils.size_to_bytes(reserve)
        image_size_bytes = available_size.free - reserved_size
        if available_size.free < reserved_size + TREADMILL_MIN_VG_SIZE:
            raise exc.NodeSetupError('Not enough free disk space')
        if fs.create_excl(filename, image_size_bytes):
            break

    if retries == 0:
        raise exc.NodeSetupError('Something is messing with disk image creation')


_TREADMILL_LOOPDEV_NB = 8

def _init_loopback_devices():
    """Create and initialize loopback devices."""
    for i in range(0, _TREADMILL_LOOPDEV_NB):
        if not os.path.exists('/dev/loop%s' % i):
            subproc.check_call(['mknod', '-m660', '/dev/loop%s' % i, 'b',
             '7', str(i)])
            subproc.check_call(['chown', 'root.disk', '/dev/loop%s' % i])
            continue


def _loop_dev_for(filename):
    """Lookup the loop device associated with a given filename.

    :param filename:
        Name of the file
    :type filename:
        ``str``
    :returns:
        Name of the loop device or None if not found
    :raises:
        subprocess.CalledProcessError if the file doesn't exist
    """
    filename = os.path.realpath(filename)
    loop_dev = subproc.check_output([
     'losetup',
     '-j',
     filename])
    loop_dev = loop_dev.strip()
    match = re.match('^(?P<loop_dev>[^:]+):.*\\({fname}\\)'.format(fname=filename), loop_dev)
    if match is not None:
        loop_dev = match.groupdict()['loop_dev']
    else:
        loop_dev = None
    return loop_dev