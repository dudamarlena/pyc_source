# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bioinfokit/analys.py
# Compiled at: 2020-04-25 03:50:31
# Size of source mod 2**32: 31496 bytes
from sklearn.decomposition import PCA
import pandas as pd, re, numpy as np
from bioinfokit.visuz import screeplot, pcaplot, general
from itertools import groupby, chain, combinations
import string, sys, csv
import matplotlib.pyplot as plt
import scipy.stats as stats
from tabulate import tabulate
from statsmodels.graphics.mosaicplot import mosaic
from textwrap3 import wrap
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.formula.api import ols
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from decimal import Decimal
from pathlib import Path
from sklearn.metrics import mean_squared_error

def seqcov(file='fastq_file', gs='genome_size'):
    x = fastq.fastq_format_check(file)
    if x == 1:
        print('Error: Sequences are not in fastq format')
        sys.exit(1)
    num_reads, total_len = fastq.fqreadcounter(file)
    gs = gs * 1000000.0
    cov = round(float(total_len / gs), 2)
    print('Sequence coverage for', file, 'is', cov)


def mergevcf(file='vcf_file_com_sep'):
    vcf_files = file.split(',')
    merge_vcf = open('merge_vcf.vcf', 'w+')
    file_count = 0
    print('merging vcf files...')
    for f in vcf_files:
        if file_count == 0:
            read_file = open(f, 'rU')
            for line in read_file:
                merge_vcf.write(line)

            read_file.close()
        else:
            if file_count > 0:
                read_file = open(f, 'rU')
                for line in read_file:
                    if not line.startswith('#'):
                        merge_vcf.write(line)

                read_file.close()
        file_count += 1

    merge_vcf.close()


def pca(table='p_df'):
    d = pd.DataFrame(data=table)
    d_cols = list(d.columns.values)
    pca_out = PCA()
    pca_out.fit(d)
    prop_var = pca_out.explained_variance_ratio_
    cum_prop_var = np.cumsum(prop_var)
    rotation = pca_out.components_
    num_pc = pca_out.n_features_
    pc_list = list(range(1, num_pc + 1))
    pc_list = ['PC' + str(w) for w in pc_list]
    pca_df_var = [prop_var, cum_prop_var]
    pca_df_out = pd.DataFrame.from_dict(dict(zip(pc_list, zip(*pca_df_var))))
    pca_df_rot_out = pd.DataFrame.from_dict(dict(zip(pc_list, rotation)))
    pca_df_out.rename(index={0:'Proportion of Variance',  1:'Cumulative proportion'}, inplace=True)
    print('Component summary\n')
    print(pca_df_out)
    print('\nLoadings\n')
    pca_df_rot_out['sample'] = d_cols
    pca_df_rot_out = pca_df_rot_out.set_index('sample')
    del pca_df_rot_out.index.name
    print(pca_df_rot_out)
    pcascree = [pc_list, prop_var]
    screeplot(obj=pcascree)
    pcaplot(x=(rotation[0]), y=(rotation[1]), z=(rotation[2]), labels=d_cols, var1=(round(prop_var[0] * 100, 2)), var2=(round(prop_var[1] * 100, 2)), var3=(round(prop_var[2] * 100, 2)))


def extract_seq(file='fasta_file', id='id_file'):
    id_list = []
    id_file = open(id, 'rU')
    out_file = open('output.fasta', 'w')
    for line in id_file:
        id_name = line.rstrip('\n')
        id_list.append(id_name)

    list_len = len(id_list)
    value = [1] * list_len
    dict_list = dict(zip(id_list, value))
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if fasta_header.strip() in dict_list.keys():
            out_file.write('>' + fasta_header + '\n' + seq + '\n')

    out_file.close()
    id_file.close()


def extract_seq_nomatch(file='fasta_file', id='id_file'):
    id_list = []
    id_file = open(id, 'rU')
    out_file = open('output.fasta', 'w')
    for line in id_file:
        id_name = line.rstrip('\n')
        id_list.append(id_name)

    list_len = len(id_list)
    value = [1] * list_len
    dict_list = dict(zip(id_list, value))
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if fasta_header.strip() not in dict_list.keys():
            out_file.write('>' + fasta_header + '\n' + seq + '\n')

    out_file.close()
    id_file.close()


