# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\utils.py
# Compiled at: 2020-03-02 10:36:22
# Size of source mod 2**32: 47117 bytes
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import pandas as pd
from IPython.core.display import HTML, display
import logging, logging.handlers, itertools, seaborn as sns
from scipy.special import kv
from scipy.optimize import broyden2, newton_krylov
from scipy.optimize.nonlin import NoConvergence
from io import StringIO
import re
from pathlib import Path
LOGFILE = Path.home() / '.agglog/agg.main.logger.log'
LOGFILE.parent.mkdir(exist_ok=True, parents=True)
logger = logging.getLogger('aggregate')
logger.setLevel(logging.INFO)
rh = logging.FileHandler(LOGFILE)
rh.setLevel(logging.INFO)
rh_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)-10s | %(funcName)s (l. %(lineno) 5d) | %(message)s')
rh.setFormatter(rh_formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)-10s | %(funcName)s (l. %(lineno) 5d) | %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(rh)
logger.addHandler(ch)
logger.info('aggregate_project.__init__ | New Aggregate Session started')

def get_fmts(df):
    """
    reasonable formats for a styler

    :param df:
    :return:
    """
    fmts = {}

    def guess_fmt(nm, sz):
        named_cols = {'Err':'{:6.3e}', 
         'CV':'{:6.3f}',  'Skew':'{:6.3f}'}
        for n, f in named_cols.items():
            if nm.find(n) >= 0:
                return f

        if abs(sz) < 1:
            return '{:6.3e}'
        if abs(sz) < 10:
            return '{:6.3f}'
        if abs(sz) < 1000:
            return '{:6.0f}'
        if abs(sz) < 10000000000.0:
            return '{:,.0f}'
        return '{:5.3e}'

    for k, v in df.mean().items():
        fmts[k] = guess_fmt(k, v)

    return fmts


def tidy_agg_program(txt):
    """
    guess a nice format for an agg program

    :param txt: program text input

    """
    bits = re.split('(agg|sev|mixed|poisson|fixed)', txt)
    clean = [re.sub('[ ]+', ' ', i.strip()) for i in bits]
    sio = StringIO()
    sio.write(clean[0])
    for agg, exp, sev, sevd, fs, freq in zip(*[clean[i::6] for i in range(1, 7)]):
        nm, *rest = exp.split(' ')
        sio.write(f"\n\t{agg} {nm:^12s} {float(rest[0]):8.1f} {' '.join(rest[1:]):^20s} {sev} {sevd:^25s} {fs:>8s}   {freq}")

    return sio.getvalue()


def ft(z, padding, tilt):
    """
    fft with padding and tilt
    padding = n makes vector 2^n as long
    n=1 doubles (default)
    n=2 quadruples
    tilt is passed in as the tilting vector or None: easier for the caller to have a single instance

    :param z:
    :param padding: = 1 doubles
    :param tilt: vector of tilt values
    :return:
    """
    locft = np.fft.rfft
    if z.shape != (len(z),):
        raise ValueError('ERROR wrong shape passed into ft: ' + str(z.shape))
    else:
        if tilt is not None:
            zt = z * tilt
        else:
            zt = z
        if padding > 0:
            pad_len = zt.shape[0] * ((1 << padding) - 1)
            temp = np.hstack((zt, np.zeros(pad_len)))
        else:
            temp = zt
    return locft(temp)


def ift(z, padding, tilt):
    """
    ift that strips out padding and adjusts for tilt

    :param z:
    :param padding:
    :param tilt:
    :return:
    """
    locift = np.fft.irfft
    if z.shape != (len(z),):
        raise ValueError('ERROR wrong shape passed into ft: ' + str(z.shape))
    temp = locift(z)
    if padding != 0:
        temp = temp[0:len(temp) >> padding]
    if tilt is not None:
        temp /= tilt
    return temp


def sln_fit(m, cv, skew):
    """
    method of moments shifted lognormal fit matching given mean, cv and skewness

    :param m:
    :param cv:
    :param skew:
    :return:
    """
    if skew == 0:
        return (-np.inf, np.inf, 0)
    eta = (np.sqrt(skew ** 2 + 4) / 2 + skew / 2) ** 0.3333333333333333 - 1 / (np.sqrt(skew ** 2 + 4) / 2 + skew / 2) ** 0.3333333333333333
    sigma = np.sqrt(np.log(1 + eta ** 2))
    shift = m - cv * m / eta
    if shift > m:
        logger.warning(f"utils sln_fit | shift > m, {shift} > {m}, too extreme skew {skew}")
        shift = m - 1e-06
    mu = np.log(m - shift) - sigma ** 2 / 2
    return (
     shift, mu, sigma)


def sgamma_fit(m, cv, skew):
    """
    method of moments shifted gamma fit matching given mean, cv and skewness

    :param m:
    :param cv:
    :param skew:
    :return:
    """
    if skew == 0:
        return (np.nan, np.inf, 0)
    alpha = 4 / (skew * skew)
    theta = cv * m * skew / 2
    shift = m - alpha * theta
    return (
     shift, alpha, theta)


