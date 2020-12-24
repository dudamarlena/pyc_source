#! /usr/bin/env python
#===============================================================================
# Copyright 2014-2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================


# System imports
import os
import subprocess
import sys
from distutils.core import *
from distutils      import sysconfig
from setuptools     import setup, Extension
from os.path import join as jp
from distutils.sysconfig import get_config_vars

import numpy as np

npyver = int(np.__version__.split('.')[1])

if npyver == 9:
    print("Warning:  Detected numpy version {}".format(np.__version__))
    print("Numpy 1.10 or greater is strongly recommended.")
    print("Earlier versions have not been tested. Use at your own risk.")

if npyver < 9:
    sys.exit("Error: Detected numpy {}. The minimum requirement is 1.9, and >= 1.10 is strongly recommended".format(np.__version__))


daal_root=os.environ['DAALROOT']
IS_WIN = False
IS_MAC = False
IS_LIN = False

if 'linux' in sys.platform:
    IS_LIN = True
    lib_dir = '/lib/intel64_lin'
elif sys.platform == 'darwin':
    IS_MAC = True
    lib_dir = '/lib'
elif sys.platform in ['win32', 'cygwin']:
    IS_WIN = True
    lib_dir = '/lib/intel64_win'
else:
    assert False, sys.platform + ' not supported'

DAAL_DEFAULT_TYPE = 'double'

