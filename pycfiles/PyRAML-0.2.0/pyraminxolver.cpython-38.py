# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyraminxolver\pyraminxolver.py
# Compiled at: 2019-10-23 13:39:38
# Size of source mod 2**32: 1758 bytes
from collections import deque
import pickle, time
from . import Pyraminx, PYRAMINX_CASE_PATH

class PyraminXolver:

    def __init__--- This code section failed: ---

 L.   9         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              PYRAMINX_CASE_PATH
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           28  'to 28'
               10  STORE_FAST               'f'

 L.  10        12  LOAD_GLOBAL              pickle
               14  LOAD_METHOD              load
               16  LOAD_FAST                'f'
               18  CALL_METHOD_1         1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               graph
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH        8  '8'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

 L.  11        34  LOAD_STR                 'U'
               36  LOAD_STR                 "U'"
               38  LOAD_STR                 'R'
               40  LOAD_STR                 "R'"
               42  LOAD_STR                 'L'
               44  LOAD_STR                 "L'"
               46  LOAD_STR                 'B'
               48  LOAD_STR                 "B'"
               50  BUILD_LIST_8          8 
               52  LOAD_FAST                'self'
               54  STORE_ATTR               moves

 L.  12        56  LOAD_GLOBAL              Pyraminx
               58  CALL_FUNCTION_0       0  ''
               60  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 26

    def search(self, state, max_slack=0):
        start_time = time.time_ns()
        solutions = []
        k = 0
        queue = deque
        queue.append(state, [], [state], 0)
        while queue:
            state, moves, path, slack = queue.popleft()
            depth = self.graph[state][0]
            k += 1
            if self.graph[state][0] > 0:
                for i in range(1, 9):
                    if len(moves) > 0 and (i - 1) // 2 == (moves[(-1)] - 1) // 2:
                        pass
                    else:
                        new_state = self.graph[state][i]
                        new_slack = slack + self.graph[new_state][0] - depth + 1
                        if new_slack <= max_slack:
                            queue.append(new_state, moves + [i], path + [new_state], new_slack)

            else:
                solutions.append(self.parsemoves, len(moves), time.time_ns() - start_time, path)

        return solutions

    def parse(self, moves):
        return ' '.join[self.moves[(x - 1)] for x in moves]

    def scramble_to_state(self, algorithm):
        moves = algorithm.split' '
        state = 0
        for move in moves:
            move_idx = self.moves.indexmove + 1
            state = self.graph[state][move_idx]

        return state

    def search_scramble(self, algorithm, max_slack=0):
        state = self.scramble_to_statealgorithm
        return self.search(state, max_slack=max_slack)