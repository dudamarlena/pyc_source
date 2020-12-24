# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/apiscrub/__init__.py
# Compiled at: 2018-10-09 16:34:36
# Size of source mod 2**32: 3721 bytes
"""API Scrubber"""

def should_keep(tag, keep, item):
    """
    Determine whether we should keep an item based on the set of tag values
    that were given to be kept. If the `x-only` tag is present, then at least
    one match means we keep the item, otherwise remove it. If not present,
    then we default to keeping it.
    """
    if tag in item:
        only = item[tag]
        if isinstance(only, str):
            only = [
             only]
        del item[tag]
        if not set(only) & keep:
            return False
    return True


def process(tag, keep, piece):
    """
    Process a data structure to filter out items. This also removes the special
    `x-only` property, if present.
    """
    removed_paths = []
    _process(tag, keep, piece, '#', removed_paths)
    _clean_refs(removed_paths, piece)


def _process(tag, keep, piece, path, removed_paths):
    removed = []
    for k, v in list(piece.items()):
        if v is None:
            continue
        cur_path = path + '/' + str(k).replace('~', '~0').replace('/', '~1')
        if hasattr(v, 'get'):
            if should_keep(tag, keep, v):
                removed = _process(tag, keep, v, cur_path, removed_paths)
                if k == 'properties':
                    if 'required' in piece:
                        for r in removed:
                            if r in piece['required']:
                                piece['required'].remove(r)

                    else:
                        del piece[k]
                        removed.append(k)
                        removed_paths.append(cur_path)
            elif hasattr(v, 'append'):
                for item in v[:]:
                    if hasattr(item, 'get'):
                        if should_keep(tag, keep, item):
                            _process(tag, keep, item, cur_path, removed_paths)
                        else:
                            v.remove(item)

                del (v or piece)[k]
                removed.append(k)
                removed_paths.append(cur_path)

    return removed


def _clean_refs(removed_refs, piece):
    for k, v in list(piece.items()):
        if v is None:
            continue
        else:
            if hasattr(v, 'get'):
                if v.get('$ref') in removed_refs:
                    del piece[k]
                    continue
                _clean_refs(removed_refs, v)
        if hasattr(v, 'append'):
            for item in v[:]:
                if hasattr(item, 'get'):
                    if item.get('$ref') in removed_refs:
                        v.remove(item)
                if not v:
                    del piece[k]