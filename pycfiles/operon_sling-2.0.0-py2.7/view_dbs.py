# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sling/tasks/view_dbs.py
# Compiled at: 2019-11-01 07:27:20
import argparse, sling, os

def run():
    parser = argparse.ArgumentParser(description='View available HMM collections and their parameters', usage='sling view_dbs')
    databases = sling.utils.databases
    databases = ['default'] + databases
    d = os.path.abspath(os.path.dirname(sling.__file__))
    data_env = os.path.join(d, 'data/')
    for db in databases:
        print '################  Name: ' + db + '  ################'
        req = {}
        with open(os.path.join(data_env, db + '.txt')) as (f):
            for line in f:
                toks = line.strip().split()
                req[toks[0]] = toks[1]

        print 'Order: ' + req['order']
        print 'Maximum overlap: ' + req['max_overlap']
        print 'Maximum distance: ' + req['max_distance']
        print 'Maximum hit length: ' + req['max_hit_length']
        print 'Minimum hit length: ' + req['min_hit_length']
        print 'Maximum upstream length: ' + req['max_upstream_length']
        print 'Minimum upstream length: ' + req['min_upstream_length']
        print 'Maximum downstream length: ' + req['max_downstream_length']
        print 'Minimum downstream length: ' + req['min_downstream_length']
        print 'Maximum difference from average length (if given): ' + req['max_diff_avg_length']
        print '\n'