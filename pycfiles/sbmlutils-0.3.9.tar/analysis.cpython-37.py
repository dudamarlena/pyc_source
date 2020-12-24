# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/analysis.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 3259 bytes
"""
Generic analysis and plots of DFBA simulations.
"""
import logging, warnings
from matplotlib import pyplot as plt

def set_matplotlib_parameters():
    """ Sets default plot parameters.

    :return:
    """
    plt.rcParams.update({'axes.labelsize':'large', 
     'axes.labelweight':'bold', 
     'axes.titlesize':'small', 
     'axes.titleweight':'bold', 
     'legend.fontsize':'small', 
     'xtick.labelsize':'large', 
     'ytick.labelsize':'large'})


class DFBAAnalysis(object):
    __doc__ = ' Plot and analysis functions for given results. '

    def __init__(self, df, ode_model):
        """ Constructor.

        :param df: Solution DataFrame
        :param ode_model: flattened roadrunner ode model
        """
        self.df = df
        self.rr_comp = ode_model

    def save_csv(self, filepath):
        """ Save results to csv. """
        if filepath is None:
            raise ValueError('filepath required')
        self.df.to_csv(filepath, sep='\t', index=False)

    def plot_species(self, filepath, filter=None, **kwargs):
        """ Plot species.

        :param filepath: filepath to save figure, if None plot is shown
        :return:
        :rtype:
        """
        species_ids = ['[{}]'.format(s) for s in self.rr_comp.model.getFloatingSpeciesIds()] + ['[{}]'.format(s) for s in self.rr_comp.model.getBoundarySpeciesIds()]
        filtered_sids = []
        for sid in species_ids:
            if not sid.startswith('[fba__'):
                if sid.startswith('[update__'):
                    continue
                else:
                    filtered_sids.append(sid)

        (self.plot_ids)(ids=filtered_sids, ylabel='species', title='DFBA species timecourse', filepath=filepath, **kwargs)

    def plot_reactions(self, filepath, filter=None, **kwargs):
        """ Plot species.

        :param filepath: filepath to save figure, if None plot is shown
        :return:
        :rtype:
        """
        reaction_ids = self.rr_comp.model.getReactionIds()
        (self.plot_ids)(ids=reaction_ids, ylabel='reactions', title='DFBA reaction timecourse', filepath=filepath, 
         filter=None, **kwargs)

    def plot_ids(self, ids, filepath=None, ylabel=None, title=None, filter=None, **kwargs):
        """ Plot given ids against time

        :param filepath:
        :param ids: subset of ids to plot
        :param title:
        :param ylabel:
        :return:
        """

        def filter_true(oid):
            return True

        if filter is None:
            filter = filter_true
        else:
            fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
            x_time = self.df['time']
            for oid in ids:
                if filter(oid):
                    (ax1.plot)(x_time, self.df[oid], label=oid, **kwargs)

            ax1.set_xlabel('time')
            if ylabel:
                ax1.set_ylabel(ylabel)
            if title:
                ax1.set_title(title)
            ax1.legend()
            ax1.set_xlim(min(x_time), max(x_time) * 1.5)
            if filepath:
                fig.savefig(filepath, bbox_inches='tight')
                logging.info('plot_ids: {}'.format(filepath))
            else:
                plt.show()