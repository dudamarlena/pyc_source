# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/baselines.py
# Compiled at: 2019-07-19 04:40:38
# Size of source mod 2**32: 8416 bytes
from __future__ import print_function, division, absolute_import
import matplotlib
matplotlib.use('Agg')
import os
os.environ['ODIN'] = 'gpu,float32,seed=5218'
import numpy as np
from odin import visual as V
from odin.ml import GMM, PLDA, PPCA, SupervisedPPCA
from odin.visual import print_dist, merge_text_graph, plot_confusion_matrix, plot_figure, plot_histogram_layers, plot_save, generate_random_colors
from odin.utils import unique_labels, ctext, auto_logging, batching, UnitTimer, ArgController, get_script_path, mpi
from odin.stats import train_valid_test_split
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.svm import SVC, SVR
from sklearn.manifold import Isomap, SpectralEmbedding, MDS
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.multioutput import MultiOutputRegressor
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.cluster import FeatureAgglomeration
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, explained_variance_score
from sisua.data import read_CITEseq_PBMC, EXP_DIR
from sisua.data.const import PBMC_markers_to_symbols, PBMC_colors
from sisua.analysis.latent_benchmarks import plot_latents
from sisua.utils import plot_figure, plot_evaluate_classifier, plot_evaluate_reconstruction, plot_evaluate_regressor
TRAIN_PERCENTAGE = 0.6
NUM_COMPONENTS = 64
DATA = 'data_norm'
PROTEIN_ORDER = list(PBMC_markers_to_symbols.keys())
mRNA_ORDER = list(PBMC_markers_to_symbols.values())
ds = read_CITEseq_PBMC(override=False)
data = ds[DATA]
gene_name = np.array(ds['cols'][:])
human_cols = [True if 'HUMAN_' in i else False for i in gene_name]
data = data[:, human_cols]
gene_name = np.array([i for i in gene_name if 'HUMAN_' in i])
y_names = ds['meta_cols'][2:12]
ids = {j.replace('mRNA.HUMAN_', ''):i for i, j in enumerate(y_names)}
y_mRNA_names = [y_names[ids[i]].replace('mRNA.HUMAN_', '') for i in mRNA_ORDER]
y_mRNA = ds['metadata'][:, 2:12][:, [ids[i] for i in mRNA_ORDER]]
y_prot_names = [i.replace('protein.count.', '') for i in ds['meta_cols'][12:22]]
y_prot = ds['metadata'][:, 12:22]
assert y_mRNA_names == mRNA_ORDER and y_prot_names == PROTEIN_ORDER
y_bin = ds['y_bin'] if 'y_bin' in ds else None
y_prob = ds['y_prob'] if 'y_prob' in ds else None
num_samples = data.shape[0]
ids = get_rng().permutation(num_samples)
train, valid, test = train_valid_test_split(ids, train=TRAIN_PERCENTAGE, inc_test=True, seed=(get_rng().randint(0, 1000000000.0)))
X_train, y_mRNA_train, y_prot_train, y_bin_train, y_prob_train = (data[train], y_mRNA[train], y_prot[train], y_bin[train], y_prob[train])
X_valid, y_mRNA_valid, y_prot_valid, y_bin_valid, y_prob_valid = (data[valid], y_mRNA[valid], y_prot[valid], y_bin[valid], y_prob[valid])
X_test, y_mRNA_test, y_prot_test, y_bin_test, y_prob_test = (data[test], y_mRNA[test], y_prot[test], y_bin[test], y_prob[test])
print(ctext('Train:', 'cyan'), X_train.shape, y_mRNA_train.shape, y_prot_train.shape, y_bin_train.shape, y_prob_train.shape)
print(ctext('Valid:', 'cyan'), X_valid.shape, y_mRNA_valid.shape, y_prot_valid.shape, y_bin_valid.shape, y_prob_valid.shape)
print(ctext('Test:', 'cyan'), X_test.shape, y_mRNA_test.shape, y_prot_test.shape, y_bin_test.shape, y_prob_test.shape)
random_state = get_rng().randint(0, 1000000000.0)
with UnitTimer(name='Fit PCA'):
    pca = PCA(n_components=NUM_COMPONENTS, random_state=random_state)
    pca.fit(X_train)
with UnitTimer(name='Fit PPCA'):
    ppca = PPCA(n_components=NUM_COMPONENTS, verbose=True, random_state=random_state)
    ppca.fit(X_train)
with UnitTimer(name='Fit S-PPCA'):
    sppca = SupervisedPPCA(n_components=NUM_COMPONENTS, verbose=True, extractor='supervised', random_state=random_state)
    X_, y_ = [], []
    for i, j in zip(X_train, y_bin_train):
        for _ in range(int(np.sum(j))):
            X_.append(i)

        for c in np.nonzero(j)[0]:
            y_.append(c)

    X_, y_ = np.array(X_), np.array(y_)
    ids = get_rng().permutation(X_.shape[0])
    sppca.fit(X_[ids], y_[ids])
for transformer_name, transformer in [
 (
  'PCA', pca),
 (
  'PPCA', ppca),
 (
  'SPPCA', sppca)]:
    print(ctext('Methods:', 'yellow'), ctext(transformer_name, 'cyan'))
    Z_train = transformer.transform(X_train)
    Z_valid = transformer.transform(X_valid)
    Z_test = transformer.transform(X_test)
    plot_latents_binary(X=Z_test, y=y_prot_test, labels=y_prot_names,
      title=('[%s]Test-Prot' % transformer_name),
      ax=224)
    for name, classifier in [
     (
      'SVCrbf', OneVsRestClassifier(SVC(kernel='rbf', random_state=random_state)))]:
        print('Testing Classifier:', ctext(name, 'cyan'))
        classifier.fit(X=np.concatenate([Z_train, Z_valid], axis=0), y=np.concatenate([y_bin_train, y_bin_valid], axis=0))
        y_bin_test_pred = classifier.predict(Z_test)
        plot_evaluate_classifier(y_pred=y_bin_test_pred, y_true=y_bin_test, labels=y_prot_names,
          title=('[%s]%s-%s' % (transformer_name, 'Classification', name)))

    for name, classifier in [
     (
      'Elastic', MultiOutputRegressor(ElasticNetCV(random_state=random_state)))]:
        print('Testing Regressor:', ctext(name, 'cyan'))
        classifier.fit(X=np.concatenate([Z_train, Z_valid], axis=0), y=np.concatenate([y_prot_train, y_prot_valid], axis=0))
        y_prot_test_pred = classifier.predict(Z_test)
        plot_evaluate_regressor(y_pred=y_prot_test_pred, y_true=y_prot_test, labels=y_prot_names,
          title=('[%s]%s-%s' % (transformer_name, 'Regression', name)))

    V.plot_save(os.path.join(EXP_DIR, 'baseline_%s.png' % transformer_name.lower()))