def estimate_agg_percentile(m, cv, skew, p=0.999):
    """
    Come up with an estimate of the tail of the distribution based on the three parameter fits, ln and gamma

    :param m:
    :param cv:
    :param skew:
    :param p:
    :return:
    """
    pn = pl = pg = 0
    if skew <= 0:
        fzn = ss.norm(scale=(m * cv), loc=m)
        pn = fzn.isf(1 - p)
    else:
        shift, mu, sigma = sln_fit(m, cv, skew)
        fzl = ss.lognorm(sigma, scale=(np.exp(mu)), loc=shift)
        shift, alpha, theta = sgamma_fit(m, cv, skew)
        fzg = ss.gamma(alpha, scale=theta, loc=shift)
        pl = fzl.isf(1 - p)
        pg = fzg.isf(1 - p)
    return max(pn, pl, pg, m * (1 + ss.norm.isf(1 - p) * cv))


def axiter_factory(axiter, n, figsize=None, height=2, aspect=1, nr=5):
    """
    axiter = check_axiter(axiter, ...) to allow chaining
    TODO can this be done in the class somehow?

    :param axiter:
    :param n:
    :param figsize:
    :param height:
    :param aspect:
    :param nr:
    :return:
    """
    if axiter is None:
        return AxisManager(n, figsize, height, aspect, nr)
    return axiter


class AxisManager(object):
    """AxisManager"""
    __slots__ = [
     'n', 'nr', 'r', 'ax', 'axs', 'c', 'f', 'faxs', 'it']

    def __init__(self, n, figsize=None, height=2, aspect=1, nr=5):
        self.n = n
        self.nr = nr
        self.r, self.c = self.grid_size(n)
        if figsize is None:
            h = self.r * height
            w = self.c * height * aspect
            figsize = (
             w, h / 0.96)
        else:
            self.f, self.axs = plt.subplots((self.r), (self.c), figsize=figsize)
            if n == 1:
                self.ax = self.axs
                self.it = None
            else:
                self.faxs = self.axs.flatten()
            self.it = iter(self.faxs)
            self.ax = None

    def __next__(self):
        if self.n > 1:
            self.ax = next(self.it)
        return self.ax

    def grid_size(self, n, subgrid=False):
        """
        appropriate grid size given class parameters

        :param n:
        :param subgrid: call is for a subgrid, no special treatment for 6 and 8
        :return:
        """
        r = (self.nr - 1 + n) // self.nr
        c = min(n, self.nr)
        if not subgrid:
            if self.nr > 3 and n == 6 and self.nr != 6:
                r = 2
                c = 3
            elif self.nr > 4:
                if n == 8:
                    if self.nr != 8:
                        r = 2
                        c = 4
        return (
         r, c)

    def dimensions(self):
        """
        return dimensions (width and height) of current layout

        :return:
        """
        return (
         self.r, self.c)

    def grid(self, size=0):
        """
        return a block of axes suitable for Pandas
        if size=0 return all the axes

        :param size:
        :return:
        """
        if size == 0:
            return self.faxs
        if size == 1:
            return self.__next__()
        assert self.n >= size
        return [self.__next__() for _ in range(size)]

    def tidy(self):
        """
        delete unused axes to tidy up a plot

        :return:
        """
        if self.it is not None:
            for ax in self.it:
                self.f.delaxes(ax)

    @staticmethod
    def good_grid(n):
        """
        Good layout for n plots
        :param n:
        :return:
        """
        basic = {1:(1, 1), 
         2:(1, 2),  3:(1, 3),  4:(2, 2),  5:(2, 3),  6:(2, 3),  7:(2, 4),  8:(2, 4), 
         9:(3, 3),  10:(4, 3),  11:(4, 3),  12:(4, 3),  13:(5, 3),  14:(5, 3),  15:(5, 3), 
         16:(4, 4),  17:(5, 4),  18:(5, 4),  19:(5, 4),  20:(5, 4)}
        if n <= 20:
            r, c = basic[n]
        else:
            c = 4
            r = n // c
            if r * c < n:
                r += 1
        return (
         r, c)

    @staticmethod
    def size_figure(r, c, aspect=1.5):
        """
        reasonable figure size for n plots
        :param r:
        :param c:
        :param aspect:
        :return:
        """
        w = min(6, 8 / c)
        h = w / aspect
        tw = w * c
        th = h * r
        if th > 10.5:
            tw = 10.5 / th * tw
            th = 10.5
        return (tw, th)

    @staticmethod
    def make_figure(n, aspect=1.5, **kwargs):
        """
        make the figure and iterator
        :param n:
        :param aspect:
        :return:
        """
        r, c = AxisManager.good_grid(n)
        w, h = AxisManager.size_figure(r, c, aspect)
        f, axs = (plt.subplots)(r, c, figsize=(w, h), constrained_layout=True, squeeze=False, **kwargs)
        axi = iter(axs.flatten())
        return (
         f, axs, axi)

    @staticmethod
    def print_fig(n, aspect=1.5):
        """
        printout code...to insert (TODO copy to clipboard!)
        :param n:
        :param aspect:
        :return:
        """
        r, c = AxisManager.good_grid(n)
        w, h = AxisManager.size_figure(r, c, aspect)
        l1 = f"f, axs = plt.subplots({r}, {c}, figsize=({w}, {h}), constrained_layout=True, squeeze=False)"
        l2 = 'axi = iter(axs.flatten())'
        return '\n'.join([l1, l2])

    @staticmethod
    def tidy_up(f, ax):
        """
        delete unused frames out of a figure
        :param ax:
        :return:
        """
        for a in ax:
            f.delaxes(a)


