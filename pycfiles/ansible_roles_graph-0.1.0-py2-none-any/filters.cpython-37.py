# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/filters.py
# Compiled at: 2019-10-30 07:28:41
# Size of source mod 2**32: 604 bytes
__doc__ = 'Jinja2 filters module.'
import typing

def listify(value: typing.Union[(typing.List, str)]) -> str:
    """Turn a list of items into a Markdown formatted list."""
    linked = []
    if isinstance(value, list):
        for default in value:
            linked.append(f"  * ``{default}``")

        return '\n{}'.format('\n'.join(linked))
    return f"``{value}``"


def quicklistify(value: typing.Dict[(str, typing.Any)]) -> str:
    """Inline Markdown link a list of defaults."""
    linked = []
    for default in value:
        linked.append(f"[{default}](#{default})")

    return ', '.join(linked)