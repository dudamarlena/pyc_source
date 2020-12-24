# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\carlo\projects\marlin\marlin\bookmark.py
# Compiled at: 2020-04-05 21:51:07
# Size of source mod 2**32: 1333 bytes
from marlin.manage import ManageBookmark
from marlin.styles import label, color
from pathlib import Path
import click

@click.command()
@click.argument('bookmark_name')
@click.argument('bookmark_path', default=(Path.cwd()))
def main(bookmark_name, bookmark_path):
    """
    Bookmark the current folder.
    """
    bookmark_object = ManageBookmark(bookmark_name, str(bookmark_path))
    bookmark_object.create_marlin_folder()
    all_bookmarks = bookmark_object.list_bookmark()
    if bookmark_name in all_bookmarks:
        click.confirm((exist_msg(bookmark_name)), abort=True)
    else:
        click.confirm((bookmark_msg(bookmark_name)), abort=True)
    bookmark_object.add_bookmark()
    click.echo(bookmarked_msg(bookmark_name))


def exist_msg(bookmark_name):
    msg = 'Bookmark already exists. Overwrite'
    return f"\n{label('info')} {msg} {color('yellow', bookmark_name)}?"


def bookmark_msg(bookmark_name):
    msg = 'Do you want to bookmark'
    return f"\n{label('info')} {msg} {color('yellow', bookmark_name)}"


def bookmarked_msg(bookmark_name):
    msg = 'has been bookmarked.'
    return f"{label('good')} {color('yellow', bookmark_name)} {msg}"


if __name__ == '__main__':
    main()