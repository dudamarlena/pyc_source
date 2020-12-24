# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_docker/utils.py
# Compiled at: 2018-01-01 16:23:40
# Size of source mod 2**32: 1080 bytes
import os, bonobo
from bonobo.util.collections import cast
from bonobo_docker import settings
from bonobo_docker.logging import logger

def run_docker(*args, dry_run=False):
    cmd = ' '.join(('docker', ) + args)
    logger.info(('[DRY] ' if dry_run else '') + cmd)
    if not dry_run:
        return os.system(cmd)


def get_image():
    return '{}:{}'.format(settings.IMAGE, bonobo.__version__)


def get_volumes(*, with_local_packages=False):
    cache_path = os.path.expanduser('~/.cache')
    volumes = {}
    volumes[cache_path] = {'bind': '/home/bonobo/.cache'}
    if with_local_packages:
        from bonobo.util.pkgs import bonobo_packages
        for name in bonobo_packages:
            volumes[bonobo_packages[name].location] = {'bind': '/home/bonobo/src/' + name}

    return volumes


@cast(tuple)
def get_volumes_args(*, with_local_packages=False):
    for hostpath, volumespec in get_volumes(with_local_packages=with_local_packages).items():
        yield '-v {}:{}{}'.format(hostpath, volumespec['bind'], ':ro' if volumespec.get('mode') == 'ro' else '')