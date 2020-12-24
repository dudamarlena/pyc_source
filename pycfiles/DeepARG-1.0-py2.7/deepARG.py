# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/predict/bin/deepARG.py
# Compiled at: 2020-04-25 14:56:05
import os, sys, json
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import numpy as np
from lasagne import layers
from lasagne import init
import lasagne
from lasagne.updates import sgd, nesterov_momentum
from nolearn.lasagne import NeuralNet
import theano, process_blast, cPickle
from deeparg.predict.bin.model import model
import math
from itertools import islice
from tqdm import tqdm
import logging
logger = logging.getLogger()
floatX = theano.config.floatX

def chunks(data, size=10000):
    it = iter(data)
    for i in xrange(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}


def make_xy(alignments, Features):
    SF = {i:True for i in Features}
    samples = alignments.keys()
    X = alignments.values()
    for i in SF:
        try:
            a = X[0][i]
        except:
            X[0].update({i: 0})

    return [
     samples, X]


def main(deepL, clf, alignments, version):
    S, X = make_xy(alignments, deepL['features'])
    h = DictVectorizer(sparse=False)
    del alignments
    X = h.fit_transform(X)
    X = X.astype(floatX)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(X)
    proba = clf.predict_proba(X)
    preds = []
    probs = []
    deepL['Y_rev'].update({10000: 'unclassified'})
    SP = []
    for ix, p in enumerate(proba):
        npx = np.argsort(p)
        px = npx[(-1)]
        if 0.0 < p[px] < 0.9:
            preds.append(npx[(-2)])
            probs.append(p[npx[(-2)]])
            SP.append(S[ix])
            preds.append(px)
            probs.append(p[px])
            SP.append(S[ix])
        elif p[px] >= 0.9:
            preds.append(px)
            probs.append(p[px])
            SP.append(S[ix])

    return [ [SP[ix], deepL['Y_rev'][i], probs[ix]] for ix, i in enumerate(preds) ]


import operator

def process(fin, fon, iden, version, evalue, prob, minCoverage, pipeline, version_m, args):
    fi = fin
    logger.info('Loading deep learning model ...')
    deepL = cPickle.load(open(args.data_path + '/model/' + version_m + '/metadata' + version + '.pkl'))
    clf = NeuralNet(layers=model(deepL['input_nodes'], deepL['output_nodes']), update=nesterov_momentum, update_learning_rate=0.01, update_momentum=0.9, regression=False, max_epochs=100, verbose=2)
    clf.load_params_from(args.data_path + '/model/' + version_m + '/model' + version + '.pkl')
    logger.info('loading gene lengths')
    glen = {i.split()[0]:float(i.split()[1]) for i in open(args.data_path + '/database/' + version_m + '/features.gene.length')}
    logger.info('Loading sample to analyze')
    align, BH = process_blast.make_alignments_json(fi, iden=iden, eval=evalue, coverage=minCoverage, BitScore=True, Features=deepL['features'], glen=glen, pipeline=pipeline)
    logger.info('Predicting ARG-like reads: Running deepARG' + version + ' model version ' + version_m)
    logger.info('input dataset is splitted into chunks of 10000 reads')
    chunks_input = chunks(align, size=10000)
    predict = []
    for _chunk in tqdm(chunks_input, total=int(len(align) / 10000), unit='chunks'):
        predict += main(deepL, clf, _chunk, version)

    logger.info('Predicting ARGs')
    fo = open(fon + '.ARG', 'w')
    fo2 = open(fon + '.potential.ARG', 'w')
    fo.write('#ARG\tquery-start\tquery-end\tread_id\tpredicted_ARG-class\tbest-hit\tprobability\tidentity\talignment-length\talignment-bitscore\talignment-evalue\tcounts\n')
    fo2.write('#ARG\tquery-start\tquery-end\tread_id\tpredicted_ARG-class\tbest-hit\tprobability\tidentity\talignment-length\talignment-bitscore\talignment-evalue\tcounts\n')
    for i in tqdm(predict):
        x_align = align[i[0]]
        x_align = {o:x_align[o] for o in x_align.keys() if '|' + i[1] + '|' in o}
        if x_align:
            x_bh = max(x_align.iteritems(), key=operator.itemgetter(1))[0]
            bs_bh = x_align[x_bh]
            if i[2] >= prob:
                fo.write(('\t').join([
                 x_bh.split('|')[(-1)].upper(),
                 BH[i[0]][2][8],
                 BH[i[0]][2][9],
                 i[0],
                 i[1],
                 x_bh,
                 str(i[2]),
                 BH[i[0]][2][2],
                 BH[i[0]][2][3],
                 BH[i[0]][2][(-1)],
                 BH[i[0]][2][(-2)],
                 '1']) + '\n')
            else:
                x_bh = BH[i[0]][0]
                bs_bh = BH[i[0]][1]
                fo2.write(('\t').join([
                 x_bh.split('|')[(-1)].upper(),
                 BH[i[0]][2][8],
                 BH[i[0]][2][9],
                 i[0],
                 i[1],
                 x_bh,
                 str(i[2]),
                 BH[i[0]][2][2],
                 BH[i[0]][2][3],
                 BH[i[0]][2][(-1)],
                 BH[i[0]][2][(-2)],
                 '1']) + '\n')
        else:
            x_bh = BH[i[0]][0]
            bs_bh = BH[i[0]][1]
            fo2.write(('\t').join([
             x_bh.split('|')[(-1)].upper(),
             BH[i[0]][2][8],
             BH[i[0]][2][9],
             i[0],
             i[1],
             'undefined',
             str(i[2]),
             BH[i[0]][2][2],
             BH[i[0]][2][3],
             BH[i[0]][2][(-1)],
             BH[i[0]][2][(-2)],
             '1']) + '\n')

    fo.close()
    fo2.close()