all_modules = {
        'daal.data_management': '_data_management_',
        'daal.data_management.db': '_db_',
        'daal.data_management.features': '_features_',
        'daal.data_management.modifiers': '_modifiers_',
        'daal.data_management.modifiers.csv': '_csv_',
        'daal.algorithms': '_algorithms_',
        'daal.algorithms.adaboost': '_adaboost_',
        'daal.algorithms.adaboost.prediction': '_prediction_',
        'daal.algorithms.adaboost.quality_metric_set': '_quality_metric_set_',
        'daal.algorithms.adaboost.training': '_training_',
        'daal.algorithms.association_rules': '_association_rules_',
        'daal.algorithms.bacon_outlier_detection': '_bacon_outlier_detection_',
        'daal.algorithms.boosting': '_boosting_',
        'daal.algorithms.boosting.prediction': '_prediction1_',
        'daal.algorithms.boosting.training': '_training1_',
        'daal.algorithms.brownboost': '_brownboost_',
        'daal.algorithms.brownboost.prediction': '_prediction2_',
        'daal.algorithms.brownboost.quality_metric_set': '_quality_metric_set1_',
        'daal.algorithms.brownboost.training': '_training2_',
        'daal.algorithms.cholesky': '_cholesky_',
        'daal.algorithms.classifier': '_classifier_',
        'daal.algorithms.classifier.prediction': '_prediction3_',
        'daal.algorithms.classifier.quality_metric.binary_confusion_matrix': '_binary_confusion_matrix_',
        'daal.algorithms.classifier.quality_metric.multiclass_confusion_matrix': '_multiclass_confusion_matrix_',
        'daal.algorithms.classifier.training': '_training3_',
        'daal.algorithms.correlation_distance': '_correlation_distance_',
        'daal.algorithms.cosine_distance': '_cosine_distance_',
        'daal.algorithms.covariance': '_covariance_',
        'daal.algorithms.decision_forest': '_decision_forest_',
        'daal.algorithms.decision_forest.classification': '_classification_',
        'daal.algorithms.decision_forest.classification.prediction': '_prediction4_',
        'daal.algorithms.decision_forest.classification.training': '_training4_',
        'daal.algorithms.decision_forest.regression': '_regression_',
        'daal.algorithms.decision_forest.regression.prediction': '_prediction5_',
        'daal.algorithms.decision_forest.regression.training': '_training5_',
        'daal.algorithms.decision_forest.training': '_training6_',
        'daal.algorithms.decision_tree': '_decision_tree_',
        'daal.algorithms.decision_tree.classification': '_classification1_',
        'daal.algorithms.decision_tree.classification.prediction': '_prediction6_',
        'daal.algorithms.decision_tree.classification.training': '_training7_',
        'daal.algorithms.decision_tree.regression': '_regression1_',
        'daal.algorithms.decision_tree.regression.prediction': '_prediction7_',
        'daal.algorithms.decision_tree.regression.training': '_training8_',
        'daal.algorithms.distributions': '_distributions_',
        'daal.algorithms.distributions.bernoulli': '_bernoulli_',
        'daal.algorithms.distributions.normal': '_normal_',
        'daal.algorithms.distributions.uniform': '_uniform_',
        'daal.algorithms.em_gmm': '_em_gmm_',
        'daal.algorithms.em_gmm.init': '_init_',
        'daal.algorithms.engines': '_engines_',
        'daal.algorithms.engines.mcg59': '_mcg59_',
        'daal.algorithms.engines.mt19937': '_mt19937_',
        'daal.algorithms.engines.mt2203': '_mt2203_',
        'daal.algorithms.gbt': '_gbt_',
        'daal.algorithms.gbt.classification': '_classification2_',
        'daal.algorithms.gbt.classification.prediction': '_prediction8_',
        'daal.algorithms.gbt.classification.training': '_training9_',
        'daal.algorithms.gbt.regression': '_regression2_',
        'daal.algorithms.gbt.regression.prediction': '_prediction9_',
        'daal.algorithms.gbt.regression.training': '_training10_',
        'daal.algorithms.gbt.training': '_training11_',
        'daal.algorithms.implicit_als': '_implicit_als_',
        'daal.algorithms.implicit_als.prediction.ratings': '_ratings_',
        'daal.algorithms.implicit_als.training': '_training12_',
        'daal.algorithms.implicit_als.training.init': '_init1_',
        'daal.algorithms.kdtree_knn_classification': '_kdtree_knn_classification_',
        'daal.algorithms.kdtree_knn_classification.prediction': '_prediction10_',
        'daal.algorithms.kdtree_knn_classification.training': '_training13_',
        'daal.algorithms.kernel_function': '_kernel_function_',
        'daal.algorithms.kernel_function.linear': '_linear_',
        'daal.algorithms.kernel_function.rbf': '_rbf_',
        'daal.algorithms.kmeans': '_kmeans_',
        'daal.algorithms.kmeans.init': '_init2_',
        'daal.algorithms.linear_model': '_linear_model_',
        'daal.algorithms.linear_model.prediction': '_prediction11_',
        'daal.algorithms.linear_model.training': '_training14_',
        'daal.algorithms.linear_regression': '_linear_regression_',
        'daal.algorithms.linear_regression.prediction': '_prediction12_',
        'daal.algorithms.linear_regression.quality_metric.group_of_betas': '_group_of_betas_',
        'daal.algorithms.linear_regression.quality_metric.single_beta': '_single_beta_',
        'daal.algorithms.linear_regression.quality_metric_set': '_quality_metric_set2_',
        'daal.algorithms.linear_regression.training': '_training15_',
        'daal.algorithms.logistic_regression': '_logistic_regression_',
        'daal.algorithms.logistic_regression.prediction': '_prediction13_',
        'daal.algorithms.logistic_regression.training': '_training16_',
        'daal.algorithms.logitboost': '_logitboost_',
        'daal.algorithms.logitboost.prediction': '_prediction14_',
        'daal.algorithms.logitboost.quality_metric_set': '_quality_metric_set3_',
        'daal.algorithms.logitboost.training': '_training17_',
        'daal.algorithms.low_order_moments': '_low_order_moments_',
        'daal.algorithms.math.abs': '_abs_',
        'daal.algorithms.math.logistic': '_logistic_',
        'daal.algorithms.math.relu': '_relu_',
        'daal.algorithms.math.smoothrelu': '_smoothrelu_',
        'daal.algorithms.math.softmax': '_softmax_',
        'daal.algorithms.math.tanh': '_tanh_',
        'daal.algorithms.multi_class_classifier': '_multi_class_classifier_',
        'daal.algorithms.multi_class_classifier.prediction': '_prediction15_',
        'daal.algorithms.multi_class_classifier.quality_metric_set': '_quality_metric_set4_',
        'daal.algorithms.multi_class_classifier.training': '_training18_',
        'daal.algorithms.multinomial_naive_bayes': '_multinomial_naive_bayes_',
        'daal.algorithms.multinomial_naive_bayes.prediction': '_prediction16_',
        'daal.algorithms.multinomial_naive_bayes.quality_metric_set': '_quality_metric_set5_',
        'daal.algorithms.multinomial_naive_bayes.training': '_training19_',
        'daal.algorithms.multivariate_outlier_detection': '_multivariate_outlier_detection_',
        'daal.algorithms.neural_networks': '_neural_networks_',
        'daal.algorithms.neural_networks.initializers': '_initializers_',
        'daal.algorithms.neural_networks.initializers.gaussian': '_gaussian_',
        'daal.algorithms.neural_networks.initializers.truncated_gaussian': '_truncated_gaussian_',
        'daal.algorithms.neural_networks.initializers.uniform': '_uniform1_',
        'daal.algorithms.neural_networks.initializers.xavier': '_xavier_',
        'daal.algorithms.neural_networks.layers': '_layers_',
        'daal.algorithms.neural_networks.layers.abs': '_abs1_',
        'daal.algorithms.neural_networks.layers.abs.backward': '_backward_',
        'daal.algorithms.neural_networks.layers.abs.forward': '_forward_',
        'daal.algorithms.neural_networks.layers.average_pooling1d': '_average_pooling1d_',
        'daal.algorithms.neural_networks.layers.average_pooling1d.backward': '_backward1_',
        'daal.algorithms.neural_networks.layers.average_pooling1d.forward': '_forward1_',
        'daal.algorithms.neural_networks.layers.average_pooling2d': '_average_pooling2d_',
        'daal.algorithms.neural_networks.layers.average_pooling2d.backward': '_backward2_',
        'daal.algorithms.neural_networks.layers.average_pooling2d.forward': '_forward2_',
        'daal.algorithms.neural_networks.layers.average_pooling3d': '_average_pooling3d_',
        'daal.algorithms.neural_networks.layers.average_pooling3d.backward': '_backward3_',
        'daal.algorithms.neural_networks.layers.average_pooling3d.forward': '_forward3_',
        'daal.algorithms.neural_networks.layers.backward': '_backward4_',
        'daal.algorithms.neural_networks.layers.batch_normalization': '_batch_normalization_',
        'daal.algorithms.neural_networks.layers.batch_normalization.backward': '_backward5_',
        'daal.algorithms.neural_networks.layers.batch_normalization.forward': '_forward4_',
        'daal.algorithms.neural_networks.layers.concat': '_concat_',
        'daal.algorithms.neural_networks.layers.concat.backward': '_backward6_',
        'daal.algorithms.neural_networks.layers.concat.forward': '_forward5_',
        'daal.algorithms.neural_networks.layers.convolution2d': '_convolution2d_',
        'daal.algorithms.neural_networks.layers.convolution2d.backward': '_backward7_',
        'daal.algorithms.neural_networks.layers.convolution2d.forward': '_forward6_',
        'daal.algorithms.neural_networks.layers.dropout': '_dropout_',
        'daal.algorithms.neural_networks.layers.dropout.backward': '_backward8_',
        'daal.algorithms.neural_networks.layers.dropout.forward': '_forward7_',
        'daal.algorithms.neural_networks.layers.eltwise_sum': '_eltwise_sum_',
        'daal.algorithms.neural_networks.layers.eltwise_sum.backward': '_backward9_',
        'daal.algorithms.neural_networks.layers.eltwise_sum.forward': '_forward8_',
        'daal.algorithms.neural_networks.layers.elu': '_elu_',
        'daal.algorithms.neural_networks.layers.elu.backward': '_backward10_',
        'daal.algorithms.neural_networks.layers.elu.forward': '_forward9_',
        'daal.algorithms.neural_networks.layers.forward': '_forward10_',
        'daal.algorithms.neural_networks.layers.fullyconnected': '_fullyconnected_',
        'daal.algorithms.neural_networks.layers.fullyconnected.backward': '_backward11_',
        'daal.algorithms.neural_networks.layers.fullyconnected.forward': '_forward11_',
        'daal.algorithms.neural_networks.layers.lcn': '_lcn_',
        'daal.algorithms.neural_networks.layers.lcn.backward': '_backward12_',
        'daal.algorithms.neural_networks.layers.lcn.forward': '_forward12_',
        'daal.algorithms.neural_networks.layers.locallyconnected2d': '_locallyconnected2d_',
        'daal.algorithms.neural_networks.layers.locallyconnected2d.backward': '_backward13_',
        'daal.algorithms.neural_networks.layers.locallyconnected2d.forward': '_forward13_',
        'daal.algorithms.neural_networks.layers.logistic': '_logistic1_',
        'daal.algorithms.neural_networks.layers.logistic.backward': '_backward14_',
        'daal.algorithms.neural_networks.layers.logistic.forward': '_forward14_',
        'daal.algorithms.neural_networks.layers.loss': '_loss_',
        'daal.algorithms.neural_networks.layers.loss.backward': '_backward15_',
        'daal.algorithms.neural_networks.layers.loss.forward': '_forward15_',
        'daal.algorithms.neural_networks.layers.loss.logistic_cross': '_logistic_cross_',
        'daal.algorithms.neural_networks.layers.loss.logistic_cross.backward': '_backward16_',
        'daal.algorithms.neural_networks.layers.loss.logistic_cross.forward': '_forward16_',
        'daal.algorithms.neural_networks.layers.loss.softmax_cross': '_softmax_cross_',
        'daal.algorithms.neural_networks.layers.loss.softmax_cross.backward': '_backward17_',
        'daal.algorithms.neural_networks.layers.loss.softmax_cross.forward': '_forward17_',
        'daal.algorithms.neural_networks.layers.lrn': '_lrn_',
        'daal.algorithms.neural_networks.layers.lrn.backward': '_backward18_',
        'daal.algorithms.neural_networks.layers.lrn.forward': '_forward18_',
        'daal.algorithms.neural_networks.layers.maximum_pooling1d': '_maximum_pooling1d_',
        'daal.algorithms.neural_networks.layers.maximum_pooling1d.backward': '_backward19_',
        'daal.algorithms.neural_networks.layers.maximum_pooling1d.forward': '_forward19_',
        'daal.algorithms.neural_networks.layers.maximum_pooling2d': '_maximum_pooling2d_',
        'daal.algorithms.neural_networks.layers.maximum_pooling2d.backward': '_backward20_',
        'daal.algorithms.neural_networks.layers.maximum_pooling2d.forward': '_forward20_',
        'daal.algorithms.neural_networks.layers.maximum_pooling3d': '_maximum_pooling3d_',
        'daal.algorithms.neural_networks.layers.maximum_pooling3d.backward': '_backward21_',
        'daal.algorithms.neural_networks.layers.maximum_pooling3d.forward': '_forward21_',
        'daal.algorithms.neural_networks.layers.pooling1d': '_pooling1d_',
        'daal.algorithms.neural_networks.layers.pooling1d.backward': '_backward22_',
        'daal.algorithms.neural_networks.layers.pooling1d.forward': '_forward22_',
        'daal.algorithms.neural_networks.layers.pooling2d': '_pooling2d_',
        'daal.algorithms.neural_networks.layers.pooling2d.backward': '_backward23_',
        'daal.algorithms.neural_networks.layers.pooling2d.forward': '_forward23_',
        'daal.algorithms.neural_networks.layers.pooling3d': '_pooling3d_',
        'daal.algorithms.neural_networks.layers.pooling3d.backward': '_backward24_',
        'daal.algorithms.neural_networks.layers.pooling3d.forward': '_forward24_',
        'daal.algorithms.neural_networks.layers.prelu': '_prelu_',
        'daal.algorithms.neural_networks.layers.prelu.backward': '_backward25_',
        'daal.algorithms.neural_networks.layers.prelu.forward': '_forward25_',
        'daal.algorithms.neural_networks.layers.relu': '_relu1_',
        'daal.algorithms.neural_networks.layers.relu.backward': '_backward26_',
        'daal.algorithms.neural_networks.layers.relu.forward': '_forward26_',
        'daal.algorithms.neural_networks.layers.reshape': '_reshape_',
        'daal.algorithms.neural_networks.layers.reshape.backward': '_backward27_',
        'daal.algorithms.neural_networks.layers.reshape.forward': '_forward27_',
        'daal.algorithms.neural_networks.layers.smoothrelu': '_smoothrelu1_',
        'daal.algorithms.neural_networks.layers.smoothrelu.backward': '_backward28_',
        'daal.algorithms.neural_networks.layers.smoothrelu.forward': '_forward28_',
        'daal.algorithms.neural_networks.layers.softmax': '_softmax1_',
        'daal.algorithms.neural_networks.layers.softmax.backward': '_backward29_',
        'daal.algorithms.neural_networks.layers.softmax.forward': '_forward29_',
        'daal.algorithms.neural_networks.layers.spatial_average_pooling2d': '_spatial_average_pooling2d_',
        'daal.algorithms.neural_networks.layers.spatial_average_pooling2d.backward': '_backward30_',
        'daal.algorithms.neural_networks.layers.spatial_average_pooling2d.forward': '_forward30_',
        'daal.algorithms.neural_networks.layers.spatial_maximum_pooling2d': '_spatial_maximum_pooling2d_',
        'daal.algorithms.neural_networks.layers.spatial_maximum_pooling2d.backward': '_backward31_',
        'daal.algorithms.neural_networks.layers.spatial_maximum_pooling2d.forward': '_forward31_',
        'daal.algorithms.neural_networks.layers.spatial_pooling2d': '_spatial_pooling2d_',
        'daal.algorithms.neural_networks.layers.spatial_pooling2d.backward': '_backward32_',
        'daal.algorithms.neural_networks.layers.spatial_pooling2d.forward': '_forward32_',
        'daal.algorithms.neural_networks.layers.spatial_stochastic_pooling2d': '_spatial_stochastic_pooling2d_',
        'daal.algorithms.neural_networks.layers.spatial_stochastic_pooling2d.backward': '_backward33_',
        'daal.algorithms.neural_networks.layers.spatial_stochastic_pooling2d.forward': '_forward33_',
        'daal.algorithms.neural_networks.layers.split': '_split_',
        'daal.algorithms.neural_networks.layers.split.backward': '_backward34_',
        'daal.algorithms.neural_networks.layers.split.forward': '_forward34_',
        'daal.algorithms.neural_networks.layers.stochastic_pooling2d': '_stochastic_pooling2d_',
        'daal.algorithms.neural_networks.layers.stochastic_pooling2d.backward': '_backward35_',
        'daal.algorithms.neural_networks.layers.stochastic_pooling2d.forward': '_forward35_',
        'daal.algorithms.neural_networks.layers.tanh': '_tanh1_',
        'daal.algorithms.neural_networks.layers.tanh.backward': '_backward36_',
        'daal.algorithms.neural_networks.layers.tanh.forward': '_forward36_',
        'daal.algorithms.neural_networks.layers.transposed_conv2d': '_transposed_conv2d_',
        'daal.algorithms.neural_networks.layers.transposed_conv2d.backward': '_backward37_',
        'daal.algorithms.neural_networks.layers.transposed_conv2d.forward': '_forward37_',
        'daal.algorithms.neural_networks.prediction': '_prediction17_',
        'daal.algorithms.neural_networks.training': '_training20_',
        'daal.algorithms.normalization.minmax': '_minmax_',
        'daal.algorithms.normalization.zscore': '_zscore_',
        'daal.algorithms.optimization_solver': '_optimization_solver_',
        'daal.algorithms.optimization_solver.adagrad': '_adagrad_',
        'daal.algorithms.optimization_solver.cross_entropy_loss': '_cross_entropy_loss_',
        'daal.algorithms.optimization_solver.iterative_solver': '_iterative_solver_',
        'daal.algorithms.optimization_solver.lbfgs': '_lbfgs_',
        'daal.algorithms.optimization_solver.logistic_loss': '_logistic_loss_',
        'daal.algorithms.optimization_solver.mse': '_mse_',
        'daal.algorithms.optimization_solver.objective_function': '_objective_function_',
        'daal.algorithms.optimization_solver.precomputed': '_precomputed_',
        'daal.algorithms.optimization_solver.sgd': '_sgd_',
        'daal.algorithms.optimization_solver.sum_of_functions': '_sum_of_functions_',
        'daal.algorithms.pca': '_pca_',
        'daal.algorithms.pca.quality_metric.explained_variance': '_explained_variance_',
        'daal.algorithms.pca.quality_metric_set': '_quality_metric_set6_',
        'daal.algorithms.pca.transform': '_transform_',
        'daal.algorithms.pivoted_qr': '_pivoted_qr_',
        'daal.algorithms.qr': '_qr_',
        'daal.algorithms.quality_metric': '_quality_metric_',
        'daal.algorithms.quality_metric_set': '_quality_metric_set7_',
        'daal.algorithms.quantiles': '_quantiles_',
        'daal.algorithms.regression': '_regression3_',
        'daal.algorithms.regression.prediction': '_prediction18_',
        'daal.algorithms.regression.training': '_training21_',
        'daal.algorithms.ridge_regression': '_ridge_regression_',
        'daal.algorithms.ridge_regression.prediction': '_prediction19_',
        'daal.algorithms.ridge_regression.training': '_training22_',
        'daal.algorithms.sorting': '_sorting_',
        'daal.algorithms.stump': '_stump_',
        'daal.algorithms.stump.prediction': '_prediction20_',
        'daal.algorithms.stump.training': '_training23_',
        'daal.algorithms.svd': '_svd_',
        'daal.algorithms.svm': '_svm_',
        'daal.algorithms.svm.prediction': '_prediction21_',
        'daal.algorithms.svm.quality_metric_set': '_quality_metric_set8_',
        'daal.algorithms.svm.training': '_training24_',
        'daal.algorithms.univariate_outlier_detection': '_univariate_outlier_detection_',
        'daal.algorithms.weak_learner': '_weak_learner_',
        'daal.algorithms.weak_learner.prediction': '_prediction22_',
        'daal.algorithms.weak_learner.training': '_training25_',
        'daal.daal': '_daal_',
        'daal.services': '_services_',
}

