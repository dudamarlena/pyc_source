# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/utils.py
# Compiled at: 2020-02-05 04:05:47
# Size of source mod 2**32: 974 bytes
import json
from slugify import slugify

def get_slug(text, js_safe=True):
    """ slug from text to build URL parts """
    if js_safe:
        return slugify(text, regex_pattern='[^-a-z0-9_]+').replace('-', '_')
    else:
        return slugify(text)


def clean_text(text):
    """ cleaned-down version of text as Youtube is very permissive with descriptions """
    return text.strip().replace('\n', ' ').replace('\r', ' ')


def save_json(cache_dir, key, data):
    """ save JSON collection to path """
    with open(cache_dir.joinpath(f"{key}.json"), 'w') as (fp):
        json.dump(data, fp, indent=4)


def load_json(cache_dir, key):
    """ load JSON collection from path or None """
    fname = cache_dir.joinpath(f"{key}.json")
    if not fname.exists():
        return
    try:
        with open(fname, 'r') as (fp):
            return json.load(fp)
    except Exception:
        return