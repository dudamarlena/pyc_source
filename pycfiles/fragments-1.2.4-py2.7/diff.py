# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fragments/diff.py
# Compiled at: 2012-11-06 05:50:09
from __future__ import unicode_literals
from . import color

def _visible_in_diff(merge_result, context_lines=3):
    """Collects the set of lines that should be visible in a diff with a certain number of context lines"""
    i = old_line = new_line = 0
    while i < len(merge_result):
        line_or_conflict = merge_result[i]
        if isinstance(line_or_conflict, tuple):
            yield (
             old_line, new_line, line_or_conflict)
            old_line += len(line_or_conflict[0])
            new_line += len(line_or_conflict[1])
        else:
            for j in list(range(max(0, i - context_lines), i)) + list(range(i + 1, min(len(merge_result), i + 1 + context_lines))):
                if isinstance(merge_result[j], tuple):
                    yield (
                     old_line, new_line, line_or_conflict)
                    break
            else:
                yield

            old_line += 1
            new_line += 1
        i += 1

    yield
    return


def _split_diff(merge_result, context_lines=3):
    """Split diffs and context lines into groups based on None sentinel"""
    collect = []
    for item in _visible_in_diff(merge_result, context_lines=context_lines):
        if item is None:
            if collect:
                yield collect
            collect = []
        else:
            collect.append(item)

    return


def _diff_group_position(group):
    """Generate a unified diff position line for a diff group"""
    old_start = group[0][0]
    new_start = group[0][1]
    old_length = new_length = 0
    for old_line, new_line, line_or_conflict in group:
        if isinstance(line_or_conflict, tuple):
            old, new = line_or_conflict
            old_length += len(old)
            new_length += len(new)
        else:
            old_length += 1
            new_length += 1

    if old_length:
        old_start += 1
    if new_length:
        new_start += 1
    return color.LineNumber(b'@@ -%s,%s +%s,%s @@' % (old_start, old_length, new_start, new_length))


def _diff_group(group):
    """Generate a diff section for diff group"""
    yield _diff_group_position(group)
    for old_line, new_line, line_or_conflict in group:
        if isinstance(line_or_conflict, tuple):
            old, new = line_or_conflict
            for o in old:
                yield color.Deleted(b'-' + o.strip(b'\n'))

            if new and old and new[(-1)].endswith(b'\n') and not old[(-1)].endswith(b'\n'):
                yield b'\\ No newline at end of file'
            for n in new:
                yield color.Added(b'+' + n.strip(b'\n'))

            if old and new and old[(-1)].endswith(b'\n') and not new[(-1)].endswith(b'\n'):
                yield b'\\ No newline at end of file'
        else:
            yield b' ' + line_or_conflict.strip(b'\n')


def _full_diff(merge_result, key, context_lines=3):
    """Generate a full diff based on a Weave merge result"""
    header_printed = False
    for group in _split_diff(merge_result, context_lines=context_lines):
        if not header_printed:
            header_printed = True
            yield color.Header(b'diff a/%s b/%s' % (key, key))
            yield color.DeletedHeader(b'--- %s' % key)
            yield color.AddedHeader(b'+++ %s' % key)
        for l in _diff_group(group):
            yield l