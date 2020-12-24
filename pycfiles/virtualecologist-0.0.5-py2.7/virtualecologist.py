# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/virtualecologist/virtualecologist.py
# Compiled at: 2016-01-27 23:28:40
"""
VirtualEcologist

This module evaluates plant survey data collected in plots along a transect.
First the error rate that is expected between two people is evaluated for
different lifeforms (e.g. grass, shrubs, trees). The model is then used to
examine a large dataset collected by one person to calculate the minimum
detectable difference as plots are reduced from each transect.

--- You need two datasets ---
1) Pilot data: A csv file with NO header.
    3 columns:
    observer 1 estimate (e.g. 54),
    observer 2 estimate (e.g. 60),
    functional group name (e.g. grass, tree)

2) Full dataset: A csv file collected by one observer WITH header.
    5 columns:
    Site name (header title: site)
    Functional group name (header title: lifeform) <= entries same as file1
    Transect identity (header title: transect)
    Plot identity (header title: plot)
    Percentage cover estimate (header title: cover) <= units should match file1

--- The virtual ecologist ---
File one is used to train the virtual ecologist. If no training data is
available you can skip the initial stage and accept an error rate between
participants of 10% (for one standard deviation).

--- The functional groups ---
If you have pilot data for one functional group, you can assign the same error
rate for all other functional groups in the large dataset. This might not
be sensible (i.e. estimating grass cover may be more accurate than canopy
cover of trees). If you have pilot data for several functional groups but not
all of them are represented in the full dataset, the ones without data are
assigned the average value of the error rate of all other groups.

Created on Thu Mar 19 12:30:56 2015
Last updated Sun Jan 17 2016
Author: Ray Blick
"""
import csv, pandas as pd, numpy as np, math
from scipy import stats
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import re

