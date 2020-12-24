# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/notizen/venv-py3.4/lib/python3.4/site-packages/notizen/indices.py
# Compiled at: 2016-02-02 09:29:35
# Size of source mod 2**32: 1296 bytes
"""
FIXME
"""
import pickle, logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def add_file_to_tag_index(tags_index: dict, fileinfo: dict) -> None:
    """Adds entries into the Tags Index"""
    tags_l = fileinfo.get('tags', None)
    if not tags_l:
        return
    filepath = fileinfo['filepath']
    for tag in tags_l:
        file_l = tags_index.get(tag, [])
        file_l = list(set(file_l + [filepath]))
        tags_index[tag] = file_l


def load_indices(where_from: str) -> tuple:
    """Loads the indices from the file refered by :where_from
    and returns a tuple: (tags_index, ).
    Should not find the file, it will return empty indices."""
    try:
        with open(where_from, 'br') as (f):
            idx = pickle.load(file=f)
        tags_index = idx['tags_index']
    except FileNotFoundError:
        tags_index = {}
        LOGGER.info('File "{}" was not found.'.format(where_from))

    return (
     tags_index,)


def save_indices(tags_index: dict, where: str) -> None:
    """Save the indices into the file refered by :where."""
    idx = {'tags_index': tags_index}
    with open(where, 'bw') as (f):
        pickle.dump(obj=idx, file=f, protocol=-1)