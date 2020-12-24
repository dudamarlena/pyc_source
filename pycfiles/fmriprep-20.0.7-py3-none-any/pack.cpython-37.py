# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/wheel/wheel/cli/pack.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 3208 bytes
from __future__ import print_function
import os.path, re, sys
from wheel.cli import WheelError
from wheel.wheelfile import WheelFile
DIST_INFO_RE = re.compile('^(?P<namever>(?P<name>.+?)-(?P<ver>\\d.*?))\\.dist-info$')
BUILD_NUM_RE = re.compile(b'Build: (\\d\\w*)$')

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
        else:
            dist_info_dir = dist_info_dirs[0]
            name_version = DIST_INFO_RE.match(dist_info_dir).group('namever')
            existing_build_number = None
            wheel_file_path = os.path.join(directory, dist_info_dir, 'WHEEL')
            with open(wheel_file_path) as (f):
                tags = []
                for line in f:
                    if line.startswith('Tag: '):
                        tags.append(line.split(' ')[1].rstrip())

                if not tags:
                    raise WheelError('No tags present in {}/WHEEL; cannot determine target wheel filename'.format(dist_info_dir))
            build_number = build_number if build_number is not None else existing_build_number
            if build_number is not None:
                if build_number:
                    name_version += '-' + build_number
                if build_number != existing_build_number:
                    replacement = ('Build: %s\r\n' % build_number).encode('ascii') if build_number else b''
                    with open(wheel_file_path, 'rb+') as (f):
                        wheel_file_content = f.read()
                        if not BUILD_NUM_RE.subn(replacement, wheel_file_content)[1]:
                            wheel_file_content += replacement
                        f.truncate()
                        f.write(wheel_file_content)
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