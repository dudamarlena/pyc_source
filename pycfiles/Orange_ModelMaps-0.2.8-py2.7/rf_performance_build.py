# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/examples/ensemble/rf_performance_build.py
# Compiled at: 2014-01-28 12:21:25
__author__ = '"Miha Stajdohar" <miha.stajdohar@gmail.com>'
import matplotlib
matplotlib.use('Agg')
import os.path, sys, numpy as np, orangecontrib.modelmaps as mm
from Orange import data, utils
ROOT = '/home/miha/work/res/modelmaps'
ROOT = 'C:\\Users\\Miha\\work\\res\\modelmaps'

def build_rd_map(DATASET):
    fname = os.path.join(utils.environ.dataset_install_dir, '%s%s' % (DATASET, '.tab'))
    if not (os.path.exists(fname) and os.path.isfile(fname)):
        fname = os.path.join(ROOT, 'tab', '%s%s' % (DATASET, '.tab'))
        if not (os.path.exists(fname) and os.path.isfile(fname)):
            raise IOError('File %s not found.' % fname)
    build_map = mm.BuildModelMap(fname)
    trees = 150
    print 'build models...'
    models, models_1, rf_classifier, _ = build_map.build_rf_models(trees=trees, max_depth=None, three_folds=False)
    print 'build model data...'
    table = build_map.build_model_data(models)
    table_1 = build_map.build_model_data(models_1)
    print 'build matrix...'
    smx = build_map.build_model_matrix(models)
    smx_1 = build_map.build_model_matrix(models_1)
    mm.save(os.path.join(ROOT, '_ensemble_', 'rf_%s_%d_tree_base_%s' % (DATASET, len(models), sys.platform)), smx, table, build_map.data())
    mm.save(os.path.join(ROOT, '_ensemble_', 'rf_%s_%d_tree_base_%s' % (DATASET, len(models_1), sys.platform)), smx_1, table_1, build_map.data())
    return


DO = [
 'iris', 'breast-cancer-wisconsin', 'voting', 'zoo', 'mushroom', 'adult_sample', 'glass', 'marketing', 'primary-tumor', 'vehicle', 'wdbc', 'dermatology']
DO = ['marketing']
for d in DO:
    build_rd_map(d)