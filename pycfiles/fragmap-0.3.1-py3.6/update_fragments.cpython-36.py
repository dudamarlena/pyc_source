# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\update_fragments.py
# Compiled at: 2019-09-05 14:04:48
# Size of source mod 2**32: 12228 bytes
import copy
from .load_commits import BinaryHunk, nonnull_file, oldrange, newrange
from . import debug

class FragmentBoundNode:
    _diff_i = None
    _fragment = None
    _filename = None
    _line = None
    _kind = None
    START = 1
    END = 2

    def __lt__(a, b):
        return a._filename < b._filename or a._filename == b._filename and a._line < b._line

    def __init__(self, diff_i, file_patch, fragment_i, line, kind):
        self._diff_i = diff_i
        if file_patch.delta.is_binary:
            self._fragment = BinaryHunk(file_patch)
        else:
            self._fragment = file_patch.hunks[fragment_i]
        self._fragment_i = fragment_i
        self._filename = nonnull_file(file_patch.delta)
        self._line = line
        self._kind = kind

    def __repr__(self):
        kind_str = 'START'
        if self._kind == FragmentBoundNode.END:
            kind_str = 'END'
        return '<Node: (%s, %d), (%s, %d), %s>' % (self._diff_i, self._fragment_i, self._filename, self._line, kind_str)


class FragmentBoundLine:
    _nodehistory = None
    _startdiff_i = None
    _kind = None

    def __lt__(a, b):

        def lt_at_diff(a, b, diff_i):
            a_file = a._nodehistory[diff_i]._filename
            b_file = b._nodehistory[diff_i]._filename
            a_line = a._nodehistory[diff_i]._line
            b_line = b._nodehistory[diff_i]._line
            if a._kind == FragmentBoundNode.END:
                a_line += 1
            if b._kind == FragmentBoundNode.END:
                b_line += 1
            if a_file < b_file:
                debug.get('sorting').debug('file %s < %s at diff %d', a_file, b_file, diff_i)
                return True
            else:
                if a_file == b_file:
                    if a_line < b_line:
                        debug.get('sorting').debug('line %d < %d at diff %d', a_line, b_line, diff_i)
                        return True
                return False

        debug.get('sorting').debug('<<<<< Comparing %s and %s', a, b)
        common_diffs = set(a._nodehistory.keys()) & set(b._nodehistory.keys())
        common_diffs -= {a._startdiff_i - 1, b._startdiff_i - 1}
        first_common_diff_i = min(common_diffs)
        prev_diff_i = first_common_diff_i - 1
        debug.get('sorting').debug('First_common=%d', first_common_diff_i)
        if lt_at_diff(a, b, prev_diff_i):
            debug.get('sorting').debug('Lines are < at prev diff %d', prev_diff_i)
            return True
        else:
            if lt_at_diff(a, b, first_common_diff_i):
                debug.get('sorting').debug('Lines are < at first diff %d', first_common_diff_i)
                return True
            debug.get('sorting').debug('Lines are !<')
            return False

    def eq_at_diff(a, b, diff_i):
        a_file = a._nodehistory[diff_i]._filename
        b_file = b._nodehistory[diff_i]._filename
        a_line = a._nodehistory[diff_i]._line
        b_line = b._nodehistory[diff_i]._line
        if a._kind == FragmentBoundNode.END:
            a_line += 1
        if b._kind == FragmentBoundNode.END:
            b_line += 1
        if a_file != b_file:
            debug.get('grouping').debug('file %s != %s at diff %d', a_file, b_file, diff_i)
            return False
        else:
            if a_line != b_line:
                debug.get('grouping').debug('line %d != %d at diff %d', a_line, b_line, diff_i)
                return False
            return True

    def __eq__(a, b):
        if a._kind != b._kind and a._startdiff_i == b._startdiff_i:
            debug.get('grouping').debug('kind %d != %d and same startdiff %d', a._kind, b._kind, a._startdiff_i)
            return False
        else:
            debug.get('grouping').debug('===== Comparing %s and %s', a, b)
            common_diffs = set(a._nodehistory.keys()) & set(b._nodehistory.keys())
            common_diffs -= {a._startdiff_i - 1, b._startdiff_i - 1}
            first_common_diff_i = min(common_diffs)
            prev_diff_i = first_common_diff_i - 1
            if a.eq_at_diff(b, first_common_diff_i):
                if a.eq_at_diff(b, prev_diff_i):
                    if a._kind == b._kind or a._startdiff_i != b._startdiff_i:
                        debug.get('grouping').debug('Lines are ==')
                        return True
            debug.get('grouping').debug('Lines are !=')
            return False

    def __init__(self, node):
        self._startdiff_i = node._diff_i
        self._nodehistory = {self._startdiff_i - 1: node}
        self._kind = node._kind

    def __repr__(self):
        return ' \n<FragmentBoundLine: %d, %s>' % (
         self._startdiff_i,
         ''.join(['\n %d: %s' % (key, val) for key, val in sorted(self._nodehistory.items())]))

    def last(self):
        return self._nodehistory[max(self._nodehistory.keys())]

    def update_unchanged(self, diff_i):
        """
    Update the node line with no changes. Simply clones
    the latest node, adds it to the history and returns it.
    """
        if diff_i not in self._nodehistory:
            if diff_i < 0:
                diff_i = 0
            updated_node = copy.copy(self._nodehistory[(diff_i - 1)])
            self._nodehistory[diff_i] = updated_node
        return self._nodehistory[diff_i]

    def update(self, diff_i, filename, line):
        updated_node = self.update_unchanged(diff_i)
        debug.get('update').debug('Updating %s with (%d, %s, %d)', self, diff_i, filename, line)
        updated_node._diff_i = diff_i
        updated_node._filename = filename
        updated_node._line = line