def lognorm_lev(mu, sigma, n, limit):
    """
    return E(min(X, limit)^n) for lognormal using exact calculation
    currently only for n=1, 2

    :param mu:
    :param sigma:
    :param n:
    :param limit:
    :return:
    """
    if limit == -1:
        return np.exp(n * mu + n * n * sigma * sigma / 2)
    phi = ss.norm.cdf
    ll = np.log(limit)
    sigma2 = sigma * sigma
    phi_l = phi((ll - mu) / sigma)
    phi_l2 = phi((ll - mu - n * sigma2) / sigma)
    unlimited = np.exp(n * mu + n * n * sigma2 / 2)
    return unlimited * phi_l2 + limit ** n * (1 - phi_l)


def html_title(txt, n=1, title_case=True):
    """

    :param txt:
    :param n:
    :param title_case:
    :return:
    """
    if title_case:
        display(HTML('<h{:}> {:}'.format(n, txt.replace('_', ' ').title())))
    else:
        display(HTML('<h{:}> {:}'.format(n, txt.replace('_', ' '))))


def sensible_jump(n, desired_rows=20):
    """
    return a sensible jump size to output desired_rows given input of n

    :param n:
    :param desired_rows:
    :return:
    """
    if n < desired_rows:
        return 1
    j = int(n / desired_rows)
    return round(j, -len(str(j)) + 1)


def suptitle_and_tight(title, **kwargs):
    """
    deal with tight layout when there is a suptitle

    :param title:
    :return:
    """
    (plt.suptitle)(title, **kwargs)
    plt.tight_layout(rect=[0, 0, 1, 0.96])


def insurability_triangle(figsize=(10, 3)):
    """
    Illustrate the insurability triangle...

    ::

        λ = A / L
        ROE = (P-L) / (A - P) = (P/L - 1) / (A/L - P/L)
            = (1/LR - 1) / (λ - 1/LR) = (1 - LR) / (λLR - 1)

    Hence

    ::

        δ = ROE / (1 + ROE) = (1 - LR) / [LR (λ - 1)]

    :return:
    """
    f, axs = plt.subplots(1, 3, figsize=figsize)
    it = iter(axs.flatten())
    λs = [1.5, 2, 3, 5, 10, 25, 50, 100]
    LR = np.linspace(0, 1, 101)
    plt.sca(next(it))
    for λ in λs:
        δ = (1 - LR) / LR / (λ - 1)
        plt.plot(LR, δ, label=f"λ={λ}")

    plt.legend()
    plt.ylim(0, 1)
    plt.xlabel('Loss Ratio')
    plt.ylabel('δ Investor Discount Rate')
    plt.title('Profitability vs. Loss Ratio \nBy PML to EL Ratio')
    LR = np.linspace(0, 1, 101)
    plt.sca(next(it))
    for λ in λs:
        levg = np.where(λ * LR > 1, 1 / (λ * LR - 1), 4)
        plt.plot(LR, levg, label=f"λ={λ}")

    plt.ylim(0, 3)
    plt.xlabel('Loss Ratio')
    plt.ylabel('Premium to Surplus Ratio')
    plt.title('Premium to Surplus Ratio vs. Loss Ratio \nBy PML to EL Ratio')
    δ = np.linspace(0.0, 0.3, 301)
    plt.sca(next(it))
    for λ in λs:
        LR = 1 / (1 + δ * (λ - 1))
        plt.plot(δ, LR, label=f"λ={λ}")

    plt.ylim(0, 1)
    plt.ylabel('Loss Ratio')
    plt.xlabel('Investor Discount Rate')
    plt.title('Loss Ratio vs. Investor Discount Rate \nBy PML to EL Ratio')


def read_log():
    """
    read and return the log file

    :return:
    """
    df = pd.read_csv(LOGFILE, sep='|', header=0, names=['datetime', 'context', 'type', 'routine', 'log'], parse_dates=[
     0])
    for c in df.select_dtypes(object):
        df[c] = df[c].str.strip()

    df = df.dropna()
    df = df.set_index('datetime')
    return df


