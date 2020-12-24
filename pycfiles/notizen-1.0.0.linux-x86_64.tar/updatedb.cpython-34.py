# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/notizen/venv-py3.4/lib/python3.4/site-packages/notizen/updatedb.py
# Compiled at: 2016-02-02 09:29:35
# Size of source mod 2**32: 2575 bytes
"""
FIXME
"""
import re, os, logging
from os import path
from notizen import indices
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
RE_TAG = re.compile('^\\s*tags:(.*)$', re.IGNORECASE)
RE_KEYWORDS = re.compile('^\\s*keywords:(.*)$', re.IGNORECASE)
RE_TITLE = re.compile('^\\s*title:(.*)$', re.IGNORECASE)
RE_SUMMARY = re.compile('^\\s*summary:(.*)$', re.IGNORECASE)
RE_FILE = re.compile('^.*\\.md$', re.IGNORECASE)

def get_info_from_file(filepath: str) -> dict:
    """Provides a dictionary with the info extracted from a file.
    Currently only the tags and the path to the file."""
    with open(filepath, 'r') as (f):
        ten_first_lines = f.readlines()[:10]
    info = {'filepath': filepath}
    for line in ten_first_lines:
        result = RE_TAG.match(line)
        if not result:
            result = RE_KEYWORDS.match(line)
        if result:
            tags_str = result.groups()[0]
            tags_l = tags_str.split(',')
            tags_l = [t.strip() for t in tags_l]
            tags_l += info.get('tags', [])
            info.update({'tags': tags_l})
            continue
        result = RE_TITLE.match(line)
        if result:
            title_str = result.groups()[0]
            title_str = title_str.strip()
            info.update({'title': title_str})
        result = RE_SUMMARY.match(line)
        if result:
            summary_str = result.groups()[0]
            summary_str = summary_str.strip()
            info.update({'summary': summary_str})
            continue

    return info


def update_tags_index(tags_index: dict, notes_path: str) -> None:
    """Walks all the directory path, extracts info for each
    Markdown file and updates the Tags Index provided."""
    for root, dirs, files in os.walk(notes_path):
        for filepath in files:
            filepath = path.join(root, filepath)
            if not RE_FILE.match(filepath):
                continue
            fileinfo = get_info_from_file(filepath)
            indices.add_file_to_tag_index(tags_index, fileinfo)