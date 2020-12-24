# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/modules/benchmarking/get_consensus_novel_predictions.py
# Compiled at: 2019-11-19 09:10:26
# Size of source mod 2**32: 7536 bytes
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt, pandas as pd, sys, os, pickle
from mantis_ml.config_class import Config
clf_alias = {'ExtraTreesClassifier':'ET', 
 'SVC':'SVC',  'DNN':'DNN',  'RandomForestClassifier':'RF',  'XGBoost':'XGB',  'GradientBoostingClassifier':'GB',  'Stacking':'Stacking'}
color_palette = {'Stacking':'#684392',  'ExtraTreesClassifier':'#35A037',  'SVC':'#651124',  'DNN':'#000000',  'RandomForestClassifier':'#1F7AB9',  'XGBoost':'#F07E21',  'GradientBoostingClassifier':'#E32321'}
best_clf_per_disease = {'CKD':'XGBoost',  'GGE':'XGBoost',  'ALS':'ExtraTreesClassifier'}

def plot_grouped_barplot(df, out_filename, width=0.1, relaxation=0):
    df = df.copy()
    fig, ax = plt.subplots(figsize=(20, 10))
    pos = list(range(df.shape[0]))
    gene_names = df['Gene_Name']
    df.drop(['Gene_Name'], axis=1, inplace=True)
    for i in range(len(df.columns)):
        clf = df.columns.values[i]
        x_coord = [p + width * i for p in pos]
        plt.bar(x_coord, (df[clf].values), width, alpha=0.5, color=(color_palette[clf]), label=clf)

    ax.set_ylabel('mantis-ml percentile score')
    title_str = 'mantis-ml performance per classifier for a set of consensus genes after overlap with collapsing results'
    title_str += '\n(found in ' + str(len(df.columns) - relaxation) + ' out of ' + str(len(df.columns)) + ' classifiers)'
    ax.set_title(title_str)
    ax.set_xticks([p + (len(df.columns) / 4 + 1) * width for p in pos])
    ax.set_xticklabels(gene_names)
    if len(pos) > 20:
        plt.xticks(rotation='vertical')
    plt.legend(loc='upper right')
    ax.legend(bbox_to_anchor=(1.05, 1))
    fig.savefig((out_dir + gene_class + '.' + out_filename + '.pdf'), bbox_inches='tight')