class MomentAggregator(object):
    """MomentAggregator"""
    __slots__ = [
     'freq_1', 'freq_2', 'freq_3', 'sev_1', 'sev_2', 'sev_3', 'agg_1', 'agg_2', 'agg_3',
     'tot_freq_1', 'tot_freq_2', 'tot_freq_3',
     'tot_sev_1', 'tot_sev_2', 'tot_sev_3',
     'tot_agg_1', 'tot_agg_2', 'tot_agg_3', 'freq_moms']

    def __init__(self, freq_moms=None):
        self.agg_1 = self.agg_2 = self.agg_3 = 0
        self.tot_agg_1 = self.tot_agg_2 = self.tot_agg_3 = 0
        self.freq_1 = self.freq_2 = self.freq_3 = 0
        self.tot_freq_1 = self.tot_freq_2 = self.tot_freq_3 = 0
        self.sev_1 = self.sev_2 = self.sev_3 = 0
        self.tot_sev_1 = self.tot_sev_2 = self.tot_sev_3 = 0
        self.freq_moms = freq_moms

    def add_fs(self, f1, f2, f3, s1, s2, s3):
        """
        accumulate new moments defined by f and s

        used by Portfolio

        compute agg for the latest values

        :param f1:
        :param f2:
        :param f3:
        :param s1:
        :param s2:
        :param s3:
        :return:
        """
        self.freq_1 = f1
        self.freq_2 = f2
        self.freq_3 = f3
        self.sev_1 = s1
        self.sev_2 = s2
        self.sev_3 = s3
        self.tot_freq_1, self.tot_freq_2, self.tot_freq_3 = self.cumulate_moments(self.tot_freq_1, self.tot_freq_2, self.tot_freq_3, f1, f2, f3)
        self.tot_sev_1 = self.tot_sev_1 + f1 * s1
        self.tot_sev_2 = self.tot_sev_2 + f1 * s2
        self.tot_sev_3 = self.tot_sev_3 + f1 * s3
        self.agg_1, self.agg_2, self.agg_3 = self.agg_from_fs(f1, f2, f3, s1, s2, s3)
        self.tot_agg_1, self.tot_agg_2, self.tot_agg_3 = self.cumulate_moments(self.tot_agg_1, self.tot_agg_2, self.tot_agg_3, self.agg_1, self.agg_2, self.agg_3)

    def add_f1s(self, f1, s1, s2, s3):
        """
        accumulate new moments defined by f1 and s - fills in f2, f3 based on
        stored frequency distribution

        used by Aggregate

        compute agg for the latest values

        :param f1:
        :param s1:
        :param s2:
        :param s3:
        :return:
        """
        f1, f2, f3 = self.freq_moms(f1)
        self.add_fs(f1, f2, f3, s1, s2, s3)

    def get_fsa_stats(self, total, remix=False):
        """
        get the current f x s = agg statistics_df and moments
        total = true use total else, current
        remix = true for total only, re-compute freq statistics_df based on total freq 1

        :param total: binary
        :param remix: combine all sevs and recompute the freq moments from total freq
        :return:
        """
        if total:
            if remix:
                f1 = self.tot_freq_1
                f1, f2, f3 = self.freq_moms(f1)
                s1, s2, s3 = self.tot_sev_1 / f1, self.tot_sev_2 / f1, self.tot_sev_3 / f1
                a1, a2, a3 = self.agg_from_fs(f1, f2, f3, s1, s2, s3)
                return [
                 
                  f1, f2, f3, *self.static_moments_to_mcvsk(f1, f2, f3),
                 
                  s1, s2, s3, *self.static_moments_to_mcvsk(s1, s2, s3),
                 
                  a1, a2, a3, *self.static_moments_to_mcvsk(a1, a2, a3)]
            return [
             
              self.tot_freq_1, self.tot_freq_2, self.tot_freq_3, *self.moments_to_mcvsk('freq', True),
             
              self.tot_sev_1 / self.tot_freq_1, self.tot_sev_2 / self.tot_freq_1,
              self.tot_sev_3 / self.tot_freq_1, *self.moments_to_mcvsk('sev', True),
             
              self.tot_agg_1, self.tot_agg_2, self.tot_agg_3, *self.moments_to_mcvsk('agg', True)]
        else:
            return [self.freq_1, self.freq_2, self.freq_3, *self.moments_to_mcvsk('freq', False),
             
              self.sev_1, self.sev_2, self.sev_3, *self.moments_to_mcvsk('sev', False),
             
              self.agg_1, self.agg_2, self.agg_3, *self.moments_to_mcvsk('agg', False)]

    @staticmethod
    def factorial_to_noncentral(f1, f2, f3):
        nc2 = f2 + f1
        nc3 = f3 + 3 * f2 + f1
        return (
         nc2, nc3)

    @staticmethod
    def agg_from_fs(f1, f2, f3, s1, s2, s3):
        """
        aggregate_project moments from freq and sev components

        :param f1:
        :param f2:
        :param f3:
        :param s1:
        :param s2:
        :param s3:
        :return:
        """
        return (
         f1 * s1,
         f1 * s2 + (f2 - f1) * s1 ** 2,
         f1 * s3 + f3 * s1 ** 3 + 3 * (f2 - f1) * s1 * s2 + (-3 * f2 + 2 * f1) * s1 ** 3)

    def moments_to_mcvsk(self, mom_type, total=True):
        """
        convert noncentral moments into mean, cv and skewness
        type = agg | freq | sev | mix
        delegates work

        :param mom_type:
        :param total:
        :return:
        """
        if mom_type == 'agg':
            if total:
                return MomentAggregator.static_moments_to_mcvsk(self.tot_agg_1, self.tot_agg_2, self.tot_agg_3)
            return MomentAggregator.static_moments_to_mcvsk(self.agg_1, self.agg_2, self.agg_3)
        elif mom_type == 'freq':
            if total:
                return MomentAggregator.static_moments_to_mcvsk(self.tot_freq_1, self.tot_freq_2, self.tot_freq_3)
            return MomentAggregator.static_moments_to_mcvsk(self.freq_1, self.freq_2, self.freq_3)
        elif mom_type == 'sev':
            if total:
                return MomentAggregator.static_moments_to_mcvsk(self.tot_sev_1 / self.tot_freq_1, self.tot_sev_2 / self.tot_freq_1, self.tot_sev_3 / self.tot_freq_1)
            return MomentAggregator.static_moments_to_mcvsk(self.sev_1, self.sev_2, self.sev_3)

    def moments(self, mom_type, total=True):
        """
        vector of the moments; convenience function

        :param mom_type:
        :param total:
        :return:
        """
        if mom_type == 'agg':
            if total:
                return (self.tot_agg_1, self.tot_agg_2, self.tot_agg_3)
            return (
             self.agg_1, self.agg_2, self.agg_3)
        elif mom_type == 'freq':
            if total:
                return (self.tot_freq_1, self.tot_freq_2, self.tot_freq_3)
            return (
             self.freq_1, self.freq_2, self.freq_3)
        elif mom_type == 'sev':
            if total:
                return (self.tot_sev_1 / self.tot_freq_1, self.tot_sev_2 / self.tot_freq_1,
                 self.tot_sev_3 / self.tot_freq_1)
            return (
             self.sev_1, self.sev_2, self.sev_3)

    @staticmethod
    def cumulate_moments(m1, m2, m3, n1, n2, n3):
        """
        Moments of sum of indepdendent variables

        :param m1: 1st moment, E(X)
        :param m2: 2nd moment, E(X^2)
        :param m3: 3rd moment, E(X^3)
        :param n1:
        :param n2:
        :param n3:
        :return:
        """
        t1 = m1 + n1
        t2 = m2 + 2 * m1 * n1 + n2
        t3 = m3 + 3 * m2 * n1 + 3 * m1 * n2 + n3
        return (
         t1, t2, t3)

    @staticmethod
    def static_moments_to_mcvsk(ex1, ex2, ex3):
        """
        returns mean, cv and skewness from non-central moments

        :param ex1:
        :param ex2:
        :param ex3:
        :return:
        """
        m = ex1
        var = ex2 - ex1 ** 2
        if np.allclose(var, 0):
            var = 0
        else:
            if var < 0:
                logger.error(f"MomentAggregator.static_moments_to_mcvsk | weird var < 0 = {var}; ex={ex1}, ex2={ex2}")
            else:
                sd = np.sqrt(var)
                if m == 0:
                    cv = np.nan
                    logger.warning(f"MomentAggregator.static_moments_to_mcvsk | encountered zero mean, called with {ex1}, {ex2}, {ex3}")
                else:
                    cv = sd / m
            if sd == 0:
                skew = np.nan
            else:
                skew = (ex3 - 3 * ex1 * ex2 + 2 * ex1 ** 3) / sd ** 3
        return (
         m, cv, skew)

    @staticmethod
    def column_names():
        """
        list of the moment and statistics_df names for f x s = a

        :return:
        """
        return [i + j for i, j in itertools.product(['freq', 'sev', 'agg'], [f"_{i}" for i in range(1, 4)] + [
         '_m', '_cv', '_skew'])]

    def stats_series(self, name, limit, pvalue, remix):
        """
        combine elements into a reporting series
        handles order, index names etc. in one place

        :param name: series name
        :param limit:
        :param pvalue:
        :param remix: called from Aggregate want remix=True to collect mix terms; from Portfolio remix=False
        :return:
        """
        idx = pd.MultiIndex.from_arrays([['freq'] * 6 + ['sev'] * 6 + ['agg'] * 8,
         ([
          'ex1', 'ex2', 'ex3'] + ['mean', 'cv', 'skew']) * 3 + ['limit', 'P99.9e']],
          names=[
         'component', 'measure'])
        all_stats = self.get_fsa_stats(total=True, remix=remix)
        p999e = estimate_agg_percentile(*all_stats[15:18], *(pvalue,))
        return pd.Series([*all_stats, limit, p999e], name=name, index=idx)


