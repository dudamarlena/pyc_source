# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_posterior_predictive_checks.py
# Compiled at: 2019-07-16 04:25:49
import os
from scipy import stats
import numpy as np, matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table, Column
import sys, dependencies.WeightedKDE as WeightedKDE
from dependencies.walker_random_sampling import WalkerRandomSampling
from beagle_utils import prepare_data_saving, prepare_plot_saving, BeagleDirectories, set_plot_ticks
jy = 1e-23

class PosteriorPredictiveChecks(object):

    def chi_square(self, y, E_y, sig_y):
        """ 
        An example of a "discrepancy function", the chi-square

        Parameters
        ----------
        y : float
            "Observed" value

        E_y : float
            "Expected" (theoretical) value

        sig_y: float
            Standard deviation of the "observed" values

        Returns 
        ------
        float    

        Notes
        -----
        Negative values of sig_y produce a mask, i.e. those values are not
        considered in the chi-square computation.
        For further details on "discrepancy functions" see Gelman, Meng & Stern (1996).
        """
        if y.ndim == 1:
            loc = np.where(sig_y > 0.0)[0]
            return np.sum((y[loc] - E_y[loc]) ** 2 / sig_y[loc] ** 2)
        if y.ndim == 2:
            my = np.ma.masked_array(y, mask=sig_y <= 0.0)
            mE_y = np.ma.masked_array(E_y, mask=sig_y <= 0.0)
            msig_y = np.ma.masked_array(sig_y, mask=sig_y <= 0.0)
            return np.ma.sum((my - mE_y) ** 2 / msig_y ** 2, axis=0)

    def load(self, file_name):
        """ 
        Load a file containing the posterior predictive checks

        Parameters
        ----------
        file_name : str
            Name of the file.
        """
        name = os.path.join(BeagleDirectories.results_dir, BeagleDirectories.pypbeagle_data, file_name)
        my_table = Table.read(name)
        self.data = my_table

    def compute_replicated(self, observed_catalogue, filters, ID, n_replicated=2000, seed=1234):
        strID = str(ID)
        file = os.path.join(BeagleDirectories.results_dir, strID + '_' + BeagleDirectories.suffix + '.fits.gz')
        out_name = strID + '_BEAGLE_replic_data.fits.gz'
        out_name = prepare_data_saving(out_name)
        if os.path.isfile(out_name):
            hdulist = fits.open(file)
            beagle_data = hdulist['MARGINAL PHOTOMETRY'].data
            n_samples = len(hdulist['MARGINAL PHOTOMETRY'].data.field(0))
            cols = hdulist['MARGINAL PHOTOMETRY'].columns
            model_flux = np.zeros((filters.n_bands, n_samples), np.float32)
            for j in range(filters.n_bands):
                name = '_' + filters.data['label'][j] + '_'
                model_flux[j, :] = beagle_data[name] / jy

            hdulist.close()
            hdulist = fits.open(out_name)
            replic_data_rows = hdulist[1].data['row_index']
            noiseless_flux = model_flux[:, replic_data_rows]
            replic_flux = np.zeros((filters.n_bands, len(replic_data_rows)), np.float32)
            for col_name in hdulist[1].columns.names:
                if col_name in cols.names:
                    replic_flux[j, :] = hdulist[1].data[col_name]

            return (replic_flux, noiseless_flux, model_flux, n_data)
        if os.path.isfile(file):
            hdulist = fits.open(file)
            beagle_data = hdulist['MARGINAL PHOTOMETRY'].data
            probability = hdulist['POSTERIOR PDF'].data['probability']
            n_samples = len(probability)
            row_indices = np.arange(n_samples)
            wrand = WalkerRandomSampling(probability, keys=row_indices, rand_seed=seed)
            replic_data_rows = wrand.random(n_replicated)
            obs_flux = np.zeros(filters.n_bands, np.float32)
            obs_flux_err = np.zeros(filters.n_bands, np.float32)
            model_flux = np.zeros((filters.n_bands, n_samples), np.float32)
            noiseless_flux = np.zeros((filters.n_bands, n_replicated), np.float32)
            replic_flux = np.zeros((filters.n_bands, n_replicated), np.float32)
            n_data = 0
            obs_flux, obs_flux_err = observed_catalogue.extract_fluxes(filters, ID)
            n_data = np.count_nonzero(obs_flux_err > 0.0)
            for j in range(filters.n_bands):
                name = '_' + filters.data['label'][j] + '_'
                model_flux[j, :] = beagle_data[name] / jy

            noiseless_flux = model_flux[:, replic_data_rows]
            for j in range(filters.n_bands):
                if obs_flux_err[j] > 0.0:
                    replic_flux[j, :] = noiseless_flux[j, :] + np.random.normal(scale=obs_flux_err[j], size=n_replicated)
                else:
                    replic_flux[j, :] = -99.99999

            new_hdu = fits.HDUList(fits.PrimaryHDU())
            ID_col = fits.Column(name='row_index', format='I')
            cols = hdulist['MARGINAL PHOTOMETRY'].columns
            new_hdu.append(fits.BinTableHDU.from_columns(ID_col + cols, nrows=n_replicated, fill=True))
            j = 0
            for col_name in new_hdu[1].columns.names:
                if col_name in cols.names:
                    new_hdu[1].data[col_name] = replic_flux[j, :]
                    j += 1

            new_hdu[1].data['row_index'] = replic_data_rows
            new_hdu.writeto(out_name)
        hdulist.close()
        return (
         replic_flux, noiseless_flux, model_flux, n_data)

    def compute(self, observed_catalogue, filters, discrepancy=None, n_replicated=2000, file_name=None):
        """ 
        Compute  posterior predictive checks quantities.

        Parameters
        ----------
        observed_catalogue : `beagle_photometry.PhotometricCatalogue`
            Class containing an observed photometric catalogue.

        filters : `beagle_filters.PhotometricFilters`
            Class containing a set of photometric filters.

        discrepancy : function, optional
            The discrepancy function used in the posterior predicitve check.

        n_replicated: int, optional
            The number of replicated data to draw.

        file_name : str, optional
            Name of the output catalogue, wuthout including the direcory tree.
            It will be saved into the RESULTS_DIR/pypbeagle_DATA folder (which
            will be created if not present).
        """
        if file_name is None:
            file_name = 'PPC.fits'
        if discrepancy is None:
            discrepancy = self.chi_square
        objID = Column(data=observed_catalogue.data['ID'], name='ID', dtype=np.int32)
        n_obj = len(observed_catalogue.data['ID'])
        n_used_bands = Column(name='n_used_bands', dtype=np.int32, length=n_obj)
        deg_of_freedom = Column(name='dof', dtype=np.int32, length=n_obj)
        aver_chi_square = Column(name='aver_chi_square', dtype=np.float32, length=n_obj)
        left_cumul_probability = Column(name='left_cumul_probability', dtype=np.float32, length=n_obj)
        right_cumul_probability = Column(name='right_cumul_probability', dtype=np.float32, length=n_obj)
        aver_red_chi_square = Column(name='aver_red_chi_square', dtype=np.float32, length=n_obj)
        p_value = Column(name='p_value', dtype=np.float32, length=n_obj)
        my_cols = [
         objID, n_used_bands, deg_of_freedom, aver_chi_square,
         aver_red_chi_square, left_cumul_probability,
         right_cumul_probability, p_value]
        my_table = Table(my_cols)
        model_flux = np.zeros(filters.n_bands, np.float32)
        for i in range(n_obj):
            ID = objID[i]
            strID = str(objID[i])
            file = os.path.join(BeagleDirectories.results_dir, strID + '_' + BeagleDirectories.suffix + '.fits.gz')
            if os.path.isfile(file):
                print ''
                print 'HERE'
                obs_flux, obs_flux_err = observed_catalogue.extract_fluxes(filters, ID)
                replic_flux, noiseless_flux, model_flux, n_data = self.compute_replicated(observed_catalogue, filters, ID)
                hdulist = fits.open(file)
                probability = hdulist['POSTERIOR PDF'].data['probability']
                n_samples = model_flux.shape[1]
                n_replicated = replic_flux.shape[1]
                ext_obs_flux = obs_flux.reshape(filters.n_bands, 1).repeat(n_replicated, 1)
                ext_obs_flux_err = obs_flux_err.reshape(filters.n_bands, 1).repeat(n_replicated, 1)
                discrepancy_data = discrepancy(ext_obs_flux, noiseless_flux, ext_obs_flux_err)
                discrepancy_repl_data = discrepancy(replic_flux, noiseless_flux, ext_obs_flux_err)
                my_table['p_value'][i] = 1.0 * np.count_nonzero(discrepancy_repl_data > discrepancy_data) / n_replicated
                dof = n_data
                my_table['n_used_bands'][i] = n_data
                my_table['dof'][i] = dof
                ext_obs_flux = obs_flux.reshape(filters.n_bands, 1).repeat(n_samples, 1)
                ext_obs_flux_err = obs_flux_err.reshape(filters.n_bands, 1).repeat(n_samples, 1)
                av_chi_square = np.sum(probability * self.chi_square(ext_obs_flux, model_flux, ext_obs_flux_err)) / np.sum(probability)
                my_table['aver_chi_square'][i] = av_chi_square
                my_table['aver_red_chi_square'][i] = av_chi_square / dof
                cdf = stats.chi2.cdf(av_chi_square, dof)
                my_table['left_cumul_probability'][i] = cdf
                my_table['right_cumul_probability'][i] = 1.0 - cdf
                hdulist.close()

        self.columns = my_cols
        self.data = my_table
        name = prepare_data_saving(file_name)
        my_table.write(name)
        return

    def plot_chi2(self, plot_name='BEAGLE_average_chi_square.pdf'):
        """ 
        Plots the distribution (histogram) of the average chi-square.

        Parameters
        ----------
        plot_name: str, optional
            File name of the output plot.
        """
        xdata = self.data['aver_chi_square']
        n_data = len(xdata)
        min_x = 0.0
        max_x = 50.0
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_ylabel('Number of galaxies')
        ax.set_xlabel('$\\langle \\chi^2 \\rangle$')
        ax.set_xlim((min_x, max_x))
        set_plot_ticks(ax, prune_y='lower')
        kwargs = {'alpha': 0.7, 'linewidth': 0.5}
        n, bins, patches = ax.hist(xdata, bins=50, range=(
         min_x, max_x), color='gray', **kwargs)
        dx = bins[1:] - bins[0:-1]
        norm = np.sum(n * dx)
        mask = np.zeros(n_data, dtype=bool)
        mask[self.data['dof'] > 0] = True
        min_dof = np.amin(self.data['dof'][mask])
        max_dof = np.amax(self.data['dof'][mask])
        dof_range = np.arange(min_dof, max_dof + 1)
        frac_data = np.zeros(len(dof_range), dtype=np.float32)
        for i in range(len(dof_range)):
            dof = dof_range[i]
            loc = np.where(self.data['dof'] == dof)[0]
            frac_data[i] = 1.0 * len(loc) / n_data

        frac_data /= np.sum(frac_data)
        xdata = np.linspace(min_x, max_x, 1000)
        chi_distr = np.zeros(len(xdata), dtype=np.float32)
        for i in range(len(dof_range)):
            dof = dof_range[i]
            chi_distr += frac_data[i] * stats.chi2.pdf(xdata, dof)

        chi_distr *= norm
        ax.plot(xdata, chi_distr, color='black', linestyle='--')
        name = prepare_plot_saving(plot_name)
        fig.savefig(name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype='a4', format='pdf', transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        return

    def plot_p_value(self, plot_name='BEAGLE_p_value.pdf', broken_axis=False):
        """ 
        Plots the distribution (histogram) of the p-value.

        Parameters
        ----------
        plot_name : str, optional
            File name of the output plot.

        broken_axis : bool, optionak
            If True, then the y-axis is broken to allow a larger dynamic range
            without loosing details.
        """
        xdata = self.data['p_value']
        n_data = len(xdata)
        min_x = 0.0
        max_x = 1.0
        fig = plt.figure()
        if broken_axis:
            fig, axs = plt.subplots(2, 1, sharex=True)
            fig.subplots_adjust(left=0.13, bottom=0.1)
        else:
            fig, axs = plt.subplots(1, 1)
            axs = (axs,)
        ylabel = 'Number of galaxies'
        xlabel = '$p$-value'
        fig.text(0.5, 0.02, xlabel, ha='center')
        fig.text(0.03, 0.5, ylabel, va='center', rotation='vertical')
        kwargs = {'alpha': 0.7, 'linewidth': 0.5}
        for ax in axs:
            n, bins, patches = ax.hist(xdata, bins=50, range=(
             min_x, max_x), color='gray', **kwargs)
            ax.set_xlim((min_x, max_x))

        if broken_axis:
            set_plot_ticks(axs[0], n_x=4, n_y=3, prune_y='lower')
            set_plot_ticks(axs[1], n_x=4, n_y=3, prune_y='both')
            max_y = np.max(n[1:])
            axs[1].set_ylim((0, max_y * 1.12))
            axs[0].set_ylim((n[0] * 0.8, n[0] * 1.04))
            axs[0].spines['bottom'].set_visible(False)
            axs[1].spines['top'].set_visible(False)
            axs[0].xaxis.tick_top()
            axs[0].tick_params(labeltop='off')
            axs[1].xaxis.tick_bottom()
            d = 0.015
            kwargs = dict(transform=axs[0].transAxes, color='k', clip_on=False)
            axs[0].plot((-d, +d), (-d, +d), **kwargs)
            axs[0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
            kwargs.update(transform=axs[1].transAxes)
            axs[1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
            axs[1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        else:
            set_plot_ticks(axs[0], n_x=4, n_y=4, prune_y='lower')
            axs[0].set_ylim((0, np.max(n) * 1.1))
        levels = (0.01, 0.05)
        for lev in levels:
            l = lev
            frac = 1.0 * len(np.where(xdata <= l)[0]) / n_data
            print 'Fraction of galaxies with p-value < ' + ('{:.2f}').format(lev) + (' = {:.2f}').format(frac)

        name = prepare_plot_saving(plot_name)
        fig.savefig(name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype='a4', format='pdf', transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        return