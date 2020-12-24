# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\fatihshen\Documents\MagicStatDev\MagicStat\algorithms\correlation.py
# Compiled at: 2018-12-29 08:45:40
# Size of source mod 2**32: 8469 bytes
import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import kendalltau
import math
from statistics import mean, stdev
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource

class Correlation:
    p_values = None
    c_values_for_export = None
    js_resources = None
    css_resources = None
    SIGNIFICANCE_THRESHOLD = 0.05
    correlation_exists = False
    corr_matrix = None
    cohensd_df = None
    mean_df_dic = None
    stdev_df_dic = None
    interpretation = ''
    interpretation_export = None
    explr = None
    error = None
    error_exist = False
    corr_type = None
    corr_type_label = None
    corr_type_value_label = None

    def __init__(self, explr, corr_type):
        self.explr = explr
        self.corr_type = corr_type
        self.correlation_type_labels(corr_type)
        if len(self.explr.non_cat_vars) < 2:
            self.error = 'You cannot apply the Correlation model because the dataset must include at least two numeric variables!'
            self.error_exist = True

    def data_preprocess(self, selected_vars, _df):
        df = _df
        try:
            selected_vars = selected_vars.split(',')
            allUserSelectedVars = [] + selected_vars
            if len(allUserSelectedVars) < 2:
                error = 'Please select at least two variables!'
                raise Exception(error)
            df = df[allUserSelectedVars]
            return df
        except Exception as err:
            try:
                error = str(err)
                raise Exception(error)
            finally:
                err = None
                del err

    def apply(self, sel_vars):
        result = None
        try:
            result = self.correlation(sel_vars)
        except Exception as err:
            try:
                error = 'Something went wrong while applying a correlation model: ' + str(err)
                raise Exception(error)
            finally:
                err = None
                del err

        return result

    def correlation(self, sel_vars):
        error_exist = False
        basic_stats = ''
        try:
            df = self.data_preprocess(sel_vars, self.explr.my_df)
            self.p_values = self.calculate_pvalues(df)
            p_values_dic = self.p_values.to_dict()
            variables = list(self.p_values.columns.unique())
            corr = df.corr(method=(self.corr_type))
            self.c_values_for_export = corr
            corr_dic = corr.to_dict()
            self.corr_matrix = corr.values
            self.mean_df_dic = {col:mean(df[col]) for col in df.columns}
            self.stdev_df_dic = {col:stdev(df[col]) for col in df.columns}
            corr_heatmap = self.get_corr_matrix_figure(df)
            corr_pairs = self.get_correlation_pairs(df)
            fig_list = {}
            fig_list['corr_fig_heat_map'] = corr_heatmap
            bokeh_script, bokeh_div = components(fig_list)
            dof = len(self.explr.my_df[sel_vars.split(',')[0]]) - 2
            result = {'js_resources':self.js_resources, 
             'css_resources':self.css_resources,  'corr_pairs':corr_pairs,  'basic_stats':basic_stats, 
             'dof':dof,  'interpretation':self.interpretation,  'corr_dic':corr_dic,  'corr':corr, 
             'bokeh_script':bokeh_script,  'bokeh_div':bokeh_div,  'p_values':self.p_values,  'p_values_dic':p_values_dic, 
             'variables':variables,  'correlation_exists':self.correlation_exists,  'corr_type':self.corr_type, 
             'correlation_type_label':self.corr_type_label,  'internal_error':'', 
             'error_exist':error_exist}
        except Exception as err:
            try:
                error = 'Error: ' + str(err)
                error_exist = True
                result = {'internal_error':error,  'error_exist':error_exist}
            finally:
                err = None
                del err

        return result

    def get_corr_matrix_figure(self, df):
        symbols = df.columns
        N = len(symbols)
        factors = list(symbols)
        x_list = []
        y_list = []
        corr_list = []
        p_value_list = []
        colors = []
        dfcols = pd.DataFrame(columns=(df.columns))
        self.cohensd_df = dfcols.transpose().join(dfcols, how='outer')
        for i in range(N):
            for j in range(N):
                x_list.append(symbols[j])
                y_list.append(symbols[i])
                cor = self.corr_matrix[(i, j)]
                corr_list.append(cor)
                p_value_list.append(self.p_values[symbols[i]][symbols[j]])
                rgb = (int(abs(cor) * 255), 0, int((1 - abs(cor)) * 255))
                colors.append('#%02x%02x%02x' % rgb)

        source = ColumnDataSource(data=dict(x=x_list,
          y=y_list,
          corr_value=corr_list,
          p_value=p_value_list,
          color=colors))
        hover = HoverTool(tooltips=[
         (
          'correlation value (' + self.corr_type_value_label + ')', '@corr_value'),
         ('p value', '@p_value')])
        p = figure(x_range=factors, y_range=(list(reversed(factors))), title='Correlation Heatmap', tools=[hover], toolbar_location='below', x_axis_location='above')
        p.rect(x='x', y='y', color='color', source=source, width=1, height=1)
        p.xaxis.major_label_orientation = math.pi / 2
        return p

    def get_correlation_pairs(self, df):
        cor_pairs = []
        cor_pairs2 = []
        symbols = list(df.columns)
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                pair_symbols1 = str(symbols[i]) + '-' + str(symbols[j])
                pair_symbols2 = str(symbols[j]) + '-' + str(symbols[i])
                if i != j and pair_symbols1 not in cor_pairs and pair_symbols2 not in cor_pairs:
                    cor_pairs.append(pair_symbols1)
                    cor_pairs.append(pair_symbols2)
                    cor_pairs2.append(pair_symbols1)

        return cor_pairs2

    def get_corr_scatter_plot(self, df, var1, var2):
        error_exist = False
        try:
            x_list = []
            y_list = []
            corr_values = []
            var1_list = list(df[var1])
            var2_list = list(df[var2])
            for i in range(len(var1_list)):
                x_list.append(var1_list[i])
                y_list.append(var2_list[i])
                corr_values.append((var1_list[i], var2_list[i]))

            source = ColumnDataSource(data=dict(x=x_list,
              y=y_list,
              _value=corr_values))
            hover = HoverTool(tooltips=[
             (
              var1 + ', ' + var2, '@_value')])
            p = figure(title='Pearson Correlation Scatter Plot', tools=[hover])
            p.circle('x', 'y', size=5, source=source)
            p.xaxis.axis_label = var1
            p.yaxis.axis_label = var2
            fig_list = {}
            fig_list['corr_fig_scatter_plot'] = p
            bokeh_script, bokeh_div = components(fig_list)
            result = {'js_resources':self.js_resources, 
             'css_resources':self.css_resources,  'bokeh_script':bokeh_script, 
             'bokeh_div':bokeh_div,  'corr_type':self.corr_type,  'internal_error':'', 
             'error_exist':error_exist}
        except Exception as err:
            try:
                error = 'Error: ' + str(err)
                error_exist = True
                result = {'internal_error':error,  'error_exist':error_exist}
            finally:
                err = None
                del err

        return result

    def calculate_pvalues(self, df):
        df = df.dropna()._get_numeric_data()
        dfcols = pd.DataFrame(columns=(df.columns))
        pvalues = dfcols.transpose().join(dfcols, how='outer')
        if self.corr_type == 'pearson':
            for r in df.columns:
                for c in df.columns:
                    pvalues[r][c] = pearsonr(df[r], df[c])[1]

        else:
            if self.corr_type == 'spearman':
                for r in df.columns:
                    for c in df.columns:
                        pvalues[r][c] = spearmanr(df[r], df[c])[1]

            else:
                if self.corr_type == 'kendall':
                    for r in df.columns:
                        for c in df.columns:
                            pvalues[r][c] = kendalltau(df[r], df[c])[1]

        return pvalues

    def correlation_type_labels(self, correlation_type):
        if correlation_type == 'pearson':
            self.corr_type_label = 'Pearson Correlation (r)'
            self.corr_type_value_label = 'r'
        else:
            if correlation_type == 'spearman':
                self.corr_type_label = "Spearman's Correlation (rho)"
                self.corr_type_value_label = 'rho'
            else:
                if correlation_type == 'kendall':
                    self.corr_type_label = 'Kendall Correlation (tau)'
                    self.corr_type_value_label = 'tau'