# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_pdf.py
# Compiled at: 2019-07-16 04:25:49
import logging, numpy as np, os, json
from matplotlib import rc
from matplotlib.colors import colorConverter
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from collections import OrderedDict
from astropy.io import fits
from getdist import plots, MCSamples
from beagle_utils import BeagleDirectories, prepare_plot_saving, plot_exists

class PDF(object):

    def __init__(self, params_file, **kwargs):
        with open(params_file) as (f):
            self.adjust_params = json.load(f, object_pairs_hook=OrderedDict)
        self.mock_catalogue = kwargs.get('mock_catalogue')
        self.single_solutions = None
        if kwargs.get('plot_single_solution') is not None:
            self.single_solutions = OrderedDict()
            with fits.open(kwargs.get('plot_single_solution')) as (f):
                self.single_solutions['ID'] = f[1].data['ID']
                self.single_solutions['row'] = f[1].data['row_index']
        self.triangle_font_size = kwargs.get('fontsize')
        return

    def plot_triangle(self, ID, params_to_plot=None, suffix=None, replot=False, M_star=False, show=False):
        """ 
        Draw a "triangle plot" with the 1D and 2D posterior probability

        Parameters
        ----------
        ID : str or int
            Object ID

        M_star : bool, optional
            If set, the routine will plot the mass currenly locked into stars
            instead of the mass of star formed (i.e., the plotted mass will
            accout for the return fraction)

        """
        if suffix is None:
            plot_name = str(ID) + '_BEAGLE_triangle.pdf'
        else:
            plot_name = str(ID) + '_BEAGLE_triangle_' + suffix + '.pdf'
        if plot_exists(plot_name) and not replot and not show:
            logging.warning('The plot "' + plot_name + '" already exists. \n Exiting the function.')
            return
        else:
            fits_file = os.path.join(BeagleDirectories.results_dir, str(ID) + '_' + BeagleDirectories.suffix + '.fits.gz')
            hdulist = fits.open(fits_file)
            param_values = OrderedDict()
            for key, value in self.adjust_params.iteritems():
                extName = 'POSTERIOR PDF'
                if 'extName' in value:
                    extName = value['extName']
                colName = key
                if 'colName' in value:
                    colName = value['colName']
                param_values[key] = hdulist[extName].data[colName]

            probability = hdulist['posterior pdf'].data['probability']
            n_rows = probability.size
            if params_to_plot is None:
                _params_to_plot = list()
                for key, value in self.adjust_params.iteritems():
                    _params_to_plot.append(key)

            else:
                _params_to_plot = params_to_plot
            if M_star and 'mass' in _params_to_plot:
                param_values['mass'][:] = np.log10(hdulist['galaxy properties'].data['M_star'][:])
            nParamsToPlot = len(_params_to_plot)
            names = list()
            labels = list()
            ranges = dict()
            samps = np.zeros((n_rows, nParamsToPlot))
            keys = list()
            j = 0
            for key, par in self.adjust_params.iteritems():
                keys.append(key)
                for par_name in _params_to_plot:
                    if key == par_name:
                        names.append(key)
                        label = par['label'].replace('$', '')
                        labels.append(label)
                        samps[:, j] = param_values[key]
                        ranges.update({key: par['range']})
                        if 'log' in par:
                            if par['log']:
                                samps[:, j] = np.log10(param_values[key])
                                ranges.update({key: np.log10(par['range'])})
                        j += 1
                        break

            settings = {'contours': [
                          0.68, 0.95, 0.99], 
               'range_ND_contour': 1, 
               'range_confidence': 0.001, 
               'fine_bins': 200, 
               'fine_bins_2d': 80, 
               'smooth_scale_1D': 0.3, 
               'smooth_scale_2D': 0.5, 
               'tight_gap_fraction': 0.15}
            samples = MCSamples(samples=samps, names=names, ranges=ranges, weights=probability, labels=labels, settings=settings)
            g = plots.getSubplotPlotter()
            g.settings.num_plot_contours = 3
            g.settings.prob_y_ticks = True
            if self.triangle_font_size is None:
                g.settings.lab_fontsize = 7 + 4 * g.settings.subplot_size_inch
                g.settings.axes_fontsize = 4 + 4 * g.settings.subplot_size_inch
            else:
                g.settings.lab_fontsize = self.triangle_font_size
                g.settings.axes_fontsize = self.triangle_font_size
            line_args = {'lw': 2, 'color': colorConverter.to_rgb('#006FED')}
            g.triangle_plot(samples, filled=True, line_args=line_args)
            g.fig.subplots_adjust(wspace=0.1, hspace=0.1)
            prune = 'both'
            for i in range(len(names)):
                for i2 in range(i, len(names)):
                    _ax = g._subplot(i, i2)
                    _ax.xaxis.set_major_locator(plt.MaxNLocator(3, prune=prune))
                    _ax.yaxis.set_major_locator(plt.MaxNLocator(3, prune=prune))

            for i, ax in enumerate([ g.subplots[(i, i)] for i in range(nParamsToPlot) ]):
                par_name = keys[i]
                if i < nParamsToPlot - 1:
                    ax.tick_params(which='both', labelbottom=False, top=True, labeltop=True, left=False, labelleft=False)
                else:
                    ax.tick_params(which='both', labelbottom=True, top=True, labeltop=False, left=False, labelleft=False)
                y0, y1 = ax.get_ylim()
                lev = samples.get1DDensity(par_name).getLimits(settings['contours'][0])
                ax.add_patch(Rectangle((lev[0], y0), lev[1] - lev[0], y1 - y0, facecolor='grey', alpha=0.5))
                if self.mock_catalogue is not None:
                    name = names[i]
                    value = self.mock_catalogue.get_param_values(ID, (name,))
                    if 'log' in self.adjust_params[name]:
                        if self.adjust_params[name]['log']:
                            value = np.log10(value)
                    ax.plot(value, y0 + (y1 - y0) * 0.05, marker='D', ms=8, color='green')

            if self.single_solutions is not None:
                row = self.single_solutions['row'][(self.single_solutions['ID'] == ID)]
                for i in range(nParamsToPlot):
                    parX = keys[i]
                    valueX = param_values[parX][row]
                    if 'log' in self.adjust_params[parX]:
                        if self.adjust_params[parX]['log']:
                            valueX = np.log10(valueX)
                    for j in range(nParamsToPlot):
                        ax = g.subplots[(i, j)]
                        if ax is None:
                            continue
                        if i == j:
                            ax.plot(valueX, y0 + (y1 - y0) * 0.05, marker='*', ms=12, color='darkorange')
                        else:
                            parY = keys[j]
                            valueY = param_values[parY][row]
                            if 'log' in self.adjust_params[parY]:
                                if self.adjust_params[parY]['log']:
                                    valueY = np.log10(valueY)
                            ax.plot(valueY, valueX, marker='*', ms=12, color='darkorange')

            if show:
                plt.show()
            else:
                name = prepare_plot_saving(plot_name)
                g.export(name)
            plt.close()
            hdulist.close()
            return