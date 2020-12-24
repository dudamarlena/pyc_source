# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alphan/Documents/svn/academic/bu/research/implementation/lomap-ltl_optimal_multi-agent_planner/trunk/examples/ijrr2014_rec_hor/environment.py
# Compiled at: 2015-04-14 16:17:38


class Environment:

    def __init__(self, case):
        """Defines regions in the environment.
                """
        self.global_reqs = dict()
        self.local_reqs = dict()
        if case == 'case1':
            self.global_reqs[(3, 1)] = {'reqs': {'photo'}, 'color': 'green'}
            self.global_reqs[(5, 10)] = {'reqs': {'upload'}, 'color': 'blue'}
            self.global_reqs[(9, 7)] = {'reqs': {'upload'}, 'color': 'blue'}
            self.local_reqs = dict()
            self.local_reqs[(1, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(2, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(3, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(4, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(5, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(6, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(7, 7)] = {'reqs': {'unsafe'}, 'on': True, 'color': 'yellow'}
            self.local_reqs[(9, 4)] = {'reqs': {'extinguish'}, 'on': True, 'color': 'red'}
            self.local_reqs[(9, 2)] = {'reqs': {'assist'}, 'on': True, 'color': 'cyan'}
        elif case == 'case2':
            self.global_reqs[(3, 3)] = {'reqs': {'photo1'}, 'color': 'LightGreen'}
            self.global_reqs[(19, 6)] = {'reqs': {'photo2'}, 'color': 'Green'}
            self.global_reqs[(11, 10)] = {'reqs': {'upload'}, 'color': 'blue'}
            self.local_reqs = dict()
            self.local_reqs[(8, 8)] = {'reqs': {'pickup'}, 'on': True, 'color': 'red'}
            self.local_reqs[(6, 7)] = {'reqs': {'dropoff'}, 'on': True, 'color': 'cyan'}
            self.local_reqs[(9, 6)] = {'reqs': {'pickup'}, 'on': True, 'color': 'red'}
            self.local_reqs[(3, 5)] = {'reqs': {'dropoff'}, 'on': True, 'color': 'cyan'}
        elif case == 'case3':
            self.global_reqs[(3, 3)] = {'reqs': {'photo1'}, 'color': 'LightGreen'}
            self.global_reqs[(19, 6)] = {'reqs': {'photo2'}, 'color': 'DarkGreen'}
            self.global_reqs[(11, 10)] = {'reqs': {'upload'}, 'color': 'blue'}
            self.local_reqs = dict()
            self.local_reqs[(14, 8)] = {'reqs': {'pickup1'}, 'on': True, 'color': 'Red'}
            self.local_reqs[(12, 7)] = {'reqs': {'dropoff1'}, 'on': True, 'color': 'Cyan'}
            self.local_reqs[(13, 4)] = {'reqs': {'pickup2'}, 'on': True, 'color': 'DarkRed'}
            self.local_reqs[(16, 6)] = {'reqs': {'dropoff2'}, 'on': True, 'color': 'DarkCyan'}
        else:
            assert False, 'Case %s is not implemented' % case