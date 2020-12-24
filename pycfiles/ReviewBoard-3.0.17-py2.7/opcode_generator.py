# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/opcode_generator.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, re
from django.utils import six
from django.utils.six.moves import range
from reviewboard.diffviewer.processors import filter_interdiff_opcodes, post_process_filtered_equals

class MoveRange(object):
    """Stores information on a move range.

    This will store the start and end of the range, and all groups that
    are a part of it.
    """

    def __init__(self, start, end, groups=[]):
        self.start = start
        self.end = end
        self.groups = groups

    @property
    def last_group(self):
        return self.groups[(-1)]

    def add_group(self, group, group_index):
        if self.groups[(-1)] != group:
            self.groups.append((group, group_index))

    def __repr__(self):
        return b'<MoveRange(%d, %d, %r)>' % (self.start, self.end, self.groups)


class DiffOpcodeGenerator(object):
    ALPHANUM_RE = re.compile(b'\\w')
    WHITESPACE_RE = re.compile(b'\\s')
    MOVE_PREFERRED_MIN_LINES = 2
    MOVE_MIN_LINE_LENGTH = 20
    TAB_SIZE = 8

    def __init__(self, differ, diff=None, interdiff=None):
        self.differ = differ
        self.diff = diff
        self.interdiff = interdiff

    def __iter__(self):
        """Returns opcodes from the differ with extra metadata.

        This is a wrapper around a differ's get_opcodes function, which returns
        extra metadata along with each range. That metadata includes
        information on moved blocks of code and whitespace-only lines.

        This returns a list of opcodes as tuples in the form of
        (tag, i1, i2, j1, j2, meta).
        """
        self.groups = []
        self.removes = {}
        self.inserts = []
        opcodes = self.differ.get_opcodes()
        opcodes = self._apply_processors(opcodes)
        opcodes = self._generate_opcode_meta(opcodes)
        opcodes = self._apply_meta_processors(opcodes)
        self._group_opcodes(opcodes)
        self._compute_moves()
        for opcodes in self.groups:
            yield opcodes

    def _apply_processors(self, opcodes):
        if self.diff and self.interdiff:
            opcodes = filter_interdiff_opcodes(opcodes, self.diff, self.interdiff)
        for opcode in opcodes:
            yield opcode

    def _generate_opcode_meta(self, opcodes):
        for tag, i1, i2, j1, j2 in opcodes:
            meta = {b'whitespace_chunk': False, 
               b'whitespace_lines': []}
            if tag == b'replace':
                assert i2 - i1 == j2 - j1
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    if self.WHITESPACE_RE.sub(b'', self.differ.a[i]) == self.WHITESPACE_RE.sub(b'', self.differ.b[j]):
                        meta[b'whitespace_lines'].append((i + 1, j + 1))

                if len(meta[b'whitespace_lines']) == i2 - i1:
                    meta[b'whitespace_chunk'] = True
            elif tag == b'equal':
                for group in self._compute_chunk_indentation(i1, i2, j1, j2):
                    ii1, ii2, ij1, ij2, indentation_changes = group
                    if indentation_changes:
                        new_meta = dict({b'indentation_changes': indentation_changes}, **meta)
                    else:
                        new_meta = meta
                    yield (tag, ii1, ii2, ij1, ij2, new_meta)

                continue
            yield (tag, i1, i2, j1, j2, meta)

    def _apply_meta_processors(self, opcodes):
        if self.interdiff:
            opcodes = post_process_filtered_equals(opcodes)
        for opcode in opcodes:
            yield opcode

    def _group_opcodes(self, opcodes):
        for group_index, group in enumerate(opcodes):
            self.groups.append(group)
            tag = group[0]
            if tag in ('delete', 'replace'):
                i1 = group[1]
                i2 = group[2]
                for i in range(i1, i2):
                    line = self.differ.a[i].strip()
                    if line:
                        self.removes.setdefault(line, []).append((
                         i, group, group_index))

            if tag in ('insert', 'replace'):
                self.inserts.append(group)

    def _compute_chunk_indentation(self, i1, i2, j1, j2):
        indentation_changes = {}
        prev_has_indent = False
        prev_start_i = i1
        prev_start_j = j1
        for i, j in zip(range(i1, i2), range(j1, j2)):
            old_line = self.differ.a[i]
            new_line = self.differ.b[j]
            new_indentation_changes = {}
            indent_info = self._compute_line_indentation(old_line, new_line)
            has_indent = indent_info is not None
            if has_indent:
                key = b'%d-%d' % (i + 1, j + 1)
                new_indentation_changes[key] = indent_info
            if has_indent != prev_has_indent:
                if prev_start_i != i or prev_start_j != j:
                    yield (prev_start_i, i, prev_start_j, j, indentation_changes)
                prev_start_i = i
                prev_start_j = j
                prev_has_indent = has_indent
                indentation_changes = new_indentation_changes
            elif has_indent:
                indentation_changes.update(new_indentation_changes)

        if prev_start_i != i2 or prev_start_j != j2:
            yield (
             prev_start_i, i2, prev_start_j, j2, indentation_changes)
        return

    def _compute_line_indentation(self, old_line, new_line):
        if old_line == new_line:
            return
        else:
            old_line_stripped = old_line.lstrip()
            new_line_stripped = new_line.lstrip()
            old_line_indent_len = len(old_line) - len(old_line_stripped)
            new_line_indent_len = len(new_line) - len(new_line_stripped)
            old_line_indent = old_line[:old_line_indent_len]
            new_line_indent = new_line[:new_line_indent_len]
            norm_old_line_indent = old_line_indent.expandtabs(self.TAB_SIZE)
            norm_new_line_indent = new_line_indent.expandtabs(self.TAB_SIZE)
            norm_old_line_indent_len = len(norm_old_line_indent)
            norm_new_line_indent_len = len(norm_new_line_indent)
            norm_old_line_len = norm_old_line_indent_len + len(old_line_stripped)
            norm_new_line_len = norm_new_line_indent_len + len(new_line_stripped)
            line_len_diff = norm_new_line_len - norm_old_line_len
            if line_len_diff == 0:
                return
            is_indent = line_len_diff > 0
            if is_indent:
                raw_indent_len = new_line_indent_len
            else:
                raw_indent_len = old_line_indent_len
            raw_indent_len -= len(os.path.commonprefix([
             old_line_indent[::-1],
             new_line_indent[::-1]]))
            return (
             is_indent,
             raw_indent_len,
             abs(norm_old_line_indent_len - norm_new_line_indent_len))

    def _compute_moves(self):
        r_move_indexes_used = set()
        for insert in self.inserts:
            self._compute_move_for_insert(r_move_indexes_used, *insert)

    def _compute_move_for_insert(self, r_move_indexes_used, itag, ii1, ii2, ij1, ij2, imeta):
        """Compute move information for a given insert-like chunk.

        Args:
            r_move_indexes_used (set):
                All remove indexes that have already been included in a move
                range.

            itag (unicode):
                The chunk tag for the insert (``insert`` or ``replace``).

            ii1 (int):
                The 0-based start of the chunk on the original side.

            ii2 (int):
                The 0-based start of the next chunk on the original side.

            ij1 (int):
                The 0-based start of the chunk on the modification side.

            ij2 (int):
                The 0-based start of the next chunk on the modification side.

            imeta (dict):
                The metadata for the chunk for the modification, where the move
                ranges may be stored.
        """
        i_move_cur = ij1
        i_move_range = MoveRange(i_move_cur, i_move_cur)
        r_move_ranges = {}
        move_key = None
        is_replace = itag == b'replace'
        while i_move_cur < ij2:
            try:
                iline = self.differ.b[i_move_cur].strip()
            except IndexError:
                iline = None

            updated_range = False
            if iline and iline in self.removes:
                for ri, rgroup, rgroup_index in self.removes[iline]:
                    if ri in r_move_indexes_used:
                        continue
                    r_move_range = r_move_ranges.get(move_key)
                    if not r_move_range or ri != r_move_range.end + 1:
                        move_key = b'%s-%s-%s-%s' % rgroup[1:5]
                        r_move_range = r_move_ranges.get(move_key)
                    if r_move_range:
                        if ri == r_move_range.end + 1:
                            r_move_range.end = ri
                            r_move_range.add_group(rgroup, rgroup_index)
                            updated_range = True
                    elif not is_replace or i_move_cur - ij1 != ri - ii1:
                        r_move_ranges[move_key] = MoveRange(ri, ri, [(rgroup, rgroup_index)])
                        updated_range = True
                    if updated_range:
                        break

                if not updated_range and r_move_ranges:
                    i_move_cur -= 1
                    move_key = None
            elif iline == b'' and move_key:
                r_move_range = r_move_ranges.get(move_key)
                if r_move_range:
                    new_end_i = r_move_range.end + 1
                    if new_end_i < len(self.differ.a) and self.differ.a[new_end_i].strip() == b'':
                        r_move_range.end = new_end_i
                        last_group, last_group_index = r_move_range.last_group
                        if new_end_i >= last_group[2]:
                            cur_group_index = r_move_range.last_group[1] + 1
                            r_move_range.add_group(self.groups[cur_group_index], cur_group_index)
                        updated_range = True
            i_move_cur += 1
            if not updated_range or i_move_cur == ij2:
                if r_move_ranges:
                    r_move_range = self._find_longest_move_range(r_move_ranges)
                    r_move_range = self._determine_move_range(r_move_range)
                    if r_move_range:
                        i_range = range(i_move_range.start + 1, i_move_cur + 1)
                        r_range = range(r_move_range.start + 1, r_move_range.end + 2)
                        moved_to_ranges = dict(zip(r_range, i_range))
                        for group, group_index in r_move_range.groups:
                            rmeta = group[(-1)]
                            rmeta.setdefault(b'moved-to', {}).update(moved_to_ranges)

                        imeta.setdefault(b'moved-from', {}).update(dict(zip(i_range, r_range)))
                        r_move_indexes_used.update(r - 1 for r in r_range)
                move_key = None
                i_move_range = MoveRange(i_move_cur, i_move_cur)
                r_move_ranges = {}

        return

    def _find_longest_move_range(self, r_move_ranges):
        r_move_range = None
        for iter_move_range in six.itervalues(r_move_ranges):
            if not r_move_range:
                r_move_range = iter_move_range
            else:
                len1 = r_move_range.end - r_move_range.start
                len2 = iter_move_range.end - iter_move_range.start
                if len1 < len2:
                    r_move_range = iter_move_range
                elif len1 == len2:
                    r_move_range = None

        return r_move_range

    def _determine_move_range(self, r_move_range):
        """Determines if a move range is valid and should be included.

        This performs some tests to try to eliminate trivial changes that
        shouldn't have moves associated.

        Specifically, a move range is valid if it has at least one line
        with alpha-numeric characters and is at least 4 characters long when
        stripped.

        If the move range is valid, any trailing whitespace-only lines will
        be stripped, ensuring it covers only a valid range of content.
        """
        if not r_move_range:
            return
        else:
            end_i = r_move_range.end
            lines = self.differ.a[r_move_range.start:end_i + 1]
            new_end_i = None
            valid = False
            for i, line in enumerate(reversed(lines)):
                line = line.strip()
                if line:
                    if len(line) >= 4 and self.ALPHANUM_RE.search(line):
                        valid = True
                    if new_end_i is None or valid:
                        new_end_i = end_i - i
                    if valid:
                        break

            valid = valid and (new_end_i - r_move_range.start + 1 >= self.MOVE_PREFERRED_MIN_LINES or len(self.differ.a[r_move_range.start].strip()) >= self.MOVE_MIN_LINE_LENGTH)
            if not valid:
                return
            assert new_end_i is not None
            return MoveRange(r_move_range.start, new_end_i, r_move_range.groups)


_generator = DiffOpcodeGenerator

def get_diff_opcode_generator_class():
    """Returns the DiffOpcodeGenerator class used for generating opcodes."""
    return _generator


def set_diff_opcode_generator_class(renderer):
    """Sets the DiffOpcodeGenerator class used for generating opcodes."""
    assert renderer
    globals()[b'_generator'] = renderer


def get_diff_opcode_generator(*args, **kwargs):
    """Returns a DiffOpcodeGenerator instance used for generating opcodes."""
    return _generator(*args, **kwargs)