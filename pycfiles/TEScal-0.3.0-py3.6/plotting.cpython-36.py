# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tescal/plotting/plotting.py
# Compiled at: 2018-09-12 19:18:31
# Size of source mod 2**32: 54594 bytes
import numpy as np, pickle
from math import ceil
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt, seaborn as sns

def plot_psd(noise, lgcoverlay=True, lgcsave=False, savepath=None):
    """
    Function to plot the noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz).

    Parameters
    ----------
        noise : Object
            Noise object to be plotted
        lgcoverlay : boolean, optional
            If True, psd's for all channels are overlayed in a single plot, 
            If False, each psd for each channel is plotted in a seperate subplot
        lgcsave : boolean, optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
    """
    if noise.psd is None:
        print('Need to calculate the psd first')
        return
    else:
        if lgcoverlay:
            plt.figure(figsize=(12, 8))
            plt.title('{} PSD'.format(noise.name))
            plt.xlabel('frequency [Hz]')
            plt.ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
            plt.grid(which='both')
            for ichan, channel in enumerate(noise.channames):
                plt.loglog((noise.freqs[1:]), (np.sqrt(noise.psd[ichan][1:])), label=channel)

            lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
            if lgcsave:
                try:
                    plt.savefig((savepath + noise.name.replace(' ', '_') + '_PSD_overlay.png'), bbox_extra_artists=(
                     lgd,),
                      bbox_inches='tight')
                except:
                    print('Invalid save path. Figure not saved')

            plt.show()
        else:
            num_subplots = len(noise.channames)
            nrows = int(ceil(num_subplots / 2))
            ncolumns = 2
            fig, axes = plt.subplots(nrows, ncolumns, figsize=(6 * num_subplots, 6 * num_subplots))
            plt.suptitle(('{} PSD'.format(noise.name)), fontsize=40)
            for ii in range(nrows * 2):
                if ii < nrows:
                    irow = ii
                    jcolumn = 0
                else:
                    irow = ii - nrows
                    jcolumn = 1
                if ii < num_subplots:
                    if nrows > 1:
                        axes[(irow, jcolumn)].set_title(noise.channames[ii])
                        axes[(irow, jcolumn)].set_xlabel('frequency [Hz]')
                        axes[(irow, jcolumn)].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                        axes[(irow, jcolumn)].grid(which='both')
                        axes[(irow, jcolumn)].loglog(noise.freqs[1:], np.sqrt(noise.psd[ii][1:]))
                if ii < num_subplots:
                    if nrows == 1:
                        axes[jcolumn].set_title(noise.channames[ii])
                        axes[jcolumn].set_xlabel('frequency [Hz]')
                        axes[jcolumn].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                        axes[jcolumn].grid(which='both')
                        axes[jcolumn].loglog(noise.freqs[1:], np.sqrt(noise.psd[ii][1:]))
                if nrows == 1:
                    axes[jcolumn].axis('off')
                else:
                    axes[(irow, jcolumn)].axis('off')

            plt.tight_layout()
            plt.subplots_adjust(top=0.95)
            if lgcsave:
                try:
                    plt.savefig(savepath + noise.name.replace(' ', '_') + '_PSD_subplot.png')
                except:
                    print('Invalid save path. Figure not saved')

            plt.show()


def plot_reim_psd(noise, lgcsave=False, savepath=None):
    """
    Function to plot the real vs imaginary noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz).
    This is done to check for thermal muon tails making it passed the quality cuts

    Parameters
    ----------
        noise : Object
            Noise object to be plotted
        lgcsave : boolean, optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
            
    """
    if noise.real_psd is None:
        print('Need to calculate the psd first')
        return
    num_subplots = len(noise.channames)
    nrows = int(ceil(num_subplots / 2))
    ncolumns = 2
    fig, axes = plt.subplots(nrows, ncolumns, figsize=(6 * num_subplots, 6 * num_subplots))
    plt.suptitle(('{} Real vs Imaginary PSD'.format(noise.name)), fontsize=40)
    for ii in range(nrows * 2):
        if ii < nrows:
            irow = ii
            jcolumn = 0
        else:
            irow = ii - nrows
            jcolumn = 1
        if ii < num_subplots and nrows > 1:
            axes[(irow, jcolumn)].set_title(noise.channames[ii])
            axes[(irow, jcolumn)].set_xlabel('frequency [Hz]')
            axes[(irow, jcolumn)].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
            axes[(irow, jcolumn)].grid(which='both')
            axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.real_psd[ii][1:])), label='real')
            axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.imag_psd[ii][1:])), label='imag')
            axes[(irow, jcolumn)].legend()
        else:
            if ii < num_subplots:
                if nrows == 1:
                    axes[jcolumn].set_title(noise.channames[ii])
                    axes[jcolumn].set_xlabel('frequency [Hz]')
                    axes[jcolumn].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                    axes[jcolumn].grid(which='both')
                    axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.real_psd[ii][1:])), label='real')
                    axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.imag_psd[ii][1:])), label='imag')
                    axes[jcolumn].legend()
            if nrows == 1:
                axes[jcolumn].axis('off')
            else:
                axes[(irow, jcolumn)].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    if lgcsave:
        try:
            plt.savefig(savepath + noise.name.replace(' ', '_') + '_ReIm_PSD.png')
        except:
            print('Invalid save path. Figure not saved')

    plt.show()


