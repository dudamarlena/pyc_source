# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/wheel/wheel/cli/pack.py
# Compiled at: 2019-07-30 18:46:56
# Size of source mod 2**32: 2263 bytes
from __future__ import print_function
import os.path, re, sys
from wheel.cli import WheelError
from wheel.wheelfile import WheelFile
DIST_INFO_RE = re.compile('^(?P<namever>(?P<name>.+?)-(?P<ver>\\d.*?))\\.dist-info$')

def pack(directory, dest_dir, build_number):
    """Repack a previously unpacked wheel directory into a new wheel file.

    The .dist-info/WHEEL file must contain one or more tags so that the target
    wheel file name can be determined.

    :param directory: The unpacked wheel directory
    :param dest_dir: Destination directory (defaults to the current directory)
    """
    dist_info_dirs = [fn for fn in os.listdir(directory) if os.path.isdir(os.path.join(directory, fn)) if DIST_INFO_RE.match(fn)]
    if len(dist_info_dirs) > 1:
        raise WheelError('Multiple .dist-info directories found in {}'.format(directory))
    else:
        if not dist_info_dirs:
            raise WheelError('No .dist-info directories found in {}'.format(directory))
    dist_info_dir = dist_info_dirs[0]
    name_version = DIST_INFO_RE.match(dist_info_dir).group('namever')
    if build_number:
        name_version += '-' + build_number
    with open(os.path.join(directory, dist_info_dir, 'WHEEL')) as (f):
        tags = [line.split(' ')[1].rstrip() for line in f if line.startswith('Tag: ')]
        if not tags:
            raise WheelError('No tags present in {}/WHEEL; cannot determine target wheel filename'.format(dist_info_dir))
    impls = sorted({tag.split('-')[0] for tag in tags})
    abivers = sorted({tag.split('-')[1] for tag in tags})
    platforms = sorted({tag.split('-')[2] for tag in tags})
    tagline = '-'.join(['.'.join(impls), '.'.join(abivers), '.'.join(platforms)])
    wheel_path = os.path.join(dest_dir, '{}-{}.whl'.format(name_version, tagline))
    with WheelFile(wheel_path, 'w') as (wf):
        print(('Repacking wheel as {}...'.format(wheel_path)), end='')
        sys.stdout.flush()
        wf.write_files(directory)
    print('OK')