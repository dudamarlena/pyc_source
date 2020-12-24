# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/local_file_manager.py
# Compiled at: 2020-05-04 14:48:31
# Size of source mod 2**32: 1410 bytes
from pathlib import Path
import click

def find_file_directory(data_dir, _format=None):
    """
    Find the files by format on the data_dir
    :param data_dir: The local directory where the files are
    :type data_dir: Path
    :param _format:
    :type _format:
    """
    if _format is not None:
        _format = _format.replace('.', '')
        files = [f for f in data_dir.glob('*{}'.format(_format))]
        if len(files) > 1:
            print_choices([f.resolve().expanduser() for f in files])
            file_index = click.prompt('Select the file', type=(click.Choice(range(1, len(files) + 1))),
              show_choices=True,
              value_proc=parse)
            click.secho('Selected from your computer {}'.format(files[(file_index - 1)]))
            return str(files[(file_index - 1)])
        if len(files) == 1:
            click.secho('Selected from your computer {}'.format(files[0]))
            return str(files[0])
        click.secho('There is not files with format {} on {}'.format(_format, data_dir))


def print_choices(choices):
    for index, choice in enumerate(choices):
        click.echo('[{}] {}'.format(index + 1, choice))


def parse(value):
    try:
        return int(value)
    except:
        return value