def plot_corrcoeff(noise, lgcsmooth=True, nwindow=7, lgcsave=False, savepath=None):
    """
    Function to plot the cross channel correlation coefficients. Since there are typically few traces,
    the correlations are often noisy. a savgol_filter is used to smooth out some of the noise

    Parameters
    ----------
        noise : Object
            noise object to be plotted
        lgcsmooth : boolean, optional
            If True, a savgol_filter will be used when plotting. 
        nwindow : int, optional
            the number of bins used for the window in the savgol_filter
        lgcsave : boolean, optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
    """
    if noise.corrcoeff is None:
        print('Need to calculate the corrcoeff first')
        return
    plt.figure(figsize=(12, 8))
    plt.title('{} \n Cross Channel Correlation Coefficients'.format(noise.name))
    for ii in range(noise.corrcoeff.shape[0]):
        for jj in range(noise.corrcoeff.shape[1]):
            if ii > jj:
                label = '{} - {}'.format(noise.channames[ii], noise.channames[jj])
                if lgcsmooth:
                    plt.plot((noise.freqs[1:]), savgol_filter((noise.corrcoeff[ii][jj][1:]), nwindow, 3, mode='nearest'), label=label,
                      alpha=0.5)
                else:
                    plt.plot((noise.freqs[1:]), (noise.corrcoeff[ii][jj][1:]), label=label, alpha=0.5)
                plt.xscale('log')

    plt.xlabel('frequency [Hz]')
    plt.ylabel('Correlation Coeff [COV(x,y)/$\\sigma_x \\sigma_y$]')
    plt.grid(which='both')
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=1.0)
    if lgcsave:
        try:
            plt.savefig((savepath + noise.name.replace(' ', '_') + '_corrcoeff.png'), bbox_extra_artists=(lgd,), bbox_inches='tight')
        except:
            print('Invalid save path. Figure not saved')

    plt.show()


def plot_csd(noise, whichcsd=[
 '01'], lgcreal=True, lgcsave=False, savepath=None):
    """
    Function to plot the cross channel noise spectrum referenced to the TES line in
    units of Amperes^2/Hz

    Parameters
    ----------
        noise : Object
            Noise object to be plotted
        whichcsd : list, optional
            a list of strings, where each element of the list refers to the pair of 
            indices of the desired csd plot
        lgcreal : boolean, optional
            If True, the Re(csd) is plotted. If False, the Im(csd) is plotted
        lgcsave : boolean, optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
    """
    if noise.csd is None:
        print('Must calculate the csd first')
        return
    x_plt_label = []
    y_plt_label = []
    for label in whichcsd:
        if type(label) == str:
            x_plt_label.append(int(label[0]))
            y_plt_label.append(int(label[1]))
            if int(label[0]) > noise.real_csd.shape[0] - 1 or int(label[1]) > noise.real_csd.shape[1] - 1:
                print('index out of range')
                return
        else:
            print("Invalid selection. Please provide a list of strings for the desired plots. Ex: ['01','02'] ")
            return

    for ii in range(len(x_plt_label)):
        plt.figure(figsize=(12, 8))
        if lgcreal:
            title = '{} Re(CSD) for channels: {}-{}'.format(noise.name, noise.channames[x_plt_label[ii]], noise.channames[y_plt_label[ii]])
            plt.loglog(noise.freqs[1:], noise.real_csd[x_plt_label[ii]][y_plt_label[ii]][1:])
        else:
            title = '{} Im(CSD) for channels: {}-{}'.format(noise.name, noise.channames[x_plt_label[ii]], noise.channames[y_plt_label[ii]])
            plt.loglog(noise.freqs[1:], noise.imag_csd[x_plt_label[ii]][y_plt_label[ii]][1:])
        plt.title(title)
        plt.grid(True, which='both')
        plt.xlabel('frequency [Hz]')
        plt.ylabel('CSD [A$^2$/Hz]')
        if lgcsave:
            try:
                plt.savefig(savepath + noise.name.replace(' ', '_') + '_csd{}.png'.format(ii))
            except:
                print('Invalid save path. Figure not saved')

        plt.show()