class VirtualEcologist():
    """
    A class of methods to reduce the number of plots along transect lines.
    """

    def __init__(self, pilot_data, full_data):
        self.pilot_data = pilot_data
        self.full_data = full_data
        self.mse_output = {}
        self.dataset = {}
        self.fg_dict = {}
        self.ttest_results = []
        self.plot_data = []
        self.trigger_points = []
        self.trigger = None
        self.site = None
        self.lifeform = None
        return

    def print_table(self, data_dictionary):
        """
        Prints a data_dictionary in table form.
        """
        iteration = 0
        t = PrettyTable(['ID', 'Lifeform', 'MSE', 'Pilot data'])
        for group in data_dictionary:
            if group in self.fg_dict:
                pilot_data = 'yes'
            else:
                pilot_data = 'no'
            iteration += 1
            t.add_row([iteration, group, round(data_dictionary[group], 3),
             pilot_data])

        print t.get_string(sortby='ID')

    def train_observer(self):
        """
        Returns a dictionary containing Mean Square Error of estimates.
        Input is a csv with 3 columns: observer 1 estimates, observer 2
        estimates and functional group names.

        # Test normal case
        >>> train_observer("ve_testdata.csv")
        {'grass': 13.090909090909092, 'shrubs': 27.2, 'trees': 13.153846153846153}

        # Test no arguments
        >>> train_observer()
        Traceback (most recent call last):
        ...
        TypeError: train_observer() takes exactly 1 argument (0 given)

        # Test numeric argument
        >>> train_observer(23)
        Traceback (most recent call last):
        ...
        TypeError: coercing to Unicode: need string or buffer, int found
        """
        with open(self.pilot_data, 'r') as (f):
            file_reader = csv.reader(f)
            for row in file_reader:
                est_one = row[0]
                est_two = row[1]
                fg_key = row[2]
                if fg_key not in self.fg_dict:
                    self.fg_dict[fg_key] = 1
                else:
                    self.fg_dict[fg_key] += 1
                square_difference = (float(est_one) - float(est_two)) ** 2
                self.mse_output[fg_key] = self.mse_output.get(fg_key, 0) + square_difference

            for entry in self.mse_output:
                if entry in self.fg_dict:
                    self.mse_output[entry] = self.mse_output.get(entry, 0) / self.fg_dict[entry]

            return self.mse_output

    def match_full_dataset(self):
        """
        Updates the dictionary of Mean Square Error rates. If no pilot data
        is used, each lifeform is assigned an error of 10%. For lifeforms not
        in pilot data, each new lifeform is assigned a mean value based
        on the pilot data.
        """
        count_dict = dict()
        list_of_groups = []
        self.dataset = pd.read_csv(self.full_data)
        for row in self.dataset['lifeform']:
            if row not in count_dict:
                count_dict[row] = 1
            else:
                count_dict[row] += 1

        number_of_groups = len(count_dict)
        for entry in count_dict:
            if entry not in self.mse_output:
                list_of_groups.append(entry)

        if list_of_groups == []:
            print 'All functional groups have been trained.'
        else:
            dictionary_value = 0
            dictionary_iteration = 0
            for key in self.mse_output:
                dictionary_value += self.mse_output[key]
                dictionary_iteration += 1

            if len(list_of_groups) == len(count_dict):
                for item in list_of_groups:
                    PseudoObserver.output[item] = 100

            else:
                for item in list_of_groups:
                    if item not in self.mse_output:
                        self.mse_output[item] = dictionary_value / dictionary_iteration

    def create_barchart(self, lifeforms=None):
        """
        Returns a bar chart for lifeforms across all sites.
        """
        sites = []
        if lifeforms != None:
            dropped_groups = lifeforms.split(',')
        else:
            dropped_groups = []
        sites_by_group = dict(list(self.dataset.groupby(['site'])))
        for location in sites_by_group:
            site_dictionary = {}
            for row in sites_by_group[location]['lifeform']:
                if row not in site_dictionary:
                    site_dictionary[row] = 1
                else:
                    site_dictionary[row] += 1

            for i, j in site_dictionary.items():
                put_data_together = (
                 location, i, j)
                sites.append(put_data_together)

        data = pd.DataFrame(sites, columns=list(['site', 'lifeform', 'count']))
        data = data[(~data.lifeform.isin(dropped_groups))]
        df_data = data.groupby(['site', 'lifeform']).aggregate(sum).unstack()
        df_data.fillna(0, inplace=True)
        percentiles = df_data.apply(lambda c: c / c.sum() * 100, axis=1)
        my_colors = [
         'DarkKhaki', 'Khaki', 'PaleGoldenrod',
         'LightGoldenrodYellow', 'white', 'grey', 'darkgrey']
        ax = percentiles.plot(kind='bar', stacked=True, color=my_colors, ylim=(0, 100))
        h, l = ax.get_legend_handles_labels()
        labels = []
        for i in l:
            i = re.sub('\\W', '', i.split(',')[1])
            labels.append(i)

        ax.legend(h, labels, loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 8})
        ax.set_position([0.1, 0.6, 0.6, 0.35])
        ax.grid('off')
        fig = ax.get_figure()
        fig.savefig('lifeforms_barchart.png', format='png', dpi=1000)
        plt.close(fig)
        return

    def create_pdf_figure(self):
        """
        Prints a table containing the group name and sigma that
        will define the VirtualEcologist model. Returns nothing if
        match_full_dataset() has not been instantiated.
        """
        for group in self.mse_output:
            x = np.random.normal(50, math.sqrt(self.mse_output[group]), 1000)
            count, bins, ignored = plt.hist(x, 30, range=[0, 100], normed=True, color='White')
            plt.plot(bins, 1 / (math.sqrt(self.mse_output[group]) * np.sqrt(2 * np.pi)) * np.exp(-(bins - 50) ** 2 / (2 * math.sqrt(self.mse_output[group]) ** 2)), linewidth=2, color='Black')
            plt.text(5, 0.09, group + ' [' + str(round(np.sqrt(self.mse_output[group]), 2)) + ']', size=16)
            plt.ylim((0, 0.1))
            plt.xlim((0, 100))
            plt.ylabel('Probability of cover estimate', size=14)
            plt.xlabel('Percentage cover estimate for a single species (0-100)', size=14)
            plt.plot([50, 50], [0, 0.1], 'Grey', lw=2, linestyle='--')
            name = group
            name = re.sub('/', '_', name)
            plt.savefig(name + '.png', format='png', dpi=1000)
            plt.clf()

    def calc_mmd(self, site, lifeform, trigger=10, iterations=100, min_plot=4, figure=True):
        """
        Returns number of plots to reduce per transect. Takes two
        arguments; site name (e.g. shrubswamp) and lifeform (e.g. shrub).
        These arguments must be in the dataset that is being used.

        Three default values are added:
            1) a 10% trigger value
            2) 100 iterations
            3) minimum plot reduction of 4 per transect
            4) save figure to local directory

        These can be altered by the user.
        E.g.
        # increase trigger level
        test.calc_mmd('forestA', 'tree', trigger = 20)

        # turn off plotting
        test.calc_mmd('forestB', 'shrub', figure = False)
        """
        counter = 0
        self.trigger = trigger
        self.site = site
        self.lifeform = lifeform
        for i in range(iterations):
            counter += 1
            ve_estimates = []
            for row in np.array(self.dataset):
                if row[2] in self.mse_output:
                    observer_estimate = row[5]
                    sd = math.sqrt(self.mse_output[row[2]])
                    virtual_ecologist = np.random.normal(observer_estimate, sd)
                    if virtual_ecologist >= 100:
                        virtual_ecologist = 100
                    elif virtual_ecologist <= 0:
                        virtual_ecologist = 0
                    ve_estimates.append(virtual_ecologist)

            self.dataset['virtual_ecologist'] = ve_estimates
            temp_data_holder = self.dataset[self.dataset['site'].str.contains(self.site)]
            find_longest_transect = len(temp_data_holder['plot'].unique())
            subset_data = dict(list(temp_data_holder.groupby(['site', 'transect'])))
            plot_iterator = 0
            for i in range(find_longest_transect):
                plotnames_list = []
                for subset in subset_data:
                    transect_length = len(subset_data[subset]['plot'].unique()) - plot_iterator
                    if transect_length <= min_plot:
                        reduce_transect_length = min_plot
                    else:
                        reduce_transect_length = transect_length
                    sorted_data = subset_data[subset]['plot']
                    sorted_data = sorted(sorted_data.unique())
                    sorted_data = sorted_data[:reduce_transect_length]
                    for plot_name in sorted_data:
                        if plot_name not in plotnames_list:
                            plotnames_list.append(plot_name)

                plot_iterator += 1
                reduced_transect = temp_data_holder[temp_data_holder['plot'].isin(plotnames_list)]
                lifeform_data = reduced_transect[reduced_transect['lifeform'].str.contains(self.lifeform)]
                lifeform_data = dict(list(lifeform_data.groupby(['site', 'transect', 'lifeform'])))
                group_data_array = []
                for group in lifeform_data:
                    real_observer = lifeform_data[group]['cover'].sum() / len(lifeform_data[group]['cover'])
                    virtual_observer = lifeform_data[group]['virtual_ecologist'].sum() / len(lifeform_data[group]['virtual_ecologist'])
                    plot_occupancy = len(lifeform_data[group]['plot'].unique())
                    output = (
                     group[0], group[1], group[2], real_observer,
                     virtual_observer, plot_occupancy)
                    group_data_array.append(output)

                result = pd.DataFrame(group_data_array, columns=list(['site',
                 'transect', 'lifeform', 'cover', 'virtual', 'occupancy']))
                result.sort(['site', 'transect', 'lifeform'], ascending=True, inplace=True)
                mmd_subset = dict(list(result.groupby(['site', 'lifeform'])))
                for subset in mmd_subset:
                    A = mmd_subset[subset]['cover']
                    B = mmd_subset[subset]['virtual']
                    number_of_transects = len(mmd_subset[subset]['cover'])
                    calculated_difference = [ a - b for a, b in zip(A, B) ]
                    stand_dev = np.array(calculated_difference).std()
                    min_detect_change = np.sqrt(4 * stand_dev ** 2 * 3.24 / number_of_transects)
                    plot_occupancy = mmd_subset[subset]['occupancy'].sum()
                    if min_detect_change >= int(self.trigger):
                        mdc_trigger_point = (
                         counter, plot_iterator, min_detect_change,
                         plot_occupancy, number_of_transects)
                        self.trigger_points.append(mdc_trigger_point)
                    mdc_data = (
                     plot_iterator, subset[0], subset[1], min_detect_change,
                     number_of_transects, plot_occupancy)
                    self.plot_data.append(mdc_data)
                    test = stats.ttest_rel(mmd_subset[subset]['cover'], mmd_subset[subset]['virtual'])
                    data_str = (plot_iterator, subset[0], subset[1], list(test)[0],
                     round(list(test)[1], 3), number_of_transects)
                    self.ttest_results.append(data_str)

        if figure == True:
            self._create_mdd_figure()

    def _create_mdd_figure(self):
        """
        Saves a figure in png format for site and lifeform.
        """
        mdc_dataframe = pd.DataFrame(self.plot_data, columns=list(['dropped_plots',
         'site', 'lifeform', 'mdc', 'n', 'occupancy']))
        if self.trigger_points != []:
            trigger_dataframe = pd.DataFrame(self.trigger_points, columns=list(['loop',
             'dropped_plots', 'mdc', 'occupancy', 'n']))
            mean_trigger_point = np.mean(list(trigger_dataframe.groupby('loop')['dropped_plots'].min()))
            mean_occupancy = np.mean(list(trigger_dataframe.groupby('loop')['occupancy'].max()))
            print ('Max number of plots you can drop (if each transect still has 4 plots) is: {0}').format(round(mean_trigger_point, 2))
            print ('The trigger value was exceeded when the minimum number of plots per transect was less than: {0}').format(round(mean_occupancy, 2))
        else:
            mean_trigger_point = 0
        mdc_x = list(mdc_dataframe['dropped_plots'].unique())
        mdc_n_output = mdc_dataframe['n'][0:max(mdc_x)]
        mdc_po_output = mdc_dataframe['occupancy'][0:max(mdc_x)]
        mdc_mean_output = list(mdc_dataframe.groupby('dropped_plots')['mdc'].mean())
        mdc_sd_output = list(mdc_dataframe.groupby('dropped_plots')['mdc'].std())
        mdc_se_output = mdc_sd_output / np.sqrt(mdc_n_output) * 1.96
        if max(mdc_po_output) + 10 >= max(mdc_mean_output) + max(mdc_se_output):
            set_y_axis_limits = max(mdc_po_output) + 10
        else:
            set_y_axis_limits = max(mdc_mean_output) + max(mdc_se_output) + 10
        plt.errorbar(mdc_x, mdc_mean_output, yerr=mdc_se_output, color='black', lw=1.5, linestyle='-', label='MDD - 95% CI')
        plt.plot([0, max(mdc_x)], [int(self.trigger), int(self.trigger)], color='grey', lw=2, linestyle=':')
        plt.ylim(0, set_y_axis_limits)
        plt.xlim(0, max(mdc_x) + 1)
        mdc_n_transects = mdc_dataframe['n'][0]
        plt.title(self.site + ' [' + self.lifeform + ' | ' + str(mdc_n_transects) + ' transects]')
        plt.plot(mdc_x, mdc_po_output, label='plot occupancy', color='grey', lw=1, linestyle='--')
        plt.plot([mean_trigger_point, mean_trigger_point], [0, set_y_axis_limits], color='grey', lw=1, linestyle='-')
        if mean_trigger_point != 0:
            plt.text(mean_trigger_point + 0.1, max(mdc_mean_output) + max(mdc_se_output), round(mean_trigger_point, 2), size=16)
        plt.ylabel('Minimum detectable difference (%)', size=14)
        plt.xlabel('Number of plots dropped from each transect', size=14)
        plt.savefig('MDD_' + self.site + '_' + self.lifeform + '.png', format='png', dpi=1000)


if __name__ == '__main__':
    test = VirtualEcologist('/home/ray/python/scripts/VE/data/TrainingData.csv', '/home/ray/python/scripts/VE/data/NP2014_vegdata.csv')
    test.train_observer()
    test.match_full_dataset()
    test.print_table(test.mse_output)
    test.calc_mmd(site='West Carne', lifeform='ATw')