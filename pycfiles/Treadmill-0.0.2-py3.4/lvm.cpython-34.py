# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/lvm.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 9812 bytes
"""Linux Volume Manager operations."""
import logging, os, re
from . import subproc
_LOGGER = logging.getLogger(__name__)
_LVCREATE_EEXISTS_MSG_RE = re.compile('^  Logical volume "[^\\"]+" already exists in volume group "[^\\"]+"$')

def pvcreate(device):
    """Create a new LVM physical volume.
    """
    return subproc.check_call([
     'lvm',
     'pvcreate',
     '--force',
     '--yes',
     device])


def pvdisplay():
    """Gather LVM physical volume information.
    """
    cmd = [
     'lvm',
     'pvdisplay',
     '--colon']
    info = subproc.check_output(cmd)
    info_data = [line.strip().split(':') for line in info.strip().split('\n') if line]
    return [{'block_dev': pv_data[0],  'group': pv_data[1],  'status': pv_data[4],  'extent_size': int(pv_data[7], base=10),  'extent_nb': int(pv_data[8], base=10),  'extent_free': int(pv_data[9], base=10),  'extent_alloc': int(pv_data[10], base=10)} for pv_data in info_data]


def vgcreate(group, device):
    """Create a new LVM volume group.
    """
    return subproc.check_call([
     'lvm',
     'vgcreate',
     '--autobackup', 'n',
     group,
     device])


def vgremove(group):
    """Destroy a LVM volume group.
    """
    return subproc.check_call([
     'lvm',
     'vgremove',
     '--force',
     group])


def vgactivate(group):
    """Activate a LVM volume group.
    """
    return subproc.check_call([
     'lvm',
     'vgchange',
     '--activate', 'y',
     group])


def _parse_vg_data(vg_data):
    """Parse LVM volume group data.
    """
    if len(vg_data) != 17:
        _LOGGER.critical('Invalid volume group info: %r', vg_data)
        return
    return {'name': vg_data[0], 
     'access': vg_data[1], 
     'status': vg_data[2], 
     'number': int(vg_data[3], base=10), 
     'lv_max': int(vg_data[4], base=10), 
     'lv_cur': int(vg_data[5], base=10), 
     'lv_open_count': int(vg_data[6], base=10), 
     'max_size': int(vg_data[7], base=10), 
     'pv_max': int(vg_data[8], base=10), 
     'pv_cur': int(vg_data[9], base=10), 
     'pv_actual': int(vg_data[10], base=10), 
     'size': int(vg_data[11], base=10), 
     'extent_size': int(vg_data[12], base=10), 
     'extent_nb': int(vg_data[13], base=10), 
     'extent_alloc': int(vg_data[14], base=10), 
     'extent_free': int(vg_data[15], base=10), 
     'uuid': vg_data[16]}


def vgsdisplay():
    """Gather LVM volume groups information.
    """
    cmd = [
     'lvm',
     'vgdisplay',
     '--colon']
    info = subproc.check_output(cmd)
    info_data = [line.strip().split(':') for line in info.strip().split('\n') if line]
    return [_parse_vg_data(vg_data) for vg_data in info_data]


def vgdisplay(group):
    """Gather a LVM volume group information.
    """
    cmd = [
     'lvm',
     'vgdisplay',
     '--colon',
     group]
    info = subproc.check_output(cmd)
    info_data = [line.strip().split(':') for line in info.strip().split('\n') if line]
    assert len(info_data) == 1, 'Unexpected LVM output.'
    return _parse_vg_data(info_data[0])


def lvcreate(volume, size_in_bytes, group):
    """Create a new LVM logical volume.
    """
    cmd = [
     'lvm',
     'lvcreate',
     '--autobackup', 'n',
     '--size', '{size}B'.format(size=size_in_bytes),
     '--name', volume,
     group]
    return subproc.check_call(cmd)


def lvremove(volume, group):
    """Remove a LVM logical volume.
    """
    qualified_volume = os.path.join(group, volume)
    return subproc.check_call([
     'lvm',
     'lvremove',
     '--autobackup', 'n',
     '--force',
     qualified_volume])


def _parse_lv_data(lv_data):
    """Parse LVM logical volume data.
    """
    if len(lv_data) != 13:
        _LOGGER.critical('Invalid logical volume info: %r', lv_data)
        return
    return {'block_dev': lv_data[0], 
     'name': os.path.basename(lv_data[0]), 
     'group': lv_data[1], 
     'open_count': int(lv_data[5], base=10), 
     'extent_size': int(lv_data[7], base=10), 
     'extent_alloc': int(lv_data[8], base=10), 
     'dev_major': int(lv_data[11], base=10), 
     'dev_minor': int(lv_data[12], base=10)}


def lvsdisplay(group=None):
    """Gather LVM volumes information.
    """
    cmd = [
     'lvm',
     'lvdisplay',
     '--colon']
    if group is not None:
        cmd.append(group)
    info = subproc.check_output(cmd)
    info_data = [line.strip().split(':') for line in info.strip().split('\n') if line]
    return [_parse_lv_data(lv_data) for lv_data in info_data]


def lvdisplay(volume, group):
    """Gather a LVM volume information.
    """
    cmd = [
     'lvm',
     'lvdisplay',
     '--colon',
     os.path.join(group, volume)]
    info = subproc.check_output(cmd)
    info_data = [line.strip().split(':') for line in info.strip().split('\n') if line]
    assert len(info_data) == 1, 'Unexpected LVM output.'
    return _parse_lv_data(info_data[0])


__all__ = [
 'lvcreate',
 'lvdisplay',
 'lvremove',
 'lvsdisplay',
 'pvcreate',
 'vgactivate',
 'vgcreate',
 'vgdisplay',
 'vgremove',
 'vgsdisplay']