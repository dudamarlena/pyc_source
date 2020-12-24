# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/examples/ensemble/rf_performance_plot_2.py
# Compiled at: 2014-01-26 00:07:45
import matplotlib
matplotlib.use('Agg')
import os.path, re, cPickle as pickle, matplotlib.pyplot as plt, scipy.stats, numpy as np
from itertools import groupby
from operator import itemgetter
ROOT = '/Users/miha/work/res/modelmaps'
scores = {}

def plot_scores(scoring_method):
    print 'drawing plots...'
    fig = plt.figure(figsize=(6, 8), dpi=300)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, top=0.976, bottom=0.017, left=0.074, right=0.983)

    def add_scores_plot(i, DATASET):
        ax = fig.add_subplot(4, 3, i)
        scores[DATASET][scoring_method].sort()
        x, y, std, med = ([], [], [], [])
        for k, g in groupby(scores[DATASET][scoring_method], key=itemgetter(0)):
            i, s = zip(*list(g))
            x.append(i[0])
            y.append(np.mean(s))
            std.append(np.std(s))
            med.append(np.median(s))

        last_x = x[(-1)]
        last_y = y[(-1)]
        y = np.array(y)
        std = np.array(std)
        ax.plot(x, y, '-', color='k', linewidth=0.5)
        miny, maxy = min(y), max(y)
        scores[DATASET][(scoring_method + '_mm')].sort()
        x, y, std, med = ([], [], [], [])
        for k, g in groupby(scores[DATASET][(scoring_method + '_mm')], key=itemgetter(0)):
            i, s = zip(*list(g))
            x.append(i[0])
            y.append(sum(s) / len(s))
            std.append(np.std(s))
            med.append(np.median(s))

        y.append(last_y)
        x.append(last_x)
        y = np.array(y)
        std = np.array(std)
        ax.plot(x, y, '-', color='g', linewidth=0.5)
        miny = min(y) if min(y) < miny else miny
        maxy = max(y) if max(y) > maxy else maxy
        ax.set_yticks([round(miny - 0.005, 2), round(maxy + 0.005, 2)])
        ax.set_ybound(round(miny - 0.005, 2), round(maxy + 0.005, 2))
        for label in ax.get_xticklabels():
            label.set_fontsize('xx-small')

        for label in ax.get_yticklabels():
            label.set_fontsize('xx-small')

        ax.set_xlabel('trees', size='small')
        ax.set_ylabel(scoring_method.upper(), size='small')
        subtitle = (' ').join([ s[0].upper() + s[1:].lower() for s in re.split('_|-', DATASET) if s != 'sample' ])
        ax.set_title('%s' % subtitle, weight='bold', size='small')

    counter = 1
    for DATASET in sorted(scores.keys()):
        if DATASET == 'marketing':
            continue
        add_scores_plot(counter, DATASET)
        counter += 1

    ax = fig.add_subplot(4, 3, counter)
    ax.plot([0], [0], 'k-', [0], [0], 'g-')
    ax.set_axis_off()
    plt.legend(['Random Forest', 'Model-map-based forest'], frameon=False)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize='xx-small')
    fig.savefig(os.path.join(ROOT, '_ensemble_', 'res_%s_%s.pdf' % (EXPMARKER, scoring_method)))


