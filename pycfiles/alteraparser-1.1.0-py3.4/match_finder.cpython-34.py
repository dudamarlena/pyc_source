# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/match_finder.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 2854 bytes
from .processor import Processor, ProcessingResult
from .vertex import VertexCategory

class MatchFinder(Processor):

    def __init__(self, input):
        self._MatchFinder__path = []
        self._MatchFinder__input = input
        self._MatchFinder__buffer = []
        self._MatchFinder__match_char = None
        self._MatchFinder__stopped = False
        self._MatchFinder__debug = False

    def process(self, vertex, path):
        if self._MatchFinder__stopped:
            return ProcessingResult.STOP
        else:
            if not self._MatchFinder__match_char:
                self._MatchFinder__match_char = self._MatchFinder__get_next_char()
            if self._MatchFinder__match_char:
                return self._MatchFinder__process_with_char_search(vertex)
            return self._MatchFinder__process_without_char_search(vertex)

    def undo(self, vertex, path):
        if not self._MatchFinder__path:
            return
        v, ch = self._MatchFinder__path[(-1)]
        if vertex is v:
            self._MatchFinder__path.pop()
            if ch is not None:
                if self._MatchFinder__match_char:
                    self._MatchFinder__buffer.append(self._MatchFinder__match_char)
                    self._MatchFinder__match_char = None
                self._MatchFinder__buffer.append(ch)
        if v.is_group_end():
            if v.is_rule_end:
                self._MatchFinder__stopped = True

    def get_path(self):
        return self._MatchFinder__path

    path = property(get_path)

    def get_stopped(self):
        return self._MatchFinder__stopped

    stopped = property(get_stopped)

    def debug_mode(self, debug=True):
        self._MatchFinder__debug = debug
        return self

    def __process_with_char_search(self, vertex):
        catg = vertex.get_category()
        if catg == VertexCategory.MATCHER:
            if self._MatchFinder__debug:
                print("Searching for '{}'".format(self._MatchFinder__match_char))
                print(vertex)
            if vertex.matches(self._MatchFinder__match_char):
                self._MatchFinder__path.append((vertex, self._MatchFinder__match_char))
                if self._MatchFinder__debug:
                    print('Match: {}'.format(self._MatchFinder__match_char))
                self._MatchFinder__match_char = None
                return ProcessingResult.CONTINUE
            else:
                return ProcessingResult.GO_BACK
        else:
            if catg == VertexCategory.FINAL:
                return ProcessingResult.GO_BACK
            else:
                self._MatchFinder__path.append((vertex, None))
                return ProcessingResult.CONTINUE

    def __process_without_char_search(self, vertex):
        catg = vertex.get_category()
        if catg == VertexCategory.MATCHER:
            return ProcessingResult.GO_BACK
        else:
            if catg == VertexCategory.FINAL:
                return ProcessingResult.STOP
            self._MatchFinder__path.append((vertex, None))
            return ProcessingResult.CONTINUE

    def __get_next_char(self):
        if self._MatchFinder__buffer:
            return self._MatchFinder__buffer.pop()
        else:
            if self._MatchFinder__input.has_next_char():
                return self._MatchFinder__input.get_next_char()
            return