def fqreadcounter(file='fastq_file'):
    general.depr_mes('bioinfokit.analys.fastq.fqreadcounter')


def fasta_reader(file='fasta_file'):
    read_file = open(file, 'rU')
    fasta_iter = (rec[1] for rec in groupby(read_file, lambda line: line[0] == '>'))
    for record in fasta_iter:
        fasta_header = record.__next__()[1:].strip()
        fasta_header = re.split('\\s+', fasta_header)[0]
        seq = ''.join((s.strip() for s in fasta_iter.__next__()))
        yield (fasta_header, seq)


def rev_com(seq=None, file=None):
    if seq is not None:
        rev_seq = seq[::-1]
        rev_seq = rev_seq.translate(str.maketrans('ATGCUN', 'TACGAN'))
        return rev_seq
    if file is not None:
        out_file = open('output_revcom.fasta', 'w')
        fasta_iter = fasta_reader(file)
        for record in fasta_iter:
            fasta_header, seq = record
            rev_seq = seq[::-1]
            rev_seq = rev_seq.translate(str.maketrans('ATGCUN', 'TACGAN'))
            out_file.write('>' + fasta_header + '\n' + rev_seq + '\n')

        out_file.close()


def ext_subseq(file='fasta_file', id='chr', st='start', end='end', strand='plus'):
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if id == fasta_header.strip():
            if strand == 'plus':
                sub_seq = seq[int(st - 1):int(end)]
                print(sub_seq)
        if id == fasta_header.strip() and strand == 'minus':
            seq = rev_com(seq)
            sub_seq = seq[int(st - 1):int(end)]
            print(sub_seq)


def fastq_format_check(file='fastq_file'):
    general.depr_mes('bioinfokit.analys.fastq.fastq_format_check')


def tcsv(file='tab_file'):
    tab_file = csv.reader((open(file, 'r')), dialect=(csv.excel_tab))
    csv_file = csv.writer(open('out.csv', 'w', newline=''), dialect=(csv.excel))
    for record in tab_file:
        csv_file.writerow(record)


def ttsam(df='dataframe', xfac=None, res=None, evar=True):
    general.depr_mes('bioinfokit.visuz.stat.ttsam')


def chisq(table='table'):
    general.depr_mes('bioinfokit.visuz.stat.chisq')


class fastq:

    def __init__(self):
        pass

    def fastq_reader(file='fastq_file'):
        fastq_file = open(file, 'r')
        for line in fastq_file:
            header_1 = line.rstrip()
            read = next(fastq_file).rstrip()
            header_2 = next(fastq_file).rstrip()
            read_qual_asc = next(fastq_file).rstrip()
            yield (header_1, read, header_2, read_qual_asc)

    def fqreadcounter(file='fastq_file'):
        read_file = open(file, 'rU')
        num_lines = 0
        total_len = 0
        for line in read_file:
            num_lines += 1
            header_1 = line.rstrip()
            read = next(read_file).rstrip()
            len_read = len(read)
            total_len += len_read
            header_2 = next(read_file).rstrip()
            read_qual = next(read_file).rstrip()

        read_file.close()
        num_reads = num_lines / 4
        return (num_reads, total_len)

    def fastq_format_check(file='fastq_file'):
        read_file = open(file, 'r')
        x = 0
        for line in read_file:
            header = line.rstrip()
            if not header.startswith('@'):
                x = 1
            else:
                x = 0
            break

        return x

    def detect_fastq_variant(file='fastq_file'):
        count = 0
        check = []
        fastq_file = open(file, 'rU')
        for line in fastq_file:
            header_1 = line.rstrip()
            read = next(fastq_file).rstrip()
            header_2 = next(fastq_file).rstrip()
            read_qual_asc = next(fastq_file).rstrip()
            asc_list = list(read_qual_asc)
            asc_list = list(map(ord, asc_list))
            min_q = min(asc_list)
            max_q = max(asc_list)
            check.append(min_q)
            check.append(max_q)
            count += 1
            if count == 40000:
                break

        fastq_file.close()
        min_q = min(check)
        max_q = max(check)
        if 64 > min_q >= 33:
            if max_q == 74:
                return 1
        if min_q >= 64:
            if 74 < max_q <= 104:
                return 2
        if 64 > min_q >= 33:
            if max_q <= 73:
                return 3

    def split_fastq(file='fastq_file'):
        x = fastq.fastq_format_check(file)
        if x == 1:
            print('Error: Sequences are not in sanger fastq format')
            sys.exit(1)
        fastq_iter = fastq.fastq_reader(file)
        out_file_name_1 = open(Path(file).stem + '_1.fastq', 'w')
        out_file_name_2 = open(Path(file).stem + '_2.fastq', 'w')
        i = 1
        for record in fastq_iter:
            header_1, read, header_2, read_qual_asc = record
            if i % 2 == 0:
                out_file_name_2.write(header_1 + '\n' + read + '\n' + header_2 + '\n' + read_qual_asc + '\n')
            else:
                out_file_name_1.write(header_1 + '\n' + read + '\n' + header_2 + '\n' + read_qual_asc + '\n')
            i += 1

        out_file_name_1.close()
        out_file_name_2.close()


