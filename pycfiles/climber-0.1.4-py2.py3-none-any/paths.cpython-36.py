# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/climb/paths.py
# Compiled at: 2015-05-23 14:30:54
# Size of source mod 2**32: 771 bytes
ROOT_PATH = '/'
SEPARATOR = '/'

def format_path(current_path, path, default=None):
    if path:
        path = path.strip()
    if not path:
        if default:
            return default
        return current_path
    else:
        absolute = path.startswith(ROOT_PATH)
        if not absolute:
            path = SEPARATOR.join((current_path, path))
        parts = split_path(path)
        result = []
        for part in parts:
            if part == '.':
                continue
            else:
                if part == '..':
                    result = result[:-1]
                else:
                    result.append(part)

        new_path = ROOT_PATH + SEPARATOR.join(result)
        return new_path


def split_path(path):
    if not path:
        return []
    else:
        return [part for part in path.strip().split(SEPARATOR) if part]