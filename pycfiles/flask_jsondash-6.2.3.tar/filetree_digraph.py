# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_jsondash/flask_jsondash/data_utils/filetree_digraph.py
# Compiled at: 2017-06-07 18:53:35
"""
flask_jsondash.data_utils.filetree_digraph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A utility for getting digraph friendly data structures
from the list of files and directories on a given path.

:copyright: (c) 2016 by Chris Tabor.
:license: MIT, see LICENSE for more details.
"""
import errno, os, click
try:
    _unicode = unicode
except NameError:
    _unicode = str

def path_hierarchy(path, hierarchy=[], prev=None):
    """Create a dotfile representation of a filesystem tree.

    Format is suitable for graphviz applications.
    """
    valid_path = any([isinstance(path, _unicode), isinstance(path, str)])
    assert valid_path, 'Requires a valid path!'
    name = os.path.basename(path)
    if prev is not None:
        prev = str(prev)
        if all([prev != '', prev != '.']):
            hierarchy.append(('"{}" -> "{}"').format(prev, name))
    try:
        hierarchy += [ path_hierarchy(os.path.join(path, contents), prev=name) for contents in os.listdir(path)
                     ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise

    return hierarchy


def make_dotfile(path):
    """Generate the recursive path and then format into dotfile format."""
    _res = [ w for w in path_hierarchy(path) if not isinstance(w, list) ]
    res = 'digraph {\n'
    for item in _res:
        if item.startswith(' ->'):
            continue
        res += ('\t{};\n').format(item)

    res += '}\n'
    return res


@click.command()
@click.option('--dot', '-d', default=None, help='Output specified file as a dotfile.')
@click.option('--path', '-p', default='.', help='The starting path')
def get_dotfile_tree(path, dot):
    """CLI wrapper for existing functions."""
    res = make_dotfile(path)
    if path == '.':
        raise ValueError('Running in the same directory when no folders are present does not make sense.')
    if dot is not None:
        with open(dot, 'w') as (dotfile):
            dotfile.write(res)
        return
    else:
        print res
        return


if __name__ == '__main__':
    get_dotfile_tree()