class format:

    def __init__(self):
        pass

    def fqtofa(file='fastq_file'):
        x = fastq.fastq_format_check(file)
        if x == 1:
            print('Error: Sequences are not in sanger fastq format')
            sys.exit(1)
        read_file = open(file, 'rU')
        out_file = open('output.fasta', 'w')
        for line in read_file:
            header_1 = line.rstrip()
            read = next(read_file).rstrip()
            header_2 = next(read_file).rstrip()
            read_qual = next(read_file).rstrip()
            out_file.write(header_1 + '\n' + '\n'.join(wrap(read, 60)) + '\n')

        read_file.close()

    def tabtocsv(file='tab_file'):
        tab_file = csv.reader((open(file, 'r')), dialect=(csv.excel_tab))
        csv_file = csv.writer(open('output.csv', 'w', newline=''), dialect=(csv.excel))
        for record in tab_file:
            csv_file.writerow(record)

    def csvtotab(file='csv_file'):
        csv_file = csv.reader((open(file, 'r')), dialect=(csv.excel))
        tab_file = csv.writer(open('output.txt', 'w', newline=''), dialect=(csv.excel_tab))
        for record in csv_file:
            tab_file.writerow(record)

    def hmmtocsv(file='hmm_file'):
        hmm_file = open(file, 'rU')
        csv_file = open('ouput_hmm.csv', 'w')
        for line in hmm_file:
            line = line.strip()
            if not line.startswith('#'):
                data = re.split(' +', line)
                if len(data) == 19:
                    data[18] = data[18].replace(',', ' ')
                    csv_file.write(str.join(',', data))
                    csv_file.write('\n')
                elif len(data) > 19:
                    ele = list(range(18, len(data)))
                    data[18] = ' '.join([e for i, e in enumerate(data) if i in ele])
                    data[18] = data[18].replace(',', '')
                    csv_file.write(str.join(',', data[0:19]))
                    csv_file.write('\n')

        hmm_file.close()
        csv_file.close()

    def fq_qual_var(file=None):
        if file is None:
            print('Error: No sanger fastq file provided')
            sys.exit(1)
        else:
            x = fastq.fastq_format_check(file)
            if x == 1:
                print('Error: Sequences are not in sanger fastq format')
                sys.exit(1)
            else:
                qual_format = fastq.detect_fastq_variant(file)
                if qual_format == 1:
                    print('The fastq quality format is illumina 1.8+ (Offset +33)')
                else:
                    if qual_format == 2:
                        print('The fastq quality format is illumina 1.3/1.4 (Offset +64)')
                    else:
                        if qual_format == 3:
                            print('The fastq quality format is Sanger (Offset +33)')
                        else:
                            print('\nError: Wrong quality format\n')
                            sys.exit(1)


