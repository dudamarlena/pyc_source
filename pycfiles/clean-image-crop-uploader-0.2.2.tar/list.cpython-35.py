# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/list.py
# Compiled at: 2018-03-25 08:15:21
# Size of source mod 2**32: 682 bytes
__doc__ = 'Listing config files.'
import click
from .config import Config
_use_meta_tag_text_dict = {True: '[META]', False: ''}

def list_configs():
    """Show the path config lists to command line."""
    config = Config()
    glob_paths = config.list_glob_path()
    if len(glob_paths) == 0:
        click.echo('No path settings. To add new setting, please use "clean add".')
    for i in enumerate(config.list_glob_path()):
        use_meta_tag_text = _use_meta_tag_text_dict[i[1]['use_meta_tag']]
        click.echo('[{}] {} => {} {}'.format(i[0], i[1]['glob'], i[1]['path'], use_meta_tag_text))