def find_consensus_from_selected_classifiers(clf_subset, df, relaxation=0):
    df = df.copy()
    df['classifier_hits'] = df.sum(axis=1)
    df = df.loc[df['classifier_hits'] >= len(clf_subset) - relaxation, :]
    df.sort_values(by='classifier_hits', ascending=False, inplace=True)
    df = df[['Gene_Name']]
    for clf in clf_subset:
        tmp_mantis_ml_file = str(cfg.superv_ranked_pred / (clf + '.All_genes.mantis-ml_percentiles.csv'))
        tmp_mantis_df = pd.read_csv(tmp_mantis_ml_file, header=0, index_col=0)
        tmp_mantis_df = tmp_mantis_df.rename(columns={'mantis_ml_perc': clf})
        tmp_mantis_df.drop(['mantis_ml_proba'], axis=1, inplace=True)
        df = df.merge(tmp_mantis_df, left_on='Gene_Name', right_on='Gene_Name', how='left')

    top_clf = best_clf_per_disease[disease]
    if top_clf not in df.columns:
        top_clf = df.columns.values[0]
    df.sort_values(by=top_clf, inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df


def get_cons_list_and_plot(df, clf_subset, relaxation=0, width=0.1):
    filename_suffix = '_'.join([clf_alias[c] for c in clf_subset])
    if len(clf_subset) == 7:
        filename_suffix = 'all_classifiers'
    cons_df = find_consensus_from_selected_classifiers(clf_subset, df, relaxation=relaxation)
    plot_grouped_barplot(cons_df, ('consensus.' + filename_suffix), relaxation=relaxation, width=width)
    print('\n> ' + ', '.join(clf_subset) + ':')
    consensus_novel_genes = cons_df['Gene_Name'].values
    print(consensus_novel_genes)
    with open(out_dir + gene_class + '.consensus_novel_genes.' + filename_suffix + '.top_ratio' + str(top_ratio) + '.txt', 'w') as (fh):
        for g in consensus_novel_genes:
            fh.write(g + '\n')


if __name__ == '__main__':
    overlap_collapsing_base_dir = 'misc/overlap-collapsing-analyses'
    config_file = sys.argv[1]
    gene_class = sys.argv[2]
    top_ratio = float(sys.argv[3])
    print('gene class:', gene_class, 'top_ratio:', top_ratio)
    cfg = Config(config_file)
    sorted_classifiers = []
    avg_aucs_file = str(cfg.superv_out / 'Avg_AUC_per_classifier.txt')
    with open(avg_aucs_file) as (fh):
        for line in fh:
            tmp_clf, tmp_auc = line.split('\t')
            sorted_classifiers.append(tmp_clf)

    if 'CKD' in cfg.phenotype:
        input_dir = 'CKD_JASN_2019'
        disease = 'CKD'
        try:
            top_classifiers = sorted_classifiers[:2]
        except:
            top_classifiers = sorted_classifiers

        relaxation = 2
    if 'Epilepsy' in cfg.phenotype:
        input_dir = 'Epilepsy-LancetNeurology_2017'
        disease = 'GGE'
        try:
            top_classifiers = sorted_classifiers[:2]
        except:
            top_classifiers = sorted_classifiers

        relaxation = 2
    if 'ALS' in cfg.phenotype:
        input_dir = 'ALS_Science_2015'
        disease = 'ALS'
        try:
            top_classifiers = sorted_classifiers[:2]
        except:
            top_classifiers = sorted_classifiers

        relaxation = 2
        if gene_class == 'Known':
            relaxation = len(classifiers) - 1
    out_dir = '../../../' + overlap_collapsing_base_dir + '/' + input_dir + '/Hypergeometric_results/'
    all_novel_genes = []
    novel_genes_df = pd.DataFrame()
    for clf in sorted_classifiers:
        tmp_df = pd.read_csv(('../../../' + overlap_collapsing_base_dir + '/' + input_dir + '/Hypergeometric_results/' + gene_class + '_overlaping_genes.Top_' + str(top_ratio) + '.' + clf_alias[clf] + '.' + disease + '.csv'), header=None)
        tmp_novel_genes = tmp_df.iloc[:, 0].tolist()
        if len(all_novel_genes) > 0:
            all_novel_genes = list(set(all_novel_genes) & set(tmp_novel_genes))
        else:
            all_novel_genes = tmp_novel_genes
        tmp_df[clf] = 1
        tmp_df.index = tmp_novel_genes
        tmp_df.drop((tmp_df.columns[0]), axis=1, inplace=True)
        if len(novel_genes_df) > 0:
            novel_genes_df = novel_genes_df.merge(tmp_df, left_index=True, right_index=True, how='outer')
        else:
            novel_genes_df = tmp_df

    novel_genes_df.fillna(0, inplace=True)
    novel_genes_df.reset_index(inplace=True)
    novel_genes_df.columns.values[0] = 'Gene_Name'
    print(novel_genes_df)
    get_cons_list_and_plot(novel_genes_df, sorted_classifiers, relaxation=relaxation)
    clf_subset = top_classifiers
    width = 0.3
    get_cons_list_and_plot(novel_genes_df, clf_subset, width=width)
    tmp_clf_subset = [
     top_classifiers[0]]
    get_cons_list_and_plot(novel_genes_df, tmp_clf_subset, width=width)
    tmp_clf_subset = [
     top_classifiers[1]]
    get_cons_list_and_plot(novel_genes_df, tmp_clf_subset, width=width)