class MomentWrangler(object):
    """MomentWrangler"""
    __slots__ = [
     '_central', '_noncentral', '_factorial']

    def __init__(self):
        self._central = None
        self._noncentral = None
        self._factorial = None

    @property
    def central(self):
        return self._central

    @central.setter
    def central(self, value):
        self._central = value
        ex1, ex2, ex3 = value
        self._noncentral = (
         ex1, ex2 + ex1 ** 2, ex3 + 3 * ex2 * ex1 + ex1 ** 3)
        self._make_factorial()

    @property
    def noncentral(self):
        return self._noncentral

    @noncentral.setter
    def noncentral(self, value):
        self._noncentral = value
        self._make_factorial()
        self._make_central()

    @property
    def factorial(self):
        return self._factorial

    @factorial.setter
    def factorial(self, value):
        self._factorial = value
        ex1, ex2, ex3 = value
        self._noncentral = (
         ex1, ex2 + ex1, ex3 + 3 * ex2 + ex1)
        self._make_central()

    @property
    def stats(self):
        m, v, c3 = self._central
        sd = np.sqrt(v)
        if m == 0:
            cv = np.nan
        else:
            cv = sd / m
        if sd == 0:
            skew = np.nan
        else:
            skew = c3 / sd ** 3
        return pd.Series((m, v, sd, cv, skew), index=('ex', 'var', 'sd', 'cv', 'skew'))

    def _make_central(self):
        ex1, ex2, ex3 = self._noncentral
        self._central = (
         ex1, ex2 - ex1 ** 2, ex3 - 3 * ex2 * ex1 + 2 * ex1 ** 3)

    def _make_factorial(self):
        """ add factorial from central """
        ex1, ex2, ex3 = self._noncentral
        self._factorial = (
         ex1, ex2 - ex1, ex3 - 3 * ex2 + 2 * ex1)


