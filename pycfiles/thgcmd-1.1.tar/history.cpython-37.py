# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/history.py
# Compiled at: 2019-07-17 15:07:37
# Size of source mod 2**32: 11567 bytes
"""
History management classes
"""
import re
from typing import List, Union
import attr
from . import utils
from .parsing import Statement

@attr.s(frozen=True)
class HistoryItem:
    __doc__ = 'Class used to represent one command in the History list'
    _listformat = ' {:>4}  {}'
    _ex_listformat = ' {:>4}x {}'
    statement = attr.ib(default=None, validator=(attr.validators.instance_of(Statement)))
    idx = attr.ib(default=None, validator=(attr.validators.instance_of(int)))

    def __str__(self):
        """A convenient human readable representation of the history item"""
        return self.statement.raw

    @property
    def raw(self) -> str:
        """Return the raw input from the user for this item"""
        return self.statement.raw

    @property
    def expanded(self) -> str:
        """Return the command as run which includes shortcuts and aliases resolved plus any changes made in hooks"""
        return self.statement.expanded_command_line

    def pr(self, script=False, expanded=False, verbose=False) -> str:
        """Represent a HistoryItem in a pretty fashion suitable for printing.

        If you pass verbose=True, script and expanded will be ignored

        :return: pretty print string version of a HistoryItem
        """
        if verbose:
            ret_str = self._listformat.format(self.idx, self.raw.rstrip())
            if self.raw != self.expanded.rstrip():
                ret_str += '\n' + self._ex_listformat.format(self.idx, self.expanded.rstrip())
        elif expanded:
            ret_str = self.expanded.rstrip()
        else:
            ret_str = self.raw.rstrip()
            if self.statement.multiline_command:
                ret_str = ret_str.replace('\n', ' ')
            else:
                ret_str = script or self._listformat.format(self.idx, ret_str)
        return ret_str


class History(list):
    __doc__ = 'A list of HistoryItems that knows how to respond to user requests.\n\n    Here are some key methods:\n\n    select() - parse user input and return a list of relevant history items\n    str_search() - return a list of history items which contain the given string\n    regex_search() - return a list of history items which match a given regex\n    get() - return a single element of the list, using 1 based indexing\n    span() - given a 1-based slice, return the appropriate list of history items\n    '

    def __init__(self, seq=()):
        super().__init__(seq)
        self.session_start_index = 0

    def start_session(self) -> None:
        """Start a new session, thereby setting the next index as the first index in the new session."""
        self.session_start_index = len(self)

    def _zero_based_index(self, onebased: Union[(int, str)]) -> int:
        """Convert a one-based index to a zero-based index."""
        result = int(onebased)
        if result > 0:
            result -= 1
        return result

    def append(self, new):
        """Append a HistoryItem to end of the History list.

        :param new: command line to convert to HistoryItem and add to the end of the History list
        """
        history_item = HistoryItem(new, len(self) + 1)
        super().append(history_item)

    def clear(self):
        """Remove all items from the History list."""
        super().clear()
        self.start_session()

    def get(self, index: Union[(int, str)]) -> HistoryItem:
        """Get item from the History list using 1-based indexing.

        :param index: optional item to get (index as either integer or string)
        :return: a single HistoryItem
        """
        index = int(index)
        if index == 0:
            raise IndexError('The first command in history is command 1.')
        else:
            if index < 0:
                return self[index]
            return self[(index - 1)]

    spanpattern = re.compile('^\\s*(?P<start>-?[1-9]\\d*)?(?P<separator>:|(\\.{2,}))?(?P<end>-?[1-9]\\d*)?\\s*$')

    def span(self, span: str, include_persisted: bool=False) -> List[HistoryItem]:
        """Return an index or slice of the History list,

        :param span: string containing an index or a slice
        :param include_persisted: if True, then retrieve full results including from persisted history
        :return: a list of HistoryItems

        This method can accommodate input in any of these forms:

            a
            -a
            a..b or a:b
            a.. or a:
            ..a or :a
            -a.. or -a:
            ..-a or :-a

        Different from native python indexing and slicing of arrays, this method
        uses 1-based array numbering. Users who are not programmers can't grok
        0 based numbering. Programmers can usually grok either. Which reminds me,
        there are only two hard problems in programming:

        - naming
        - cache invalidation
        - off by one errors

        """
        if span.lower() in ('*', '-', 'all'):
            span = ':'
        else:
            results = self.spanpattern.search(span)
            if not results:
                raise ValueError('History indices must be positive or negative integers, and may not be zero.')
            else:
                sep = results.group('separator')
                start = results.group('start')
                if start:
                    start = self._zero_based_index(start)
                else:
                    end = results.group('end')
                    if end:
                        end = int(end)
                        if end == -1:
                            end = None
                        else:
                            if end < -1:
                                end += 1
                    elif start is not None and end is not None:
                        result = self[start:end]
                    else:
                        if start is not None and sep is not None:
                            result = self[start:]
                        else:
                            if end is not None:
                                if sep is not None:
                                    if include_persisted:
                                        result = self[:end]
                                else:
                                    result = self[self.session_start_index:end]
                            else:
                                if start is not None:
                                    result = [self[start]]
                                else:
                                    if include_persisted:
                                        result = self[:]
                                    else:
                                        result = self[self.session_start_index:]
        return result

    def str_search(self, search: str, include_persisted: bool=False) -> List[HistoryItem]:
        """Find history items which contain a given string

        :param search: the string to search for
        :param include_persisted: if True, then search full history including persisted history
        :return: a list of history items, or an empty list if the string was not found
        """

        def isin(history_item):
            sloppy = utils.norm_fold(search)
            inraw = sloppy in utils.norm_fold(history_item.raw)
            inexpanded = sloppy in utils.norm_fold(history_item.expanded)
            return inraw or inexpanded

        search_list = self if include_persisted else self[self.session_start_index:]
        return [item for item in search_list if isin(item)]

    def regex_search(self, regex: str, include_persisted: bool=False) -> List[HistoryItem]:
        """Find history items which match a given regular expression

        :param regex: the regular expression to search for.
        :param include_persisted: if True, then search full history including persisted history
        :return: a list of history items, or an empty list if the string was not found
        """
        regex = regex.strip()
        if regex.startswith('/'):
            if regex.endswith('/'):
                regex = regex[1:-1]
        finder = re.compile(regex, re.DOTALL | re.MULTILINE)

        def isin(hi):
            return finder.search(hi.raw) or finder.search(hi.expanded)

        search_list = self if include_persisted else self[self.session_start_index:]
        return [itm for itm in search_list if isin(itm)]

    def truncate(self, max_length: int) -> None:
        """Truncate the length of the history, dropping the oldest items if necessary

        :param max_length: the maximum length of the history, if negative, all history
                           items will be deleted
        :return: nothing
        """
        if max_length <= 0:
            del self[:]
        else:
            if len(self) > max_length:
                last_element = len(self) - max_length
                del self[0:last_element]