def get_sdl_cflags():
    if IS_LIN or IS_MAC:
        cflags = ['-fstack-protector', '-fPIC', '-D_FORTIFY_SOURCE=2', '-Wformat', '-Wformat-security']
        if IS_LIN:
            return cflags + ['-O2']
        elif IS_MAC:
            return cflags + []
    elif IS_WIN:
        return ['-GS', '-O2']


def get_sdl_ldflags():
    if IS_LIN:
        return ['-Wl,-z,noexecstack', '-Wl,-z,relro', '-Wl,-z,now']
    elif IS_MAC:
        return []
    elif IS_WIN:
        return ['-NXCompat', '-DynamicBase']

def get_type_defines():
    daal_type_defines = ['DAAL_ALGORITHM_FP_TYPE', 'DAAL_SUMMARY_STATISTICS_TYPE', 'DAAL_DATA_TYPE']
    return ["-D{}={}".format(d, DAAL_DEFAULT_TYPE) for d in daal_type_defines]



def getpyexts():
    include_dir_plat = ['./daal/include', daal_root + '/include']
    using_intel = os.environ.get('cc', '') in ['icc', 'icpc', 'icl']
    eca = get_type_defines()
    ela = []

    if using_intel and IS_WIN:
        include_dir_plat.append(jp(os.environ.get('ICPP_COMPILER16', ''), 'compiler', 'include'))
        eca += ['-std=c++11', '-w']
    elif not using_intel and IS_WIN:
        eca += ['-wd4267', '-wd4244', '-wd4101', '-wd4996']
    else:
        eca += ['-std=c++11', '-w']

    # Security flags
    eca += get_sdl_cflags()
    ela += get_sdl_ldflags()

    if sys.version_info[0] >= 3:
        eca.append('-DSWIGPY_USE_CAPSULE_')

    if IS_WIN:
        libraries_plat = ['daal_thread', 'daal_core_dll', 'odbc32']
    else:
        libraries_plat = ['daal_core', 'daal_thread']

    if IS_MAC:
        ela.append('-stdlib=libc++')
        ela.append("-Wl,-rpath,{}".format(jp(daal_root, 'lib')))
        ela.append("-Wl,-rpath,{}".format(jp(daal_root, '..', 'tbb', 'lib')))
    elif IS_WIN:
        ela.append('-IGNORE:4197')

    exts = []
    for m in all_modules:
        stem = m.replace('.', '__')[6:]
        s = m + '.'
        if m in ['daal.daal'] or not any(e.startswith(s) for e in all_modules):
            ext = ".".join([m.rsplit(".",1)[0], all_modules[m]])
        else:
            ext = ".".join([m, all_modules[m]])
        exts.append(Extension(ext,
                              [jp('daal', 'wrp', '_' + stem + '.cpp')],
                              include_dirs=include_dir_plat + [np.get_include()],
                              extra_compile_args=eca,
                              extra_link_args=ela,
                              libraries=libraries_plat,
                              library_dirs=[daal_root + lib_dir],
                              language='c++')),
    return exts

def getpypkgs():
    pkgs = ['daal']
    for m in all_modules:
        s = m + '.'
        if any(e.startswith(s) for e in all_modules):
            pkgs.append(m)
    return pkgs

def getpymods():
    mods = []
    for m in all_modules:
        s = m + '.'
        if m not in ['daal.daal'] and not any(e.startswith(s) for e in all_modules):
            mods.append(m)
    return mods

cfg_vars = get_config_vars()
for key, value in get_config_vars().items():
    if type(value) == str:
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

# daal setup
setup(  name        = "pydaal",
        description = "Python API to Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL)",
        author      = "Intel",
        version     = "2020.0.0.20191003",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Other Audience',
            'Intended Audience :: Science/Research',
            'License :: Other/Proprietary License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Topic :: System',
            'Topic :: Software Development',
          ],
        setup_requires = ['numpy>=1.9'],
        packages = getpypkgs(),
        ext_modules = getpyexts(),
        py_modules = getpymods(),
)
