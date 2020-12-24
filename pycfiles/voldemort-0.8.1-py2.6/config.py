# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/voldemort/config.py
# Compiled at: 2013-08-02 16:32:58
import os, logging
from yaml import load, dump, Loader, Dumper
log = logging.getLogger(__name__)
DEFAULT_CONFIG = '# voldemort configuration file\nlayout_dirs :\n              - layout\n              - include\nposts_dir   : posts\nsite_dir    : _site\npost_url    : "%Y/%m/%d"\npaginate    : 5\n'

class Config(object):
    """Converts a dict to object.
    """

    def __init__(self, dict):
        self.__dict__.update(dict)


def load_config(work_dir, name='settings.yaml'):
    """Loads the configuration from the working directory. Else loads
    the default config.
    """
    log.info('Loading voldemort configuration')
    config_file = os.path.join(work_dir, name)
    if not os.path.exists(config_file):
        write_config = raw_input('No configuration file found. Write default config? [Y/n]: ')
        write_config = (write_config == 'Y' or write_config == 'y' or write_config == '') and True or False
        if write_config:
            log.info('Writing default config at %s' % config_file)
            with open(config_file, 'w') as (f):
                f.write(DEFAULT_CONFIG)
    with open(config_file, 'r') as (f):
        config = load(f, Loader=Loader)
    default_config = load(DEFAULT_CONFIG, Loader=Loader)
    default_config.update(config)
    config = Config(default_config)
    config.layout_dirs = [ os.path.join(work_dir, ld) for ld in config.layout_dirs
                         ]
    config.posts_dir = os.path.join(work_dir, config.posts_dir)
    config.site_dir = os.path.join(work_dir, config.site_dir)
    return config