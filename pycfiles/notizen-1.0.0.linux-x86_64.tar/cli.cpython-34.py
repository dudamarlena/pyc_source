# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/notizen/venv-py3.4/lib/python3.4/site-packages/notizen/cli.py
# Compiled at: 2016-02-02 09:29:35
# Size of source mod 2**32: 3311 bytes
"""
Command-line Interface to index and to search into the notes.
"""
import os, click, logging
from os import path
from clickclick import AliasedGroup
import notizen
from notizen import indices
from notizen.updatedb import update_tags_index
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
CONFIG_DIR_PATH = click.get_app_dir('notizen')
INDICES_FILE_PATH = path.join(CONFIG_DIR_PATH, 'indices.pickle')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_COMMAND = 'test_default'

class AliasedDefaultGroup(AliasedGroup):

    def resolve_command(self, ctx, args):
        cmd_name = args[0]
        cmd = AliasedGroup.get_command(self, ctx, cmd_name)
        if not cmd:
            cmd_name = DEFAULT_COMMAND
            cmd = AliasedGroup.get_command(self, ctx, cmd_name)
            new_args = args
        else:
            new_args = args[1:]
        return (
         cmd_name, cmd, new_args)


def print_version(ctx, param, value):
    """Shows the --version banner.
    With additional info in case of someone wants to report a bug."""
    if not value or ctx.resilient_parsing:
        return
    msg = "{1} version {0}\n{3}\n\nDistributed under {4} license.\nAuthors: {5}.\n{6}\nPlatform: '{2}'."
    args = (
     notizen.__version__, notizen.__program_name__,
     notizen.get_platform_id(), notizen.__short_description__,
     notizen.__license__, ', '.join(notizen.__authors__),
     notizen.__url__)
    msg = msg.format(*args)
    click.echo(msg)
    ctx.exit()


@click.group(cls=AliasedDefaultGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help='Print the current version number and exit.')
@click.pass_context
def cli(context):
    pass


@cli.command('updatedb')
@click.option('--index-path', default=None, help='Path to the index file.', type=str)
@click.argument('path')
@click.pass_obj
def updatedb(obj, index_path: str, path: str) -> None:
    """Command to index all the notes with their tags."""
    tags_index = {}
    update_tags_index(tags_index, path)
    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)
    indices.save_indices(tags_index, index_path)


@cli.command()
@click.option('--index-path', default=None, help='Path to the index file.', type=str)
@click.argument('tag')
@click.pass_obj
def locate(obj, index_path: str, tag: str) -> None:
    """Show matching files with the given :tag."""
    if index_path is None:
        index_path = INDICES_FILE_PATH
    tags_index, = indices.load_indices(index_path)
    matching_files = tags_index.get(tag, None)
    if matching_files is None:
        msg = 'No matching files with "{}" tag.\n\nMisspelled? or inexistent?'
        msg = msg.format(tag)
        print(msg)
        return
    msg = '{} matching files under tag "{}":'
    print(msg.format(len(matching_files), tag))
    for f in matching_files:
        print('\t{}'.format(f))


def main():
    cli()


if __name__ == '__main__':
    main()