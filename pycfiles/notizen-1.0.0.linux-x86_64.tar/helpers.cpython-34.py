# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/notizen/venv-py3.4/lib/python3.4/site-packages/notizen/helpers.py
# Compiled at: 2016-01-06 10:22:11
# Size of source mod 2**32: 1454 bytes
import os, re, logging
from os import path
from notizen import file_processing
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
RE_FILE = re.compile('^.*\\.md$', re.IGNORECASE)

def show_matching_files(matching_files: list, tag: str) -> None:
    """Print the list of matching files. Or a notification if there were no results."""
    if matching_files is None:
        msg = 'No matching files with "{}" tag.\n\nMisspelled? or inexistent?'
        msg = msg.format(tag)
        print(msg)
        return
    msg = '{} matching files under tag "{}":'
    print(msg.format(len(matching_files), tag))
    for f in matching_files:
        print('\t{}'.format(f))


def walk_and_index(notes_path: str, index_fn: 'function') -> None:
    """Walks all the directory path, extracts info for each
    Markdown file and triggers the .index() of the engine."""
    for root, dirs, files in os.walk(notes_path):
        for filepath in files:
            filepath = path.join(root, filepath)
            if not RE_FILE.match(filepath):
                continue
            fileinfo = file_processing.get_info_from_file(filepath)
            index_fn(fileinfo)