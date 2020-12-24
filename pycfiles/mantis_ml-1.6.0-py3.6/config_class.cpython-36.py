# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/config_class.py
# Compiled at: 2019-11-29 08:07:54
# Size of source mod 2**32: 10448 bytes
import os, sys
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import re, yaml
from pathlib import Path
from shutil import copyfile
import pandas as pd
from random import randint
import string, ntpath

class Config:

    def __init__(self, config_file, output_dir, verbose=False):
        self.config_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = output_dir
        self.verbose = verbose
        self.output_dir = re.sub('\\/$', '', self.output_dir)
        static_config_file = Path(self.config_dir_path + '/conf/.config')
        with open(static_config_file, 'r') as (ymlfile):
            static_conf = yaml.load(ymlfile, Loader=(yaml.FullLoader))
        if self.verbose:
            print('\n> Static config:')
            for k, v in static_conf.items():
                print(k + ':\t', v)

        self.config_file = Path(config_file)
        with open(self.config_file, 'r') as (ymlfile):
            input_conf = yaml.load(ymlfile, Loader=(yaml.FullLoader))
        if self.verbose:
            print('\n> Input config:')
            for k, v in input_conf.items():
                print(k + ':\t', v)

        self.conf = {**static_conf, **input_conf}
        if self.verbose:
            print('\n> Full config:')
            for k, v in self.conf.items():
                print(k + ':\t', v)

        self.custom_known_genes_file = None
        self.init_variables()
        self.init_directories()

    def get_valid_filename_from_str(self, str_val):
        valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
        valid_chars = frozenset(valid_chars)
        filename = ''.join(c for c in str_val if c in valid_chars)
        filename = filename.replace(' ', '_')
        return filename

    def init_variables(self, list_delim=',\\s+'):
        self.Y = self.conf['static']['Y_label']
        self.gene_name = self.conf['static']['gene_name']
        required_field_error_msg = "\n[Error] Please provide 'Disease/Phenotype terms:' in input config file and re-run.\nSee also example config file (example-input/config.yaml) from mantis-ml GitHub repo)."
        if 'Disease/Phenotype terms' not in self.conf:
            sys.exit(required_field_error_msg)
        else:
            if self.conf['Disease/Phenotype terms'] is None:
                sys.exit(required_field_error_msg)
            else:
                self.seed_include_terms = re.split(list_delim, self.conf['Disease/Phenotype terms'])
                self.phenotype = self.get_valid_filename_from_str(ntpath.basename(self.output_dir))
                print('Phenotype/Output dir:', self.phenotype)
                if 'Additional associated terms' not in self.conf:
                    self.additional_include_terms = []
                else:
                    self.additional_include_terms = self.conf['Additional associated terms']
                    if self.additional_include_terms is None:
                        self.additional_include_terms = []
                    else:
                        self.additional_include_terms = re.split(list_delim, self.additional_include_terms)
                    if 'Diseases/Phenotypes to exclude' not in self.conf:
                        self.exclude_terms = []
                    else:
                        self.exclude_terms = self.conf['Diseases/Phenotypes to exclude']
                        if self.exclude_terms is None:
                            self.exclude_terms = []
                        else:
                            self.exclude_terms = re.split(list_delim, self.exclude_terms)
            self.highlighted_genes = None
            if self.highlighted_genes is None:
                self.highlighted_genes = []
            else:
                self.highlighted_genes = re.split(list_delim, self.highlighted_genes)
        if self.verbose:
            print('Disease/Phenotype terms:', self.seed_include_terms)
            print('\nDiseases/Phenotypes to exclude:', self.exclude_terms)
            print('Additional associated terms:', self.additional_include_terms)
            print('Genes to highlight:', self.highlighted_genes)
        self.include_disease_features = self.conf['run_advanced']['include_disease_features']
        self.generic_classifier = self.conf['run_advanced']['generic_classifier']
        if self.generic_classifier == 'None':
            self.generic_classifier = None
        self.hide_seed_genes_ratio = self.conf['run_advanced']['hide_seed_genes_ratio']
        self.seed_pos_ratio = self.conf['run_advanced']['seed_pos_ratio']
        self.random_seeds = self.conf['run_advanced']['random_seeds']
        self.classifiers = self.conf['pu_params']['classifiers']
        self.iterations = self.conf['pu_params']['iterations']
        self.nthreads = self.conf['pu_params']['nthreads']
        self.data_dir = Path(self.config_dir_path + '/' + self.conf['static']['data_dir'])
        self.hgnc_genes_series = pd.read_csv((self.data_dir / 'exac-broadinstitute/all_hgnc_genes.txt'), header=None).loc[:, 0]
        self.out_root = Path(self.output_dir)
        print(self.out_root)
        self.figs_dir = self.out_root / 'Output-Figures'
        self.processed_data_dir = self.out_root / 'processed-feature-tables'
        self.unsuperv_out = self.out_root / 'unsupervised-learning'
        self.superv_out = self.out_root / 'supervised-learning'
        self.superv_pred = self.superv_out / 'gene_predictions'
        self.superv_proba_pred = self.superv_out / 'gene_proba_predictions'
        self.superv_ranked_by_proba = self.superv_out / 'ranked-by-proba_predictions'
        self.superv_ranked_pred = self.out_root / 'Gene-Predictions'
        self.benchmark_out = self.figs_dir / 'benchmarking'
        self.eda_out = self.figs_dir / 'EDA'
        self.unsuperv_figs_out = self.figs_dir / 'unsupervised-learning'
        self.superv_figs_out = self.figs_dir / 'supervised-learning'
        self.superv_feat_imp = self.superv_figs_out / 'feature-importance'
        self.superv_figs_gene_proba = self.superv_figs_out / 'gene_proba_predictions'
        self.overlap_out_dir = self.out_root / 'Overlap-Enrichment-Results'
        self.hypergeom_figs_out = self.overlap_out_dir / 'hypergeom-enrichment-figures'
        self.overlap_gene_predictions = self.overlap_out_dir / 'Gene-Predictions-After-Overlap'
        self.run_boruta = self.conf['run_steps']['run_boruta']
        self.run_unsupervised = self.conf['run_steps']['run_unsupervised']
        self.boruta_figs_dir = self.figs_dir / 'boruta'
        self.feature_selection_dir = self.out_root / 'feature_selection'
        self.boruta_tables_dir = self.feature_selection_dir / 'boruta'
        self.discard_highly_correlated = self.conf['eda_filters']['discard_highly_correlated']
        self.create_plots = self.conf['eda_filters']['create_plots']
        self.drop_missing_data_features = self.conf['eda_filters']['drop_missing_data_features']
        self.drop_gene_len_features = self.conf['eda_filters']['drop_gene_len_features']
        self.manual_feature_selection = self.conf['eda_filters']['manual_feature_selection']
        self.missing_data_thres = self.conf['eda_parameters']['missing_data_thres']
        self.high_corr_thres = self.conf['eda_parameters']['high_corr_thres']
        self.feature_selection = self.conf['supervised_filters']['feature_selection']
        self.boruta_iterations = self.conf['supervised_filters']['boruta_iterations']
        self.boruta_decision_thres = self.conf['supervised_filters']['boruta_decision_thres']
        self.add_original_features_in_stacking = self.conf['supervised_filters']['add_original_features_in_stacking']
        self.test_size = self.conf['supervised_filters']['test_size']
        self.balancing_ratio = self.conf['supervised_filters']['balancing_ratio']
        self.random_fold_split = self.conf['supervised_filters']['random_fold_split']
        self.kfold = self.conf['supervised_filters']['kfold']
        print('P/U Balancing ratio: ', self.balancing_ratio)
        self.random_state = 2018
        self.out_data_dir = Path(self.out_root / 'data')
        self.compiled_data_dir = Path(self.out_data_dir / 'compiled_feature_tables')
        self.generic_feature_table = Path(self.compiled_data_dir / 'generic_feature_table.tsv')
        self.filtered_by_disease_feature_table = Path(self.compiled_data_dir / 'filtered_by_disease_feature_table.tsv')
        self.ckd_specific_feature_table = Path(self.compiled_data_dir / 'ckd_specific_feature_table.tsv')
        self.cardiov_specific_feature_table = Path(self.compiled_data_dir / 'cardiov_specific_feature_table.tsv')
        self.complete_feature_table = Path(self.compiled_data_dir / 'complete_feature_table.tsv')

    def init_directories(self):
        """
                - Create output dirs
                - Copy config.yaml to out_root directory
                :return: 
                """
        dirs = [
         self.out_root, self.compiled_data_dir, self.out_root, self.out_data_dir, self.figs_dir,
         self.processed_data_dir, self.eda_out, self.unsuperv_out, self.unsuperv_figs_out,
         self.superv_out, self.superv_pred, self.superv_ranked_pred, self.superv_ranked_by_proba,
         self.superv_proba_pred, self.superv_figs_out, self.superv_feat_imp, self.superv_figs_gene_proba,
         self.overlap_out_dir, self.hypergeom_figs_out, self.overlap_gene_predictions, self.benchmark_out,
         self.boruta_figs_dir, self.feature_selection_dir, self.boruta_tables_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)

        src_conf = str(self.config_file)
        dest_conf = str(self.out_root / 'config.yaml')
        copyfile(src_conf, dest_conf)
        self.locked_config_path = dest_conf


if __name__ == '__main__':
    conf_file = sys.argv[1]
    cfg = Config(conf_file)