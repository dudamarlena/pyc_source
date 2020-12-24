# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/modules/pre_processing/eda_wrapper.py
# Compiled at: 2019-11-14 14:47:10
# Size of source mod 2**32: 3431 bytes
import matplotlib
matplotlib.use('agg')
import sys
from mantis_ml.modules.pre_processing.eda import EDA
from mantis_ml.config_class import Config

class EDAWrapper:

    def __init__(self, cfg):
        self.cfg = cfg
        self.high_corr_thres = self.cfg.high_corr_thres
        self.test_size = self.cfg.test_size
        self.balancing_ratio = self.cfg.balancing_ratio
        self.eda = EDA(self.cfg)

    def run(self):
        df, gene_names = self.eda.read_input_feature_table()
        if self.cfg.create_plots:
            tmp_df = df.select_dtypes(exclude=['object']).copy()
            self.eda.plot_feature_corr_map(tmp_df, 'pre_filtered')
        df = self.eda.drop_duplicate_features(df)
        df = self.eda.drop_uninformative_features(df)
        df = self.eda.fix_feature_data_types(df)
        self.eda.check_for_missing_data(df)
        df = self.eda.standardise_features(df)
        print('Categorical features:')
        print(df.loc[:, df.dtypes == object].columns)
        all_features_df = df.copy()
        all_features_df = self.eda.dummify_categorical_vars(all_features_df)
        self.eda.save_feature_table_to_file(all_features_df, gene_names, file_descr='unfiltered')
        if self.cfg.discard_highly_correlated:
            df = self.eda.drop_elems_w_high_corr(df, thres=(self.high_corr_thres))
        if self.cfg.create_plots:
            tmp_df = df.select_dtypes(exclude=['object']).copy()
            self.eda.plot_feature_corr_map(tmp_df, 'post_filtering')
        if self.cfg.create_plots:
            self.eda.plot_hist_for_numeric_features(df)
        if self.cfg.create_plots:
            self.eda.plot_hist_for_non_numerical_features(df)
        df = self.eda.dummify_categorical_vars(df)
        if self.cfg.manual_feature_selection:
            df = self.eda.select_features_manually(df)
        self.eda.save_feature_table_to_file(df, gene_names)
        train_df, test_df = self.eda.split_into_train_and_test_sets(df, test_size=(self.test_size), random_state=1, prefix='full')
        balanced_df = self.eda.fix_classes_imbalance(df, gene_names, balancing_ratio=(self.balancing_ratio))
        train_df, test_df = self.eda.split_into_train_and_test_sets(balanced_df, test_size=(self.test_size),
          random_state=1)
        print('\n____ EDA pre-processing complete! ____\n')


if __name__ == '__main__':
    config_file = '../../config.yaml'
    cfg = Config(config_file)
    eda_wrapper = EDAWrapper(cfg)
    eda_wrapper.run()