class stat:

    def __init__(self):
        pass

    def anova(self, df='dataframe', xfac=None, res=None):
        df = df.dropna()
        df = df[[xfac[0], res]]
        if not (xfac and res is not None):
            raise AssertionError('xfac or res variable is missing')
        grand_mean = df[res].mean()
        total_obs = df.count()[0]
        if len(xfac) == 1:
            levels = df[xfac[0]].unique()
            assert len(levels) > 2, 'levels must be more than 2; use two-sample t-test for two levels'
            levels.sort()
            ss_trt_between = np.sum(df.groupby(xfac).count() * (df.groupby(xfac).mean() - grand_mean) ** 2)[0]
            ss_err_within = 0
            for name, group in df.groupby(xfac):
                ss_err_within = ss_err_within + np.sum((group[res] - group[res].mean()) ** 2)

            ss_total = ss_trt_between + ss_err_within
            df_trt_between = len(levels) - 1
            df_err_within = total_obs - len(levels)
            df_total = df_trt_between + df_err_within
            ms_trt_between = ss_trt_between / df_trt_between
            ms_err_within = ss_err_within / df_err_within
            f_value = ms_trt_between / ms_err_within
            p_value = '%.4E' % Decimal(stats.f.sf(f_value, df_trt_between, df_err_within))
            anova_table = []
            anova_table.append([
             'Model', df_trt_between, ss_trt_between, round(ms_trt_between, 4), round(f_value, 4), p_value])
            anova_table.append(['Error', df_err_within, ss_err_within, round(ms_err_within, 4), '', ''])
            anova_table.append(['Total', df_total, ss_total, '', '', ''])
            print('\nANOVA Summary:\n')
            print(tabulate(anova_table, headers=['Source', 'Df', 'Sum Squares', 'Mean Squares', 'F', 'Pr(>F)']), '\n')

    def oanova(table='table', res=None, xfac=None, ph=False, phalpha=0.05):
        model = ols(('{} ~ C({})'.format(res, xfac)), data=table).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        levels = table[xfac].unique()
        fac_list = []
        data_summary = []
        for i in levels:
            temp_summary = []
            temp = table.loc[(table[xfac] == i, res)]
            fac_list.append(temp)
            temp_summary.append(i)
            temp_summary.extend(temp.describe().to_numpy())
            data_summary.append(temp_summary)

        print('\nTable Summary\n')
        print(tabulate(data_summary, headers=['Group', 'Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']), '\n')
        w, pvalue1 = stats.shapiro(model.resid)
        w, pvalue2 = (stats.bartlett)(*fac_list)
        if pvalue1 < 0.05:
            print('Warning: Data is not drawn from normal distribution')
        else:
            if pvalue2 < 0.05:
                print('Warning: treatments do not have equal variances')
            print('\nOne-way ANOVA Summary\n')
            print(anova_table)
            print('\n')
            if ph:
                m_comp = pairwise_tukeyhsd(endog=(table[res]), groups=(table[xfac]), alpha=phalpha)
                print('\nPost-hoc Tukey HSD test\n')
                print(m_comp, '\n')
            print('ANOVA Assumption tests\n')
            print('Shapiro-Wilk (P-value):', pvalue1, '\n')
            print('Bartlett (P-value):', pvalue2, '\n')

    def lin_reg(self, df='dataframe', y=None, x=None):
        df = df.dropna()
        if not (x and y is not None):
            raise AssertionError('Provide proper column names for X and Y variables')
        if not type(x) is list:
            assert type(y) is list, 'X or Y column names should be list'
        assert df.shape[0] >= 4, 'Very few data'
        self.X = df[x].to_numpy()
        self.Y = df[y].to_numpy()
        p = len(x)
        e = p + 1
        n = len(df[y])
        reg_out = LinearRegression().fit(self.X, self.Y)
        r_sq = round(reg_out.score(self.X, self.Y), 4)
        r_sq_adj = round(1 - (1 - r_sq) * ((n - 1) / (n - p - 1)), 4)
        rmse = round(np.sqrt(1 - r_sq) * np.std(self.Y), 4)
        reg_intercept = reg_out.intercept_
        reg_slopes = reg_out.coef_
        self.y_hat = reg_out.predict(self.X)
        self.residuals = self.Y - self.y_hat
        regSS = np.sum((self.y_hat - np.mean(self.Y)) ** 2)
        residual_sse = np.sum((self.Y - self.y_hat) ** 2)
        sst = np.sum((self.Y - np.mean(self.Y)) ** 2)
        eq = ''
        for i in range(p):
            eq = eq + ' + ' + '(' + str(round(reg_slopes[0][i], 4)) + '*' + x[i] + ')'

        self.reg_eq = str(round(reg_intercept[0], 4)) + eq
        sigma_sq_hat = round(residual_sse / (n - e), 4)
        res_stdev = round(np.sqrt(sigma_sq_hat))
        self.std_residuals = self.residuals / res_stdev
        X_mat = np.empty(shape=(n, e), dtype=(np.float))
        X_mat[:, 0] = 1
        X_mat[:, 1:e] = self.X
        var_hat = np.linalg.inv(X_mat.T @ X_mat) * sigma_sq_hat
        standard_error = []
        for param in range(e):
            standard_error.append(round(np.sqrt(var_hat[(param, param)]), 4))

        params = list(chain(*[['Intercept'], x]))
        estimates = list(chain(*[[reg_intercept[0]], reg_slopes[0]]))
        tabulate_list = []
        for param in range(e):
            tabulate_list.append([params[param], estimates[param], standard_error[param],
             estimates[param] / standard_error[param],
             '%.4E' % Decimal(stats.t.sf(np.abs(estimates[param] / standard_error[param]), n - e) * 2)])

        anova_table = []
        anova_table.append(['Model', p, regSS, round(regSS / p, 4), round(regSS / p / (residual_sse / (n - e)), 4),
         '%.4E' % Decimal(stats.f.sf(regSS / p / (residual_sse / (n - e)), p, n - e))])
        anova_table.append(['Error', n - e, residual_sse, round(residual_sse / (n - e), 4), '', ''])
        anova_table.append(['Total', n - 1, sst, '', '', ''])
        print('\nRegression equation:\n')
        print(self.reg_eq)
        print('\nRegression Summary:')
        print(tabulate([['Dependent variables', x], ['Independent variables', y],
         [
          'Coefficient of determination (r-squared)', r_sq], ['Adjusted r-squared', r_sq_adj],
         [
          'Root Mean Square Error (RMSE)', rmse],
         [
          'Mean of Y', round(np.mean(self.Y), 4)], ['Residual standard error', round(np.sqrt(sigma_sq_hat), 4)],
         [
          'No. of Observations', n]], '\n'))
        print('\nRegression Coefficients:\n')
        print(tabulate(tabulate_list, headers=['Parameter', 'Estimate', 'Std Error', 't-value', 'P-value Pr(>|t|)']), '\n')
        print('\nANOVA Summary:\n')
        print(tabulate(anova_table, headers=['Source', 'Df', 'Sum Squares', 'Mean Squares', 'F', 'Pr(>F)']), '\n')
        if p > 1:
            vif_table = []
            vif_df = df[x]
            df_corr = vif_df.corr()
            vif_mat = np.linalg.inv(df_corr)
            self.vif = vif_mat.diagonal()
            for i in range(len(self.vif)):
                vif_table.append([x[i], self.vif[i]])

            print('\nVariance inflation factor (VIF)\n')
            print(tabulate(vif_table, headers=['Variable', 'VIF']), '\n')

    def ttsam(df='dataframe', xfac=None, res=None, evar=True, alpha=0.05):
        df = df.dropna()
        if xfac:
            if res is None:
                raise Exception('xfac or res variable is missing')
        levels = df[xfac].unique()
        levels.sort()
        if len(levels) != 2:
            raise Exception('there must be only two levels')
        a_val = df.loc[(df[xfac] == levels[0], res)].to_numpy()
        b_val = df.loc[(df[xfac] == levels[1], res)].to_numpy()
        a_count, b_count = len(a_val), len(b_val)
        count = [a_count, b_count]
        mean = [df.loc[(df[xfac] == levels[0], res)].mean(), df.loc[(df[xfac] == levels[1], res)].mean()]
        sem = [df.loc[(df[xfac] == levels[0], res)].sem(), df.loc[(df[xfac] == levels[1], res)].sem()]
        sd = [df.loc[(df[xfac] == levels[0], res)].std(), df.loc[(df[xfac] == levels[1], res)].std()]
        ci = (1 - alpha) * 100
        dfa = a_count - 1
        dfb = b_count - 1
        with np.errstate(invalid='ignore'):
            var_a = np.nan_to_num(np.var(a_val, ddof=1))
            var_b = np.nan_to_num(np.var(b_val, ddof=1))
        mean_diff = mean[0] - mean[1]
        varci_low = []
        varci_up = []
        tcritvar = [
         stats.t.ppf((1 + (1 - alpha)) / 2, dfa), stats.t.ppf((1 + (1 - alpha)) / 2, dfb)]
        for i in range(len(levels)):
            varci_low.append(mean[i] - tcritvar[i] * sem[i])
            varci_up.append(mean[i] + tcritvar[i] * sem[i])

        var_test = 'equal'
        w, pvalue = stats.levene(a_val, b_val)
        if pvalue < alpha:
            print('Warning: the two group variance are not equal. Rerun the test with evar=False')
        if evar is True:
            p_var = (dfa * var_a + dfb * var_b) / (dfa + dfb)
            se = np.sqrt(p_var * (1.0 / a_count + 1.0 / b_count))
            dfr = dfa + dfb
        else:
            if a_count == 1 or b_count == 1:
                raise Exception('Not enough observation for either levels. The observations should be > 1 for both levels')
            a_temp = var_a / a_count
            b_temp = var_b / b_count
            dfr = (a_temp + b_temp) ** 2 / (a_temp ** 2 / (a_count - 1) + b_temp ** 2 / (b_count - 1))
            se = np.sqrt(a_temp + b_temp)
            var_test = 'unequal'
        tval = np.divide(mean_diff, se)
        oneside_pval = stats.t.sf(np.abs(tval), dfr)
        twoside_pval = oneside_pval * 2
        tcritdiff = stats.t.ppf((1 + (1 - alpha)) / 2, dfr)
        diffci_low = mean_diff - tcritdiff * se
        diffci_up = mean_diff + tcritdiff * se
        print('\nTwo sample', levels, 't-test with', var_test, 'variance', '\n')
        print(tabulate([['Mean diff', mean_diff], ['t', tval], ['Std Error', se], ['df', dfr],
         [
          'P-value (one-tail)', oneside_pval], ['P-value (two-tail)', twoside_pval],
         [
          'Lower ' + str(ci) + '%', diffci_low], ['Upper ' + str(ci) + '%', diffci_up]]), '\n')
        print('Parameter estimates\n')
        print(tabulate([[levels[0], count[0], mean[0], sd[0], sem[0], varci_low[0], varci_up[0]],
         [levels[1], count[1],
          mean[1], sd[1], sem[1],
          varci_low[1], varci_up[1]]],
          headers=[
         'Level', 'Number', 'Mean', 'Std Dev', 'Std Error',
         'Lower ' + str(ci) + '%', 'Upper ' + str(ci) + '%']), '\n')
        fig = plt.figure()
        df.boxplot(column=res, by=xfac, grid=False)
        plt.ylabel(res)
        plt.savefig('ttsam_boxplot.png', format='png', bbox_inches='tight', dpi=300)

    def chisq(df='dataframe'):
        tabulate_list = []
        chi_ps, p_ps, dof_ps, expctd_ps = stats.chi2_contingency(df.to_dict('split')['data'])
        tabulate_list.append(['Pearson', dof_ps, chi_ps, p_ps])
        chi_ll, p_ll, dof_ll, expctd_ll = stats.chi2_contingency((df.to_dict('split')['data']), lambda_='log-likelihood')
        tabulate_list.append(['Log-likelihood', dof_ll, chi_ll, p_ll])
        mosaic_dict = dict()
        m = df.to_dict('split')
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                mosaic_dict[(m['index'][i], m['columns'][j])] = m['data'][i][j]

        print('\nChi-squared test\n')
        print(tabulate(tabulate_list, headers=['Test', 'Df', 'Chi-square', 'P-value']))
        print('\nExpected frequency counts\n')
        print(tabulate(expctd_ps, headers=(df.to_dict('split')['columns']), showindex='always'))
        labels = lambda k:         if mosaic_dict[k] != 0:
