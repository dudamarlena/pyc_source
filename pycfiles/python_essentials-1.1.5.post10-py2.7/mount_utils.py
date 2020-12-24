# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/mount_utils.py
# Compiled at: 2015-02-07 20:42:38
import argparse, subprocess as sp, os, sys, re, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
import file_line_utils
mount_default = 'mount'
bash = 'dash'
ifconfig = 'ifconfig'
losetup = 'losetup'
partprobe = 'partprobe'
btrfs = 'btrfs'
umount = 'umount'
IMAGE_MODE_PT = 'partition-table'
IMAGE_MODE_FS = 'file-system'
image_modes = [IMAGE_MODE_PT, IMAGE_MODE_FS]
MOUNT_MODE_NFS = 1
MOUNT_MODE_CIFS = 2
mount_mode_default = MOUNT_MODE_CIFS

def mount_dsm_sparse_file(shared_folder_name, image_mount_target, network_mount_target, image_file_name, remote_host, username, uid=1000, gid=1000, mount_mode=mount_mode_default, credentials_file=None, mount=mount_default):
    """a wrapper around `mount_sparse_file` and different remote mount methods (NFS, cifs, etc.) (sparse file support is horrible for all of them...). It has been written to deal with Synology DSM 5.0 (path specifications, etc.). `credentials_file` can be used of the `credentials` option of `mount.cifs` will be passed to the `mount` command, if `None` the `username` option with value will be passed to the `mount` command which will request the password from input at a prompt. `uid` and `gid` are values for options of `mount.cifs` (which default to Ubuntu defaults for the first user)."""
    if mount_mode == MOUNT_MODE_NFS:
        lazy_mount(source='%s:/volume1/%s' % (remote_host, shared_folder_name), target=network_mount_target, fs_type='nfs', options_str='nfsvers=4', mount=mount)
    elif mount_mode == MOUNT_MODE_CIFS:
        if credentials_file is None:
            options_str = 'username=%s,rw,uid=%d,gid=%d' % (username, uid, gid)
        else:
            if not os.path.exists(credentials_file):
                raise ValueError("credentials_file '%s' doesn't exist" % (credentials_file,))
            options_str = 'credentials=%s,rw,uid=%d,gid=%d' % (credentials_file, uid, gid)
        lazy_mount(source='//%s/%s' % (remote_host, shared_folder_name), target=network_mount_target, fs_type='cifs', options_str=options_str, mount=mount)
    else:
        raise ValueError("mount_mode '%s' not supported" % (mount_mode,))
    mount_sparse_file(image_file=os.path.join(network_mount_target, image_file_name), image_mount_target=image_mount_target, image_mode=IMAGE_MODE_FS, mount=mount)
    return


def mount_sparse_file(image_file, image_mount_target, image_mode=IMAGE_MODE_FS, mount=mount_default):
    """Handles mounting `image_file` at `image_mount_target` according to `image_mode` which determines the remote filesystem to use."""
    image_file_loop_dev = losetup_wrapper(image_file)
    if image_mode == IMAGE_MODE_PT:
        sp.check_call([partprobe, image_file_loop_dev])
        lazy_mount('%sp1' % image_file_loop_dev, image_mount_target, 'btrfs', mount=mount)
        sp.check_call([btrfs, 'device', 'scan', '%sp1' % image_file_loop_dev])
    elif image_mode == IMAGE_MODE_FS:
        lazy_mount(image_file_loop_dev, image_mount_target, 'btrfs', mount=mount)
        sp.check_call([btrfs, 'device', 'scan', image_file_loop_dev])
    else:
        raise ValueError('image_mode has to be one of %s, but is %s' % (str(image_modes), image_mode))


def unmount_sparse_file(mount_target):
    """Unmounts the parse file which has been mounted under `mount_target` and removes the association of that sparse file with its loop device. The loop device will be determined automatically based on `losetup`."""
    mount_source = get_mount_source(mount_target)
    if mount_source is None:
        raise ValueError("mount_target '%s' isn't using a loop device" % (mount_target,))
    logger.info("mount_target '%s' was using loop device '%s'" % (mount_target, mount_source))
    sp.check_call([umount, mount_target])
    sp.check_call([losetup, '-d', mount_source])
    return


def get_mount_source(mount_target):
    """Determines the directory or filesystem which is mounted under `mount_target` and returns it or `None` is no directory of filesystem is mounted under `mount_target`."""
    for mount_source, mount_target0 in [ tuple(re.split('[\\s]+', x)[0:2]) for x in file_line_utils.file_lines('/proc/mounts', comment_symbol='#') ]:
        if mount_target0 == mount_target:
            return mount_source

    return


def losetup_wrapper(file):
    """A wrapper around finding the next free loop device with `losetup` and associating `file` with it with one function call. Returns the found loop device `file` has been associated to."""
    try:
        loop_dev = sp.check_output([losetup, '-f']).decode('utf-8').strip()
    except sp.CalledProcessError as ex:
        raise RuntimeError('no free loop device')

    sp.check_call([losetup, loop_dev, file])
    return loop_dev


def check_mounted(source, target, mount=mount_default):
    """Checks whether `source` is mounted under `target` and `True` if and only if that's the case - and `False` otherwise."""
    mount_lines = sp.check_output([mount]).decode('utf-8').strip().split('\n')
    for mount_line in mount_lines:
        mount_line_split = mount_line.split(' ')
        target0 = mount_line_split[1]
        if target0 == target:
            return True

    return False


def lazy_mount(source, target, fs_type, options_str=None, mount=mount_default):
    """Checks if `source` is already mounted under `target` and skips (if it is) or mounts `source` under `target` otherwise as type `fs_type`. Due to the fact that the type can be omitted for certain invokations of `mount` (e.g. `mount --bind`), this function allows `fs_type` to be `None` which means no type will be specified. Uses `mount` as binary for the mount command."""
    if check_mounted(source, target, mount=mount):
        return
    else:
        if not os.path.lexists(target):
            if os.path.isfile(source):
                os.mknod(target, mode=493)
            else:
                os.makedirs(target)
        cmds = [
         mount]
        if fs_type != None and fs_type != '':
            cmds += ['-t', fs_type]
        if options_str is not None and options_str != '':
            cmds += ['-o', options_str]
        cmds += [source, target]
        sp.check_call(cmds)
        return