def plot_one(DATASET, scoring_method, plot_model_map=True):
    print 'drawing plots...'
    fig = plt.figure(figsize=(3, 2), dpi=300)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, top=0.9, bottom=0.15, left=0.15, right=0.96)
    ax = fig.add_subplot(111)
    scores[DATASET][scoring_method].sort()
    x, y, std, med = ([], [], [], [])
    for k, g in groupby(scores[DATASET][scoring_method], key=itemgetter(0)):
        i, s = zip(*list(g))
        x.append(i[0])
        y.append(np.mean(s))
        std.append(np.std(s))
        med.append(np.median(s))

    y = np.array(y)
    std = np.array(std)
    ax.plot(x, y, '-', color='k', linewidth=0.5, label='Random Forest')
    if plot_model_map:
        pass
    miny, maxy = min(y), max(y)
    if plot_model_map:
        scores[DATASET][(scoring_method + '_mm')].sort()
        x, y, std, med = ([], [], [], [])
        for k, g in groupby(scores[DATASET][(scoring_method + '_mm')], key=itemgetter(0)):
            i, s = zip(*list(g))
            x.append(i[0])
            y.append(sum(s) / len(s))
            std.append(np.std(s))
            med.append(np.median(s))

        y = np.array(y)
        std = np.array(std)
        ax.plot(x, y, '-', color='g', linewidth=0.5, label='Model-map-based forest')
        miny = min(y) if min(y) < miny else miny
        maxy = max(y) if max(y) > maxy else maxy
    ax.set_yticks([round(miny - 0.005, 2), round(maxy + 0.005, 2) - 0.15])
    ax.set_ybound(round(miny - 0.005, 2), round(maxy + 0.005, 2) - 0.15)
    for label in ax.get_xticklabels():
        label.set_fontsize('xx-small')

    for label in ax.get_yticklabels():
        label.set_fontsize('xx-small')

    if plot_model_map:
        leg = plt.legend(frameon=False)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize='x-small')
    ax.set_xlabel('trees', size='small')
    ax.set_ylabel(scoring_method.upper(), size='small')
    subtitle = (' ').join([ s[0].upper() + s[1:].lower() for s in re.split('_|-', DATASET) if s != 'sample' ])
    ax.set_title('%s' % subtitle, weight='bold', size='small')
    fig.savefig(os.path.join(ROOT, '_ensemble_', 'res_%s_%s_%s.pdf' % (EXPMARKER, DATASET, scoring_method)))


EXPMARKER = '120_120_3fold_tree_base'
DO = ['breast-cancer-wisconsin', 'voting', 'zoo', 'mushroom', 'adult_sample', 'glass', 'primary-tumor', 'vehicle', 'wdbc', 'dermatology', 'iris', 'marketing']
for DATASET in DO:
    fname = os.path.join(ROOT, '_ensemble_', 'scores_%s_%s.pkl' % (EXPMARKER, DATASET))
    print fname
    if os.path.exists(fname) and os.path.isfile(fname):
        scores.update(pickle.load(open(fname, 'rb')))

plot_scores('brier')
plot_one('marketing', 'brier', plot_model_map=True)

def best_scores(scores):
    x = []
    scores.sort()
    for k, g in groupby(scores, key=itemgetter(0)):
        i, s = zip(*list(g))
        x.append((i[0], np.mean(s)))

    best = min(x, key=itemgetter(1))[0]
    print 'best', best
    return [ s for t, s in scores if t == best ]


def average_scores(scores):
    x = []
    scores.sort()
    for k, g in groupby(scores, key=itemgetter(0)):
        i, s = zip(*list(g))
        x.append(np.mean(s))

    return np.array(x)


x = average_scores(scores['marketing']['brier'])
y = average_scores(scores['marketing']['brier_mm'])
trim = min(len(x), len(y))
print np.sum(x[:trim] - y[:trim])
ranks = scipy.stats.mstats.rankdata(np.array([x[:trim], y[:trim]]), axis=0)
print ('\n').join('%s: %.3f' % (name, r) for r, name in zip(np.mean(ranks, axis=1), ['RF', 'MM forest']))
print scipy.stats.wilcoxon(x[:trim], y[:trim])
x = best_scores(scores['marketing']['brier'])
y = best_scores(scores['marketing']['brier_mm'])
print 'Marketing'
print 'best RF:', max(x)
print 'best MM:', max(y)
print "Student's t-test:", scipy.stats.ttest_ind(x, y)
for scoring_method in ['ca', 'auc', 'brier']:
    print scoring_method.upper()
    x, y = [], []
    for DATASET in scores:
        trim = min(len(list(average_scores(scores[DATASET][scoring_method]))), len(list(average_scores(scores[DATASET][(scoring_method + '_mm')]))))
        x.extend(list(average_scores(scores[DATASET][scoring_method]))[:trim])
        y.extend(list(average_scores(scores[DATASET][(scoring_method + '_mm')]))[:trim])

    print 'Ranks'
    ranks = scipy.stats.mstats.rankdata(np.array([x, y]), axis=0)
    print ('\n').join('%s: %.3f' % (name, r) for r, name in zip(np.mean(ranks, axis=1), ['RF', 'MM forest']))
    print scipy.stats.wilcoxon(x, y)