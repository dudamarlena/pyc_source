# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/cli.py
# Compiled at: 2018-02-27 04:38:46
# Size of source mod 2**32: 974 bytes
import os, sys, click
from .service import evaluate

@click.command('')
@click.option('--path', default='.', help='path to project or repository')
@click.option('--max-length', default=50, help='Max line count for a function')
def main(path: str, max_length: int):
    """Simple tool to evaluate function lengths in a code base (directory)."""
    try:
        fpath = full_path(path)
    except AssertionError:
        raise click.BadParameter('path specified needs to be a directory', param_hint=[
         '--path'])

    try:
        evaluate(fpath, max_length)
    except AssertionError:
        sys.exit(1)
    else:
        sys.exit(0)


def full_path(path: str):
    if path == '.':
        return os.getcwd()
    assert os.path.isdir(path)
    if os.path.isabs(path):
        return path
    return os.path.abspath(path)


if __name__ == '__main__':
    main()