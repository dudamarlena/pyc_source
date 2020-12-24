# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\fatihshen\Documents\MagicStatDev\MagicStat\algorithms\explore.py
# Compiled at: 2019-01-05 18:49:41
# Size of source mod 2**32: 12526 bytes
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import HoverTool, ColumnDataSource
from numpy import histogram

class Explore:
    my_df = None
    MAX_NUMBER_OF_VARIABLES = 500
    MAX_NUMBER_OF_DATA_POINTS = 1000000
    all_variables = None
    non_cat_vars = None
    cat_vars = None
    vars_with_binary_values = None
    possible_cat_vars = None
    CAT_VAR_NUMBER_CRITERIA = 11
    PAGINATION_INTERVAL = 10
    pagination_tuple = None
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    b_div = None
    script = None
    key_index_dic = None
    data_variables = None
    first_five_rows = None

    def __init__(self, my_df):
        self.my_df = my_df

    def explore_data(self, upload_result):
        global rows
        error = ''
        result = {}
        summary_data = None
        try:
            self.data_variables = list(self.my_df.columns)
            if len(self.data_variables) > self.MAX_NUMBER_OF_VARIABLES:
                error = 'You have too many variables! Your dataset cannot have more than ' + str(self.MAX_NUMBER_OF_VARIABLES) + ' variables!'
                raise Exception(error)
            else:
                if len(self.my_df.index) > self.MAX_NUMBER_OF_DATA_POINTS:
                    error = 'Your dataset is huge. You cannot have more than ' + str(self.MAX_NUMBER_OF_DATA_POINTS) + ' data points in your dataset!'
                    raise Exception(error)
                headers2 = ''
                for data_var in self.data_variables:
                    headers2 = headers2 + data_var + ', '

                headers2 = headers2[:len(headers2) - 2]
                self.summary_data = self.my_df.describe()
                self.summary_data = self.drop_id_variable(self.summary_data)
                self.summary_data = self.summary_data.T
                self.summary_data[['count']] = self.summary_data[['count']].astype(int)
                self.summary_data[['mean', 'std', 'min', '25%', '50%', '75%', 'max']] = self.summary_data[['mean', 'std', 'min', '25%', '50%', '75%', 'max']].applymap('{0:.2f}'.format)
                self.summary_data.rename(columns={'std': 'sd'}, inplace=True)
                self.first_five_rows = self.my_df.head()
                self.first_five_rows_dic = self.first_five_rows.T.to_dict()
                self.first_five_rows = self.first_five_rows.rename(index={i - 1:'' for i in range(1, len(self.first_five_rows.index) + 1)})
                possible_cat_vars = self.check_possible_cat_vars(self.non_cat_vars)
                if possible_cat_vars != '':
                    possible_cat_vars = '<b>Note</b>: ' + possible_cat_vars
                cat_headers = ''
                for header in self.cat_vars:
                    cat_headers = cat_headers + header + ', '

                cat_headers = cat_headers[:len(cat_headers) - 2]
                if cat_headers == '':
                    cat_headers = 'No categorical variables found.'
                non_cat_headers = ''
                for header in self.non_cat_vars:
                    non_cat_headers = non_cat_headers + header + ', '

                non_cat_headers = non_cat_headers[:len(non_cat_headers) - 2]
                if non_cat_headers == '':
                    non_cat_headers = 'No numeric variables found'
                rows = self.my_df.index
                self.pagination_tuple = divmod(len(self.data_variables), self.PAGINATION_INTERVAL)
                pagination_remainder = int(self.pagination_tuple[1])
                if pagination_remainder > 0:
                    pagination_range = range(int(self.pagination_tuple[0]) + 1)
                else:
                    pagination_range = range(int(self.pagination_tuple[0]))
            pagination_dic = {i:str(i * self.PAGINATION_INTERVAL + 1) + '-' + str((i + 1) * self.PAGINATION_INTERVAL) for i in pagination_range}
            result = {'fileData':self.my_df, 
             'headers':self.data_variables,  'headers2':headers2,  'rows':rows,  'upload_result':upload_result, 
             'summary_data':self.summary_data,  'cat_data_headers':cat_headers, 
             'non_cat_data_headers':non_cat_headers,  'cat_vars':self.cat_vars,  'non_cat_vars':self.non_cat_vars, 
             'possible_cat_vars':possible_cat_vars, 
             'first_five_rows':self.first_five_rows,  'first_five_rows_dic':self.first_five_rows_dic,  'pagination_dic':pagination_dic, 
             'internal_error':''}
        except Exception as err:
            try:
                error = str(err)
                raise Exception(error)
            finally:
                err = None
                del err

        return result

    def explore_figures(self, pag_index):
        fig_list = {}
        result = None
        try:
            pagination_start_index = pag_index * self.PAGINATION_INTERVAL + 1
            pagination_end_index = (pag_index + 1) * self.PAGINATION_INTERVAL
            df = self.my_df.copy()
            df_figures = self.drop_id_variable(df)
            df_figures_vars = list(df_figures.columns)
            for data_var_index in range(len(df_figures_vars)):
                if data_var_index + 1 >= pagination_start_index:
                    if not data_var_index + 1 <= pagination_end_index or df_figures_vars[data_var_index] in self.cat_vars or df_figures_vars[data_var_index] in self.possible_cat_vars:
                        plot = self.draw_histogram_for_categorical(df_figures_vars[data_var_index])
                    else:
                        plot = self.draw_histogram_for_non_categorical(df_figures_vars[data_var_index])
                    if plot is not None:
                        fig_list[df_figures_vars[data_var_index]] = plot

            self.script, self.b_div = components(fig_list)
            result = {'bokeh_script':self.script, 
             'bokeh_div':self.b_div,  'js_resources':self.js_resources, 
             'css_resources':self.css_resources}
        except Exception as err:
            try:
                error = 'Internal error: ' + str(err)
                result = {'internal_error':error,  'error_exist':True}
            finally:
                err = None
                del err

        return result

    def drop_id_variable(self, _df):
        for col in list(_df.columns):
            counts = self.value_counts_of_series(self.my_df[col])
            counts = counts.to_dict()
            var_list = list(self.my_df[col])
            total_var_length = len(var_list)
            possible_list = [i for i in range(len(var_list))]
            possible_list2 = [i + 1 for i in range(len(var_list))]
            if not total_var_length == len(counts) or var_list == possible_list or var_list == possible_list2:
                _df.drop(col, axis=1, inplace=True)

        return _df

    def draw_histogram_for_categorical(self, column_name):
        counts = self.value_counts_of_series(self.my_df[column_name])
        var_df = counts.to_frame()
        counts = counts.to_dict()
        counts = {self.get_category_label_for_figure(str(k)):v for k, v in counts.items()}
        x_values = []
        y_values = []
        for key in counts:
            x_values.append(key)
            y_values.append(counts[key])

        source = ColumnDataSource(data=dict(x=x_values,
          y=y_values))
        hover = HoverTool(tooltips=[
         (
          column_name, '@x'),
         ('frequency value', '@y')])
        p = figure(x_range=x_values, plot_height=350, title='Frequency', tools=[
         hover])
        p.vbar(x='x', top='y', width=0.5, source=source, color='#696969', line_color='black')
        p.y_range.start = 0
        p.xgrid.grid_line_color = None
        p.xaxis.axis_label = column_name
        p.xaxis.major_label_orientation = 1.2
        p.outline_line_color = None
        return p

    def draw_histogram_for_non_categorical(self, column_name):
        data_values = self.my_df[column_name].tolist()
        hist, edges = histogram(data_values, density=False, bins='auto')
        x_range = self.x_range_values(list(edges))
        source = ColumnDataSource(data=dict(top=hist,
          left=(edges[:-1]),
          right=(edges[1:]),
          x_range=x_range))
        hover = HoverTool(tooltips=[
         ('frequency value', '@top'),
         ('x_range', '@x_range')])
        p = figure(plot_height=350, title='Frequency', tools=[hover])
        p.quad(top='top', bottom=0, left='left', right='right', color='#696969', line_color='black', source=source)
        return p

    def x_range_values(self, edges_list):
        x_range_vals = []
        for i in range(len(edges_list) - 1):
            if i == 0:
                x = '['
            else:
                x = '('
            x = x + '{:.2f}'.format(edges_list[i]) + ', ' + '{:.2f}'.format(edges_list[(i + 1)])
            x = x + ']'
            x_range_vals.append(x)

        return x_range_vals

    def value_counts_of_series(self, mySeries):
        return mySeries.value_counts().sort_index()

    def check_possible_cat_vars(self, non_cat_vars):
        import numpy as np
        self.possible_cat_vars = []
        is_integer_var = False
        possible_cat_var_str = ''
        for var in non_cat_vars:
            unique_vals = set(self.my_df[var])
            for val in unique_vals:
                try:
                    x = isinstance(val, (int, np.integer))
                    is_integer_var = True
                except:
                    is_integer_var = False
                    break

            if is_integer_var and len(unique_vals) <= self.CAT_VAR_NUMBER_CRITERIA and var not in self.cat_vars:
                self.possible_cat_vars.append(var)

        for i in range(len(self.possible_cat_vars)):
            if not len(self.possible_cat_vars) == 1:
                if i == 0:
                    if len(self.possible_cat_vars) == 2:
                        possible_cat_var_str += self.possible_cat_vars[i]
                if i == len(self.possible_cat_vars) - 1:
                    if len(self.possible_cat_vars) > 1:
                        possible_cat_var_str += ' and ' + self.possible_cat_vars[i]
                possible_cat_var_str += self.possible_cat_vars[i] + ', '

        if len(self.possible_cat_vars) == 1 and possible_cat_var_str != '':
            possible_cat_var_str += ' seems to be a categorical variable. While applying your statistical model(s), make sure to count this variable as categorical if that is the case.'
        else:
            if len(self.possible_cat_vars) > 1:
                if possible_cat_var_str != '':
                    possible_cat_var_str += ' seem to be categorical variables. While applying your statistical model(s), make sure to count the related variable(s) as categorical if that is the case.'
            return possible_cat_var_str

    def get_category_label_for_figure(self, str_label):
        if len(str_label) > 10:
            return str_label[0:10] + '...'
        return str_label