def update_new_bound(fragment, bound_kind):
    """
  Update a bound that belongs to the current diff. Simply apply whatever
  fragment it belongs to.
  """
    line = 0
    marker = newrange(fragment)
    if bound_kind == FragmentBoundNode.START:
        line = marker._start
        debug.get('update').debug('Setting new start line to %d', line)
    else:
        if bound_kind == FragmentBoundNode.END:
            line = marker._end
            debug.get('update').debug('Setting new end line to %d', line)
    return line


def update_inherited_bound(line, bound_kind, file_patch):
    """
  Update a bound inherited from an older patch. Must never be
  called for bounds belonging to the newest patch. Use
  update_new_bound for them.
  """
    marker = None
    for patch_fragment in file_patch.hunks:
        if oldrange(patch_fragment)._start <= line:
            marker = patch_fragment
        else:
            break

    if marker is None:
        if file_patch.delta.is_binary:
            marker = BinaryHunk(file_patch)
    debug.get('update').debug('Update_line: %d %s %s', line, bound_kind, file_patch)
    debug.get('update').debug('Marker: %s', marker)
    if marker is not None:
        if line <= oldrange(marker)._end:
            debug.get('update').debug('Line %d is inside range %s', line, oldrange(marker))
            if bound_kind == FragmentBoundNode.START:
                line = newrange(marker)._start
                debug.get('update').debug('Setting start line to %d', line)
            else:
                if bound_kind == FragmentBoundNode.END:
                    line = newrange(marker)._end
                    debug.get('update').debug('Setting end line to %d', line)
        else:
            debug.get('update').debug('Line %d is after range %s; shifting %d' % (
             line, oldrange(marker), newrange(marker)._end - oldrange(marker)._end))
            line += newrange(marker)._end - oldrange(marker)._end
    return line


def update_line(line, bound_kind, fragment, startdiff_i, diff_i, file_patch):
    if diff_i == startdiff_i:
        return update_new_bound(fragment, bound_kind)
    else:
        return update_inherited_bound(line, bound_kind, file_patch)


def update_file_positions(file_node_lines, file_patch, diff_i):
    """
  Update all the nodes belonging in a file with a file patch.
  """
    for node_line in file_node_lines:
        debug.get('update').debug('Node before: %s', node_line.last())
        node_line.update(diff_i, file_patch.delta.new_file.path, update_line(node_line.last()._line, node_line.last()._kind, node_line.last()._fragment, node_line._startdiff_i, diff_i, file_patch))
        debug.get('update').debug('Node after: %s', node_line.last())


def update_positions(node_lines, patch, diff_i):
    """
  Update all node lines with a multi-file patch.
  """
    if len(patch.filepatches) > 0:
        for file_patch in patch.filepatches:
            oldfile = file_patch.delta.old_file.path
            file_node_lines = []
            for nl in node_lines:
                debug.get('update').debug('last: %s', nl.last()._filename)
                if nl.last()._filename == oldfile:
                    file_node_lines += [nl]
                else:
                    nl.update_unchanged(diff_i)

            debug.get('update').debug('Updating file: %s', oldfile)
            debug.get('update').debug('Node lines: %s', file_node_lines)
            update_file_positions(file_node_lines, file_patch, diff_i)
            debug.get('update').debug('Updated node lines: %s', file_node_lines)

    else:
        debug.get('update').debug('No fragments in patch')
        for nl in node_lines:
            debug.get('update').debug('last: %s', nl.last()._filename)
            nl.update_unchanged(diff_i)

    return node_lines


def extract_nodes(diff, diff_i):
    node_list = []
    for file_patch in diff.filepatches:
        for fragment_i in range(len(file_patch.hunks)):
            fragment = file_patch.hunks[fragment_i]
            node_list += [
             FragmentBoundNode(diff_i, file_patch, fragment_i, oldrange(fragment)._start, FragmentBoundNode.START),
             FragmentBoundNode(diff_i, file_patch, fragment_i, oldrange(fragment)._end, FragmentBoundNode.END)]

        if file_patch.delta.is_binary:
            binary_fragment = BinaryHunk(file_patch)
            node_list += [
             FragmentBoundNode(diff_i, file_patch, -1, oldrange(binary_fragment)._start, FragmentBoundNode.START),
             FragmentBoundNode(diff_i, file_patch, -1, oldrange(binary_fragment)._end, FragmentBoundNode.END)]

    return node_list


def extract_node_lines(diff, diff_i):
    return list(map(FragmentBoundLine, extract_nodes(diff, diff_i)))


def update_all_positions_to_latest(diff_list):
    """
  Update all diffs to the latest patch, letting
  newer diffs act as patches for older diffs.
  Assumes diff_list is sorted in ascending time.
  """
    debug.get('update').debug('update_all_positions: %s', diff_list)
    node_line_list = []
    for i in range(len(diff_list)):
        node_line_list += extract_node_lines(diff_list[i], i)
        debug.get('update').debug('= All to latest: All extracted: %d %s', i, node_line_list)
        update_positions(node_line_list, diff_list[i], i)
        debug.get('update').debug('= All to latest: All updated: %s', node_line_list)

    return node_line_list