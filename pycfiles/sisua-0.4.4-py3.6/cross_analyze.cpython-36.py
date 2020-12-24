# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/cross_analyze.py
# Compiled at: 2019-06-26 10:10:57
# Size of source mod 2**32: 7668 bytes
from __future__ import print_function, division, absolute_import
import os, time, pickle
from six import string_types
from multiprocessing import Process
from itertools import product
import seaborn as sns
from matplotlib import pyplot as plt
from odin.utils import as_tuple, ctext, catch_warnings_ignore, ArgController
import numpy as np

def get_arguments():
    args = ArgController().add('-ds', "name of multiple datasets for cross-data analysis: 'cross8k_ly,crossecc_ly'", 'cross8k_ly,crossecc_ly').add('-model', "name of model for testing, for example: 'vae', 'movae', 'vae,movae'", 'movae').add('-path', 'Saving all figures to given output folder', '/tmp/cross_analysis').add('--verbose', 'Enable verbose logging', False).add('-nprocess', 'Number of multiple processes for running the experiments', 2).parse()
    datasets = [i.strip().lower() for i in str(args.ds).split(',') if len(i.strip()) > 0]
    model = [i.strip().lower() for i in str(args.model).split(',') if len(i.strip()) > 0]
    nprocess = int(args.nprocess)
    return dict(datasets=datasets, models=model, outpath=(args.path),
      verbose=(bool(args.verbose)),
      nprocess=nprocess)


all_datasets = None

def _analyze(ds_name, model_path, outpath, y_true, all_proteins, verbose):
    global all_datasets
    from sisua.analysis import Posterior
    with open(model_path, 'rb') as (f):
        infer = pickle.load(f)
    ds_infer = infer.configs['dataset']
    ds = [j for i, j in all_datasets if i == ds_name][0]
    path = os.path.join(outpath, 'data%s_model%s' % (
     ds_name.replace('_', '').upper(),
     ds_infer.replace('_', '').upper()))
    path = os.path.join(path, infer.short_id)
    if not os.path.exists(path):
        os.mkdir(path)
    if verbose:
        print('\nData:%s - Model:%s' % (
         ctext(ds_name, 'yellow'),
         ctext(ds_infer, 'yellow')))
        print(' Outpath:', ctext(path, 'cyan'))
    pos = Posterior(infer, ds=ds)
    with catch_warnings_ignore(RuntimeWarning):
        pos.new_figure().plot_latents_binary_scatter(size=4).plot_latents_distance_heatmap().plot_correlation_marker_pairs()
        if infer.is_semi_supervised:
            y_pred = {i:j for i, j in zip(dict(all_datasets)[ds_infer]['y_col'], infer.predict_y(ds['X']).T) if i in all_proteins}
            y_pred = np.hstack([y_pred[i][:, np.newaxis] for i in all_proteins])
            pos.plot_protein_predicted_series(y_true_new=y_true,
              y_pred_new=y_pred,
              labels_new=all_proteins)
            for prot_name in all_proteins:
                pos.plot_protein_scatter(protein_name=prot_name, y_true_new=y_true,
                  y_pred_new=y_pred,
                  labels_new=all_proteins)

        pos.save_plots(path, dpi=80)


def cross_analyze(datasets, outpath, models, nprocess=1, verbose=False):
    global all_datasets
    from sisua.data import get_dataset
    from sisua.data.path import EXP_DIR
    from sisua.data.utils import standardize_protein_name
    assert nprocess > 0, 'Number of processes must be greater than 0'
    datasets = as_tuple(datasets, t=string_types)
    if not len(datasets) > 1:
        raise AssertionError('Require more than one datasets for cross analysis')
    else:
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        models = as_tuple(models, t=string_types)
        assert len(models) > 0, 'At least one model must be given'
    all_datasets = {name:get_dataset(name)[0] for name in datasets}
    all_datasets = [(name,
     dict(X=(ds['X'][:]), X_col=(ds['X_col']), X_row=(ds['X_row']), y=(ds['y']), y_col=(np.array([standardize_protein_name(i) for i in ds['y_col']])))) for name, ds in all_datasets.items()]
    genes = all_datasets[0][1]['X_col']
    for name, ds in all_datasets:
        assert np.all(ds['X_col'] == genes), 'Set of training genes mis-match'

    all_proteins = set(all_datasets[0][1]['y_col'])
    for name, ds in all_datasets:
        all_proteins &= set(ds['y_col'])

    all_proteins = sorted(all_proteins)
    if verbose:
        print('Datasets       :', ctext(', '.join(datasets), 'yellow'))
        print('Model          :', ctext(', '.join(models), 'yellow'))
        print('Shared proteins:', ctext(', '.join(all_proteins), 'yellow'))
        for name, ds in all_datasets:
            print(' ', ctext(name, 'cyan'))
            print('   X    :', ds['X'].shape)
            print('   X_col:', ds['X_col'])
            print('   y    :', ds['y'].shape)
            print('   y_col:', ', '.join(ds['y_col']))

    all_models = []
    for ds_name in datasets:
        if verbose:
            print("Search model for dataset '%s' ..." % ctext(ds_name, 'yellow'))
        exp_path = os.path.join(EXP_DIR, ds_name)
        for model_name in os.listdir(exp_path):
            if model_name.split('_')[0] in models:
                path = os.path.join(exp_path, model_name, 'model.pkl')
                if os.path.exists(path):
                    all_models.append(path)
                    if verbose:
                        print(' ', ctext(model_name, 'cyan'))

    if verbose:
        print('%s datasets and %s models => %s experiments' % (
         ctext(len(all_datasets), 'yellow'),
         ctext(len(all_models), 'yellow'),
         ctext(len(all_datasets) * len(all_models), 'yellow')))
    all_data_name = [i[0] for i in all_datasets]
    all_model_name = [i.split('/')[(-3)] for i in all_models]
    for name1, name2 in product(all_data_name, all_model_name):
        path = os.path.join(outpath, 'data%s_model%s' % (
         name1.replace('_', '').upper(),
         name2.replace('_', '').upper()))
        if not os.path.exists(path):
            os.mkdir(path)
            if verbose:
                print('Create output folder:', ctext(path, 'yellow'))

    processes = []
    for ds_name, ds in all_datasets:
        y_true = {i:j for i, j in zip(ds['y_col'], ds['y'].T) if i in all_proteins}
        y_true = np.hstack([y_true[i][:, np.newaxis] for i in all_proteins])
        for model_path in all_models:
            processes.append(Process(target=_analyze,
              args=(
             ds_name, model_path, outpath, y_true, all_proteins, verbose)))
            if len(processes) >= nprocess:
                [p.start() for p in processes]
                [p.join() for p in processes]
                processes = []

    if len(processes) > 0:
        [p.start() for p in processes]
        [p.join() for p in processes]


if __name__ == '__main__':
    cross_analyze(**get_arguments())