def plot_decorrelatednoise(noise, lgcoverlay=False, lgcdata=True, lgcuncorrnoise=True, lgccorrelated=False, lgcsum=False, lgcsave=False, savepath=None):
    """
    Function to plot the de-correlated noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz) 
    from fitted parameters calculated calculate_deCorrelated_noise

    Parameters
    ----------
        noise : Object
            Noise object to be plotted
        lgcoverlay : boolean, optional
            If True, de-correlated for all channels are overlayed in a single plot, 
            If False, the noise for each channel is plotted in a seperate subplot
        lgcdata : boolean, optional
            Only applies when lgcoverlay = False. If True, the csd data is plotted
        lgcuncorrnoise : boolean, optional
            Only applies when lgcoverlay = False. If True, the de-correlated noise is plotted
        lgccorrelated : boolean, optional
            Only applies when lgcoverlay = False. If True, the correlated component of the fitted noise 
            is plotted
        lgcsum : boolean, optional
            Only applies when lgcoverlay = False. If True, the sum of the fitted de-correlated noise and
            and correlated noise is plotted
        lgcsave : boolean, optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
    """
    if noise.uncorrnoise is None:
        print('Need to de-correlate the noise first')
        return
    else:
        if lgcoverlay:
            plt.figure(figsize=(12, 8))
            plt.xlabel('frequency [Hz]')
            plt.ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
            plt.grid(which='both')
            plt.title('{} de-correlated noise'.format(noise.name))
            for ichan, channel in enumerate(noise.channames):
                plt.loglog((noise.freqs[1:]), (np.sqrt(noise.uncorrnoise[ichan][1:])), label=channel)

            lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
            if lgcsave:
                try:
                    plt.savefig((savepath + noise.name.replace(' ', '_') + '_deCorrNoise_overlay.png'), bbox_extra_artists=(
                     lgd,),
                      bbox_inches='tight')
                except:
                    print('Invalid save path. Figure not saved')

            plt.show()
        else:
            num_subplots = len(noise.channames)
            nrows = int(ceil(num_subplots / 2))
            ncolumns = 2
            fig, axes = plt.subplots(nrows, ncolumns, figsize=(6 * num_subplots, 6 * num_subplots))
            plt.suptitle(('{} de-correlated noise'.format(noise.name)), fontsize=40)
            for ii in range(nrows * 2):
                if ii < nrows:
                    irow = ii
                    jcolumn = 0
                else:
                    irow = ii - nrows
                    jcolumn = 1
                if ii < num_subplots and nrows > 1:
                    axes[(irow, jcolumn)].set_title(noise.channames[ii])
                    axes[(irow, jcolumn)].set_xlabel('frequency [Hz]')
                    axes[(irow, jcolumn)].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                    axes[(irow, jcolumn)].grid(which='both')
                    if lgcdata:
                        axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.real_csd[ii][ii][1:])), label='data',
                          alpha=0.4)
                    if lgcuncorrnoise:
                        axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.uncorrnoise[ii][1:])), label='uncorrelated noise',
                          alpha=0.6)
                    if lgccorrelated:
                        axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.corrnoise[ii][1:])), label='correlated noise',
                          alpha=0.6)
                    if lgcsum:
                        axes[(irow, jcolumn)].loglog((noise.freqs[1:]), (np.sqrt(noise.uncorrnoise[ii][1:] + noise.corrnoise[ii][1:])), label='total noise',
                          alpha=0.6)
                    axes[(irow, jcolumn)].legend()
                elif ii < num_subplots:
                    if nrows == 1:
                        axes[jcolumn].set_title(noise.channames[ii])
                        axes[jcolumn].set_xlabel('frequency [Hz]')
                        axes[jcolumn].set_ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                        axes[jcolumn].grid(which='both')
                        if lgcdata:
                            axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.real_csd[ii][ii][1:])), label='data',
                              alpha=0.4)
                        if lgcuncorrnoise:
                            axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.uncorrnoise[ii][1:])), label='uncorrelated noise',
                              alpha=0.6)
                        if lgccorrelated:
                            axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.corrnoise[ii][1:])), label='correlated noise',
                              alpha=0.6)
                        if lgcsum:
                            axes[jcolumn].loglog((noise.freqs[1:]), (np.sqrt(noise.uncorrnoise[ii][1:] + noise.corrnoise[ii][1:])), label='total noise',
                              alpha=0.6)
                        axes[jcolumn].legend()
                else:
                    if nrows == 1:
                        axes[jcolumn].axis('off')
                    else:
                        axes[(irow, jcolumn)].axis('off')

            plt.tight_layout()
            plt.subplots_adjust(top=0.95)
            if lgcsave:
                try:
                    plt.savefig(savepath + noise.name.replace(' ', '_') + '_deCorrNoise_subplot.png')
                except:
                    print('Invalid save path. Figure not saved')

            plt.show()


def compare_noise(arr, channels, lgcdecorrelatednoise=False, lgcsave=False, savepath=None):
    """
    Function to plot multiple psd's from different noise objects on the same figure. Each channel will
    be plotted in its own figure.
    
    Parameters
    ----------
        arr : array_like
            Array of noise objects
        channels : list 
            List of strings, each string is a channel to plot. ex ['PSA1','PAS2']
        lgcdecorrelatednoise : boolean, optional
            If False, the psd is for each channel is plotted. If True, the calculated
            de-correlated noise is plotted
        lgcsave : boolean , optional
            If True, the figure is saved in the user provided directory
        savepath : str, optional
            Absolute path for the figure to be saved
    """
    if type(channels) == np.ndarray or type(channels) == list:
        for chan in channels:
            if chan in set(sum([arr[ii].channames for ii in range(len(arr))], [])):
                plt.figure(figsize=(12, 8))
                plt.title(chan)
                plt.xlabel('Frequency [Hz]')
                plt.ylabel('Input Referenced Noise [A/$\\sqrt{\\mathrm{Hz}}$]')
                plt.grid(which='both')
                for ii in range(len(arr)):
                    if chan in arr[ii].chann_dict:
                        chan_index = arr[ii].chann_dict[chan]
                        if lgcdecorrelatednoise:
                            if arr[ii].uncorrnoise is not None:
                                plt.loglog((arr[ii].freqs[1:]), (np.sqrt(arr[ii].uncorrnoise[chan_index][1:])), label=(arr[ii].name + ' de-correlated noise'))
                            else:
                                print('The de-correlated noise for file: {} has not been calculated yet'.format(arr[ii].name))
                        else:
                            plt.loglog((arr[ii].freqs[1:]), (np.sqrt(arr[ii].psd[chan_index][1:])), label=(arr[ii].name))
                    else:
                        print('channel: {} not found for file: {} '.format(chan, arr[ii].name))

                lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
                if lgcsave:
                    try:
                        plt.savefig((savepath + chan + '_PSD_comparison.png'), bbox_extra_artists=(lgd,), bbox_inches='tight')
                    except:
                        print('Invalid save path. Figure not saved')

                plt.show()
            else:
                print('Invalid channel name: {} '.format(chan))

    else:
        print("Please provide desired channels in format of a list of numpy.ndarray. ex ['PSA1','PAS2']")


