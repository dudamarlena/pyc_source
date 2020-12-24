# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_jsondash/flask_jsondash/data_utils/filetree.py
# Compiled at: 2017-05-11 01:26:49
# Size of source mod 2**32: 2215 bytes
"""
flask_jsondash.data_utils.filetree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A utility for getting d3 friendly hierarchical data structures
from the list of files and directories on a given path.

Re-purposed from: github.com/christabor/MoAL/blob/master/MOAL/get_file_tree.py

:copyright: (c) 2016 by Chris Tabor.
:license: MIT, see LICENSE for more details.
"""
import errno, json, os
from pprint import pprint
import click
try:
    _unicode = unicode
except NameError:
    _unicode = str

def path_hierarchy(path):
    """Create a json representation of a filesystem tree.

    Format is suitable for d3.js application.

    Taken from:
    http://unix.stackexchange.com/questions/164602/
        how-to-output-the-directory-structure-to-json-format
    """
    valid_path = any([isinstance(path, _unicode), isinstance(path, str)])
    assert valid_path, 'Requires a valid path!'
    name = os.path.basename(path)
    hierarchy = {'type': 'folder', 
     'name': name, 
     'path': path}
    try:
        hierarchy['children'] = [path_hierarchy(os.path.join(path, contents)) for contents in os.listdir(path)]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy


@click.command()
@click.option('--ppr/--no-ppr', default=False, help='Pretty-print results.')
@click.option('--indent', '-i', default=4, help='How far to indent if using json.')
@click.option('--jsonfile', '-j', default=None, help='Output specified file as json.')
@click.option('--path', '-p', default='.', help='The starting path')
def get_tree(path, jsonfile, ppr, indent):
    """CLI wrapper for recursive function."""
    res = path_hierarchy(path)
    if jsonfile is not None:
        with open(jsonfile, 'w') as (jsonfile):
            jsonfile.write(json.dumps(res, indent=indent))
        return
    if ppr:
        pprint(res, indent=indent)
    else:
        print(res)


if __name__ == '__main__':
    get_tree()