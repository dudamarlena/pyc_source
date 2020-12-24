# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/processors.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import re
from reviewboard.diffviewer.diffutils import split_line_endings
CHUNK_RANGE_RE = re.compile(b'^@@ -(?P<orig_start>\\d+)(,(?P<orig_len>\\d+))? \\+(?P<new_start>\\d+)(,(?P<new_len>\\d+))? @@', re.M)

def filter_interdiff_opcodes(opcodes, filediff_data, interfilediff_data):
    """Filters the opcodes for an interdiff to remove unnecessary lines.

    An interdiff may contain lines of code that have changed as the result of
    updates to the tree between the time that the first and second diff were
    created. This leads to some annoyances when reviewing.

    This function will filter the opcodes to remove as much of this as
    possible. It will only output non-"equal" opcodes if it falls into the
    ranges of lines dictated in the uploaded diff files.
    """

    def _find_range_info(diff):
        lines = split_line_endings(diff)
        process_changes = False
        process_trailing_context = False
        ranges = []
        chunk_start = None
        chunk_len = 0
        lines_of_context = 0
        for line in lines:
            if process_changes:
                if line.startswith(('-', '+')):
                    start = chunk_start - 1 + lines_of_context
                    chunk_len -= lines_of_context
                    if lines_of_context > 0:
                        start -= 1
                    ranges.append((start, start + chunk_len))
                    process_changes = False
                    process_trailing_context = True
                    lines_of_context = 0
                    continue
                else:
                    lines_of_context += 1
            elif process_trailing_context:
                if line.startswith(b' '):
                    lines_of_context += 1
                    continue
                else:
                    lines_of_context = 0
            m = CHUNK_RANGE_RE.match(line)
            if m:
                if process_trailing_context and lines_of_context > 0:
                    last_range = ranges[(-1)]
                    ranges[-1] = (last_range[0],
                     last_range[1] - lines_of_context)
                chunk_start = int(m.group(b'new_start'))
                chunk_len = int(m.group(b'new_len') or b'1')
                process_changes = True
                process_trailing_context = False
                lines_of_context = 0

        if process_trailing_context and lines_of_context > 0:
            last_range = ranges[(-1)]
            ranges[-1] = (last_range[0],
             last_range[1] - lines_of_context)
        return ranges

    def _is_range_valid(line_range, tag, i1, i2):
        return line_range is not None and i1 >= line_range[0] and (tag == b'delete' or i1 != i2)

    orig_ranges = _find_range_info(filediff_data)
    new_ranges = _find_range_info(interfilediff_data)
    orig_range_i = 0
    new_range_i = 0
    if orig_ranges:
        orig_range = orig_ranges[orig_range_i]
    else:
        orig_range = None
    if new_ranges:
        new_range = new_ranges[new_range_i]
    else:
        new_range = None
    if not orig_range and not new_range:
        for tag, i1, i2, j1, j2 in opcodes:
            yield (tag, i1, i2, j1, j2)

        return
    for tag, i1, i2, j1, j2 in opcodes:
        while orig_range and i1 > orig_range[1]:
            orig_range_i += 1
            if orig_range_i < len(orig_ranges):
                orig_range = orig_ranges[orig_range_i]
            else:
                orig_range = None

        while new_range and j1 > new_range[1]:
            new_range_i += 1
            if new_range_i < len(new_ranges):
                new_range = new_ranges[new_range_i]
            else:
                new_range = None

        orig_starts_valid = _is_range_valid(orig_range, tag, i1, i2)
        new_starts_valid = _is_range_valid(new_range, tag, j1, j2)
        if tag in ('equal', 'replace'):
            valid_chunk = orig_starts_valid or new_starts_valid
        elif tag == b'delete':
            valid_chunk = orig_starts_valid
        elif tag == b'insert':
            valid_chunk = new_starts_valid
        if valid_chunk:
            if orig_range:
                cap_i2 = orig_range[1] + 1
            else:
                cap_i2 = i2
            if new_range:
                cap_j2 = new_range[1] + 1
            else:
                cap_j2 = j2
            if orig_starts_valid:
                valid_i2 = min(i2, cap_i2)
            else:
                valid_i2 = i2
            if new_starts_valid:
                valid_j2 = min(j2, cap_j2)
            else:
                valid_j2 = j2
            if tag in ('equal', 'replace'):
                i_diff = valid_i2 - i1
                j_diff = valid_j2 - j1
                if valid_i2 > cap_i2:
                    if not valid_j2 <= cap_j2:
                        raise AssertionError
                        max_cap = j_diff
                    elif valid_j2 > cap_j2:
                        max_cap = i_diff
                    else:
                        max_cap = max(i_diff, j_diff)
                    valid_i2 = i1 + max_cap
                    valid_j2 = j1 + max_cap
                    cap_i2 = valid_i2
                    cap_j2 = valid_j2
                yield (tag, i1, valid_i2, j1, valid_j2)
                if valid_i2 == i2 and valid_j2 == j2:
                    continue
                if orig_range is not None and i2 + 1 > cap_i2:
                    i1 = cap_i2
                if new_range is not None and j2 + 1 > cap_j2:
                    j1 = cap_j2
                valid_chunk = False
            valid_chunk or (yield (
             b'filtered-equal', i1, i2, j1, j2))

    return


def post_process_filtered_equals(opcodes):
    """Post-processes filtered-equal and equal chunks from interdiffs.

    Any filtered-out "filtered-equal" chunks will get turned back into "equal"
    chunks and merged into any prior equal chunks. Likewise, simple "equal"
    chunks will also get merged.

    "equal" chunks that have any indentation information will remain
    their own chunks, with nothing merged in.
    """
    cur_chunk = None
    for tag, i1, i2, j1, j2, meta in opcodes:
        if tag == b'equal' and not meta.get(b'indentation_changes') or tag == b'filtered-equal':
            if cur_chunk:
                i1 = cur_chunk[1]
                j1 = cur_chunk[3]
                meta = cur_chunk[5]
            cur_chunk = (b'equal', i1, i2, j1, j2, meta)
        else:
            if cur_chunk:
                yield cur_chunk
                cur_chunk = None
            yield (tag, i1, i2, j1, j2, meta)

    if cur_chunk:
        yield cur_chunk
    return