def xsden_to_meancv(xs, den):
    """
    compute mean and cv from xs and density

    consider adding: np.nan_to_num(den)

    :param xs:
    :param den:
    :return:
    """
    ex1 = np.sum(xs * den)
    ex2 = np.sum(xs ** 2 * den)
    sd = np.sqrt(ex2 - ex1 ** 2)
    if ex1 != 0:
        cv = sd / ex1
    else:
        cv = np.nan
    return (ex1, cv)


def frequency_examples(n, ν, f, κ, sichel_case, log2, xmax=500, **kwds):
    """
    Illustrate different frequency distributions and frequency moment
    calculations.

    sichel_case = gamma | ig | ''

    n = E(N) = expected claim count
    ν = CV(mixing) = asymptotic CV of any compound aggregate whose severity has a second moment
    f = proportion of certain claims, 0 <= f < 1, higher f corresponds to greater skewnesss
    κ = claims per occurrence
    g_mult = adjust EG^3 of Sichel above/below standard PIG
    """

    def ft(x):
        return np.fft.fft(x)

    def ift(x):
        return np.fft.ifft(x)

    def defuzz(x):
        x[np.abs(x) < 5e-16] = 0
        return x

    def ma(x):
        return list((MomentAggregator.static_moments_to_mcvsk)(*x))

    def row(ps):
        moms = [(x ** k * ps).sum() for k in (1, 2, 3)]
        stats = ma(moms)
        return moms + stats + [np.nan]

    def noncentral_n_moms_from_mixing_moms(n, c, g):
        """
        c=Var(G), g=E(G^3) return EN, EN2, EN3
        """
        return [
         n, n * (1 + (1 + c) * n), n * (1 + n * (3 * (1 + c) + n * g))]

    def asy_skew(g, c):
        """
        asymptotic skewnewss
        """
        return [
         (g - 3 * c - 1) / c ** 1.5]

    ans = pd.DataFrame(columns=['X', 'type', 'EX', 'EX2', 'EX3', 'mean', 'CV', 'Skew', 'Asym Skew'])
    ans = ans.set_index(['X', 'type'])
    N = 1 << log2
    x = np.arange(N, dtype=float)
    z = np.zeros(N)
    z[1] = 1
    fz = ft(z)
    dist = 'poisson'
    kernel = n * (fz - 1)
    p = np.real(ift(np.exp(kernel)))
    p = defuzz(p)
    ans.loc[(dist, 'empirical'), :] = row(p)
    temp = noncentral_n_moms_from_mixing_moms(n, 0, 1)
    ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + [np.inf]
    ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    dist = 'neg bin'
    c = ν * ν
    a = 1 / c
    θ = c
    g = 1 + 3 * c + 2 * c * c
    nb = np.real(ift((1 - θ * kernel) ** (-a)))
    nb = defuzz(nb)
    ans.loc[(dist, 'empirical'), :] = row(nb)
    temp = noncentral_n_moms_from_mixing_moms(n, c, g)
    ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + asy_skew(g, c)
    ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    dist = 'delaporte'
    c = ν * ν
    a = ((1 - f) / ν) ** 2
    θ = (1 - f) / a
    g = 2 * ν ** 4 / (1 - f) + 3 * c + 1
    delaporte = np.real(ift(np.exp(f * kernel) * (1 - θ * kernel) ** (-a)))
    delaporte = defuzz(delaporte)
    ans.loc[(dist, 'empirical'), :] = row(delaporte)
    temp = noncentral_n_moms_from_mixing_moms(n, c, g)
    ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + asy_skew(g, c)
    ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    dist = 'pig'
    c = ν * ν
    μ = c
    λ = 1 / μ
    γ = 3 * np.sqrt(μ)
    g = γ * ν ** 3 + 3 * c + 1
    pig = np.real(ift(np.exp(1 / μ * (1 - np.sqrt(1 - 2 * μ ** 2 * λ * kernel)))))
    pig = defuzz(pig)
    ans.loc[(dist, 'empirical'), :] = row(pig)
    temp = noncentral_n_moms_from_mixing_moms(n, c, g)
    ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + asy_skew(g, c)
    ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    dist = 'shifted pig'
    c = ν * ν
    μ = c / (1 - f) ** 2
    λ = (1 - f) / μ
    γ = 3 * np.sqrt(μ)
    g = γ * ν ** 3 + 3 * c + 1
    shifted_pig = np.real(ift(np.exp(f * kernel) * np.exp(1 / μ * (1 - np.sqrt(1 - 2 * μ ** 2 * λ * kernel)))))
    shifted_pig = defuzz(shifted_pig)
    ans.loc[(dist, 'empirical'), :] = row(shifted_pig)
    temp = noncentral_n_moms_from_mixing_moms(n, c, g)
    ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + asy_skew(g, c)
    ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    dist = 'poisson pascal'
    c = (n * ν ** 2 - 1 - κ) / κ
    a = 1 / c
    θ = κ * c
    λ = n / κ
    pois_pascal = np.real(ift(np.exp(λ * ((1 - θ * (fz - 1)) ** (-a) - 1))))
    pois_pascal = defuzz(pois_pascal)
    ans.loc[(dist, 'empirical'), :] = row(pois_pascal)
    g = κ * λ * (2 * c ** 2 * κ ** 2 + 3 * c * κ ** 2 * λ + 3 * c * κ ** 2 + 3 * c * κ + κ ** 2 * λ ** 2 + 3 * κ ** 2 * λ + κ ** 2 + 3 * κ * λ + 3 * κ + 1)
    g2 = n * (2 * c ** 2 * κ ** 2 + 3 * c * n * κ + 3 * c * κ ** 2 + 3 * c * κ + n ** 2 + 3 * n * κ + 3 * n + κ ** 2 + 3 * κ + 1)
    if not np.allclose(g, g2):
        raise AssertionError
    else:
        temp = [
         λ * κ, n * (κ * (1 + c + λ) + 1), g]
        ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + [
         np.nan]
        ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
        dist = 'sichel'
        c = ν * ν
        if sichel_case == 'gamma':
            target = np.array([1, ν, 2 * ν / (1 - f)])
        elif sichel_case == 'ig':
            target = np.array([1, ν, 3.0 * ν / (1 - f)])
        elif sichel_case == '':
            pass
        else:
            raise ValueError('Idiot')
        add_sichel = True
        if sichel_case in ('gamma', 'ig'):
            if sichel_case == 'gamma':
                λ = -0.5
            else:
                λ = -0.5
            μ = 1
            β = ν ** 2

            def f(arrIn):
                μ, β, λ = arrIn
                μ = np.exp(μ)
                β = np.exp(β)
                ex1, ex2, ex3 = np.array([μ ** r * kv(λ + r, μ / β) / kv(λ, μ / β) for r in (1,
                                                                                             2,
                                                                                             3)])
                sd = np.sqrt(ex2 - ex1 * ex1)
                skew = (ex3 - 3 * ex2 * ex1 + 2 * ex1 ** 3) / sd ** 3
                return np.array([ex1, sd, skew]) - target

            try:
                params1 = broyden2(f, (np.log(μ), np.log(β), λ), verbose=False, iter=10000, f_rtol=1e-11)
                params2 = newton_krylov(f, (np.log(μ), np.log(β), λ), verbose=False, iter=10000, f_rtol=1e-11)
                if np.sum((params1 - params2) ** 2) > 0.05:
                    print(f"Broyden {params1}\nNewton K {params2}")
                    m1 = np.sum(np.abs(params1))
                    m2 = np.sum(np.abs(params2))
                    if m1 < m2:
                        print(f"selecting Broyden {params1}")
                        params = params1
                    else:
                        print(f"selecting Newton K {params2}")
                        params = params2
                else:
                    print(f"Two estimates similar, selecting Bry {params1}, {params2}")
                    params = params1
            except NoConvergence as e:
                try:
                    print('ERROR: broyden did not converge')
                    print(e)
                    add_sichel = False
                    raise e
                finally:
                    e = None
                    del e

        elif sichel_case == '':
            λ = κ
            μ = 1
            β = ν ** 2
            target = np.array([1, ν])

            def f(arrIn):
                μ, β = arrIn
                μ = np.exp(μ)
                β = np.exp(β)
                ex1, ex2 = np.array([μ ** r * kv(λ + r, μ / β) / kv(λ, μ / β) for r in (1,
                                                                                        2)])
                sd = np.sqrt(ex2 - ex1 * ex1)
                return np.array([ex1, sd]) - target

            try:
                params = broyden2(f, (np.log(μ), np.log(β)), verbose=False, iter=10000, f_rtol=1e-11)
            except NoConvergence as e:
                try:
                    print('ERROR: broyden did not converge')
                    print(e)
                    add_sichel = False
                    raise e
                finally:
                    e = None
                    del e

        else:
            raise ValueError('Idiot ')
    if add_sichel:
        if sichel_case == '':
            μ, β = params
        else:
            μ, β, λ = params
        μ, β = np.exp(μ), np.exp(β)
        print(f"Sichel params {(μ, β, λ)}")
        inner = np.sqrt(1 - 2 * β * kernel)
        sichel = np.real(ift(inner ** (-λ) * kv(λ, μ * inner / β) / kv(λ, μ / β)))
        sichel = defuzz(sichel)
        ans.loc[(dist, 'empirical'), :] = row(sichel)
        mw = MomentWrangler()
        junk = [μ ** r * kv(λ + r, μ / β) / kv(λ, μ / β) for r in (1, 2, 3)]
        g = junk[2]
        temp = noncentral_n_moms_from_mixing_moms(n, c, g)
        print('Noncentral N from mixing moms            ', temp)
        mw.factorial = junk
        print('Non central N moms                       ', mw.noncentral)
        print('Empirical central N moms                 ', row(sichel))
        ans.loc[(dist, 'theoretical'), :] = temp + ma(temp) + asy_skew(g, c)
        ans.loc[(dist, 'diff'), :] = ans.loc[(dist, 'empirical'), :] / ans.loc[(dist, 'theoretical'), :] - 1
    print(ans.loc[(slice(None), 'diff'), :].abs().sum().sum())
    df = pd.DataFrame(dict(x=x, poisson=p, pois_pascal=pois_pascal, negbin=nb, delaporte=delaporte, pig=pig, shifted_pig=shifted_pig,
      sichel=sichel))
    df = df.query(f" x < {xmax} ")
    df = df.set_index('x')
    axiter = axiter_factory(None, 12, aspect=1.414, nr=4)
    all_dist = ['poisson', 'negbin', 'delaporte', 'pig', 'shifted_pig', 'pois_pascal', 'sichel']
    for vars in [all_dist,
     [
      'poisson', 'negbin', 'pig'],
     [
      'poisson', 'negbin', 'delaporte'],
     [
      'poisson', 'pig', 'shifted_pig', 'sichel'],
     [
      'poisson', 'negbin', 'pois_pascal'],
     [
      'poisson', 'delaporte', 'shifted_pig', 'sichel']]:
        pal = [sns.color_palette('Paired', 7)[i] for i in [all_dist.index(j) for j in vars]]
        df[vars].plot(kind='line', ax=(next(axiter)), color=pal)
        axiter.ax.set_xlim(0, 4 * n)
        df[vars].plot(kind='line', logy=True, ax=(next(axiter)), legend=None, color=pal)

    axiter.tidy()
    display(ans.unstack())
    return (
     df, ans)


