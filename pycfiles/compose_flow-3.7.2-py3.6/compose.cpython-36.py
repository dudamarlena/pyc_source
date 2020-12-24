# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/compose.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 2315 bytes
import logging, os
from .utils import remerge, yaml_dump, yaml_load

def get_overlay_filenames(overlay):
    logger = logging.getLogger('get_overlay_filenames')
    overlay_filenames = []
    applied = []
    for item in overlay:
        if item in applied:
            pass
        else:
            applied.append(item)
            path = None
            if isinstance(item, dict):
                name = item['name']
                path = item['path']
            else:
                name = item
            if path:
                _filename = os.path.join(path, name)
            else:
                _filename = name
            if _filename:
                if os.path.exists(_filename):
                    if os.path.isfile(_filename):
                        overlay_filenames.append(_filename)
            if name:
                name = '.{}'.format(name)
            else:
                name = ''
            _filename = 'docker-compose{}.yml'.format(name)
            if path:
                _filename = os.path.join(path, _filename)
            logging.debug('_filename={}'.format(_filename))
            if os.path.exists(_filename):
                overlay_filenames.append(_filename)
            else:
                logger.warning(f"filename={_filename} does not exist, skipping")

    if not overlay_filenames:
        overlay_filenames.append('docker-compose.yml')
    return overlay_filenames


def merge_profile(profile: dict) -> str:
    """
    Returns the merged compose file contents

    Args:
        profile: the profile data to merge
    """
    filenames = get_overlay_filenames(profile)
    if len(filenames) > 1:
        yaml_contents = []
        for item in filenames:
            with open(item, 'r') as (fh):
                yaml_contents.append(yaml_load(fh))

        merged = remerge(yaml_contents)
        content = yaml_dump(merged)
    else:
        try:
            with open(filenames[0], 'r') as (fh):
                content = fh.read()
        except FileNotFoundError:
            content = ''

    return content