'' # Avoid dead code: ''
        mosaic(mosaic_dict, labelizer=labels)
        plt.savefig('mosaic.png', format='png', bbox_inches='tight', dpi=300)


class gff:

    def __init__(self):
        pass

    def gff_to_gtf(file='gff_file'):
        read_gff_file = open(file, 'r')
        out_gtf_file = open(Path(file).stem + '.gtf', 'w')
        gene_id = ''
        transcript_id = ''
        for line in read_gff_file:
            if not line.startswith('#'):
                line = re.split('\\s+', line.strip())
                if line[2] == 'gene':
                    attr = re.split(';', line[8])
                    gene_id = attr[0].split('=')[1]
                    gene_attr_gtf = 'gene_id "' + gene_id + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')
                elif line[2] == 'mRNA' or line[2] == 'transcript':
                    cds_i, exon_i, ftr_i, ttr_i = (1, 1, 1, 1)
                    attr = re.split(';', line[8])
                    transcript_id = attr[0].split('=')[1]
                    gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')
                elif line[2] == 'CDS':
                    attr = re.split(';', line[8])
                    transcript_id_temp = attr[1].split('=')[1]
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; cds_number "' + str(cds_i) + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                        cds_i += 1
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')
                elif line[2] == 'exon':
                    attr = re.split(';', line[8])
                    transcript_id_temp = attr[1].split('=')[1]
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; exon_number "' + str(exon_i) + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                        exon_i += 1
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')
                elif line[2] == 'five_prime_UTR':
                    attr = re.split(';', line[8])
                    transcript_id_temp = attr[1].split('=')[1]
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; five_prime_UTR_number "' + str(ftr_i) + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                        ftr_i += 1
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')
                elif line[2] == 'three_prime_UTR':
                    attr = re.split(';', line[8])
                    transcript_id_temp = attr[1].split('=')[1]
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; three_prime_UTR_number "' + str(ttr_i) + '"; gene_name "' + attr[1].split('=')[1] + '"; gene_source "' + line[1] + '";'
                        ttr_i += 1
                    out_gtf_file.write('\t'.join(line[0:8]) + '\t' + gene_attr_gtf + '\n')

        read_gff_file.close()
        out_gtf_file.close()


class get_data:

    def __init__(self, data=None):
        if data == 'mlr':
            self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/reg/test_reg.csv')
        else:
            if data == 'boston':
                self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/reg/boston.csv')
            else:
                if data == 'volcano':
                    self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/volcano/testvolcano.csv')
                else:
                    if data == 'ma':
                        self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/ma/test_dataset.csv')
                    else:
                        if data == 'hmap':
                            self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/heatmap/hm_cot.csv')
                        else:
                            if data == 'mhat':
                                self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/mhat/gwas_res_sim.csv')
                            else:
                                if data == 'bdot':
                                    self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/bardot/bardot.txt', sep='\t')
                                else:
                                    if data == 'corr':
                                        self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/corr/corr_dataset.csv')
                                    else:
                                        if data == 'slr':
                                            self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/reg/test_reg_uni.csv')
                                        else:
                                            if data == 'ttest':
                                                self.data = pd.read_csv('https://reneshbedre.github.io/assets/posts/ttest/genotype.csv')
                                            else:
                                                print('Error: Provide correct parameter for data\n')