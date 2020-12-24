# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/avs_tools/EM.py
# Compiled at: 2019-09-19 11:28:06
# Size of source mod 2**32: 9416 bytes
from collections import Counter
import numpy as np, pandas as pd, click

class Txps:

    def __init__(self, num_txps):
        self.T = num_txps
        self.txp_name = []
        self.txp_len = []

    def insert(self, name, length):
        """
        insert element in txps object
        """
        if not len(self.txp_name) == len(self.txp_len):
            raise AssertionError('Wrong txp info insertion/deletion Done, Exiting')
        elif not len(self.txp_name) <= self.T:
            raise AssertionError('More Txps than expected(' + str(self.T) + '), Exiting')
        self.txp_name.append(name)
        self.txp_len.append(length)

    def get_name(self, ind):
        """
        return count of an eq class ind
        """
        return self.txp_name[ind]

    def get_len(self, ind):
        """
        return label of an eq class ind
        """
        return self.txp_len[ind]


class EqClass:

    def __init__(self, num_eq_classes):
        self.eq_labels = []
        self.eq_count = []
        self.comb_wt = [
         0] * num_eq_classes
        self.E = num_eq_classes

    def get_num_classes(self):
        """
        get count for the number of eq classes
        """
        return self.E

    def insert(self, label, count, auxs, alphas, txp_obj):
        """
        insert element in eqclass
        """
        if not len(self.eq_labels) == len(self.eq_count):
            raise AssertionError('Wrong EqClass insertion/deletion Done, Exiting')
        else:
            if not len(self.eq_labels) <= self.E:
                raise AssertionError('More Eq classes than expected(' + str(self.T) + '), Exiting')
            else:
                for x in label:
                    assert x < txp_obj.T, 'Txp label ' + str(x) + ' is wrong (more than max allowed) ' + str(txp_obj.T - 1) + ', Exiting'

                if isinstance(label, tuple):
                    self.eq_labels.append(label)
                else:
                    self.eq_labels.append(tuple(label))
            self.eq_count.append(count)
            if len(label) == 1:
                alphas[label[0]] += count

    def get_count(self, ind):
        """
        return count of an eq class ind
        """
        return self.eq_count[ind]

    def get_label(self, ind):
        """
        return label of an eq class ind
        """
        return self.eq_labels[ind]

    def get_comb_wt(self, ind):
        """
        return label of an eq class ind
        """
        return self.comb_wt[ind]


class Rld:

    def __init__(self, length_vector):
        self.R = len(length_vector)
        self.dist = Counter(length_vector)


def read_data(eq_file, rld_file):
    with open(eq_file) as (f):
        T = int(f.readline())
        E = int(f.readline())
        txp_obj = Txps(T)
        eq_obj = EqClass(E)
        alphas = [
         0.0] * T
        for _ in range(T):
            toks = f.readline().strip().split()
            txp_obj.insert(toks[0], int(toks[1]))

        for line in f:
            toks = line.strip().split()
            toks = map(int, toks)
            t = toks[0]
            eq_obj.insert(toks[1:t + 1], int(toks[(t + 1)]), toks[t + 1:], alphas, txp_obj)

    with open(rld_file) as (f):
        rld = f.readline().strip().split('\t')
        rld_obj = Rld(rld)
    return (txp_obj, eq_obj, rld_obj, alphas)


def populate_alphas(alphas_in, to, lengthcorrection):
    alphas_in = np.array(alphas_in) + 0.5
    alphas_out = np.array([1.0] * to.T)
    for ind in range(to.T):
        if lengthcorrection:
            eff_len = 0.001 * to.get_len(ind)
        else:
            eff_len = 100
        alphas_in[ind] *= eff_len

    return alphas_out


def update_comb_wts(eo, to, ro, lengthcorrection):
    for ind in range(eo.E):
        count = eo.get_count(ind)
        labels = eo.get_label(ind)
        norm = 0.0
        classLength = len(labels)
        comb_wts = np.array([])
        for lbl in labels:
            if lengthcorrection:
                txp_len = float(to.get_len(lbl))
                comb_wt = count / txp_len
            else:
                comb_wt = count / classLength
            norm += comb_wt
            comb_wts = np.concatenate([comb_wts, [comb_wt]])

        comb_wts /= norm
        eo.comb_wt[ind] = tuple(comb_wts)


def EMUpdate(to, eo, alphas_in, alphas_out):
    assert len(alphas_in) == len(alphas_out), 'size of alphas in and out does not match'
    for ind in range(eo.E):
        count = eo.get_count(ind)
        labels = eo.get_label(ind)
        auxs = eo.get_comb_wt(ind)
        gsize = len(labels)
        if gsize > 1:
            denom = 0.0
            for i in range(gsize):
                tid = labels[i]
                aux = auxs[i]
                val = alphas_in[tid] * aux
                denom += val

            if denom > 0:
                invDenom = count / denom
                for i in range(gsize):
                    tid = labels[i]
                    aux = auxs[i]
                    val = alphas_in[tid] * aux
                    if not np.isnan(val):
                        alphas_out[tid] += val * invDenom

        else:
            alphas_out[labels[0]] += count


def run_EM(to, eo, alphas_in, alphas_out):
    minAlpha = 1e-08
    alphaCheckCutoff = 0.01
    maxIter = 10000
    relDiffTolerance = 0.01
    minIter = 50
    itNum = 0
    converged = False
    while itNum < minIter or itNum < maxIter and not converged:
        EMUpdate(to, eo, alphas_in, alphas_out)
        converged = True
        maxRelDiff = -float('inf')
        for ind in range(to.T):
            if alphas_out[ind] > alphaCheckCutoff:
                relDiff = abs(alphas_in[ind] - alphas_out[ind]) / alphas_out[ind]
                if relDiff > maxRelDiff:
                    maxRelDiff = relDiff
                if relDiff > relDiffTolerance:
                    converged = False
            alphas_in[ind] = alphas_out[ind]
            alphas_out[ind] = 0.0

        if itNum % 100 == 0:
            print('iteration = ' + str(itNum) + ' | max rel diff. = ' + str(maxRelDiff))
        itNum += 1

    print('iteration = ' + str(itNum) + ' | max rel diff. = ' + str(maxRelDiff))
    alpha_sum = 0.0
    for ind in range(to.T):
        alpha = alphas_in[ind]
        if alpha < minAlpha:
            alphas_in[ind] = 0.0
        else:
            alpha_sum += alpha

    assert alpha_sum > 0, 'Something wrong with salmon run, Exiting'


@click.command()
@click.option('--eq', help='path+name to input salmon format eqclass file')
@click.option('--out', help='path+name to output abundance file')
@click.option('--lengthcorrection', is_flag=True, default=False)
@click.option('--rld', help='path to file with fragment lengths')
def main(eq, out, lengthcorrection, rld):
    to, eo, ro, alphas_in = read_data(eq, rld)
    alphas_out = populate_alphas(alphas_in, to, lengthcorrection)
    update_comb_wts(eo, to, ro, lengthcorrection)
    run_EM(to, eo, alphas_in, alphas_out)
    with open(out, 'w') as (f):
        f.write('Txp_Name\tCounts\n')
        for ind in range(to.T):
            f.write(to.get_name(ind) + '\t' + str(alphas_in[ind]) + '\n')


if __name__ == '__main__':
    main()