def plot_noise_sim(f, psd, noise_sim, istype, figsize=(12, 8), lgcsave=False, savepath=''):
    """
    Plots psd with simulated noise model
    
    Parameters
    ----------
        f : array_like
            Frequency bins for psd
        psd : array_like 
            Power spectral density
        istype : str
            Must be 'current' or 'power'
            If 'current' the noise is plotted referenced to TES current
            If 'power' the noise is plotted referenced to TES power
        figsize : tuple, optional
            Desired size of figure
        lgcsave : boolean, optional
            If True, plot is saved
        savepath : str, optional
            Directory to save trace
            
    Returns
    -------
        fig : Object
            fig object from matplotlib.pyplot
        ax : Object
            ax object from matplotlib.pyplot
    """
    freqs = f[1:]
    psd = psd[1:]
    noise_sim.freqs = freqs
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle='dotted', alpha=0.5)
    ax.set_xlabel('Frequency [Hz]')
    if istype is 'current':
        ax.set_title(f"Current Noise For $R_0$ : {noise_sim.r0 * 1000.0:.2f} $m\\Omega$")
        ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_ites()))), label='$\\sqrt{S_{ITES}}$')
        ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_iload()))), label='$\\sqrt{S_{ILoad}}$')
        ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_itfn()))), label='$\\sqrt{S_{ITFN}}$')
        ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_itot()))), label='$\\sqrt{S_{Itot}}$')
        ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_isquid()))), label='$\\sqrt{S_{Isquid}}$')
        ax.loglog(freqs, (np.sqrt(psd)), label='data')
        ax.set_ylabel('TES Current Noise $[A/\\sqrt{\\mathrm{Hz}}]$')
    else:
        if istype is 'power':
            ax.set_title(f"Power Noise For $R_0$ : {noise_sim.r0 * 1000.0:.2f} $m\\Omega$")
            ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_ptes()))), label='$\\sqrt{S_{PTES}}$')
            ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_pload()))), label='$\\sqrt{S_{PLoad}}$')
            ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_ptfn()))), label='$\\sqrt{S_{PTFN}}$')
            ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_ptot()))), label='$\\sqrt{S_{Ptot}}$')
            ax.loglog((noise_sim.freqs), (np.sqrt(np.abs(noise_sim.s_psquid()))), label='$\\sqrt{S_{Psquid}}$')
            ax.loglog(freqs, (np.sqrt(psd / np.abs(noise_sim.dIdP(freqs)) ** 2)), label='data')
            ax.set_ylabel('Input Referenced Power Noise [W/$\\sqrt{\\mathrm{Hz}}$]')
        lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        if lgcsave:
            plt.savefig((savepath + f"{istype}_noise_{noise_sim.R0:.0f}.png"), bbox_extra_artists=(lgd,), bbox_inches='tight')
        else:
            return (
             fig, ax)


def plot_full_trace(didv, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot the entire trace in time domain
    
    Parameters
    ----------
        didv : class
            The DIDV class object that the data is stored in
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
    """
    if poles == 'all':
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot((didv.time * 1000000.0), (didv.tmean * 1000000.0 - didv.offset * 1000000.0), color='black', label='mean')
    if didv.fitparams1 is not None:
        if 1 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams1[2] * 1000000.0), ((didv.didvfit1_timedomain - didv.offset) * 1000000.0), color='magenta',
              alpha=0.9,
              label='1-pole fit')
    if didv.fitparams2 is not None:
        if 2 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams2[4] * 1000000.0), ((didv.didvfit2_timedomain - didv.offset) * 1000000.0), color='green',
              alpha=0.9,
              label='2-pole fit')
    if didv.fitparams3 is not None and 3 in poleslist:
        ax.plot((didv.time * 1000000.0 + didv.fitparams3[6] * 1000000.0), ((didv.didvfit3_timedomain - didv.offset) * 1000000.0), color='orange',
          alpha=0.9,
          label='3-pole fit')
    else:
        if didv.irwinparams2priors is not None:
            if plotpriors:
                ax.plot((didv.time * 1000000.0 + didv.irwinparams2priors[6] * 1000000.0), ((didv.didvfit2priors_timedomain - didv.offset) * 1000000.0), color='cyan',
                  alpha=0.9,
                  label='2-pole fit with priors')
        ax.set_xlabel('Time ($\\mu$s)')
        ax.set_ylabel('Amplitude ($\\mu$A)')
        ax.set_xlim([didv.time[0] * 1000000.0, didv.time[(-1)] * 1000000.0])
        ax.legend(loc='upper left')
        ax.set_title('Full Trace of dIdV')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        if lgcsave:
            fig.savefig(savepath + f"full_trace_{savename}.png")
            plt.close(fig)
        else:
            plt.show()


def plot_single_period_of_trace(didv, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot a single period of the trace in time domain
    
    Parameters
    ----------
        didv : class
            The DIDV class object that the data is stored in
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
    """
    if poles == 'all':
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)
    period = 1.0 / didv.sgfreq
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot((didv.time * 1000000.0), (didv.tmean * 1000000.0 - didv.offset * 1000000.0), color='black', label='mean')
    if didv.fitparams1 is not None:
        if 1 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams1[2] * 1000000.0), ((didv.didvfit1_timedomain - didv.offset) * 1000000.0), color='magenta',
              alpha=0.9,
              label='1-pole fit')
    if didv.fitparams2 is not None:
        if 2 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams2[4] * 1000000.0), ((didv.didvfit2_timedomain - didv.offset) * 1000000.0), color='green',
              alpha=0.9,
              label='2-pole fit')
    if didv.fitparams3 is not None:
        if 3 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams3[6] * 1000000.0), ((didv.didvfit3_timedomain - didv.offset) * 1000000.0), color='orange',
              alpha=0.9,
              label='3-pole fit')
    else:
        if didv.irwinparams2priors is not None:
            if plotpriors:
                ax.plot((didv.time * 1000000.0 + didv.irwinparams2priors[6] * 1000000.0), ((didv.didvfit2priors_timedomain - didv.offset) * 1000000.0), color='cyan',
                  alpha=0.9,
                  label='2-pole fit with priors')
        ax.set_xlabel('Time ($\\mu$s)')
        ax.set_ylabel('Amplitude ($\\mu$A)')
        ax.set_xlim([didv.time[0] * 1000000.0, didv.time[0] * 1000000.0 + period * 1000000.0])
        ax.legend(loc='upper left')
        ax.set_title('Single Period of Trace')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        if lgcsave:
            fig.savefig(savepath + f"trace_one_period_{savename}.png")
            plt.close(fig)
        else:
            plt.show()


