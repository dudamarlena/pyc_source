# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/deseq.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 7168 bytes
import csv, sys, os
from subprocess import call

class DESeqRunner(object):

    def __init__(self, libs, conditions, deseq_raw_folder, deseq_extended_folder, deseq_script_path, deseq_pca_heatmap_path, gene_wise_quanti_combined_path, deseq_tmp_session_info_script, deseq_session_info, fc_shrinkage_off, cooks_cutoff_off=False):
        self._libs = libs
        self._conditions = conditions
        self._deseq_raw_folder = deseq_raw_folder
        self._deseq_extended_folder = deseq_extended_folder
        self._deseq_script_path = deseq_script_path
        self._deseq_pca_heatmap_path = deseq_pca_heatmap_path
        self._gene_wise_quanti_combined_path = gene_wise_quanti_combined_path
        self._deseq_tmp_session_info_script = deseq_tmp_session_info_script
        self._deseq_session_info = deseq_session_info
        self._cooks_cutoff_off = cooks_cutoff_off
        self._first_data_column = 11
        self._fc_shrinkage_off = fc_shrinkage_off

    def write_session_info_file(self):
        with open(self._deseq_tmp_session_info_script, 'w') as (tmp_r_script_fh):
            tmp_r_script_fh.write("library('DESeq2')\nsessionInfo()\n")
        with open(self._deseq_session_info, 'w') as (session_info_fh):
            with open(os.devnull, 'w') as (devnull):
                call(['Rscript', self._deseq_tmp_session_info_script], stdout=session_info_fh,
                  stderr=devnull)
        os.remove(self._deseq_tmp_session_info_script)

    def create_deseq_script_file(self):
        libs_to_conditions = dict([(lib, condition) for lib, condition in zip(self._libs, self._conditions)])
        head_row = open(self._gene_wise_quanti_combined_path).readline()[:-1].split('\t')
        libs = head_row[self._first_data_column - 1:]
        libs_str = ','.join(["'%s'" % lib for lib in libs])
        conditions = [libs_to_conditions[lib] for lib in libs]
        condition_str = ', '.join(["'%s'" % cond for cond in conditions])
        if not self._fc_shrinkage_off:
            beta_prior_str = ', betaPrior=TRUE'
        else:
            if self._fc_shrinkage_off:
                beta_prior_str = ''
        file_content = self._deseq_script_template() % (
         self._gene_wise_quanti_combined_path, self._first_data_column - 1,
         len(libs), self._first_data_column, libs_str, condition_str,
         beta_prior_str,
         self._deseq_pca_heatmap_path)
        file_content += self._comparison_call_strings(conditions)
        deseq_fh = open(self._deseq_script_path, 'w')
        deseq_fh.write(file_content)
        deseq_fh.close()

    def run_deseq(self):
        call(['Rscript', self._deseq_script_path])

    def merge_counting_files_with_results(self):
        for comparison_file, combo in self._comparison_files_and_combos:
            output_fh = open('%s/%s' % (
             self._deseq_extended_folder,
             comparison_file.replace('.csv', '_with_annotation_and_countings.csv')), 'w')
            output_fh.write('# Reference library (divisor): {}\n'.format(combo[1]))
            output_fh.write('# Comparison library (numerator): {}\n'.format(combo[0]))
            try:
                deseq_result_fh = open('%s/%s' % (
                 self._deseq_raw_folder, comparison_file))
            except:
                sys.stderr.write('Apparently DESeq did not generate the file "%s". Extension stopped.\n' % comparison_file)
                continue

            for counting_file_row, comparison_file_row in zip(csv.reader((open(self._gene_wise_quanti_combined_path)),
              delimiter='\t'), csv.reader(deseq_result_fh, delimiter='\t')):
                if comparison_file_row[0] == 'baseMean':
                    comparison_file_row = [''] + comparison_file_row
                    counting_file_row[self._first_data_column:] = ['%s raw countings' % lib_name for lib_name in counting_file_row[self._first_data_column:]]
                output_fh.write('\t'.join(counting_file_row + comparison_file_row[1:]) + '\n')

            output_fh.close()

    def _condition_combos(self, conditions):
        non_redundant_conditions = set(conditions)
        for cond1 in non_redundant_conditions:
            for cond2 in non_redundant_conditions:
                if not cond1 == cond2:
                    yield (
                     cond1, cond2)

    def _comparison_call_strings(self, conditions):
        call_string = ''
        condition_combos = self._condition_combos(conditions)
        self._comparison_files_and_combos = []
        cooks_cutoff_str = ''
        if self._cooks_cutoff_off:
            cooks_cutoff_str = ', cooksCutoff=FALSE'
        for index, condition_combo in enumerate(condition_combos):
            call_string += "comp%s <- results(dds, contrast=c('condition','%s', '%s')%s)\n" % (
             index, condition_combo[0], condition_combo[1],
             cooks_cutoff_str)
            comparison_file = 'deseq_comp_%s_vs_%s.csv' % (
             condition_combo[0], condition_combo[1])
            self._comparison_files_and_combos.append((
             comparison_file, list(condition_combo)))
            call_string += "write.table(comp%s, file='%s/%s', quote=FALSE, sep='\\t')\n" % (
             index, self._deseq_raw_folder, comparison_file)

        return call_string

    def _deseq_script_template(self):
        return "library('DESeq2')\nrawCountTable <- read.table('%s', skip=1, sep='\\t', quote='', comment.char='', colClasses=c(rep('character',%s), rep('numeric',%s)))\ncountTable <- round(rawCountTable[,%s:length(names(rawCountTable))])\nlibs <- c(%s)\nconds <- c(%s)\ncolnames(countTable) <- libs\nsamples <- data.frame(row.names=libs, condition=conds, lib=libs)\ndds <- DESeqDataSetFromMatrix(countData=countTable, colData=samples, design=~condition)\ndds <- DESeq(dds%s)\n\n# PCA plot\npdf('%s')\nrld <- rlog(dds)\nprint(plotPCA(rld, intgroup=c('condition')))\n\n# Heatmap\nlibrary('RColorBrewer')\nlibrary('gplots')\ndistsRL <- dist(t(assay(rld)))\nmat <- as.matrix(distsRL)\nrownames(mat) <- with(colData(dds), paste(lib, sep=' : '))\nhmcol <- colorRampPalette(brewer.pal(9, 'GnBu'))(100)\nheatmap.2(mat, trace='none', col = rev(hmcol), margin=c(13, 13))\n"