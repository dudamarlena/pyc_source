# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/message_generator/git_diff_message_generator.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 2821 bytes
from typing import List, Optional
from plover_vcs.message_generator.line_changes import LineChanges
from plover_vcs.message_generator.message_generator import MessageGenerator
import re
changes_start = re.compile('@@[^@]*@@')
dictionary_line = re.compile('"(.*)": ?"(.*)",?')
file_name = re.compile('diff --git .*\\/([^\\/\\s]*)')

class GitSingleFileDiffMessageGenerator(MessageGenerator):
    """GitSingleFileDiffMessageGenerator"""

    def get_message(self, diff: str) -> str:
        file_changed = self.get_filename(diff)
        line_changes = self.get_line_changes(diff)
        return 'Update {}\n\n{}'.format(file_changed, self.format_commit_body(line_changes))

    @staticmethod
    def get_filename(diff: str) -> Optional[str]:
        match = file_name.match(diff)
        if not match:
            return
        else:
            return match.group(1)

    @staticmethod
    def get_line_changes(diff: str) -> LineChanges:
        file_changes = changes_start.split(diff)[1]
        lines = file_changes.splitlines()
        line_changes = LineChanges()
        line_changes.added = [add[1:] for add in lines if add.startswith('+')]
        line_changes.deleted = [delete[1:] for delete in lines if delete.startswith('-')]
        return line_changes

    @staticmethod
    def format_dictionary_change(line: str) -> Optional[str]:
        """
        If the line is a change to a json dictionary, format it as
        key: value
        :param line: line to format
        :return: formatted line
        """
        match = dictionary_line.match(line)
        if not match:
            return
        else:
            return ('{} → {}'.format)(*match.groups())

    def format_lines(self, lines: List[str], prefix: str='') -> str:
        """
        formats the given lines:
        [1, 2] ->
        prefix1
        prefix2
        :param lines: lines to format together
        :param prefix: prefix to append to each line
        :return: lines as formatted string
        """
        formatted_lines = (self.format_dictionary_change(line) for line in lines)
        return '\n'.join(prefix + line for line in formatted_lines if line is not None)

    def format_commit_body(self, line_changes: LineChanges) -> str:
        body = self.format_lines(line_changes.added, 'Added Stroke: ')
        return body + '\n' + self.format_lines(line_changes.deleted, 'Deleted Stroke: ')