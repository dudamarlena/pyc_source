# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/wrappers/node2vec_embedding.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 4467 bytes
import networkx as nx, ast, numpy as np
from subprocess import call
from scipy import optimize
import os
from sklearn import linear_model
from sklearn.metrics import f1_score
from sklearn.multiclass import OneVsRestClassifier
import multiprocessing as mp
from collections import OrderedDict
from .benchmark_nodes import *
import time

def call_node2vec_binary(input_graph, output_graph, p=1, q=1, dimension=128, directed=False, weighted=True, binary='./node2vec'):
    input_params = []
    input_params.append(binary)
    input_params.append('-i:' + input_graph)
    input_params.append('-o:' + output_graph)
    input_params.append('-d:' + str(dimension))
    input_params.append('-p:' + str(p))
    input_params.append('-q:' + str(q))
    input_params.append('-v')
    if directed:
        input_params.append('-d')
    if weighted:
        input_params.append('-w')
    call(input_params)
    print('input params {}'.format(input_params))
    call(['rm', '-rf', 'tmp/*'])


def n2v_embedding(G, targets, verbose=False, sample_size=0.5, outfile_name='test.emb', p=-100, q=-100, binary_path='./node2vec', parameter_range=[0.25, 0.5, 1, 2, 4], embedding_dimension=128):
    clf = OneVsRestClassifier((linear_model.LogisticRegression()), n_jobs=(mp.cpu_count()))
    if verbose:
        print(nx.info(G))
    N = len(G.nodes())
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    tmp_graph = 'tmp/tmpgraph.edges'
    out_graph = 'tmp/tmpgraph.emb'
    number_of_nodes = len(G.nodes())
    number_of_edges = len(G.edges())
    if verbose:
        print('Graph has {} edges and {} nodes.'.format(number_of_edges, number_of_nodes))
    f = open(tmp_graph, 'w+')
    for e in G.edges(data=True):
        f.write(str(e[0]) + ' ' + str(e[1]) + ' ' + str(float(e[2]['weight'])) + '\n')

    f.close()
    if verbose:
        print('N2V training phase..')
    vals = parameter_range
    copt = 0
    cset = [0, 0]
    dim = embedding_dimension
    if float(p) > -100 and float(q) > -100:
        print('Runing specific config of N2V.')
        call_node2vec_binary(tmp_graph, outfile_name, p=p, q=q, directed=False, weighted=True)
    else:
        for x in vals:
            for y in vals:
                call_node2vec_binary(tmp_graph, outfile_name, p=x, q=y, directed=False, weighted=True, binary=binary_path)
                print('parsing {}'.format(outfile_name))
                rdict = benchmark_node_classification(outfile_name, graph,
                  targets,
                  percent=(float(sample_size)))
                mi, ma, misd, masd = rdict[float(sample_size)]
                if ma > copt:
                    if verbose:
                        print('Updating the parameters: {} {}'.format(ma, cset))
                    cset = [x, y]
                    copt = ma
                else:
                    print('Current optimum {}'.format(ma))
                call(['rm', '-rf', outfile_name])

        print('Final iteration phase..')
        call_node2vec_binary(tmp_graph, outfile_name, p=(cset[0]), q=(cset[1]), directed=False, weighted=True, binary='./node2vec')
        with open(outfile_name, 'r') as (f):
            fl = f.readline()
            print('Resulting dimensions:{}'.format(fl))
        call(['rm', '-rf', 'tmp'])


def learn_embedding(core_network, labels=[], ssize=0.5, embedding_outfile='out.emb', p=0.1, q=0.1, binary_path='./node2vec', parameter_range='[0.25,0.50,1,2,4]'):
    start = time.time()
    parameter_range = ast.literal_eval(parameter_range)
    if self.method == 'default_n2v':
        n2v_embedding(core_network, targets=labels,
          sample_size=ssize,
          verbose=(self.vb),
          outfile_name=embedding_outfile,
          p=p,
          q=q,
          binary_path=binary_path,
          parameter_range=parameter_range)
    end = time.time()
    elapsed = end - start
    return (self.method, elapsed)