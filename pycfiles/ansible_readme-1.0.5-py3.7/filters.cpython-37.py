# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/filters.py
# Compiled at: 2019-10-30 07:28:41
# Size of source mod 2**32: 604 bytes
"""Jinja2 filters module."""
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