class Answer(dict):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def __getattr__(self, item):
        return self[item]

    def __repr__(self):
        return str(self.list())

    def __str__(self):
        return self.list()

    def list(self):
        """ List elements """
        return pd.DataFrame((zip(self.keys(), [self.nice(v) for v in self.values()])),
          columns=['Item', 'Type'])

    def __str__(self):
        return '\n'.join([f"{i[0]:<20s}\t{i[1]}" for i in zip(self.keys(), [self.nice(v) for v in self.values()])])

    @staticmethod
    def nice(x):
        """ return a nice rep of x """
        if type(x) in [str, float, int]:
            return x
        return type(x)

    def summary(self):
        """
        just print out the dataframes: horz or vertical as appropriate
        reasonable styling
        :return:
        """
        for k, v in self.items():
            if isinstance(v, pd.core.frame.DataFrame):
                print(f"\n{k}\n{'=' * len(k)}\n")
                if v.shape[1] > 12:
                    display(v.head(5).T)
                else:
                    display(v.head(10))


def log_test():
    """"
    Issue logs at each level
    """
    print('Issuing five messages...')
    for l, n in zip([logger], ['logger']):
        print(n)
        l.debug('A debug message')
        l.info('A info message')
        l.warning('A warning message')
        l.error('A error message')
        l.critical('A critical message')
        print(f"...done with {n}")

    print('...done')


def subsets(x):
    """
    all non empty subsets of x, an interable
    """
    return list(itertools.chain.from_iterable((itertools.combinations(x, n) for n in range(len(x) + 1))))[1:]