def plot_zoomed_in_trace(didv, poles='all', zoomfactor=0.1, plotpriors=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot a zoomed in portion of the trace in time domain. This plot zooms in on the
    overshoot of the didv.
    
    Parameters
    ----------
        didv : class
            The DIDV class object that the data is stored in
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        zoomfactor : float, optional, optional
            Number between zero and 1 to show different amounts of the zoomed in trace.
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
    """
    if poles == 'all':
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)
    period = 1.0 / didv.sgfreq
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot((didv.time * 1000000.0), (didv.tmean * 1000000.0 - didv.offset * 1000000.0), color='black', label='mean')
    if didv.fitparams1 is not None:
        if 1 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams1[2] * 1000000.0), ((didv.didvfit1_timedomain - didv.offset) * 1000000.0), color='magenta',
              alpha=0.9,
              label='1-pole fit')
    if didv.fitparams2 is not None:
        if 2 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams2[4] * 1000000.0), ((didv.didvfit2_timedomain - didv.offset) * 1000000.0), color='green',
              alpha=0.9,
              label='2-pole fit')
    if didv.fitparams3 is not None:
        if 3 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams3[6] * 1000000.0), ((didv.didvfit3_timedomain - didv.offset) * 1000000.0), color='orange',
              alpha=0.9,
              label='3-pole fit')
    else:
        if didv.irwinparams2priors is not None:
            if plotpriors:
                ax.plot((didv.time * 1000000.0 + didv.irwinparams2priors[6] * 1000000.0), ((didv.didvfit2priors_timedomain - didv.offset) * 1000000.0), color='cyan',
                  alpha=0.9,
                  label='2-pole fit with priors')
        ax.set_xlabel('Time ($\\mu$s)')
        ax.set_ylabel('Amplitude ($\\mu$A)')
        ax.set_xlim([(0.5 - zoomfactor / 2) * period * 1000000.0, (0.5 + zoomfactor / 2) * period * 1000000.0])
        ax.legend(loc='upper left')
        ax.set_title('Zoomed In Portion of Trace')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        if lgcsave:
            fig.savefig(savepath + f"zoomed_in_trace_{savename}.png")
            plt.close(fig)
        else:
            plt.show()


def plot_didv_flipped(didv, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot the flipped trace in time domain. This function should be used to 
    test if there are nonlinearities in the didv
    
    Parameters
    ----------
        didv : class
            The DIDV class object that the data is stored in
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
    """
    if poles == 'all':
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot((didv.time * 1000000.0), ((didv.tmean - didv.offset) * 1000000.0), color='black', label='data')
    period = 1.0 / didv.sgfreq
    time_flipped = didv.time - period / 2.0
    tmean_flipped = -(didv.tmean - didv.offset)
    ax.plot((time_flipped * 1000000.0), (tmean_flipped * 1000000.0), color='blue', label='flipped data')
    if didv.fitparams1 is not None:
        if 1 in poleslist:
            ax.plot((didv.time * 1000000.0 + didv.fitparams1[2] * 1000000.0), ((didv.didvfit1_timedomain - didv.offset) * 1000000.0), color='magenta',
              alpha=0.9,
              label='1-pole fit')
    if didv.fitparams2 is not None and 2 in poleslist:
        ax.plot((didv.time * 1000000.0 + didv.fitparams2[4] * 1000000.0), ((didv.didvfit2_timedomain - didv.offset) * 1000000.0), color='green',
          alpha=0.9,
          label='2-pole fit')
    else:
        if didv.fitparams3 is not None:
            if 3 in poleslist:
                ax.plot((didv.time * 1000000.0 + didv.fitparams3[6] * 1000000.0), ((didv.didvfit3_timedomain - didv.offset) * 1000000.0), color='orange',
                  alpha=0.9,
                  label='3-pole fit')
        if didv.irwinparams2priors is not None:
            if plotpriors:
                ax.plot((didv.time * 1000000.0 + didv.irwinparams2priors[6] * 1000000.0), ((didv.didvfit2priors_timedomain - didv.offset) * 1000000.0), color='cyan',
                  alpha=0.9,
                  label='2-pole fit with priors')
        ax.set_xlabel('Time ($\\mu$s)')
        ax.set_ylabel('Amplitude ($\\mu$A)')
        ax.legend(loc='upper left')
        ax.set_title('Flipped Traces to Check Asymmetry')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        if lgcsave:
            fig.savefig(savepath + f"flipped_trace_{savename}.png")
            plt.close(fig)
        else:
            plt.show()


def plot_re_im_didv(didv, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot the real and imaginary parts of the didv in frequency space.
    Currently creates two different plots.
    
    Parameters
    ----------
        didv : class
            The DIDV class object that the data is stored in
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
    """
    if poles == 'all':
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)
    goodinds = np.abs(didv.didvmean / didv.didvstd) > 2.0
    fitinds = didv.freq > 0
    plotinds = np.logical_and(fitinds, goodinds)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter((didv.freq[plotinds]), (np.real(didv.didvmean)[plotinds]), color='blue', label='mean', s=5)
    ax.plot((didv.freq[plotinds]), (np.real(didv.didvmean + didv.didvstd)[plotinds]), color='black', label='1-$\\sigma$ bounds', alpha=0.1)
    ax.plot((didv.freq[plotinds]), (np.real(didv.didvmean - didv.didvstd)[plotinds]), color='black', alpha=0.1)
    if didv.fitparams1 is not None and 1 in poleslist:
        ax.plot((didv.freq[fitinds]), (np.real(didv.didvfit1_freqdomain)[fitinds]), color='magenta',
          label='1-pole fit')
    else:
        if didv.fitparams2 is not None:
            if 2 in poleslist:
                ax.plot((didv.freq[fitinds]), (np.real(didv.didvfit2_freqdomain)[fitinds]), color='green',
                  label='2-pole fit')
            else:
                if didv.fitparams3 is not None:
                    if 3 in poleslist:
                        ax.plot((didv.freq[fitinds]), (np.real(didv.didvfit3_freqdomain)[fitinds]), color='orange',
                          label='3-pole fit')
                    else:
                        if didv.irwinparams2priors is not None:
                            if plotpriors:
                                ax.plot((didv.freq[fitinds]), (np.real(didv.didvfit2priors_freqdomain)[fitinds]), color='cyan',
                                  label='2-pole fit with priors')
                        else:
                            ax.set_xlabel('Frequency (Hz)')
                            ax.set_ylabel('Re($dI/dV$) ($\\Omega^{-1}$)')
                            ax.set_xscale('log')
                            yhigh = max(np.real(didv.didvmean)[plotinds][(didv.freq[plotinds] < 100000.0)])
                            ylow = min(np.real(didv.didvmean)[plotinds][(didv.freq[plotinds] < 100000.0)])
                            ybnd = np.max([yhigh, -ylow])
                            ax.set_ylim([-ybnd, ybnd])
                            ax.set_xlim([min(didv.freq[fitinds]), max(didv.freq[fitinds])])
                            ax.legend(loc='upper left')
                            ax.set_title('Real Part of dIdV')
                            ax.tick_params(right=True, top=True)
                            ax.grid(which='major')
                            ax.grid(which='minor', linestyle='dotted', alpha=0.3)
                            if lgcsave:
                                fig.savefig(savepath + f"didv_real_{savename}.png")
                                plt.close(fig)
                            else:
                                plt.show()
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.scatter((didv.freq[plotinds]), (np.imag(didv.didvmean)[plotinds]), color='blue', label='x(f) mean', s=5)
                        ax.plot((didv.freq[plotinds]), (np.imag(didv.didvmean + didv.didvstd)[plotinds]), color='black', label='x(f) 1-$\\sigma$ bounds', alpha=0.1)
                        ax.plot((didv.freq[plotinds]), (np.imag(didv.didvmean - didv.didvstd)[plotinds]), color='black', alpha=0.1)
                        if didv.fitparams1 is not None:
                            if 1 in poleslist:
                                ax.plot((didv.freq[fitinds]), (np.imag(didv.didvfit1_freqdomain)[fitinds]), color='magenta',
                                  label='1-pole fit')
                else:
                    if didv.fitparams2 is not None:
                        if 2 in poleslist:
                            ax.plot((didv.freq[fitinds]), (np.imag(didv.didvfit2_freqdomain)[fitinds]), color='green',
                              label='2-pole fit')
                if didv.fitparams3 is not None:
                    if 3 in poleslist:
                        ax.plot((didv.freq[fitinds]), (np.imag(didv.didvfit3_freqdomain)[fitinds]), color='orange',
                          label='3-pole fit')
        else:
            if didv.irwinparams2priors is not None:
                if plotpriors:
                    ax.plot((didv.freq[fitinds]), (np.imag(didv.didvfit2priors_freqdomain)[fitinds]), color='cyan',
                      label='2-pole fit with priors')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Im($dI/dV$) ($\\Omega^{-1}$)')
        ax.set_xscale('log')
        yhigh = max(np.imag(didv.didvmean)[plotinds][(didv.freq[plotinds] < 100000.0)])
        ylow = min(np.imag(didv.didvmean)[plotinds][(didv.freq[plotinds] < 100000.0)])
        ybnd = np.max([yhigh, -ylow])
        ax.set_ylim([-ybnd, ybnd])
        ax.set_xlim([min(didv.freq[fitinds]), max(didv.freq[fitinds])])
        ax.legend(loc='upper left')
        ax.set_title('Imaginary Part of dIdV')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        ax.grid(which='major')
        ax.grid(which='minor', linestyle='dotted', alpha=0.3)
        if lgcsave:
            fig.savefig(savepath + f"didv_imag_{savename}.png")
            plt.close(fig)
        else:
            plt.show()


def plot_iv(IVobject, temps='all', chans='all', showfit=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot the IV curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        showfit : boolean, optional
            Boolean flag to also plot the linear fit to the normal data
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    ntemps, nch, niters = IVobject.dites.shape
    chan_names = IVobject.chan_names
    if temps == 'all':
        trange = range(ntemps)
    else:
        if np.isscalar(temps):
            trange = np.array([temps])
        else:
            trange = np.array(temps)
        if chans == 'all':
            chrange = range(nch)
        else:
            if np.isscalar(chans):
                chrange = np.array([chans])
            else:
                chrange = np.array(chans)
        ch_colors = plt.cm.viridis(np.linspace(0, 1, num=(len(trange) * len(chrange))))
        fig, ax = plt.subplots(figsize=(10, 6))
        for it, t in enumerate(trange):
            for ich, ch in enumerate(chrange):
                if ntemps > 1:
                    label_str = 'Temp {}, Channel {}'.format(t, chan_names[ch])
                else:
                    label_str = 'Channel {}'.format(chan_names[ch])
                ax.scatter((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ites[(t, ch)] * 1000000.0), label=label_str, color=(ch_colors[(it * len(chrange) + ich)]),
                  s=10.0)
                ax.plot((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ites[(t, ch)] * 1000000.0), color=(ch_colors[(it * len(chrange) + ich)]), alpha=0.5)
                ax.errorbar((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ites[(t, ch)] * 1000000.0), yerr=(IVobject.ites_err[(t, ch)] * 1000000.0), linestyle='None',
                  color='k')
                if showfit:
                    maxind = np.argmax(abs(IVobject.vb[(t, ch)]))
                    if IVobject.vb[(t, ch, maxind)] > 0:
                        vbfit = np.linspace(0, (max(IVobject.vb[(t, ch)] * 1000000.0)), num=10)
                    else:
                        vbfit = np.linspace((min(IVobject.vb[(t, ch)] * 1000000.0)), 0, num=10)
                    ax.plot(vbfit, (1.0 / IVobject.rfit[(t, ch)] * vbfit), color=(ch_colors[(it * len(chrange) + ich)]), alpha=0.1)

        ax.legend(loc='best')
        ax.set_xlabel('Bias Voltage [$\\mu V$]')
        ax.set_ylabel('Current through TES [$\\mu A$]')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        ax.set_title('$I_0$ vs. $V_b$')
        if lgcsave:
            fig.savefig(savepath + 'iv_curve_{}.png'.format(savename))
            plt.close(fig)
        else:
            return (
             fig, ax)


def plot_rv(IVobject, temps='all', chans='all', lgcsave=False, savepath='', savename=''):
    """
    Function to plot the resistance curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    ntemps, nch, niters = IVobject.r0.shape
    chan_names = IVobject.chan_names
    if temps == 'all':
        trange = range(ntemps)
    else:
        if np.isscalar(temps):
            trange = np.array([temps])
        else:
            trange = np.array(temps)
        if chans == 'all':
            chrange = range(nch)
        else:
            if np.isscalar(chans):
                chrange = np.array([chans])
            else:
                chrange = np.array(chans)
        ch_colors = plt.cm.viridis(np.linspace(0, 1, num=(len(trange) * len(chrange))))
        fig, ax = plt.subplots(figsize=(10, 6))
        for it, t in enumerate(trange):
            for ich, ch in enumerate(chrange):
                if ntemps > 1:
                    label_str = 'Temp {}, Channel {}'.format(t, chan_names[ch])
                else:
                    label_str = 'Channel {}'.format(chan_names[ch])
                ax.scatter((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.r0[(t, ch)] * 1000.0), label=label_str, color=(ch_colors[(it * len(chrange) + ich)]),
                  s=10.0)
                ax.plot((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.r0[(t, ch)] * 1000.0), color=(ch_colors[(it * len(chrange) + ich)]), alpha=0.5)
                ax.errorbar((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.r0[(t, ch)] * 1000.0), yerr=(IVobject.r0_err[(t, ch)] * 1000.0), linestyle='None',
                  color='k')

        ax.legend(loc='best')
        ax.set_xlabel('Bias Voltage [$\\mu V$]')
        ax.set_ylabel('Resistance of TES [$m \\Omega$]')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        ax.set_title('$R_0$ vs. $V_b$')
        if lgcsave:
            fig.savefig(savepath + 'rv_curve_{}.png'.format(savename))
            plt.close(fig)
        else:
            return (
             fig, ax)


def plot_pv(IVobject, temps='all', chans='all', lgcsave=False, savepath='', savename=''):
    """
    Function to plot the power curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    ntemps, nch, niters = IVobject.ptes.shape
    chan_names = IVobject.chan_names
    if temps == 'all':
        trange = range(ntemps)
    else:
        if np.isscalar(temps):
            trange = np.array([temps])
        else:
            trange = np.array(temps)
        if chans == 'all':
            chrange = range(nch)
        else:
            if np.isscalar(chans):
                chrange = np.array([chans])
            else:
                chrange = np.array(chans)
        ch_colors = plt.cm.viridis(np.linspace(0, 1, num=(len(trange) * len(chrange))))
        fig, ax = plt.subplots(figsize=(10, 6))
        for it, t in enumerate(trange):
            for ich, ch in enumerate(chrange):
                if ntemps > 1:
                    label_str = 'Temp {}, Channel {}'.format(t, chan_names[ch])
                else:
                    label_str = 'Channel {}'.format(chan_names[ch])
                ax.scatter((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ptes[(t, ch)] * 1000000000000.0), label=label_str, color=(ch_colors[(it * len(chrange) + ich)]),
                  s=10.0)
                ax.plot((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ptes[(t, ch)] * 1000000000000.0), color=(ch_colors[(it * len(chrange) + ich)]), alpha=0.5)
                ax.errorbar((IVobject.vb[(t, ch)] * 1000000.0), (IVobject.ptes[(t, ch)] * 1000000000000.0), yerr=(IVobject.ptes_err[(t, ch)] * 1000000000000.0), linestyle='None',
                  color='k')

        ax.legend(loc='best')
        ax.set_xlabel('Bias Voltage [$\\mu V$]')
        ax.set_ylabel('Power [$pW$]')
        ax.grid(linestyle='dotted')
        ax.tick_params(which='both', direction='in', right=True, top=True)
        ax.set_title('$P_0$ vs. $V_b$')
        if lgcsave:
            fig.savefig(savepath + 'pv_curve_{}.png'.format(savename))
            plt.close(fig)
        else:
            return (
             fig, ax)


def plot_all_curves(IVobject, temps='all', chans='all', showfit=True, lgcsave=False, savepath='', savename=''):
    """
    Function to plot the IV, resistance, and power curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        showfit : boolean, optional
            Boolean flag to also plot the linear fit to the normal data
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    plot_iv(IVobject, temps=temps, chans=chans, showfit=showfit, lgcsave=lgcsave, savepath=savepath, savename=savename)
    plot_rv(IVobject, temps=temps, chans=chans, lgcsave=lgcsave, savepath=savepath, savename=savename)
    plot_pv(IVobject, temps=temps, chans=chans, lgcsave=lgcsave, savepath=savepath, savename=savename)


def plotnonlin(OFnonlinOBJ, pulse, params):
    """
    Diagnostic plotting of non-linear pulse fitting
    
    Parameters
    ----------
        OFnonlinOBJ: OFnonlin object
            The OFnonlin fit object to be plotted
        pulse: ndarray
            The raw trace to be fit
        params: tuple
            Tuple containing best fit paramters
            
    Returns
    -------
        None
    """
    if OFnonlinOBJ.lgcdouble:
        A, tau_r, tau_f, t0 = params
    else:
        A, tau_f, t0 = params
        tau_r = OFnonlinOBJ.taurise
    variables = [
     A, tau_r, tau_f, t0]
    t0ind = int(t0 * OFnonlinOBJ.fs)
    nmin = t0ind - int(5 * tau_r * OFnonlinOBJ.fs)
    nmax = t0ind + int(7 * tau_f * OFnonlinOBJ.fs)
    f = OFnonlinOBJ.freqs
    cf = f > 0
    f = f[cf]
    error = OFnonlinOBJ.error[cf]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Non-Linear Two Pole Fit', fontsize=18)
    axes[0][0].grid(True, linestyle='dashed')
    axes[0][0].set_title('Frequency Domain Trace')
    axes[0][0].set_xlabel('Frequency [Hz]')
    axes[0][0].set_ylabel('Amplitude [A/$\\sqrt{\\mathrm{Hz}}$]')
    axes[0][0].loglog(f, (np.abs(OFnonlinOBJ.data[cf])), c='g', label='Pulse', alpha=0.75)
    axes[0][0].loglog(f, (np.abs((OFnonlinOBJ.twopole)(*variables))[cf]), c='r', label='Fit')
    axes[0][0].loglog(f, error, c='b', label='$\\sqrt{PSD}$', alpha=0.75)
    axes[0][0].tick_params(which='both', direction='in', right=True, top=True)
    axes[0][1].grid(True, linestyle='dashed')
    axes[0][1].set_title('Time Series Trace (Zoomed)')
    axes[0][1].set_xlabel('Time [ms]')
    axes[0][1].set_ylabel('Amplitude [Amps]')
    axes[0][1].plot((OFnonlinOBJ.time[nmin:nmax] * 1000.0), (pulse[nmin:nmax]), c='g', label='Pulse', alpha=0.75)
    axes[0][1].plot((OFnonlinOBJ.time[nmin:nmax] * 1000.0), ((OFnonlinOBJ.twopoletime)(*variables)[nmin:nmax]), c='r', label='time domain')
    axes[0][1].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    axes[0][1].tick_params(which='both', direction='in', right=True, top=True)
    axes[1][0].grid(True, linestyle='dashed')
    axes[1][0].set_title('Time Series Trace (Full)')
    axes[1][0].set_xlabel('Time [ms]')
    axes[1][0].set_ylabel('Amplitude [Amps]')
    axes[1][0].plot((OFnonlinOBJ.time * 1000.0), pulse, c='g', label='Pulse', alpha=0.75)
    axes[1][0].plot((OFnonlinOBJ.time * 1000.0), (OFnonlinOBJ.twopoletime)(*variables), c='r', label='time domain')
    axes[1][0].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    axes[1][0].tick_params(which='both', direction='in', right=True, top=True)
    axes[1][1].plot([], [], c='r', label='Best Fit')
    axes[1][1].plot([], [], c='g', label='Raw Data')
    axes[1][1].plot([], [], c='b', label='$\\sqrt{PSD}$')
    for ii in range(len(params)):
        axes[1][1].plot([], [], linestyle=' ')

    labels = [f"Amplitude: {A * 1000000.0:.4f} [$\\mu$A]",
     f"τ$_f$: {tau_f * 1000000.0:.4f} [$\\mu$s]",
     f"$t_0$: {t0 * 1000.0:.4f} [ms]",
     f"τ$_r$: {tau_r * 1000000.0:.4f} [$\\mu$s]"]
    lines = axes[1][1].get_lines()
    legend1 = plt.legend([lines[i] for i in range(3, 3 + len(params))], [labels[ii] for ii in range(len(params))], loc=1)
    legend2 = plt.legend([lines[i] for i in range(0, 3)], ['Best Fit', 'Raw Data', '$\\sqrt{PSD}$'], loc=2)
    axes[1][1].add_artist(legend1)
    axes[1][1].add_artist(legend2)
    axes[1][1].axis('off')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)