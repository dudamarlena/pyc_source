# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/tests/dummy/sanity_cfg.py
# Compiled at: 2011-05-10 05:58:20


class dummyCfg(object):

    def __init__(self):
        self.generation = True
        self.gen_dir = 'gen'
        self.mutation = True
        self.mut_dir = 'mut'
        self.combination = True
        self.comb_dir = 'comb'
        self.log_dir = 'log'
        self.incidents_dir = 'fails'
        self.tmp_dir = 'tmp'
        self.samples_dir = 'samples'