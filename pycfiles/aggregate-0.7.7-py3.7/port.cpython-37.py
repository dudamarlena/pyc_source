# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\port.py
# Compiled at: 2020-03-15 11:55:53
# Size of source mod 2**32: 186186 bytes
"""
Purpose
-------

A Portfolio represents a collection of Aggregate objects. Applications include

* Model a book of insurance
* Model a large account with several sub lines
* Model a reinsurance portfolio or large treaty

"""
import collections, json, logging
from copy import deepcopy
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib, numpy as np, pandas as pd, pypandoc
import scipy.stats as ss
from IPython.core.display import HTML, display
from matplotlib.ticker import MultipleLocator, StrMethodFormatter, MaxNLocator, FixedLocator, FixedFormatter, AutoMinorLocator
from scipy import interpolate
import re
from .distr import Aggregate, CarefulInverse, Severity
from .spectral import Distortion
from .utils import ft, ift, sln_fit, sgamma_fit, axiter_factory, AxisManager, html_title, sensible_jump, suptitle_and_tight, MomentAggregator, Answer, subsets
matplotlib.rcParams['legend.fontsize'] = 'xx-small'
logger = logging.getLogger('aggregate')

class Portfolio(object):
    __doc__ = "\n    Portfolio creates and manages a portfolio of Aggregate objects.\n\n    :param name: the name of the portfolio, no spaces or underscores\n    :param spec_list: a list of 1) dictionary: Aggregate object dictionary specifications or\n                                2) Aggregate: An actual aggregate objects or\n                                3) tuple (type, dict) as returned by uw['name'] or\n                                4) string: Names referencing objects in the optionally passed underwriter\n\n    "

    def __init__(self, name, spec_list, uw=None):
        self.name = name
        self.agg_list = []
        self.line_names = []
        logger.info(f"Portfolio.__init__| creating new Portfolio {self.name} at {super(Portfolio, self).__repr__()}")
        ma = MomentAggregator()
        max_limit = 0
        for spec in spec_list:
            if isinstance(spec, Aggregate):
                a = spec
                agg_name = spec.name
            else:
                if isinstance(spec, str):
                    if uw is None:
                        raise ValueError('Must pass valid Underwriter instance to create aggs by name')
                    try:
                        a = uw(spec)
                    except e:
                        print(f"Item {spec} not found in your underwriter")
                        raise e

                    agg_name = a.name
                else:
                    if isinstance(spec, tuple):
                        assert spec[0] == 'agg'
                        a = Aggregate(**spec[1])
                        agg_name = spec[1]['name']
                    else:
                        if isinstance(spec, dict):
                            a = Aggregate(**spec)
                            agg_name = spec['name'][0] if isinstance(spec['name'], list) else spec['name']
                        else:
                            raise ValueError(f"Invalid type {type(spec)} passed to Portfolio, expect Aggregate, str or dict.")
            self.agg_list.append(a)
            self.line_names.append(agg_name)
            self.__setattr__(agg_name, a)
            ma.add_fs(a.report_ser[('freq', 'ex1')], a.report_ser[('freq', 'ex2')], a.report_ser[('freq',
                                                                                                  'ex3')], a.report_ser[('sev',
                                                                                                                         'ex1')], a.report_ser[('sev',
                                                                                                                                                'ex2')], a.report_ser[('sev',
                                                                                                                                                                       'ex3')])
            max_limit = max(max_limit, np.max(np.array(a.limit)))

        self.line_names_ex = self.line_names + ['total']
        for n in self.line_names:
            if n == 'total':
                raise ValueError('Line names cannot equal total, it is reserved for...total')

        temp_report = pd.concat([a.report_ser for a in self.agg_list], axis=1)
        temp = pd.DataFrame(ma.stats_series('total', max_limit, 0.999, remix=False))
        self.statistics_df = pd.concat([temp_report, temp], axis=1)
        self.density_df = None
        self.augmented_df = None
        self.epd_2_assets = {}
        self.assets_2_epd = {}
        self.priority_capital_df = None
        self.priority_analysis_df = None
        self.audit_df = None
        self.padding = 0
        self.tilt_amount = 0
        self._linear_quantile_function = None
        self._cdf = None
        self._pdf = None
        self._tail_var = None
        self.bs = 0
        self.log2 = 0
        self.ex = 0
        self.last_update = 0
        self.hash_rep_at_last_update = ''
        self._distortion = None
        self.sev_calc = ''
        self._remove_fuzz = 0
        self.approx_type = ''
        self.approx_freq_ge = 0
        self.discretization_calc = ''
        self.q_temp = None
        self._renamer = None
        self.program = ''

    def __str__(self):
        """
        Goal: readability
        :return:
        """
        if self.audit_df is None:
            ex = self.statistics_df.loc[(('agg', 'mean'), 'total')]
            empex = np.nan
            isupdated = False
        else:
            ex = self.get_stat(stat='Mean')
            empex = self.get_stat()
            isupdated = True
        s = f"Portfolio name           {self.name:<15s}\nTheoretic expected loss  {ex:15,.1f}\nActual expected loss     {empex:15,.1f}\nError                    {empex / ex - 1:15.6f}\nDiscretization size      {self.log2:15d}\nBucket size              {self.bs:15.2f}\n{object.__repr__(self)}"
        if not isupdated:
            s += '\nNOT UPDATED!'
        return s

    @property
    def distortion(self):
        return self._distortion

    def remove_fuzz(self, df=None, eps=0, force=False, log=''):
        """
        remove fuzz at threshold eps. if not passed use np.finfo(np.float).eps.

        Apply to self.density_df unless df is not None

        Only apply if self.remove_fuzz or force
        :param eps:
        :param df:  apply to dataframe df, default = self.density_df
        :param force: do regardless of self.remove_fuzz
        :return:
        """
        if df is None:
            df = self.density_df
        if eps == 0:
            eps = np.finfo(np.float).eps
        if self._remove_fuzz or force:
            logger.info(f"CPortfolio.remove_fuzz | Removing fuzz from {self.name} dataframe, caller {log}")
            df.loc[:, df.select_dtypes(include=['float64']).columns] = df.select_dtypes(include=['float64']).applymap(lambda x:             if abs(x) < eps:
0 # Avoid dead code: x)

    def __repr__(self):
        s = [
         super(Portfolio, self).__repr__(), f"{{ 'name': '{self.name}'"]
        agg_list = [str({k:v for k, v in a.__dict__.items() if k in Aggregate.aggregate_keys if k in Aggregate.aggregate_keys}) for a in self.agg_list]
        s.append(f"'spec': [{', '.join(agg_list)}]")
        if self.bs > 0:
            s.append(f'"bs": {self.bs}')
            s.append(f'"log2": {self.log2}')
            s.append(f'"padding": {self.padding}')
            s.append(f'"tilt_amount": {self.tilt_amount}')
            s.append(f'"distortion": "{repr(self._distortion)}"')
            s.append(f'"sev_calc": "{self.sev_calc}"')
            s.append(f'"remove_fuzz": {self._remove_fuzz}')
            s.append(f'"approx_type": "{self.approx_type}"')
            s.append(f'"approx_freq_ge": {self.approx_freq_ge}')
        return ', '.join(s) + '}'

    def _repr_html_(self):
        s = [
         f"<h2>Portfolio object: {self.name}</h2>"]
        _n = len(self.agg_list)
        _s = '' if _n <= 1 else 's'
        s.append(f"Portfolio contains {_n} aggregate component{_s}")
        summary_sl = (slice(None), ['mean', 'cv', 'skew'])
        if self.audit_df is not None:
            _df = pd.concat((self.statistics_df.loc[summary_sl, :],
             self.audit_df[['Mean', 'EmpMean', 'MeanErr', 'CV', 'EmpCV', 'CVErr', 'P99.0']].T),
              sort=True)
            s.append(_df._repr_html_())
        else:
            s.append(self.statistics_df.loc[summary_sl, :]._repr_html_())
        return '\n'.join(s)

    def __hash__(self):
        """
        hashing behavior
        :return:
        """
        return hash(repr(self.__dict__))

    def __iter__(self):
        """
        make Portfolio iterable: for each x in Portfolio

        :return:
        """
        return iter(self.agg_list)

    def __getitem__(self, item):
        """
        alloow Portfolio[slice] to return bits of agg_list

        :param item:
        :return:
        """
        return self.agg_list[item]

    @property
    def audit(self):
        """
        Renamed version of the audit dataframe
        :return:
        """
        if self.audit_df is not None:
            return self.audit_df.rename(columns=(self.renamer))

    @property
    def density(self):
        """
        Renamed version of the density_df dataframe
        :return:
        """
        if self.density_df is not None:
            return self.density_df.rename(columns=(self.renamer))

    @property
    def augmented(self):
        """
        Renamed version of the density_df dataframe
        :return:
        """
        if self.augmented_df is not None:
            return self.augmented_df.rename(columns=(self.renamer))

    @property
    def statistics(self):
        """
        Renamed version of the statistics dataframe
        :return:
        """
        return self.statistics_df.rename(columns=(self.renamer))

    def json(self, stream=None):
        """
        write object as json

        :param    stream:
        :return:  stream or text
        """
        args = dict()
        args['bs'] = self.bs
        args['log2'] = self.log2
        args['padding'] = self.padding
        args['tilt_amount'] = self.tilt_amount
        args['distortion'] = repr(self._distortion)
        args['sev_calc'] = self.sev_calc
        args['remove_fuzz'] = self._remove_fuzz
        args['approx_type'] = self.approx_type
        args['approx_freq_ge'] = self.approx_freq_ge
        args['last_update'] = str(self.last_update)
        args['hash_rep_at_last_update'] = str(self.hash_rep_at_last_update)
        d = dict()
        d['name'] = self.name
        d['args'] = args
        d['spec_list'] = [a._spec for a in self.agg_list]
        logger.info(f"Portfolio.json| dummping {self.name} to {stream}")
        s = json.dumps(d)
        logger.debug(f"Portfolio.json | {s}")
        if stream is None:
            return s
        return stream.write(s)

    def save(self, filename='', mode='a'):
        """
        persist to json in filename; if none save to user.json

        :param filename:
        :param mode: for file open
        :return:
        """
        if filename == '':
            filename = './agg/user.json'
        with open(filename, mode=mode) as (f):
            self.json(stream=f)
            logger.info(f"Portfolio.save | {self.name} saved to {filename}")

    def __add__(self, other):
        """
        Add two portfolio objects INDEPENDENT sum (down road can look for the same severity...)

        TODO same severity!

        :param other:
        :return:
        """
        assert isinstance(other, Portfolio)
        new_spec = []
        for a in self.agg_list:
            c = deepcopy(a._spec)
            c['name'] = c['name']
            new_spec.append(c)

        for a in other.agg_list:
            c = deepcopy(a._spec)
            c['name'] = c['name']
            new_spec.append(c)

        return Portfolio(f"({self.name}) + ({other.name})", new_spec)

    def __rmul__(self, other):
        """
        new = other * self; treat as scale change

        :param other:
        :return:
        """
        assert other > 0
        new_spec = []
        for a in self.agg_list:
            new_spec.append(deepcopy(a._spec))

        for d in new_spec:
            s = d['severity']
            if 'mean' in s:
                s['mean'] *= other
            elif 'scale' in s:
                s['scale'] *= other
            else:
                raise ValueError("Cannot adjust s['name'] for scale")

        return Portfolio(f"{other} x {self.name}", new_spec)

    def __mul__(self, other):
        """
        new = self * other, other integer, sum of other independent copies

        :param other:
        :return:
        """
        assert isinstance(other, int)
        new_spec = []
        for a in self.agg_list:
            new_spec.append(deepcopy(a._spec))

        for d in new_spec:
            d['frequency']['n'] *= other

        return Portfolio(f"Sum of {other} copies of {self.name}", new_spec)

    def audits(self, kind='all', **kwargs):
        """
        produce audit plots to assess accuracy of outputs.

        Currently only exeqa available

        :param kind:
        :param kwargs: passed to pandas plot, e.g. set xlim
        :return:
        """
        if kind == 'all':
            kind = [
             'exeqa']
        for k in kind:
            if k == 'exeqa':
                temp = self.density_df.filter(regex='exeqa_.*(?<!total)$').copy()
                temp['sum'] = temp.sum(axis=1)
                temp['err'] = temp['sum'] - temp.index
                f, axs = plt.subplots(1, 2, figsize=(8, 3.75), constrained_layout=True)
                ax = axs.flatten()
                a = (temp['err'].abs().plot)(logy=True, title='Exeqa Sum Error', ax=ax[1], **kwargs)
                a.plot((self.density_df.loss), (self.density_df.p_total), label='p_total')
                a.plot((self.density_df.loss), (self.density_df.p_total * temp.err), label='prob wtd err')
                a.grid('b')
                a.legend(loc='lower left')
                if 'xlim' in kwargs:
                    kwargs['ylim'] = kwargs['xlim']
                (temp.filter(regex='exeqa_.*(?<!total)$|sum').plot)(title='exeqa and sum of parts', ax=ax[0], **kwargs).grid('b')
            f.suptitle(f"E[Xi | X=x] vs. Sum of Parts\nbs={self.bs}, log2={self.log2}, padding={self.padding}", fontsize='x-large')
            return f

    def get_stat(self, line='total', stat='EmpMean'):
        """
        Other analysis suggests that iloc and iat are about same speed but slower than ix

        :param line:
        :param stat:
        :return:
        """
        return self.audit_df.loc[(line, stat)]

    def q(self, p, kind='lower'):
        """
        return lowest quantile, appropriate for discrete bucketing.
        quantile guaranteed to be in the index
        nearest does not work because you always want to pick rounding up

        Definition 2.1 (Quantiles)
        x(α) = qα(X) = inf{x ∈ R : P[X ≤ x] ≥ α} is the lower α-quantile of X
        x(α) = qα(X) = inf{x ∈ R : P[X ≤ x] > α} is the upper α-quantile of X.

        We use the x-notation if the dependence on X is evident, otherwise the q-notion.
        Acerbi and Tasche (2002)

        :param p:
        :param kind: allow upper or lower quantiles
        :return:
        """
        if self._linear_quantile_function is None:
            self._linear_quantile_function = {}
            self.q_temp = self.density_df[['loss', 'F']].groupby('F').agg({'loss': np.min})
            self.q_temp.loc[(1, 'loss')] = self.q_temp.loss.iloc[(-1)]
            self.q_temp.loc[(0, 'loss')] = 0
            self.q_temp = self.q_temp.sort_index()
            self.q_temp['loss_s'] = self.q_temp.loss.shift(-1)
            self.q_temp.iloc[(-1, 1)] = self.q_temp.iloc[(-1, 0)]
            self._linear_quantile_function['upper'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss_s), kind='previous', bounds_error=False, fill_value='extrapolate')
            self._linear_quantile_function['lower'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss), kind='next', bounds_error=False, fill_value='extrapolate')
            self._linear_quantile_function['middle'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss_s), kind='linear', bounds_error=False, fill_value='extrapolate')
        l = float(self._linear_quantile_function[kind](p))
        if not kind == 'middle':
            assert l in self.density_df.index
        return l

    def cdf(self, x):
        """
        distribution function

        :param x:
        :return:
        """
        if self._cdf is None:
            self._cdf = interpolate.interp1d((self.density_df.loss), (self.density_df.F), kind='previous', bounds_error=False,
              fill_value='extrapolate')
        return self._cdf(x)

    def sf(self, x):
        """
        survival function

        :param x:
        :return:
        """
        return 1 - self.cdf(x)

    def pdf(self, x):
        """
        probability density function, assuming a continuous approximation of the bucketed density
        :param x:
        :return:
        """
        if self._pdf is None:
            self._pdf = interpolate.interp1d((self.density_df.loss), (self.density_df.p_total), kind='linear', bounds_error=False,
              fill_value='extrapolate')
        return self._pdf(x) / self.bs

    def var(self, p):
        """
        value at risk = alias for quantile function

        :param p:
        :return:
        """
        return self.q(p)

    def tvar(self, p):
        """
        Compute the tail value at risk at threshold p

        Definition 2.6 (Tail mean and Expected Shortfall)
        Assume E[X−] < ∞. Then
        x¯(α) = TM_α(X) = α^{−1}E[X 1{X≤x(α)}] + x(α) (α − P[X ≤ x(α)])
        is α-tail mean at level α the of X.
        Acerbi and Tasche (2002)

        We are interested in the right hand exceedence [?? note > vs ≥]
        α^{−1}E[X 1{X > x(α)}] + x(α) (P[X ≤ x(α)] − α)

        McNeil etc. p66-70 - this follows from def of ES as an integral
        of the quantile function

        :param p:
        :return:
        """
        assert self.density_df is not None
        _var = self.q(p)
        ex = self.density_df.loc[_var + self.bs:, ['p_total', 'loss']].product(axis=1).sum()
        pip = (self.density_df.loc[(_var, 'F')] - p) * _var
        t_var = 1 / (1 - p) * (ex + pip)
        return t_var

    def tvar_threshold(self, p, kind):
        """
        Find the value pt such that TVaR(pt) = VaR(p) using numerical Newton Raphson
        """
        a = self.q(p, kind)

        def f(p):
            return self.tvar(p) - a

        loop = 0
        p1 = 1 - 2 * (1 - p)
        fp1 = f(p1)
        delta = 1e-05
        while abs(fp1) > 1e-06 and loop < 10:
            df1 = (f(p1 + delta) - fp1) / delta
            p1 = p1 - fp1 / df1
            fp1 = f(p1)
            loop += 1

        if loop == 10:
            raise ValueError(f"Difficulty computing TVaR to match VaR at p={p}")
        return p1

    def equal_risk_var_tvar(self, p_v, p_t):
        """
        solve for equal risk var and tvar: find pv and pt such that sum of
        individual line VaR/TVaR at pv/pt equals the VaR(p) or TVaR(p_t)

        these won't return elements in the index because you have to interpolate
        hence using kind=middle
        """
        target_v = self.q(p_v, 'middle')
        target_t = self.tvar(p_t)

        def fv(p):
            return sum([float(a.q(p, 'middle')) for a in self]) - target_v

        def ft(p):
            return sum([float(a.tvar(p)) for a in self]) - target_t

        ans = np.zeros(2)
        for i, f in enumerate([fv, ft]):
            p1 = 1 - 2 * (1 - (p_v if i == 0 else p_t))
            fp1 = f(p1)
            loop = 0
            delta = 1e-05
            while abs(fp1) > 1e-06 and loop < 10:
                dfp1 = (f(p1 + delta) - fp1) / delta
                p1 = p1 - fp1 / dfp1
                fp1 = f(p1)
                loop += 1

            if loop == 100:
                raise ValueError(f"Trouble finding equal risk {'TVaR' if i else 'VaR'} at p_v={p_v}, p_t={p_t}. No convergence after 100 iterations. ")
            ans[i] = p1

        return ans

    def merton_perold(self, p, kind='lower'):
        """
        compute Merton Perold capital allocation at T/VaR(p) capital using VaR as risk measure
        v = q(p)
        TODO? Add TVaR MERPER
        """
        a = self.q(p, kind)
        df = self.density_df
        loss = df.loss
        ans = []
        total = 0
        for l in self.line_names:
            f = CarefulInverse.dist_inv1d(loss, df[f"ημ_{l}"])
            diff = a - f(p)
            ans.append(diff)
            total += diff

        ans.append(total)
        return ans

    def as_severity(self, limit=np.inf, attachment=0, conditional=False):
        """
        convert into a severity without recomputing

        throws error if self not updated

        :param limit:
        :param attachment:
        :param conditional:
        :return:
        """
        if self.density_df is None:
            raise ValueError('Must update prior to converting to severity')
        return Severity(sev_name=self, sev_a=(self.log2), sev_b=(self.bs), exp_attachment=attachment,
          exp_limit=limit,
          conditional=conditional)

    def fit(self, approx_type='slognorm', output='agg'):
        """
        returns a dictionary specification of the portfolio aggregate_project
        if updated uses empirical moments, otherwise uses theoretic moments

        :param approx_type: slognorm | sgamma
        :param output: return a dict or agg language specification
        :return:
        """
        if self.audit_df is None:
            m = self.statistics_df.loc[(('agg', 'mean'), 'total')]
            cv = self.statistics_df.loc[(('agg', 'cv'), 'total')]
            skew = self.statistics_df.loc[(('agg', 'skew'), 'total')]
        else:
            m, cv, skew = self.audit_df.loc[('total', ['EmpMean', 'EmpCV', 'EmpSkew'])]
        name = f"{approx_type[0:4]}~{self.name[0:5]}"
        agg_str = f"agg {name} 1 claim sev "
        if approx_type == 'slognorm':
            shift, mu, sigma = sln_fit(m, cv, skew)
            sev = {'sev_name':'lognorm', 
             'sev_shape':sigma,  'sev_scale':np.exp(mu),  'sev_loc':shift}
            agg_str += f"{np.exp(mu)} * lognorm {sigma} + {shift} "
        else:
            if approx_type == 'sgamma':
                shift, alpha, theta = sgamma_fit(m, cv, skew)
                sev = {'sev_name':'gamma', 
                 'sev_a':alpha,  'sev_scale':theta,  'sev_loc':shift}
                agg_str += f"{theta} * lognorm {alpha} + {shift} "
            else:
                raise ValueError(f"Inadmissible approx_type {approx_type} passed to fit")
        if output == 'agg':
            agg_str += ' fixed'
            return agg_str
        return {**{'name':name,  'note':f"frozen version of {self.name}",  'exp_en':1}, **sev, **{'freq_name': 'fixed'}}

    def collapse(self, approx_type='slognorm'):
        """
        returns new Portfolio with the fit

        TODO: deprecated...prefer uw(self.fit()) to go through the agg language approach

        :param approx_type: slognorm | sgamma
        :return:
        """
        spec = self.fit(approx_type, output='dict')
        logger.debug(f"Portfolio.collapse | Collapse created new Portfolio with spec {spec}")
        logger.warning('Portfolio.collapse | Collapse is deprecated; use fit() instead.')
        return Portfolio(f"Collapsed {self.name}", [spec])

    def percentiles(self, pvalues=None):
        """
        report_ser on percentiles and large losses
        uses interpolation, audit_df uses nearest

        :pvalues: optional vector of log values to use. If None sensible defaults provided
        :return: DataFrame of percentiles indexed by line and log
        """
        df = pd.DataFrame(columns=['line', 'log', 'Agg Quantile'])
        df = df.set_index(['line', 'log'])
        if pvalues is None:
            pvalues = [
             0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 0.98, 0.99, 0.994, 0.995, 0.999, 0.9999]
        for line in self.line_names_ex:
            q_agg = interpolate.interp1d((self.density_df.loc[:, f"p_{line}"].cumsum()), (self.density_df.loss), kind='linear',
              bounds_error=False,
              fill_value='extrapolate')
            for p in pvalues:
                qq = q_agg(p)
                df.loc[(line, p), :] = [float(qq)]

        df = df.unstack(level=1)
        return df

    def recommend_bucket(self):
        """
        data to help estimate a good bucket size

        :return:
        """
        df = pd.DataFrame(columns=['line', 'bs10'])
        df = df.set_index('line')
        for a in self.agg_list:
            df.loc[a.name, :] = [
             a.recommend_bucket(10)]

        df['bs11'] = df['bs10'] / 2
        df['bs12'] = df['bs10'] / 4
        df['bs13'] = df['bs10'] / 8
        df['bs14'] = df['bs10'] / 16
        df['bs15'] = df['bs10'] / 32
        df['bs16'] = df['bs10'] / 64
        df['bs17'] = df['bs10'] / 128
        df['bs18'] = df['bs10'] / 256
        df['bs19'] = df['bs10'] / 515
        df['bs20'] = df['bs10'] / 1024
        df.loc['total', :] = df.sum()
        return df

    def update(self, log2, bs, approx_freq_ge=100, approx_type='slognorm', remove_fuzz=False, sev_calc='discrete', discretization_calc='survival', padding=1, tilt_amount=0, epds=None, trim_df=True, verbose=False, add_exa=True):
        """
        create density_df, performs convolution. optionally adds additional information if ``add_exa=True``
        for allocation and priority analysis

        tilting: [@Grubel1999]: Computation of Compound Distributions I: Aliasing Errors and Exponential Tilting
        (ASTIN 1999)
        tilt x numbuck < 20 is recommended log. 210
        num buckets and max loss from bucket size

        :param log2:
        :param bs: bucket size
        :param approx_freq_ge: use method of moments if frequency is larger than ``approx_freq_ge``
        :param approx_type: type of method of moments approx to use (slognorm or sgamma)
        :param remove_fuzz: remove machine noise elements from FFT
        :param sev_calc: how to calculate the severity, discrete (point masses as xs) or continuous (uniform between xs points)
        :param discretization_calc:  survival or distribution (accurate on right or left tails)
        :param padding: for fft 1 = double, 2 = quadruple
        :param tilt_amount: for tiling methodology - see notes on density for suggested parameters
        :param epds: epd points for priority analysis; if None-> sensible defaults
        :param trim_df: remove unnecessary columns from density_df before returning
        :param verbose: level of output
        :param add_exa: run add_exa to append additional allocation information needed for pricing; if add_exa also add
        epd info
        :return:
        """
        self.log2 = log2
        self.bs = bs
        self.padding = padding
        self.tilt_amount = tilt_amount
        self.approx_type = approx_type
        self.sev_calc = sev_calc
        self._remove_fuzz = remove_fuzz
        self.approx_type = approx_type
        self.approx_freq_ge = approx_freq_ge
        self.discretization_calc = discretization_calc
        if self.hash_rep_at_last_update == hash(self):
            print(f"Nothing has changed since last update at {self.last_update}")
            return
        else:
            ft_line_density = {}
            N = 1 << log2
            MAXL = N * bs
            xs = np.linspace(0, MAXL, N, endpoint=False)
            if self.tilt_amount != 0:
                tilt_vector = np.exp(self.tilt_amount * np.arange(N))
            else:
                tilt_vector = None
        self.density_df = pd.DataFrame(index=xs)
        self.density_df['loss'] = xs
        ft_all = None
        for agg in self.agg_list:
            raw_nm = agg.name
            nm = f"p_{agg.name}"
            _a = agg.update(xs, (self.padding), tilt_vector, ('exact' if agg.n < approx_freq_ge else approx_type), sev_calc,
              discretization_calc, verbose=verbose)
            if verbose:
                display(_a)
            ft_line_density[raw_nm] = agg.ftagg_density
            self.density_df[nm] = agg.agg_density
            if ft_all is None:
                ft_all = np.copy(ft_line_density[raw_nm])
            else:
                ft_all *= ft_line_density[raw_nm]

        self.density_df['p_total'] = np.real(ift(ft_all, self.padding, tilt_vector))
        for line in self.line_names:
            ft_not = np.ones_like(ft_all)
            if np.any(ft_line_density[line] == 0):
                for not_line in self.line_names:
                    if not_line != line:
                        ft_not *= ft_line_density[not_line]

            else:
                if len(self.line_names) > 1:
                    ft_not = ft_all / ft_line_density[line]
            self.density_df[f"ημ_{line}"] = np.real(ift(ft_not, self.padding, tilt_vector))

        self.remove_fuzz(log='update')
        theoretical_stats = self.statistics_df.T.filter(regex='agg')
        theoretical_stats.columns = ['EX1', 'EX2', 'EX3', 'Mean', 'CV', 'Skew', 'Limit', 'P99.9Est']
        theoretical_stats = theoretical_stats[['Mean', 'CV', 'Skew', 'Limit', 'P99.9Est']]
        percentiles = [0.9, 0.95, 0.99, 0.996, 0.999, 0.9999, 0.999999]
        self.audit_df = pd.DataFrame(columns=([
         'Sum probs', 'EmpMean', 'EmpCV', 'EmpSkew', 'EmpEX1', 'EmpEX2', 'EmpEX3'] + ['P' + str(100 * i) for i in percentiles]))
        for col in self.line_names_ex:
            sump = np.sum(self.density_df[f"p_{col}"])
            t = self.density_df[f"p_{col}"] * self.density_df['loss']
            ex1 = np.sum(t)
            t *= self.density_df['loss']
            ex2 = np.sum(t)
            t *= self.density_df['loss']
            ex3 = np.sum(t)
            m, cv, s = MomentAggregator.static_moments_to_mcvsk(ex1, ex2, ex3)
            ps = np.zeros(len(percentiles))
            temp = self.density_df[f"p_{col}"].cumsum()
            for i, p in enumerate(percentiles):
                ps[i] = (temp > p).idxmax()

            newrow = [
             sump, m, cv, s, ex1, ex2, ex3] + list(ps)
            self.audit_df.loc[col, :] = newrow

        self.audit_df = pd.concat((theoretical_stats, self.audit_df), axis=1, sort=True)
        self.audit_df['MeanErr'] = self.audit_df['EmpMean'] / self.audit_df['Mean'] - 1
        self.audit_df['CVErr'] = self.audit_df['EmpCV'] / self.audit_df['CV'] - 1
        self.audit_df['SkewErr'] = self.audit_df['EmpSkew'] / self.audit_df['Skew'] - 1
        if add_exa:
            self.add_exa((self.density_df), details=True)
            logger.info('Adding EPDs in Portfolio.update')
            if epds is None:
                epds = np.hstack([
                 np.linspace(0.5, 0.1, 4, endpoint=False)] + [np.linspace((10 ** (-n)), (10 ** (-(n + 1))), 9, endpoint=False) for n in range(1, 7)])
                epds = np.round(epds, 7)
            self.priority_capital_df = pd.DataFrame(index=(pd.Index(epds)))
            for col in self.line_names:
                for i in range(3):
                    self.priority_capital_df.loc[:, '{:}_{:}'.format(col, i)] = self.epd_2_assets[(col, i)](epds)
                    self.priority_capital_df.loc[:, '{:}_{:}'.format('total', 0)] = self.epd_2_assets[('total',
                                                                                                       0)](epds)

                col = 'not ' + col
                for i in range(2):
                    self.priority_capital_df.loc[:, '{:}_{:}'.format(col, i)] = self.epd_2_assets[(col, i)](epds)

            self.priority_capital_df.loc[:, '{:}_{:}'.format('total', 0)] = self.epd_2_assets[('total',
                                                                                               0)](epds)
            self.priority_capital_df.columns = self.priority_capital_df.columns.str.split('_', expand=True)
            self.priority_capital_df.sort_index(axis=1, level=1, inplace=True)
            self.priority_capital_df.sort_index(axis=0, inplace=True)
        else:
            self.density_df['F'] = np.cumsum(self.density_df.p_total)
            self.density_df['S'] = 1 - self.density_df.F
        self.ex = self.audit_df.loc[('total', 'EmpMean')]
        self.last_update = np.datetime64('now')
        self.hash_rep_at_last_update = hash(self)
        if trim_df:
            self.trim_df()
        self._linear_quantile_function = None
        self.q_temp = None
        self._cdf = None

    def trim_df(self):
        """
        trim out unwanted columns from density_df

        epd used in graphics

        :return:
        """
        self.density_df = self.density_df.drop((self.density_df.filter(regex='^e_|^exi_xlea|^[a-z_]+ημ').columns),
          axis=1)

    def gradient(self, epsilon=0.0078125, kind='homog', method='forward', distortion=None, remove_fuzz=True, extra_columns=None, do_swap=True):
        """
        Compute the gradient of various quantities relative to a change in the volume of each
        portfolio component.

        Focus is on the quantities used in rate calculations: S, gS, p_total, exa, exag, exi_xgta, exi_xeqq,
        exeqa, exgta etc.

        homog:

        inhomog:

        :param epsilon: the increment to use; scale is 1+epsilon
        :param kind:    homog[ogeneous] or inhomog: homog computes impact of f((1+epsilon)X_i)-f(X_i). Inhomog
                        scales the frequency and recomputes. Note inhomog will have a slight scale issues with
                        E[Severity]
        :param method:  forward, central (using epsilon/2) or backwards
        :param distortion: if included derivatives of statistics using the distortion, such as exag are also
                            computed
        :param extra_columns: extra columns to compute dervs of. Note there is virtually no overhead of adding additional
                        columns
        :param do_swap: force the step to replace line with line+epsilon in all not line2's line2!=line1; whether you need
        this or not depends on what variables you to be differentiated. E.g. if you ask for exa_total only you don't need
        to swap. But if you want exa_A, exa_B you do, otherwise the d/dA exa_B won't be correct. TODO: replace with code!
        :return:   DataFrame of gradients and audit_df in an Answer class
        """
        if not kind == 'inhomog':
            if kind[:7] == 'inhomog':
                raise NotImplementedError(f"kind=={kind} not yet implemented")
            if method == 'central':
                raise NotImplementedError(f"method=={method} not yet implemented")
            if method not in ('forward', 'backwards', 'central'):
                raise ValueError('Inadmissible option passed to gradient.')
            if self.tilt_amount:
                raise ValueError('Gradients do not allow tilts')
        else:
            if method == 'forward':
                delta = 1 + epsilon
                dx = epsilon
                pm = '+'
            else:
                delta = 1 - epsilon
                dx = -epsilon
                pm = '-'

            def loc_ft(x):
                return ft(x, self.padding, None)

            def loc_ift(x):
                return ift(x, self.padding, None)

            xs = self.density_df['loss'].values
            tilt_vector = None
            agg_epsilon_df = pd.DataFrame(index=xs)
            new_aggs = {}
            for base_agg in self.agg_list:
                agg = base_agg.rescale(delta, kind)
                new_aggs[base_agg.name] = agg
                _a = agg.update(xs, (self.padding), tilt_vector, ('exact' if agg.n < self.approx_freq_ge else self.approx_type), (self.sev_calc),
                  (self.discretization_calc), verbose=False)
                agg_epsilon_df[f"p_{agg.name}"] = agg.agg_density
                agg_epsilon_df[f"p_total_{agg.name}"] = np.real(loc_ift(agg.ftagg_density * loc_ft(self.density_df[f"ημ_{agg.name}"])))

            self.remove_fuzz(df=agg_epsilon_df, force=remove_fuzz, log='gradient')
            percentiles = [
             0.9, 0.95, 0.99, 0.996, 0.999, 0.9999, 0.999999]
            audit_df = pd.DataFrame(columns=([
             'Sum probs', 'EmpMean', 'EmpCV', 'EmpSkew', 'EmpEX1', 'EmpEX2', 'EmpEX3'] + ['P' + str(100 * i) for i in percentiles]))
            ep = chr(949)
            D = chr(916)
            for col in agg_epsilon_df.columns:
                sump = np.sum(agg_epsilon_df[col])
                t = agg_epsilon_df[col] * xs
                ex1 = np.sum(t)
                t *= xs
                ex2 = np.sum(t)
                t *= xs
                ex3 = np.sum(t)
                m, cv, s = MomentAggregator.static_moments_to_mcvsk(ex1, ex2, ex3)
                ps = np.zeros(len(percentiles))
                temp = agg_epsilon_df[col].cumsum()
                for i, p in enumerate(percentiles):
                    ps[i] = (temp > p).idxmax()

                audit_df.loc[f"{col[2:]}{pm}{ep}", :] = [
                 sump, m, cv, s, ex1, ex2, ex3] + list(ps)

            for l in self.line_names_ex:
                audit_df.loc[l, :] = self.audit_df.loc[l, :]

            for l in self.line_names:
                audit_df.loc[f"{l}{D}", :] = audit_df.loc[f"{l}{pm}{ep}"] - audit_df.loc[l]
                audit_df.loc[f"total_{l}{D}", :] = audit_df.loc[f"total_{l}{pm}{ep}"] - audit_df.loc['total']

            audit_df = audit_df.sort_index()
            columns_of_interest = [
             'S'] + [f"exa_{line}" for line in self.line_names_ex]
            if extra_columns:
                columns_of_interest += extra_columns
            columns_p_only = [
             'loss'] + [f"p_{line}" for line in self.line_names_ex] + [f"ημ_{line}" for line in self.line_names]
            if distortion:
                _x = self.apply_distortion(distortion, create_augmented=False)
                base = _x.augmented_df
                columns_of_interest.extend(['gS'] + [f"exag_{line}" for line in self.line_names_ex])
            else:
                base = self.density_df
        answer = pd.DataFrame(index=pd.Index(xs, name='loss'), columns=pd.MultiIndex.from_arrays(((),
                                                                                                  ()), names=('partial_wrt',
                                                                                                              'line')))
        answer.columns.name = 'derivatives'

        def ae_ft(x):
            return ft(x, 1, None)

        def swap(adjust_line):
            adjusted_not_fft = {}
            adjust_line_ft = ae_ft(agg_epsilon_df[f"p_{adjust_line}"])
            base_line_ft = ae_ft(base[f"p_{adjust_line}"])
            adj_factor = adjust_line_ft / base_line_ft
            adj_factor[np.logical_and(base_line_ft == 0, adjust_line_ft == 0)] = 0
            n_and = np.sum(np.logical_and(base_line_ft == 0, adjust_line_ft == 0))
            n_or = np.sum(np.logical_or(base_line_ft == 0, adjust_line_ft == 0))
            logger.info(f"SAME? And={n_and} Or={n_or}; Zeros in fft(line) and fft(line + epsilon for {{adjust_line}}.")
            for line in self.line_names:
                if line == adjust_line:
                    adjusted_not_fft[line] = ae_ft(base[f"ημ_{line}"])
                else:
                    adjusted_not_fft[line] = ae_ft(base[f"ημ_{line}"]) * adj_factor

            return adjusted_not_fft

        for line in self.line_names:
            gradient_df = base[columns_p_only].copy()
            gradient_df[f"p_{line}"] = agg_epsilon_df[f"p_{line}"]
            gradient_df['p_total'] = agg_epsilon_df[f"p_total_{line}"]
            if do_swap:
                self.add_exa(gradient_df, details=False, ft_nots=(swap(line)))
            else:
                self.add_exa(gradient_df, details=False)
            if distortion is not None:
                gradient_df = self.apply_distortion(distortion, df_in=gradient_df, create_augmented=False).augmented_df
            answer[[(line, i) for i in columns_of_interest]] = (gradient_df[columns_of_interest] - base[columns_of_interest]) / dx

        return Answer(gradient=answer, audit=audit_df, new_aggs=new_aggs)

    def report(self, report_list='quick'):
        """

        :param report_list:
        :return:
        """
        full_report_list = [
         'statistics', 'quick', 'audit', 'priority_capital', 'priority_analysis']
        if report_list == 'all':
            report_list = full_report_list
        for r in full_report_list:
            if r in report_list:
                html_title(f"{r} Report for {self.name}", 1)
                if r == 'priority_capital':
                    if self.priority_capital_df is not None:
                        display(self.priority_capital_df.loc[0.001:0.01, :].style)
                    else:
                        html_title(f"Report {r} not generated", 2)
                elif r == 'quick':
                    if self.audit_df is not None:
                        df = self.audit_df[['Mean', 'EmpMean', 'MeanErr', 'CV', 'EmpCV', 'CVErr', 'P99.0']]
                        display(df.style)
                    else:
                        html_title(f"Report {r} not generated", 2)
                else:
                    df = getattr(self, r + '_df', None)
                    if df is not None:
                        try:
                            display(df.style)
                        except ValueError:
                            display(df)

                    else:
                        html_title(f"Report {r} not generated", 2)

    def plot--- This code section failed: ---

 L.1272         0  LOAD_FAST                'axiter'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  STORE_FAST               'do_tight'

 L.1274         8  LOAD_FAST                'kind'
               10  LOAD_STR                 'quick'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE   242  'to 242'

 L.1275        16  LOAD_FAST                'self'
               18  LOAD_ATTR                audit_df
               20  LOAD_CONST               None
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L.1276        26  LOAD_GLOBAL              axiter_factory
               28  LOAD_FAST                'axiter'
               30  LOAD_CONST               4
               32  LOAD_FAST                'figsize'
               34  LOAD_FAST                'height'
               36  LOAD_FAST                'aspect'
               38  CALL_FUNCTION_5       5  '5 positional arguments'
               40  STORE_FAST               'axiter'
               42  JUMP_FORWARD         60  'to 60'
             44_0  COME_FROM            24  '24'

 L.1278        44  LOAD_GLOBAL              axiter_factory
               46  LOAD_FAST                'axiter'
               48  LOAD_CONST               3
               50  LOAD_FAST                'figsize'
               52  LOAD_FAST                'height'
               54  LOAD_FAST                'aspect'
               56  CALL_FUNCTION_5       5  '5 positional arguments'
               58  STORE_FAST               'axiter'
             60_0  COME_FROM            42  '42'

 L.1280        60  LOAD_FAST                'self'
               62  LOAD_ATTR                statistics_df
               64  LOAD_ATTR                loc
               66  LOAD_CONST               ('agg', 'mean')
               68  BINARY_SUBSCR    
               70  LOAD_ATTR                sort_index

 L.1281        72  LOAD_CONST               True
               74  LOAD_CONST               0
               76  LOAD_CONST               ('ascending', 'axis')
               78  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               80  LOAD_ATTR                plot

 L.1282        82  LOAD_STR                 'bar'
               84  LOAD_CONST               -45
               86  LOAD_STR                 'Expected Loss'
               88  LOAD_GLOBAL              next
               90  LOAD_FAST                'axiter'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  LOAD_CONST               ('kind', 'rot', 'title', 'ax')
               96  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               98  POP_TOP          

 L.1284       100  LOAD_FAST                'self'
              102  LOAD_ATTR                statistics_df
              104  LOAD_ATTR                loc
              106  LOAD_CONST               ('agg', 'cv')
              108  BINARY_SUBSCR    
              110  LOAD_ATTR                sort_index

 L.1285       112  LOAD_CONST               True
              114  LOAD_CONST               0
              116  LOAD_CONST               ('ascending', 'axis')
              118  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              120  LOAD_ATTR                plot

 L.1286       122  LOAD_STR                 'bar'
              124  LOAD_CONST               -45
              126  LOAD_STR                 'Coeff of Variation'
              128  LOAD_GLOBAL              next
              130  LOAD_FAST                'axiter'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  LOAD_CONST               ('kind', 'rot', 'title', 'ax')
              136  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              138  POP_TOP          

 L.1288       140  LOAD_FAST                'self'
              142  LOAD_ATTR                statistics_df
              144  LOAD_ATTR                loc
              146  LOAD_CONST               ('agg', 'skew')
              148  BINARY_SUBSCR    
              150  LOAD_ATTR                sort_index

 L.1289       152  LOAD_CONST               True
              154  LOAD_CONST               0
              156  LOAD_CONST               ('ascending', 'axis')
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  LOAD_ATTR                plot

 L.1290       162  LOAD_STR                 'bar'
              164  LOAD_CONST               -45
              166  LOAD_STR                 'Skewness'
              168  LOAD_GLOBAL              next
              170  LOAD_FAST                'axiter'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  LOAD_CONST               ('kind', 'rot', 'title', 'ax')
              176  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              178  POP_TOP          

 L.1292       180  LOAD_FAST                'self'
              182  LOAD_ATTR                audit_df
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   238  'to 238'

 L.1293       190  LOAD_FAST                'self'
              192  LOAD_ATTR                audit_df
              194  LOAD_ATTR                loc
              196  LOAD_CONST               None
              198  LOAD_CONST               None
              200  BUILD_SLICE_2         2 
              202  LOAD_STR                 'P99.9'
              204  BUILD_TUPLE_2         2 
              206  BINARY_SUBSCR    
              208  LOAD_ATTR                sort_index

 L.1294       210  LOAD_CONST               True
              212  LOAD_CONST               0
              214  LOAD_CONST               ('ascending', 'axis')
              216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              218  LOAD_ATTR                plot

 L.1295       220  LOAD_STR                 'bar'
              222  LOAD_CONST               -45
              224  LOAD_STR                 '99.9th Percentile'
              226  LOAD_GLOBAL              next
              228  LOAD_FAST                'axiter'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  LOAD_CONST               ('kind', 'rot', 'title', 'ax')
              234  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              236  POP_TOP          
            238_0  COME_FROM           188  '188'
          238_240  JUMP_FORWARD       2312  'to 2312'
            242_0  COME_FROM            14  '14'

 L.1297       242  LOAD_FAST                'kind'
              244  LOAD_STR                 'density'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   664  'to 664'

 L.1298       252  LOAD_GLOBAL              isinstance
              254  LOAD_FAST                'line'
              256  LOAD_GLOBAL              str
              258  CALL_FUNCTION_2       2  '2 positional arguments'
          260_262  POP_JUMP_IF_FALSE   304  'to 304'

 L.1299       264  LOAD_FAST                'line'
              266  LOAD_STR                 'all'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   292  'to 292'

 L.1300       274  LOAD_LISTCOMP            '<code_object <listcomp>>'
              276  LOAD_STR                 'Portfolio.plot.<locals>.<listcomp>'
              278  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                line_names_ex
              284  GET_ITER         
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  STORE_FAST               'line'
              290  JUMP_FORWARD        302  'to 302'
            292_0  COME_FROM           270  '270'

 L.1302       292  LOAD_STR                 'p_'
              294  LOAD_FAST                'line'
              296  BINARY_ADD       
              298  BUILD_LIST_1          1 
              300  STORE_FAST               'line'
            302_0  COME_FROM           290  '290'
              302  JUMP_FORWARD        336  'to 336'
            304_0  COME_FROM           260  '260'

 L.1303       304  LOAD_GLOBAL              isinstance
              306  LOAD_FAST                'line'
              308  LOAD_GLOBAL              list
              310  CALL_FUNCTION_2       2  '2 positional arguments'
          312_314  POP_JUMP_IF_FALSE   332  'to 332'

 L.1304       316  LOAD_LISTCOMP            '<code_object <listcomp>>'
              318  LOAD_STR                 'Portfolio.plot.<locals>.<listcomp>'
              320  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              322  LOAD_FAST                'line'
              324  GET_ITER         
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  STORE_FAST               'line'
              330  JUMP_FORWARD        336  'to 336'
            332_0  COME_FROM           312  '312'

 L.1306       332  LOAD_GLOBAL              ValueError
              334  RAISE_VARARGS_1       1  'exception instance'
            336_0  COME_FROM           330  '330'
            336_1  COME_FROM           302  '302'

 L.1307       336  LOAD_GLOBAL              sorted
              338  LOAD_FAST                'line'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  STORE_FAST               'line'

 L.1308       344  LOAD_STR                 'subplots'
              346  LOAD_FAST                'kwargs'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   404  'to 404'
              354  LOAD_GLOBAL              len
              356  LOAD_FAST                'line'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  LOAD_CONST               1
              362  COMPARE_OP               >
          364_366  POP_JUMP_IF_FALSE   404  'to 404'

 L.1309       368  LOAD_GLOBAL              axiter_factory
              370  LOAD_FAST                'axiter'
              372  LOAD_GLOBAL              len
              374  LOAD_FAST                'line'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  LOAD_FAST                'figsize'
              380  LOAD_FAST                'height'
              382  LOAD_FAST                'aspect'
              384  CALL_FUNCTION_5       5  '5 positional arguments'
              386  STORE_FAST               'axiter'

 L.1310       388  LOAD_FAST                'axiter'
              390  LOAD_METHOD              grid
              392  LOAD_GLOBAL              len
              394  LOAD_FAST                'line'
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  STORE_FAST               'ax'
              402  JUMP_FORWARD        448  'to 448'
            404_0  COME_FROM           364  '364'
            404_1  COME_FROM           350  '350'

 L.1312       404  LOAD_GLOBAL              axiter_factory
              406  LOAD_FAST                'axiter'
              408  LOAD_CONST               1
              410  LOAD_FAST                'figsize'
              412  LOAD_FAST                'height'
              414  LOAD_FAST                'aspect'
              416  CALL_FUNCTION_5       5  '5 positional arguments'
              418  STORE_FAST               'axiter'

 L.1314       420  LOAD_GLOBAL              isinstance
              422  LOAD_FAST                'axiter'
              424  LOAD_GLOBAL              AxisManager
              426  CALL_FUNCTION_2       2  '2 positional arguments'
          428_430  POP_JUMP_IF_FALSE   444  'to 444'

 L.1315       432  LOAD_FAST                'axiter'
              434  LOAD_METHOD              grid
              436  LOAD_CONST               1
              438  CALL_METHOD_1         1  '1 positional argument'
              440  STORE_FAST               'ax'
              442  JUMP_FORWARD        448  'to 448'
            444_0  COME_FROM           428  '428'

 L.1317       444  LOAD_FAST                'axiter'
              446  STORE_FAST               'ax'
            448_0  COME_FROM           442  '442'
            448_1  COME_FROM           402  '402'

 L.1318       448  LOAD_FAST                'self'
              450  LOAD_ATTR                density_df
              452  LOAD_ATTR                loc
              454  LOAD_CONST               None
              456  LOAD_CONST               None
              458  BUILD_SLICE_2         2 
              460  LOAD_FAST                'line'
              462  BUILD_TUPLE_2         2 
              464  BINARY_SUBSCR    
              466  LOAD_ATTR                sort_index
              468  LOAD_CONST               1
              470  LOAD_CONST               ('axis',)
              472  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              474  LOAD_ATTR                plot
              476  BUILD_TUPLE_0         0 

 L.1319       478  LOAD_CONST               True
              480  LOAD_FAST                'ax'
              482  LOAD_CONST               ('sort_columns', 'ax')
              484  BUILD_CONST_KEY_MAP_2     2 
              486  LOAD_FAST                'kwargs'
              488  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              490  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              492  POP_TOP          

 L.1320       494  LOAD_STR                 'logy'
              496  LOAD_FAST                'kwargs'
              498  COMPARE_OP               in
          500_502  POP_JUMP_IF_FALSE   510  'to 510'

 L.1321       504  LOAD_STR                 'log Density'
              506  STORE_FAST               '_t'
              508  JUMP_FORWARD        514  'to 514'
            510_0  COME_FROM           500  '500'

 L.1323       510  LOAD_STR                 'Density'
              512  STORE_FAST               '_t'
            514_0  COME_FROM           508  '508'

 L.1324       514  LOAD_STR                 'subplots'
              516  LOAD_FAST                'kwargs'
              518  COMPARE_OP               in
          520_522  POP_JUMP_IF_FALSE   602  'to 602'
              524  LOAD_GLOBAL              isinstance
              526  LOAD_FAST                'ax'
              528  LOAD_GLOBAL              collections
              530  LOAD_ATTR                Iterable
              532  CALL_FUNCTION_2       2  '2 positional arguments'
          534_536  POP_JUMP_IF_FALSE   602  'to 602'

 L.1325       538  SETUP_LOOP          660  'to 660'
              540  LOAD_GLOBAL              zip
              542  LOAD_FAST                'ax'
              544  LOAD_FAST                'line'
              546  CALL_FUNCTION_2       2  '2 positional arguments'
              548  GET_ITER         
              550  FOR_ITER            598  'to 598'
              552  UNPACK_SEQUENCE_2     2 
              554  STORE_FAST               'a'
              556  STORE_FAST               'l'

 L.1326       558  LOAD_FAST                'a'
              560  LOAD_ATTR                set
              562  LOAD_FAST                'l'
              564  FORMAT_VALUE          0  ''
              566  LOAD_STR                 ' '
              568  LOAD_FAST                '_t'
              570  FORMAT_VALUE          0  ''
              572  BUILD_STRING_3        3 
              574  LOAD_CONST               ('title',)
              576  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              578  POP_TOP          

 L.1327       580  LOAD_FAST                'a'
              582  LOAD_METHOD              legend
              584  CALL_METHOD_0         0  '0 positional arguments'
              586  LOAD_METHOD              set_visible
              588  LOAD_CONST               False
              590  CALL_METHOD_1         1  '1 positional argument'
              592  POP_TOP          
          594_596  JUMP_BACK           550  'to 550'
              598  POP_BLOCK        
              600  JUMP_FORWARD       2312  'to 2312'
            602_0  COME_FROM           534  '534'
            602_1  COME_FROM           520  '520'

 L.1328       602  LOAD_GLOBAL              isinstance
              604  LOAD_FAST                'ax'
              606  LOAD_GLOBAL              collections
              608  LOAD_ATTR                Iterable
              610  CALL_FUNCTION_2       2  '2 positional arguments'
          612_614  POP_JUMP_IF_FALSE   648  'to 648'

 L.1329       616  SETUP_LOOP          660  'to 660'
              618  LOAD_FAST                'ax'
              620  GET_ITER         
              622  FOR_ITER            644  'to 644'
              624  STORE_FAST               'a'

 L.1330       626  LOAD_FAST                'a'
              628  LOAD_ATTR                set
              630  LOAD_FAST                '_t'
              632  FORMAT_VALUE          0  ''
              634  LOAD_CONST               ('title',)
              636  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              638  POP_TOP          
          640_642  JUMP_BACK           622  'to 622'
              644  POP_BLOCK        
              646  JUMP_FORWARD       2312  'to 2312'
            648_0  COME_FROM           612  '612'

 L.1332       648  LOAD_FAST                'ax'
              650  LOAD_ATTR                set
              652  LOAD_FAST                '_t'
              654  LOAD_CONST               ('title',)
              656  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              658  POP_TOP          
            660_0  COME_FROM_LOOP      616  '616'
            660_1  COME_FROM_LOOP      538  '538'
          660_662  JUMP_FORWARD       2312  'to 2312'
            664_0  COME_FROM           248  '248'

 L.1334       664  LOAD_FAST                'kind'
              666  LOAD_STR                 'audit'
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE  1446  'to 1446'

 L.1335       674  LOAD_FAST                'self'
              676  LOAD_ATTR                density_df
              678  STORE_FAST               'D'

 L.1337       680  LOAD_CONST               12
              682  STORE_FAST               'n_plots'

 L.1338       684  LOAD_GLOBAL              axiter_factory
              686  LOAD_FAST                'axiter'
              688  LOAD_FAST                'n_plots'
              690  LOAD_FAST                'figsize'
              692  LOAD_FAST                'height'
              694  LOAD_FAST                'aspect'
              696  CALL_FUNCTION_5       5  '5 positional arguments'
              698  STORE_FAST               'axiter'

 L.1341       700  LOAD_FAST                'D'
              702  LOAD_ATTR                filter
              704  LOAD_STR                 '^p_'
              706  LOAD_CONST               ('regex',)
              708  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              710  LOAD_ATTR                iloc
              712  LOAD_CONST               1
              714  LOAD_CONST               None
              716  BUILD_SLICE_2         2 
              718  LOAD_CONST               None
              720  LOAD_CONST               None
              722  BUILD_SLICE_2         2 
              724  BUILD_TUPLE_2         2 
              726  BINARY_SUBSCR    
              728  LOAD_METHOD              max
              730  CALL_METHOD_0         0  '0 positional arguments'
              732  LOAD_METHOD              max
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  STORE_FAST               'density_scale'

 L.1342       738  LOAD_GLOBAL              np
              740  LOAD_METHOD              sum
              742  LOAD_FAST                'D'
              744  LOAD_ATTR                loss
              746  LOAD_FAST                'D'
              748  LOAD_ATTR                p_total
              750  BINARY_MULTIPLY  
              752  CALL_METHOD_1         1  '1 positional argument'
              754  LOAD_CONST               1.05
              756  BINARY_MULTIPLY  
              758  STORE_FAST               'expected_loss_scale'

 L.1343       760  LOAD_FAST                'D'
              762  LOAD_ATTR                p_total
              764  LOAD_METHOD              cumsum
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  LOAD_FAST                'p'
              770  COMPARE_OP               >
              772  LOAD_METHOD              idxmax
              774  CALL_METHOD_0         0  '0 positional arguments'
              776  STORE_FAST               'large_loss_scale'

 L.1346       778  LOAD_FAST                'D'
              780  LOAD_ATTR                filter
              782  LOAD_STR                 '^p_'
              784  LOAD_CONST               1
              786  LOAD_CONST               ('regex', 'axis')
              788  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              790  STORE_FAST               'temp'

 L.1347       792  LOAD_FAST                'axiter'
              794  LOAD_METHOD              grid
              796  LOAD_CONST               1
              798  CALL_METHOD_1         1  '1 positional argument'
              800  STORE_FAST               'ax'

 L.1348       802  LOAD_FAST                'temp'
              804  LOAD_ATTR                plot
              806  LOAD_FAST                'ax'
              808  LOAD_CONST               0
              810  LOAD_FAST                'density_scale'
              812  BUILD_TUPLE_2         2 
              814  LOAD_CONST               0
              816  LOAD_FAST                'large_loss_scale'
              818  BUILD_TUPLE_2         2 
              820  LOAD_STR                 'Densities'
              822  LOAD_CONST               ('ax', 'ylim', 'xlim', 'title')
              824  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              826  POP_TOP          

 L.1350       828  LOAD_FAST                'axiter'
              830  LOAD_METHOD              grid
              832  LOAD_CONST               1
              834  CALL_METHOD_1         1  '1 positional argument'
              836  STORE_FAST               'ax'

 L.1351       838  LOAD_FAST                'temp'
              840  LOAD_ATTR                plot
              842  LOAD_FAST                'ax'
              844  LOAD_CONST               True
              846  LOAD_CONST               0
              848  LOAD_FAST                'density_scale'
              850  BUILD_TUPLE_2         2 
              852  LOAD_STR                 'Densities log/linear'
              854  LOAD_CONST               ('ax', 'logx', 'ylim', 'title')
              856  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              858  POP_TOP          

 L.1353       860  LOAD_FAST                'axiter'
              862  LOAD_METHOD              grid
              864  LOAD_CONST               1
              866  CALL_METHOD_1         1  '1 positional argument'
              868  STORE_FAST               'ax'

 L.1354       870  LOAD_FAST                'temp'
              872  LOAD_ATTR                plot
              874  LOAD_FAST                'ax'
              876  LOAD_CONST               True
              878  LOAD_CONST               0
              880  LOAD_FAST                'large_loss_scale'
              882  BUILD_TUPLE_2         2 
              884  LOAD_STR                 'Densities linear/log'
              886  LOAD_CONST               ('ax', 'logy', 'xlim', 'title')
              888  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              890  POP_TOP          

 L.1356       892  LOAD_FAST                'axiter'
              894  LOAD_METHOD              grid
              896  LOAD_CONST               1
              898  CALL_METHOD_1         1  '1 positional argument'
              900  STORE_FAST               'ax'

 L.1357       902  LOAD_FAST                'temp'
              904  LOAD_ATTR                plot
              906  LOAD_FAST                'ax'
              908  LOAD_CONST               True
              910  LOAD_CONST               True
              912  LOAD_STR                 'Densities log/log'
              914  LOAD_CONST               ('ax', 'logx', 'logy', 'title')
              916  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              918  POP_TOP          

 L.1360       920  LOAD_FAST                'D'
              922  LOAD_ATTR                filter
              924  LOAD_STR                 '^exa_[^η]'
              926  LOAD_CONST               ('regex',)
              928  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              930  STORE_FAST               'temp'

 L.1362       932  LOAD_FAST                'temp'
              934  LOAD_ATTR                shape
              936  LOAD_CONST               1
              938  BINARY_SUBSCR    
              940  LOAD_CONST               0
              942  COMPARE_OP               ==
          944_946  POP_JUMP_IF_FALSE   960  'to 960'

 L.1363       948  LOAD_GLOBAL              print
              950  LOAD_STR                 'Update exa before audit plot'
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  POP_TOP          

 L.1364       956  LOAD_CONST               None
              958  RETURN_VALUE     
            960_0  COME_FROM           944  '944'

 L.1366       960  LOAD_FAST                'axiter'
              962  LOAD_METHOD              grid
              964  LOAD_CONST               1
              966  CALL_METHOD_1         1  '1 positional argument'
              968  STORE_FAST               'ax'

 L.1367       970  LOAD_FAST                'temp'
              972  LOAD_ATTR                plot
              974  LOAD_CONST               True
              976  LOAD_FAST                'ax'
              978  LOAD_CONST               0
              980  LOAD_FAST                'large_loss_scale'
              982  BUILD_TUPLE_2         2 
              984  LOAD_CONST               0
              986  LOAD_FAST                'expected_loss_scale'
              988  BUILD_TUPLE_2         2 

 L.1368       990  LOAD_STR                 'Loss Cost by Line: $E(X_i(a))$'
              992  LOAD_CONST               ('legend', 'ax', 'xlim', 'ylim', 'title')
              994  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              996  POP_TOP          

 L.1370       998  LOAD_FAST                'axiter'
             1000  LOAD_METHOD              grid
             1002  LOAD_CONST               1
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  STORE_FAST               'ax'

 L.1371      1008  LOAD_FAST                'temp'
             1010  LOAD_METHOD              diff
             1012  CALL_METHOD_0         0  '0 positional arguments'
             1014  LOAD_ATTR                plot
             1016  LOAD_CONST               True
             1018  LOAD_FAST                'ax'
             1020  LOAD_CONST               0
             1022  LOAD_FAST                'large_loss_scale'
             1024  BUILD_TUPLE_2         2 
             1026  LOAD_CONST               0
             1028  LOAD_FAST                'D'
             1030  LOAD_ATTR                index
             1032  LOAD_CONST               1
             1034  BINARY_SUBSCR    
             1036  BUILD_TUPLE_2         2 

 L.1372      1038  LOAD_STR                 'Change in Loss Cost by Line: $\\nabla E(X_i(a))$'
             1040  LOAD_CONST               ('legend', 'ax', 'xlim', 'ylim', 'title')
             1042  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1044  POP_TOP          

 L.1375      1046  LOAD_GLOBAL              dict
             1048  LOAD_STR                 '$E(X_i/X \\mid X>a)$'

 L.1376      1050  LOAD_STR                 '$E(X_i \\mid X=a)$'

 L.1377      1052  LOAD_STR                 '$E(X_i \\mid X \\leq a)$'

 L.1378      1054  LOAD_STR                 '$E(X_i \\mid X>a)$'
             1056  LOAD_CONST               ('exi_xgta_', 'exeqa_', 'exlea_', 'exgta_')
             1058  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1060  STORE_FAST               'prefix_and_titles'

 L.1379      1062  SETUP_LOOP         1282  'to 1282'
             1064  LOAD_FAST                'prefix_and_titles'
             1066  LOAD_METHOD              keys
             1068  CALL_METHOD_0         0  '0 positional arguments'
             1070  GET_ITER         
             1072  FOR_ITER           1280  'to 1280'
             1074  STORE_FAST               'prefix'

 L.1380      1076  LOAD_STR                 '^'
             1078  LOAD_FAST                'prefix'
             1080  FORMAT_VALUE          0  ''
             1082  LOAD_STR                 '[a-zA-Z]'
             1084  BUILD_STRING_3        3 
             1086  STORE_FAST               'regex'

 L.1381      1088  LOAD_FAST                'axiter'
             1090  LOAD_METHOD              grid
             1092  LOAD_CONST               1
             1094  CALL_METHOD_1         1  '1 positional argument'
             1096  STORE_FAST               'ax'

 L.1382      1098  LOAD_FAST                'D'
             1100  LOAD_ATTR                filter
             1102  LOAD_FAST                'regex'
             1104  LOAD_CONST               ('regex',)
             1106  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1108  LOAD_ATTR                plot
             1110  LOAD_FAST                'ax'
             1112  LOAD_CONST               0
             1114  LOAD_FAST                'large_loss_scale'
             1116  BUILD_TUPLE_2         2 
             1118  LOAD_CONST               ('ax', 'xlim')
             1120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1122  POP_TOP          

 L.1383      1124  LOAD_FAST                'prefix'
             1126  LOAD_STR                 'exgta_'
             1128  COMPARE_OP               ==
         1130_1132  POP_JUMP_IF_FALSE  1144  'to 1144'

 L.1384      1134  LOAD_FAST                'ax'
             1136  LOAD_METHOD              set_title
             1138  LOAD_STR                 '$E(X_i \\mid X > a)$ by line and total'
             1140  CALL_METHOD_1         1  '1 positional argument'
             1142  POP_TOP          
           1144_0  COME_FROM          1130  '1130'

 L.1385      1144  LOAD_FAST                'prefix'
             1146  LOAD_METHOD              find
             1148  LOAD_STR                 'xi_x'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  LOAD_CONST               0
             1154  COMPARE_OP               >
         1156_1158  POP_JUMP_IF_FALSE  1204  'to 1204'

 L.1387      1160  LOAD_FAST                'D'
             1162  LOAD_ATTR                filter
             1164  LOAD_FAST                'regex'
             1166  LOAD_CONST               ('regex',)
             1168  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1170  LOAD_ATTR                sum
             1172  LOAD_CONST               1
             1174  LOAD_CONST               ('axis',)
             1176  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1178  LOAD_ATTR                plot
             1180  LOAD_FAST                'ax'
             1182  LOAD_STR                 'calced total'
             1184  LOAD_CONST               ('ax', 'label')
             1186  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1188  POP_TOP          

 L.1388      1190  LOAD_FAST                'ax'
             1192  LOAD_METHOD              set_ylim
             1194  LOAD_CONST               -0.05
             1196  LOAD_CONST               1.05
             1198  CALL_METHOD_2         2  '2 positional arguments'
             1200  POP_TOP          
             1202  JUMP_FORWARD       1250  'to 1250'
           1204_0  COME_FROM          1156  '1156'

 L.1389      1204  LOAD_FAST                'prefix'
             1206  LOAD_STR                 'exgta_'
             1208  COMPARE_OP               ==
         1210_1212  POP_JUMP_IF_TRUE   1224  'to 1224'
             1214  LOAD_FAST                'prefix'
             1216  LOAD_STR                 'exeqa_'
             1218  COMPARE_OP               ==
         1220_1222  POP_JUMP_IF_FALSE  1238  'to 1238'
           1224_0  COME_FROM          1210  '1210'

 L.1391      1224  LOAD_FAST                'ax'
             1226  LOAD_METHOD              set_ylim
             1228  LOAD_CONST               0
             1230  LOAD_FAST                'large_loss_scale'
             1232  CALL_METHOD_2         2  '2 positional arguments'
             1234  POP_TOP          
             1236  JUMP_FORWARD       1250  'to 1250'
           1238_0  COME_FROM          1220  '1220'

 L.1394      1238  LOAD_FAST                'ax'
             1240  LOAD_METHOD              set_ylim
             1242  LOAD_CONST               0
             1244  LOAD_FAST                'expected_loss_scale'
             1246  CALL_METHOD_2         2  '2 positional arguments'
             1248  POP_TOP          
           1250_0  COME_FROM          1236  '1236'
           1250_1  COME_FROM          1202  '1202'

 L.1395      1250  LOAD_FAST                'ax'
             1252  LOAD_METHOD              set_title
             1254  LOAD_FAST                'prefix_and_titles'
             1256  LOAD_FAST                'prefix'
             1258  BINARY_SUBSCR    
             1260  CALL_METHOD_1         1  '1 positional argument'
             1262  POP_TOP          

 L.1396      1264  LOAD_FAST                'ax'
             1266  LOAD_ATTR                legend
             1268  LOAD_CONST               False
             1270  LOAD_CONST               ('frameon',)
             1272  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1274  POP_TOP          
         1276_1278  JUMP_BACK          1072  'to 1072'
             1280  POP_BLOCK        
           1282_0  COME_FROM_LOOP     1062  '1062'

 L.1399      1282  LOAD_GLOBAL              next
             1284  LOAD_FAST                'axiter'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  STORE_FAST               'ax'

 L.1401      1290  LOAD_FAST                'ax'
             1292  LOAD_ATTR                plot
             1294  LOAD_FAST                'D'
             1296  LOAD_ATTR                loc
             1298  LOAD_CONST               None
             1300  LOAD_CONST               None
             1302  BUILD_SLICE_2         2 
             1304  LOAD_STR                 'p_total'
             1306  BUILD_TUPLE_2         2 
             1308  BINARY_SUBSCR    
             1310  LOAD_METHOD              cumsum
             1312  CALL_METHOD_0         0  '0 positional arguments'
             1314  LOAD_FAST                'D'
             1316  LOAD_ATTR                loss
             1318  LOAD_STR                 'total'
             1320  LOAD_CONST               ('label',)
             1322  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1324  POP_TOP          

 L.1402      1326  SETUP_LOOP         1396  'to 1396'
             1328  LOAD_FAST                'D'
             1330  LOAD_ATTR                filter
             1332  LOAD_STR                 '^p_[^t]'
             1334  LOAD_CONST               ('regex',)
             1336  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1338  LOAD_ATTR                columns
             1340  GET_ITER         
             1342  FOR_ITER           1394  'to 1394'
             1344  STORE_FAST               'c'

 L.1403      1346  LOAD_FAST                'ax'
             1348  LOAD_ATTR                plot
             1350  LOAD_FAST                'D'
             1352  LOAD_ATTR                loc
             1354  LOAD_CONST               None
             1356  LOAD_CONST               None
             1358  BUILD_SLICE_2         2 
             1360  LOAD_FAST                'c'
             1362  BUILD_TUPLE_2         2 
             1364  BINARY_SUBSCR    
             1366  LOAD_METHOD              cumsum
             1368  CALL_METHOD_0         0  '0 positional arguments'
             1370  LOAD_FAST                'D'
             1372  LOAD_ATTR                loss
             1374  LOAD_FAST                'c'
             1376  LOAD_CONST               2
             1378  LOAD_CONST               None
             1380  BUILD_SLICE_2         2 
             1382  BINARY_SUBSCR    
             1384  LOAD_CONST               ('label',)
             1386  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1388  POP_TOP          
         1390_1392  JUMP_BACK          1342  'to 1342'
             1394  POP_BLOCK        
           1396_0  COME_FROM_LOOP     1326  '1326'

 L.1404      1396  LOAD_FAST                'ax'
             1398  LOAD_ATTR                legend
             1400  LOAD_CONST               False
             1402  LOAD_CONST               ('frameon',)
             1404  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1406  POP_TOP          

 L.1405      1408  LOAD_FAST                'ax'
             1410  LOAD_METHOD              set_title
             1412  LOAD_STR                 'Lee Diagram'
             1414  CALL_METHOD_1         1  '1 positional argument'
             1416  POP_TOP          

 L.1406      1418  LOAD_FAST                'ax'
             1420  LOAD_METHOD              set_xlim
             1422  LOAD_CONST               0
             1424  LOAD_CONST               1
             1426  CALL_METHOD_2         2  '2 positional arguments'
             1428  POP_TOP          

 L.1407      1430  LOAD_FAST                'ax'
             1432  LOAD_METHOD              set_ylim
             1434  LOAD_CONST               0
             1436  LOAD_FAST                'large_loss_scale'
             1438  CALL_METHOD_2         2  '2 positional arguments'
             1440  POP_TOP          
         1442_1444  JUMP_FORWARD       2312  'to 2312'
           1446_0  COME_FROM           670  '670'

 L.1409      1446  LOAD_FAST                'kind'
             1448  LOAD_STR                 'priority'
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1766  'to 1766'

 L.1410      1456  LOAD_FAST                'self'
             1458  LOAD_METHOD              q
             1460  LOAD_FAST                'p'
             1462  CALL_METHOD_1         1  '1 positional argument'
             1464  STORE_FAST               'xmax'

 L.1411      1466  LOAD_GLOBAL              len
             1468  LOAD_FAST                'self'
             1470  LOAD_ATTR                line_names_ex
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  STORE_FAST               'n_lines'

 L.1412      1476  LOAD_CONST               3
             1478  LOAD_CONST               2
             1480  LOAD_FAST                'n_lines'
             1482  BINARY_MULTIPLY  
             1484  BINARY_ADD       
             1486  STORE_FAST               'n_plots'

 L.1413      1488  LOAD_FAST                'axiter'
             1490  LOAD_CONST               None
             1492  COMPARE_OP               is
         1494_1496  POP_JUMP_IF_FALSE  1514  'to 1514'

 L.1414      1498  LOAD_GLOBAL              axiter_factory
             1500  LOAD_FAST                'axiter'
             1502  LOAD_FAST                'n_plots'
             1504  LOAD_FAST                'figsize'
             1506  LOAD_FAST                'height'
             1508  LOAD_FAST                'aspect'
             1510  CALL_FUNCTION_5       5  '5 positional arguments'
             1512  STORE_FAST               'axiter'
           1514_0  COME_FROM          1494  '1494'

 L.1416      1514  SETUP_LOOP         1600  'to 1600'
             1516  LOAD_GLOBAL              dict
             1518  LOAD_STR                 'LEV'
             1520  LOAD_STR                 '$E(X_i\\mid X=a)$'
             1522  LOAD_STR                 '$E_2(X_i \\mid X=a)$'
             1524  LOAD_CONST               ('lev_', 'exa_', 'e2pri_')
             1526  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1528  LOAD_METHOD              items
             1530  CALL_METHOD_0         0  '0 positional arguments'
             1532  GET_ITER         
             1534  FOR_ITER           1598  'to 1598'
             1536  UNPACK_SEQUENCE_2     2 
             1538  STORE_FAST               'prefix'
             1540  STORE_FAST               'fmt'

 L.1417      1542  LOAD_FAST                'axiter'
             1544  LOAD_METHOD              grid
             1546  LOAD_CONST               1
             1548  CALL_METHOD_1         1  '1 positional argument'
             1550  STORE_FAST               'ax'

 L.1418      1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                density_df
             1556  LOAD_ATTR                filter
             1558  LOAD_FAST                'prefix'
             1560  FORMAT_VALUE          0  ''
             1562  LOAD_CONST               ('regex',)
             1564  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1566  LOAD_ATTR                plot
             1568  LOAD_FAST                'ax'
             1570  LOAD_CONST               0
             1572  LOAD_FAST                'xmax'
             1574  BUILD_TUPLE_2         2 

 L.1419      1576  LOAD_FAST                'fmt'
             1578  LOAD_CONST               ('ax', 'xlim', 'title')
             1580  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1582  POP_TOP          

 L.1420      1584  LOAD_FAST                'ax'
             1586  LOAD_METHOD              set_xlabel
             1588  LOAD_STR                 'Capital assets'
             1590  CALL_METHOD_1         1  '1 positional argument'
             1592  POP_TOP          
         1594_1596  JUMP_BACK          1534  'to 1534'
             1598  POP_BLOCK        
           1600_0  COME_FROM_LOOP     1514  '1514'

 L.1422      1600  SETUP_LOOP         1686  'to 1686'
             1602  LOAD_FAST                'self'
             1604  LOAD_ATTR                line_names
             1606  GET_ITER         
             1608  FOR_ITER           1684  'to 1684'
             1610  STORE_FAST               'line'

 L.1423      1612  LOAD_FAST                'axiter'
             1614  LOAD_METHOD              grid
             1616  LOAD_CONST               1
             1618  CALL_METHOD_1         1  '1 positional argument'
             1620  STORE_FAST               'ax'

 L.1424      1622  LOAD_FAST                'self'
             1624  LOAD_ATTR                density_df
             1626  LOAD_ATTR                filter
             1628  LOAD_STR                 '(lev|exa|e2pri)_'
             1630  LOAD_FAST                'line'
             1632  FORMAT_VALUE          0  ''
             1634  LOAD_STR                 '$'
             1636  BUILD_STRING_3        3 
             1638  LOAD_CONST               ('regex',)
             1640  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1642  LOAD_ATTR                plot
             1644  LOAD_FAST                'ax'
             1646  LOAD_CONST               0
             1648  LOAD_FAST                'xmax'
             1650  BUILD_TUPLE_2         2 

 L.1425      1652  LOAD_FAST                'line'
             1654  LOAD_METHOD              title
             1656  CALL_METHOD_0         0  '0 positional arguments'
             1658  FORMAT_VALUE          0  ''
             1660  LOAD_STR                 ' by Priority'
             1662  BUILD_STRING_2        2 
             1664  LOAD_CONST               ('ax', 'xlim', 'title')
             1666  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1668  POP_TOP          

 L.1426      1670  LOAD_FAST                'ax'
             1672  LOAD_METHOD              set_xlabel
             1674  LOAD_STR                 'Capital assets'
             1676  CALL_METHOD_1         1  '1 positional argument'
             1678  POP_TOP          
         1680_1682  JUMP_BACK          1608  'to 1608'
             1684  POP_BLOCK        
           1686_0  COME_FROM_LOOP     1600  '1600'

 L.1427      1686  SETUP_LOOP         1762  'to 1762'
             1688  LOAD_FAST                'self'
             1690  LOAD_ATTR                line_names_ex
             1692  GET_ITER         
             1694  FOR_ITER           1760  'to 1760'
             1696  STORE_FAST               'col'

 L.1428      1698  LOAD_FAST                'axiter'
             1700  LOAD_METHOD              grid
             1702  LOAD_CONST               1
             1704  CALL_METHOD_1         1  '1 positional argument'
             1706  STORE_FAST               'ax'

 L.1429      1708  LOAD_FAST                'self'
             1710  LOAD_ATTR                density_df
             1712  LOAD_ATTR                filter
             1714  LOAD_STR                 'epd_[012]_'
             1716  LOAD_FAST                'col'
             1718  FORMAT_VALUE          0  ''
             1720  BUILD_STRING_2        2 
             1722  LOAD_CONST               ('regex',)
             1724  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1726  LOAD_ATTR                plot
             1728  LOAD_FAST                'ax'
             1730  LOAD_CONST               0
             1732  LOAD_FAST                'xmax'
             1734  BUILD_TUPLE_2         2 

 L.1430      1736  LOAD_FAST                'col'
             1738  LOAD_METHOD              title
             1740  CALL_METHOD_0         0  '0 positional arguments'
             1742  FORMAT_VALUE          0  ''
             1744  LOAD_STR                 ' EPDs'
             1746  BUILD_STRING_2        2 
             1748  LOAD_CONST               True
             1750  LOAD_CONST               ('ax', 'xlim', 'title', 'logy')
             1752  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1754  POP_TOP          
         1756_1758  JUMP_BACK          1694  'to 1694'
             1760  POP_BLOCK        
           1762_0  COME_FROM_LOOP     1686  '1686'
         1762_1764  JUMP_FORWARD       2312  'to 2312'
           1766_0  COME_FROM          1452  '1452'

 L.1432      1766  LOAD_FAST                'kind'
             1768  LOAD_STR                 'collateral'
             1770  COMPARE_OP               ==
         1772_1774  POP_JUMP_IF_FALSE  2282  'to 2282'

 L.1433      1776  LOAD_FAST                'line'
             1778  LOAD_STR                 ''
             1780  COMPARE_OP               !=
         1782_1784  POP_JUMP_IF_FALSE  1796  'to 1796'
             1786  LOAD_FAST                'line'
             1788  LOAD_STR                 'all'
             1790  COMPARE_OP               !=
         1792_1794  POP_JUMP_IF_TRUE   1800  'to 1800'
           1796_0  COME_FROM          1782  '1782'
             1796  LOAD_ASSERT              AssertionError
             1798  RAISE_VARARGS_1       1  'exception instance'
           1800_0  COME_FROM          1792  '1792'

 L.1434      1800  LOAD_FAST                'axiter'
             1802  LOAD_CONST               None
             1804  COMPARE_OP               is
         1806_1808  POP_JUMP_IF_FALSE  1826  'to 1826'

 L.1435      1810  LOAD_GLOBAL              axiter_factory
             1812  LOAD_FAST                'axiter'
             1814  LOAD_CONST               2
             1816  LOAD_FAST                'figsize'
             1818  LOAD_FAST                'height'
             1820  LOAD_FAST                'aspect'
             1822  CALL_FUNCTION_5       5  '5 positional arguments'
             1824  STORE_FAST               'axiter'
           1826_0  COME_FROM          1806  '1806'

 L.1437      1826  LOAD_GLOBAL              cm
             1828  LOAD_ATTR                BuGn
             1830  STORE_FAST               'cmap'

 L.1438      1832  LOAD_FAST                'a'
             1834  LOAD_CONST               0
             1836  COMPARE_OP               ==
         1838_1840  POP_JUMP_IF_FALSE  1852  'to 1852'

 L.1439      1842  LOAD_FAST                'self'
             1844  LOAD_METHOD              q
             1846  LOAD_FAST                'p'
             1848  CALL_METHOD_1         1  '1 positional argument'
             1850  STORE_FAST               'a'
           1852_0  COME_FROM          1838  '1838'

 L.1440      1852  LOAD_FAST                'self'
             1854  LOAD_ATTR                density_df
             1856  LOAD_ATTR                loc
             1858  LOAD_CONST               0
             1860  LOAD_FAST                'a'
             1862  BUILD_SLICE_2         2 
             1864  LOAD_STR                 'p_'
             1866  LOAD_FAST                'line'
             1868  FORMAT_VALUE          0  ''
             1870  BUILD_STRING_2        2 
             1872  BUILD_TUPLE_2         2 
             1874  BINARY_SUBSCR    
             1876  LOAD_ATTR                values
             1878  STORE_FAST               'pline'

 L.1441      1880  LOAD_FAST                'self'
             1882  LOAD_ATTR                density_df
             1884  LOAD_ATTR                loc
             1886  LOAD_CONST               0
             1888  LOAD_FAST                'a'
             1890  BUILD_SLICE_2         2 
             1892  LOAD_STR                 'ημ_'
             1894  LOAD_FAST                'line'
             1896  FORMAT_VALUE          0  ''
             1898  BUILD_STRING_2        2 
             1900  BUILD_TUPLE_2         2 
             1902  BINARY_SUBSCR    
             1904  LOAD_ATTR                values
             1906  STORE_FAST               'notline'

 L.1442      1908  LOAD_FAST                'self'
             1910  LOAD_ATTR                density_df
             1912  LOAD_ATTR                loc
             1914  LOAD_CONST               0
             1916  LOAD_FAST                'a'
             1918  BUILD_SLICE_2         2 
             1920  LOAD_STR                 'loss'
             1922  BUILD_TUPLE_2         2 
             1924  BINARY_SUBSCR    
             1926  LOAD_ATTR                values
             1928  STORE_FAST               'xs'

 L.1443      1930  LOAD_FAST                'pline'
             1932  LOAD_ATTR                shape
             1934  LOAD_CONST               0
             1936  BINARY_SUBSCR    
             1938  STORE_FAST               'N'

 L.1444      1940  LOAD_GLOBAL              np
             1942  LOAD_METHOD              matmul
             1944  LOAD_FAST                'notline'
             1946  LOAD_METHOD              reshape
             1948  LOAD_FAST                'N'
             1950  LOAD_CONST               1
             1952  BUILD_TUPLE_2         2 
             1954  CALL_METHOD_1         1  '1 positional argument'
             1956  LOAD_FAST                'pline'
             1958  LOAD_METHOD              reshape
             1960  LOAD_CONST               1
             1962  LOAD_FAST                'N'
             1964  BUILD_TUPLE_2         2 
             1966  CALL_METHOD_1         1  '1 positional argument'
             1968  CALL_METHOD_2         2  '2 positional arguments'
             1970  STORE_FAST               'biv'

 L.1445      1972  LOAD_FAST                'biv'
             1974  STORE_FAST               'biv'

 L.1446  1976_1978  SETUP_LOOP         2312  'to 2312'
             1980  LOAD_CONST               (1, 0.05)
             1982  GET_ITER         
         1984_1986  FOR_ITER           2278  'to 2278'
             1988  STORE_FAST               'rho'

 L.1447      1990  LOAD_GLOBAL              next
             1992  LOAD_FAST                'axiter'
             1994  CALL_FUNCTION_1       1  '1 positional argument'
             1996  STORE_FAST               'ax'

 L.1448      1998  LOAD_FAST                'ax'
             2000  LOAD_ATTR                imshow
             2002  LOAD_FAST                'biv'
             2004  LOAD_FAST                'rho'
             2006  BINARY_POWER     
             2008  BUILD_TUPLE_1         1 
             2010  LOAD_FAST                'cmap'
             2012  LOAD_STR                 'lower'
             2014  LOAD_CONST               0
             2016  LOAD_FAST                'xs'
             2018  LOAD_CONST               -1
             2020  BINARY_SUBSCR    
             2022  LOAD_CONST               0
             2024  LOAD_FAST                'xs'
             2026  LOAD_CONST               -1
             2028  BINARY_SUBSCR    
             2030  BUILD_LIST_4          4 

 L.1449      2032  LOAD_STR                 'nearest'
             2034  LOAD_CONST               ('cmap', 'origin', 'extent', 'interpolation')
             2036  BUILD_CONST_KEY_MAP_4     4 
             2038  LOAD_FAST                'kwargs'
             2040  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             2042  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             2044  POP_TOP          

 L.1450      2046  LOAD_FAST                'a'
             2048  LOAD_FAST                'c'
             2050  BINARY_SUBTRACT  
             2052  STORE_FAST               'cy'

 L.1451      2054  LOAD_FAST                'ax'
             2056  LOAD_ATTR                plot
             2058  LOAD_FAST                'c'
             2060  LOAD_FAST                'c'
             2062  BUILD_TUPLE_2         2 
             2064  LOAD_FAST                'a'
             2066  LOAD_FAST                'c'
             2068  BINARY_SUBTRACT  
             2070  LOAD_FAST                'xs'
             2072  LOAD_CONST               -1
             2074  BINARY_SUBSCR    
             2076  BUILD_TUPLE_2         2 
             2078  LOAD_STR                 'k'
             2080  LOAD_CONST               0.5
             2082  LOAD_CONST               ('linewidth',)
             2084  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2086  POP_TOP          

 L.1452      2088  LOAD_FAST                'ax'
             2090  LOAD_ATTR                plot
             2092  LOAD_CONST               0
             2094  LOAD_FAST                'a'
             2096  BUILD_TUPLE_2         2 
             2098  LOAD_FAST                'a'
             2100  LOAD_CONST               0
             2102  BUILD_TUPLE_2         2 
             2104  LOAD_STR                 'k'
             2106  LOAD_CONST               0.5
             2108  LOAD_CONST               ('linewidth',)
             2110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2112  POP_TOP          

 L.1453      2114  LOAD_FAST                'c'
             2116  LOAD_CONST               0
             2118  COMPARE_OP               >
         2120_2122  POP_JUMP_IF_FALSE  2170  'to 2170'

 L.1454      2124  LOAD_FAST                'ax'
             2126  LOAD_ATTR                plot
             2128  LOAD_FAST                'c'
             2130  LOAD_FAST                'xs'
             2132  LOAD_CONST               -1
             2134  BINARY_SUBSCR    
             2136  BUILD_TUPLE_2         2 
             2138  LOAD_FAST                'cy'
             2140  LOAD_FAST                'xs'
             2142  LOAD_CONST               -1
             2144  BINARY_SUBSCR    
             2146  LOAD_FAST                'a'
             2148  LOAD_FAST                'c'
             2150  BINARY_TRUE_DIVIDE
             2152  LOAD_CONST               1
             2154  BINARY_SUBTRACT  
             2156  BINARY_MULTIPLY  
             2158  BUILD_TUPLE_2         2 
             2160  LOAD_STR                 'k'
             2162  LOAD_CONST               0.5
             2164  LOAD_CONST               ('linewidth',)
             2166  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2168  POP_TOP          
           2170_0  COME_FROM          2120  '2120'

 L.1455      2170  LOAD_FAST                'ax'
             2172  LOAD_ATTR                plot
             2174  LOAD_CONST               0
             2176  LOAD_FAST                'c'
             2178  LOAD_FAST                'c'
             2180  BUILD_TUPLE_3         3 
             2182  LOAD_FAST                'a'
             2184  LOAD_FAST                'c'
             2186  BINARY_SUBTRACT  
             2188  LOAD_FAST                'a'
             2190  LOAD_FAST                'c'
             2192  BINARY_SUBTRACT  
             2194  LOAD_CONST               0
             2196  BUILD_TUPLE_3         3 
             2198  LOAD_STR                 'k'
             2200  LOAD_STR                 '--'
             2202  LOAD_CONST               0.25
             2204  LOAD_CONST               ('c', 'ls', 'linewidth')
             2206  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2208  POP_TOP          

 L.1456      2210  LOAD_FAST                'ax'
             2212  LOAD_METHOD              set_xlim
             2214  LOAD_CONST               0
             2216  LOAD_FAST                'xs'
             2218  LOAD_CONST               -1
             2220  BINARY_SUBSCR    
             2222  CALL_METHOD_2         2  '2 positional arguments'
             2224  POP_TOP          

 L.1457      2226  LOAD_FAST                'ax'
             2228  LOAD_METHOD              set_ylim
             2230  LOAD_CONST               0
             2232  LOAD_FAST                'xs'
             2234  LOAD_CONST               -1
             2236  BINARY_SUBSCR    
             2238  CALL_METHOD_2         2  '2 positional arguments'
             2240  POP_TOP          

 L.1458      2242  LOAD_FAST                'ax'
             2244  LOAD_METHOD              set_xlabel
             2246  LOAD_STR                 'Line '
             2248  LOAD_FAST                'line'
           2250_0  COME_FROM           600  '600'
             2250  FORMAT_VALUE          0  ''
             2252  BUILD_STRING_2        2 
             2254  CALL_METHOD_1         1  '1 positional argument'
             2256  POP_TOP          

 L.1459      2258  LOAD_FAST                'ax'
             2260  LOAD_METHOD              set_ylabel
             2262  LOAD_STR                 'Not '
             2264  LOAD_FAST                'line'
             2266  FORMAT_VALUE          0  ''
             2268  BUILD_STRING_2        2 
             2270  CALL_METHOD_1         1  '1 positional argument'
             2272  POP_TOP          
         2274_2276  JUMP_BACK          1984  'to 1984'
             2278  POP_BLOCK        
             2280  JUMP_FORWARD       2312  'to 2312'
           2282_0  COME_FROM          1772  '1772'

 L.1462      2282  LOAD_GLOBAL              logger
             2284  LOAD_METHOD              error
             2286  LOAD_STR                 'Portfolio.plot | Unknown plot type '
             2288  LOAD_FAST                'kind'
             2290  FORMAT_VALUE          0  ''
             2292  BUILD_STRING_2        2 
             2294  CALL_METHOD_1         1  '1 positional argument'
           2296_0  COME_FROM           646  '646'
             2296  POP_TOP          

 L.1463      2298  LOAD_GLOBAL              ValueError
             2300  LOAD_STR                 'Portfolio.plot unknown plot type '
             2302  LOAD_FAST                'kind'
             2304  FORMAT_VALUE          0  ''
             2306  BUILD_STRING_2        2 
             2308  CALL_FUNCTION_1       1  '1 positional argument'
             2310  RAISE_VARARGS_1       1  'exception instance'
           2312_0  COME_FROM          2280  '2280'
           2312_1  COME_FROM_LOOP     1976  '1976'
           2312_2  COME_FROM          1762  '1762'
           2312_3  COME_FROM          1442  '1442'
           2312_4  COME_FROM           660  '660'
           2312_5  COME_FROM           238  '238'

 L.1465      2312  LOAD_FAST                'do_tight'
         2314_2316  POP_JUMP_IF_FALSE  2354  'to 2354'

 L.1466      2318  LOAD_FAST                'axiter'
             2320  LOAD_METHOD              tidy
             2322  CALL_METHOD_0         0  '0 positional arguments'
             2324  POP_TOP          

 L.1467      2326  LOAD_GLOBAL              suptitle_and_tight
             2328  LOAD_FAST                'kind'
             2330  LOAD_METHOD              title
             2332  CALL_METHOD_0         0  '0 positional arguments'
             2334  FORMAT_VALUE          0  ''
             2336  LOAD_STR                 ' Plots for '
             2338  LOAD_FAST                'self'
             2340  LOAD_ATTR                name
             2342  LOAD_METHOD              title
             2344  CALL_METHOD_0         0  '0 positional arguments'
             2346  FORMAT_VALUE          0  ''
             2348  BUILD_STRING_3        3 
             2350  CALL_FUNCTION_1       1  '1 positional argument'
             2352  POP_TOP          
           2354_0  COME_FROM          2314  '2314'

Parse error at or near `COME_FROM' instruction at offset 2250_0

    def uat_interpolation_functions(self, a0, e0):
        """
        Perform quick audit of interpolation functions

        :param a0: base assets
        :param e0: base epd
        :return:
        """
        temp = pd.DataFrame(columns=['line', 'priority', 'epd', 'a from e', 'assets', 'e from a'])
        e2a = self.epd_2_assets
        a2e = self.assets_2_epd
        for i in range(3):
            for c in self.line_names + ['total'] + ['not ' + i for i in self.line_names]:
                if (c, i) in a2e:
                    e = a2e[(c, i)](a0)
                    a = e2a[(c, i)](e0)
                    temp.loc[c + '_' + str(i), :] = (c, i, e, e2a[(c, i)](e), a, a2e[(c, i)](a))

        display(temp.style)

    def add_exa(self, df, details, ft_nots=None):
        """
        Use fft to add exa_XXX = E(X_i | X=a) to each dist

        also add exlea = E(X_i | X <= a) = sum_{x<=a} exa(x)*f(x) where f is for the total
        ie. self.density_df['exlea_attrit'] = np.cumsum( self.density_df.exa_attrit *
        self.density_df.p_total) / self.density_df.F

        and add exgta = E(X_i | X>a) since E(X) = E(X | X<= a)F(a) + E(X | X>a)S(a) we have
        exgta = (ex - exlea F) / S

        and add the actual expected losses (not theoretical) the empirical amount:
        self.density_df['e_attrit'] =  np.sum( self.density_df.p_attrit * self.density_df.loss)

        Mid point adjustment is handled by the example creation routines
        self.density_df.loss = self.density_df.loss - bs/2

        **YOU CANNOT HAVE A LINE with a name starting t!!!**

        See LCA_Examples for original code

        Alternative approach to exa: use UC=unconditional versions of exlea and exi_xgta:

        * exleaUC = np.cumsum(port.density_df['exeqa_' + col] * port.density_df.p_total)  # unconditional
        * exixgtaUC =np.cumsum(  self.density_df.loc[::-1, 'exeqa_' + col] / self.density_df.loc[::-1, 'loss']
          * self.density_df.loc[::-1, 'p_total'] )
        * exa = exleaUC + exixgtaUC * self.density_df.loss

        :param df: data frame to add to. Initially add_exa was only called by update and wrote to self.density_df. But now
        it is called by gradient too which writes to gradient_df, so we need to pass in this argument
        :param details: True = include everything; False = do not include junk around epd etc

        :param ft_nots: FFTs of the not lines (computed in gradients) so you don't round trip an FFT; gradients needs
        to recompute all the not lines each time around and it is stilly to do that twice

        """

        def minus_arg_wrapper(a_func):

            def new_fun(x):
                try:
                    x = a_func(-x)
                except ValueError:
                    x = 999

                return x

            return new_fun

        def minus_ans_wrapper(a_func):

            def new_fun(x):
                try:
                    x = -a_func(x)
                except ValueError:
                    x = 999

                return x

            return new_fun

        cut_eps = np.finfo(np.float).eps
        bs = self.bs
        if not np.all(df.p_total >= 0):
            first_neg = np.argwhere((df.p_total < 0).to_numpy()).min()
            logger.warning(f"CPortfolio.add_exa | p_total has a negative value starting at {first_neg}; NOT setting to zero...")
        else:
            sum_p_total = df.p_total.sum()
            logger.info(f"CPortfolio.add_exa | {self.name}: sum of p_total is 1 - {1 - sum_p_total:12.8e} NOT RESCALING")
            df['F'] = np.cumsum(df.p_total)
            df['S'] = np.hstack((df.p_total.to_numpy()[:0:-1].cumsum()[::-1],
             min(df.p_total.iloc[(-1)], max(0, 1.0 - df.p_total.sum()))))
            logger.info(f"CPortfolio.add_exa | {self.name}: S <= 0 values has length {len(np.argwhere((df.S <= 0).to_numpy()))}")
            df['exa_total'] = self.cumintegral(df['S'])
            df.loc[:, 'lev_total'] = df['exa_total']
            df['exlea_total'] = (df.exa_total - df.loss * df.S) / df.F
            n_ = df.shape[0]
            if n_ < 1100:
                mult = 1
            else:
                if n_ < 15000:
                    mult = 10
                else:
                    mult = 100
            loss_max = df[['loss', 'exlea_total']].query(' exlea_total>loss ').loss.max()
            if np.isnan(loss_max):
                loss_max = 0
            else:
                loss_max += mult * bs
        df.loc[0:loss_max, 'exlea_total'] = np.nan
        df['e_total'] = np.sum(df.p_total * df.loss)
        df.loc[:, 'epd_0_total'] = np.maximum(0, df.loc[:, 'e_total'] - df.loc[:, 'lev_total']) / df.loc[:, 'e_total']
        df['exgta_total'] = df.loss + (df.e_total - df.exa_total) / df.S
        df['exeqa_total'] = df.loss
        index_inv = 1.0 / np.array(df.index)
        df['e1xi_1gta_total'] = (df['p_total'] * index_inv).iloc[::-1].cumsum()

        def loc_ft(x):
            return ft(x, 1, None)

        def loc_ift(x):
            return ift(x, 1, None)

        Seq0 = df.S == 0
        for col in self.line_names:
            if ft_nots is None:
                df['exeqa_' + col] = np.real(loc_ift(loc_ft(df.loss * df[('p_' + col)]) * loc_ft(df[('ημ_' + col)]))) / df.p_total
            else:
                df['exeqa_' + col] = np.real(loc_ift(loc_ft(df.loss * df[('p_' + col)]) * ft_nots[col])) / df.p_total
            df.loc[(df.p_total < cut_eps, 'exeqa_' + col)] = 0
            df['exeqa_ημ_' + col] = np.real(loc_ift(loc_ft(df.loss * df[('ημ_' + col)]) * loc_ft(df[('p_' + col)]))) / df.p_total
            df.loc[(df.p_total < cut_eps, 'exeqa_ημ_' + col)] = 0
            stemp = 1 - df.loc[:, 'p_' + col].cumsum()
            df['lev_' + col] = self.cumintegral(stemp)
            if details:
                df['e2pri_' + col] = np.real(loc_ift(loc_ft(df[('lev_' + col)]) * loc_ft(df[('ημ_' + col)])))
            stemp = 1 - df.loc[:, 'ημ_' + col].cumsum()
            df['lev_ημ_' + col] = self.cumintegral(stemp)
            temp = np.cumsum(df[('exeqa_' + col)] * df.p_total)
            df['exlea_' + col] = temp / df.F
            df.loc[0:loss_max, 'exlea_' + col] = 0
            temp_not = np.cumsum(df[('exeqa_ημ_' + col)] * df.p_total)
            df['exlea_ημ_' + col] = temp_not / df.F
            df.loc[0:loss_max, 'exlea_ημ_' + col] = 0
            df['e_' + col] = np.sum(df[('p_' + col)] * df.loss)
            df['e_ημ_' + col] = np.sum(df[('ημ_' + col)] * df.loss)
            df['exgta_' + col] = (df[('e_' + col)] - temp) / df.S
            temp = df.loss.iloc[0]
            df.loss.iloc[0] = 1
            df['exi_x_' + col] = np.sum(df[('exeqa_' + col)] * df.p_total / df.loss)
            temp_xi_x = np.cumsum(df[('exeqa_' + col)] * df.p_total / df.loss)
            df['exi_xlea_' + col] = temp_xi_x / df.F
            df.loc[(0, 'exi_xlea_' + col)] = 0
            df.loc[(df.exlea_total == 0, 'exi_xlea_' + col)] = 0
            df['exi_x_ημ_' + col] = np.sum(df[('exeqa_ημ_' + col)] * df.p_total / df.loss)
            temp_xi_x_not = np.cumsum(df[('exeqa_ημ_' + col)] * df.p_total / df.loss)
            df['exi_xlea_ημ_' + col] = temp_xi_x_not / df.F
            df.loc[(0, 'exi_xlea_ημ_' + col)] = 0
            df.loc[(df.exlea_total == 0, 'exi_xlea_ημ_' + col)] = 0
            df.loss.iloc[0] = temp
            df['exi_xgta_' + col] = (df[f"exeqa_{col}"] / df.loss * df.p_total).shift(-1)[::-1].cumsum() / df.S
            df.loc[(Seq0, 'exi_xgta_' + col)] = 0.0
            df['exi_xgta_ημ_' + col] = (df[('exi_x_ημ_' + col)] - temp_xi_x_not) / df.S
            df.loc[(Seq0, 'exi_xgta_ημ_' + col)] = 0.0
            df['exi_xeqa_' + col] = df[('exeqa_' + col)] / df['loss']
            df.loc[(0, 'exi_xeqa_' + col)] = 0
            df['exi_xeqa_ημ_' + col] = df[('exeqa_ημ_' + col)] / df['loss']
            df.loc[(0, 'exi_xeqa_ημ_' + col)] = 0
            df[f"exa_{col}"] = (df.S * df[('exi_xgta_' + col)]).shift(1, fill_value=0).cumsum() * self.bs
            df['exa_ημ_' + col] = df[('exlea_ημ_' + col)] * df.F + df.loss * df.S * df[('exi_xgta_ημ_' + col)]
            df[f"e1xi_1gta_{col}"] = (df[f"p_{col}"] * index_inv).iloc[::-1].cumsum()
            if details:
                df.loc[:, 'epd_0_' + col] = np.maximum(0, df.loc[:, 'e_' + col] - df.loc[:, 'lev_' + col]) / df.loc[:, 'e_' + col]
                df.loc[:, 'epd_0_ημ_' + col] = np.maximum(0, df.loc[:, 'e_ημ_' + col] - df.loc[:, 'lev_ημ_' + col]) / df.loc[:, 'e_ημ_' + col]
                df.loc[:, 'epd_1_' + col] = np.maximum(0, df.loc[:, 'e_' + col] - df.loc[:, 'exa_' + col]) / df.loc[:, 'e_' + col]
                df.loc[:, 'epd_1_ημ_' + col] = np.maximum(0, df.loc[:, 'e_ημ_' + col] - df.loc[:, 'exa_ημ_' + col]) / df.loc[:, 'e_ημ_' + col]
                df.loc[:, 'epd_2_' + col] = np.maximum(0, df.loc[:, 'e_' + col] - df.loc[:, 'e2pri_' + col]) / df.loc[:, 'e_' + col]
                loss_values = df.loss.values
                for i in (0, 1, 2):
                    epd_values = -df.loc[:, 'epd_{:}_{:}'.format(i, col)].values
                    self.epd_2_assets[(col, i)] = minus_arg_wrapper(interpolate.interp1d(epd_values, loss_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))
                    self.assets_2_epd[(col, i)] = minus_ans_wrapper(interpolate.interp1d(loss_values, epd_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))

                for i in (0, 1):
                    epd_values = -df.loc[:, 'epd_{:}_ημ_{:}'.format(i, col)].values
                    self.epd_2_assets[('not ' + col, i)] = minus_arg_wrapper(interpolate.interp1d(epd_values, loss_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))
                    self.assets_2_epd[('not ' + col, i)] = minus_ans_wrapper(interpolate.interp1d(loss_values, epd_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))

        for metric in ('exi_xlea_', 'exi_xgta_', 'exi_xeqa_'):
            df[metric + 'sum'] = df.filter(regex=(metric + '[^η]')).sum(axis=1)

        if details:
            epd_values = -df.loc[:, 'epd_0_total'].values
            loss_values = df.loss.values
            self.epd_2_assets[('total', 0)] = minus_arg_wrapper(interpolate.interp1d(epd_values, loss_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))
            self.assets_2_epd[('total', 0)] = minus_ans_wrapper(interpolate.interp1d(loss_values, epd_values, kind='linear', assume_sorted=True, fill_value='extrapolate'))

    def calibrate_distortion(self, name, r0=0.0, df=5.5, premium_target=0.0, roe=0.0, assets=0.0, p=0.0, kind='lower', S_column='S'):
        """
        Find transform to hit a premium target given assets of ``assets``.
        Fills in the values in ``g_spec`` and returns params and diagnostics...so
        you can use it either way...more convenient

        :param name: name of distortion
        :param r0:   fixed parameter if applicable
        :param df:  t-distribution degrees of freedom
        :param premium_target: target premium
        :param roe:             or ROE
        :param assets: asset level
        :param p:
        :param S_column: column of density_df to use for calibration (allows routine to be used in other contexts; if
                so used must input a premium_target directly).
        :return:
        """
        if S_column == 'S':
            if assets == 0:
                assert p > 0
                assets = self.q(p, kind)
        else:
            if premium_target == 0:
                assert roe > 0
                el = self.density_df.loc[(assets, 'exa_total')]
                premium_target = (el + roe * assets) / (1 + roe)
            else:
                assets = self.density_df.loss.iloc[(-1)]
            Splus = self.density_df.loc[0:assets, S_column].values
            last_non_zero = np.argwhere(Splus)
            ess_sup = 0
            if len(last_non_zero) == 0:
                last_non_zero = len(Splus) + 1
            else:
                last_non_zero = last_non_zero.max()
            if last_non_zero + 1 < len(Splus):
                S = Splus[:last_non_zero + 1]
                ess_sup = self.density_df.index[(last_non_zero + 1)]
                logger.warning(f"CPortfolio.calibrate_distortion | Mass issues in calibrate_distortion...{name} at {last_non_zero}, loss = {ess_sup}")
            else:
                S = self.density_df.loc[0:assets - self.bs, S_column].values
            if np.all(S > 0):
                if not np.all(S[:-1] >= S[1:]):
                    raise AssertionError
                if name == 'ph':
                    lS = np.log(S)
                    shape = 0.95

                    def f(rho):
                        trho = S ** rho
                        ex = np.sum(trho) * self.bs
                        ex_prime = np.sum(trho * lS) * self.bs
                        return (ex - premium_target, ex_prime)

            elif name == 'wang':
                n = ss.norm()
                shape = 0.95

                def f(lam):
                    temp = n.ppf(S) + lam
                    tlam = n.cdf(temp)
                    ex = np.sum(tlam) * self.bs
                    ex_prime = np.sum(n.pdf(temp)) * self.bs
                    return (ex - premium_target, ex_prime)

            else:
                if name == 'ly':
                    shape = 1.25
                    mass = ess_sup * r0 / (1 + r0)

                    def f(rk):
                        num = r0 + S * (1 + rk)
                        den = 1 + r0 + rk * S
                        tlam = num / den
                        ex = np.sum(tlam) * self.bs + mass
                        ex_prime = np.sum(S * (den ** (-1) - num / den ** 2)) * self.bs
                        return (ex - premium_target, ex_prime)

                else:
                    if name == 'clin':
                        shape = 1
                        mass = ess_sup * r0

                        def f(r):
                            r0_rS = r0 + r * S
                            ex = np.sum(np.minimum(1, r0_rS)) * self.bs + mass
                            ex_prime = np.sum(np.where(r0_rS < 1, S, 0)) * self.bs
                            return (ex - premium_target, ex_prime)

                    else:
                        if name == 'lep':
                            d = r0 / (1 + r0)
                            shape = 0.25
                            rSF = np.sqrt(S * (1 - S))
                            mass = ess_sup * d

                            def f(r):
                                spread = r / (1 + r) - d
                                temp = d + (1 - d) * S + spread * rSF
                                ex = np.sum(np.minimum(1, temp)) * self.bs + mass
                                ex_prime = (1 + r) ** (-2) * np.sum(np.where(temp < 1, rSF, 0)) * self.bs
                                return (ex - premium_target, ex_prime)

                        else:
                            if name == 'tt':
                                t = ss.t(df)
                                shape = 0.95

                                def f(lam):
                                    temp = t.ppf(S) + lam
                                    tlam = t.cdf(temp)
                                    ex = np.sum(tlam) * self.bs
                                    ex_prime = np.sum(t.pdf(temp)) * self.bs
                                    return (ex - premium_target, ex_prime)

                            else:
                                if name == 'cll':
                                    shape = 0.95
                                    lS = np.log(S)
                                    lS[0] = 0
                                    ea = np.exp(r0)

                                    def f(b):
                                        uncapped = ea * S ** b
                                        ex = np.sum(np.minimum(1, uncapped)) * self.bs
                                        ex_prime = np.sum(np.where(uncapped < 1, uncapped * lS, 0)) * self.bs
                                        return (ex - premium_target, ex_prime)

                                else:
                                    if name == 'dual':
                                        shape = 2.0
                                        S = S[(S < 1)]
                                        lS = -np.log(1 - S)

                                        def f(rho):
                                            temp = (1 - S) ** rho
                                            trho = 1 - temp
                                            ex = np.sum(trho) * self.bs
                                            ex_prime = np.sum(temp * lS) * self.bs
                                            return (ex - premium_target, ex_prime)

                                    else:
                                        raise ValueError(f"calibrate_distortion not implemented for {name}")
        i = 0
        fx, fxp = f(shape)
        while abs(fx) > 1e-05 and i < 20:
            shape = shape - fx / fxp
            fx, fxp = f(shape)
            i += 1

        if abs(fx) > 1e-05:
            logger.warning(f"CPortfolio.calibrate_distortion | Questionable convergenge! {name}, target {premium_target} error {fx}, {i} iterations")
        dist = Distortion(name=name, shape=shape, r0=r0, df=df)
        dist.error = fx
        dist.assets = assets
        dist.premium_target = premium_target
        return dist

    def calibrate_distortions(self, LRs=None, ROEs=None, As=None, Ps=None, kind='lower', r0=0.03, df=5.5, strict=True):
        """
        Calibrate assets a to loss ratios LRs and asset levels As (iterables)
        ro for LY, it :math:`ro/(1+ro)` corresponds to a minimum rate on line

        :param LRs:  LR or ROEs given
        :param ROEs: ROEs override LRs
        :param As:  Assets or probs given
        :param Ps: probability levels for quantiles
        :param r0: for distortions that have a min ROL
        :param df: for tt
        :param strict: if True only use distortions with no mass at zero, otherwise
                        use anything reasonable for pricing
        :return:
        """
        ans = pd.DataFrame(columns=[
         '$a$', 'LR', '$S$', '$\\iota$', '$\\delta$', '$\\nu$', '$EL$', '$P$', 'Levg', '$K$',
         'ROE', 'param', 'error', 'method'],
          dtype=(np.float))
        ans = ans.set_index(['$a$', 'LR', 'method'], drop=True)
        if As is None:
            if Ps is None:
                raise ValueError('Must specify assets or quantile probabilities')
            else:
                As = [self.q(p, kind) for p in Ps]
        for a in As:
            exa, S = self.density_df.loc[(a, ['exa_total', 'S'])]
            if ROEs is not None:
                LRs = []
                for r in ROEs:
                    delta = r / (1 + r)
                    nu = 1 - delta
                    prem = nu * exa + delta * a
                    LRs.append(exa / prem)

            for lr in LRs:
                P = exa / lr
                profit = P - exa
                K = a - P
                iota = profit / K
                delta = iota / (1 + iota)
                nu = 1 - delta
                for dname in Distortion.available_distortions(pricing=True, strict=strict):
                    dist = self.calibrate_distortion(name=dname, r0=r0, df=df, premium_target=P, assets=a)
                    ans.loc[(a, lr, dname), :] = [S, iota, delta, nu, exa, P, P / K, K, profit / K,
                     dist.shape, dist.error]

        return ans

    def apply_distortions(self, dist_dict, As=None, Ps=None, kind='lower', axiter=None, num_plots=1):
        """
        Apply a list of distortions, summarize pricing and produce graphical output
        show loss values where  :math:`s_ub > S(loss) > s_lb` by jump

        :param dist_dict: dictionary of Distortion objects
        :param As: input asset levels to consider OR
        :param Ps: input probs (near 1) converted to assets using ``self.q()``
        :param num_plots: 0, 1 or 2
        :return:
        """
        ans = []
        if As is None:
            As = np.array([float(self.q(p, kind)) for p in Ps])
        if num_plots == 2 and axiter is None:
            axiter = axiter_factory(None, len(dist_dict))
        else:
            if num_plots == 3 and axiter is None:
                axiter = axiter_factory(None, 30)
            else:
                for g in dist_dict.values():
                    _x = self.apply_distortion(g, axiter, num_plots)
                    df = _x.augmented_df
                    temp = df.loc[As, :].filter(regex='^loss|^S|exa[g]?_[^η][\\.:~a-zA-Z0-9]*$|exag_sumparts|lr_').copy()
                    temp['method'] = g.name
                    ans.append(temp)

                ans_table = pd.concat(ans)
                ans_table['return'] = np.round(1 / ans_table.S, 0)
                df2 = ans_table.copy()
                df2 = df2.set_index(['loss', 'method', 'return', 'S'])
                df2.columns = df2.columns.str.split('_', expand=True)
                ans_stacked = pd.DataFrame(df2.stack().stack()).reset_index()
                ans_stacked.columns = ['assets', 'method', 'return', 'S', 'line', 'stat', 'value']
                mn = ans_table.filter(regex='^lr').min().min()
                mn1 = mn
                mx = ans_table.filter(regex='^lr').max().max()
                mn = np.round(mn * 20, 0) / 20
                mx = np.round(mx * 20, 0) / 20
                if mx >= 0.9:
                    mx = 1
                if mn <= 0.2:
                    mn = 0
                if mn1 < mn:
                    mn -= 0.1
                if num_plots >= 1:
                    sns.catplot(x='line', y='value', row='return', col='method', height=2.5, kind='bar', data=(ans_stacked.query(' stat=="lr" '))).set(ylim=(mn, mx), ylabel='LR')
                    sns.catplot(x='method', y='value', row='return', col='line', height=2.5, kind='bar', data=(ans_stacked.query(' stat=="lr" '))).set(ylim=(mn, mx), ylabel='LR')
                return (
                 ans_table, ans_stacked)

    def apply_distortion(self, dist, plots=None, df_in=None, create_augmented=True):
        """
        Apply the distortion, make a copy of density_df and append various columns to create augmented_df.

        augmented_df depends on the distortion but only includes variables that work for all asset levels, e.g.

        1. marginal loss, lr, roe etc.
        2. bottom up totals

        Top down total depend on where the "top" is and do not work in general. They are handled in analyze_distortions
        where you explicitly provide a top.

        Does not touch density_df: that is independent of distortions

        Optionally produce graphics of results controlled by plots a list containing none or more of:

        1. basic: exag_sumparts, exag_total df.exa_total
        2. extended: the full original set

        :type create_augmented: object
        :param dist: agg.Distortion
        :param axiter: axis iterator, if None no plots are returned
        :param plots: iterable of plot types
        :param df_in: when called from gradient you want to pass in gradient_df and use that; otherwise use self.density_df
        :param create_augmented: store the output in self.augmented_df
        :return: density_df with extra columns appended
        """
        if df_in is None:
            df = self.density_df.copy()
        else:
            df = df_in
        g, g_inv = dist.g, dist.g_inv
        if len(df.loc[(df.S < 0, 'S')] > 0):
            logger.warning(f"{len(df.loc[(df.S < 0, 'S')] > 0)} negative S values being set to zero...")
        df.loc[(df.S < 0, 'S')] = 0
        df['gS'] = g(df.S)
        gSeq0 = df.gS == 0
        df['gF'] = 1 - df.gS
        df['gp_total'] = -np.diff((df.gS), prepend=1)
        total_mass = 0
        if dist.mass:
            S = self.density_df.S
            if not np.alltrue(S.iloc[1:] <= S.iloc[:-1].values):
                logger.error('S = denstiy_df.S is not non-increasing...carrying on but you should investigate...')
            idx_ess_sup = S.to_numpy().nonzero()[0][(-1)]
            logger.warning(f"Index of ess_sup is {idx_ess_sup}")
            total_mass = np.zeros_like(S)
            total_mass[:idx_ess_sup + 1] = dist.mass
        for line in self.line_names:
            mass = 0
            if dist.mass:
                logger.error('You cannot use a distortion with a mass at this time...')
                mass = total_mass * self.density_df[f"exi_xeqa{line}"].iloc[idx_ess_sup]
                logger.warning(f"Individual line={line} weight from portfolio mass = {mass:.5g}")
                for ii in range(1, max(self.log2 - 4, 0)):
                    avg_xix = self.density_df[f"exi_xeqa{line}"].iloc[idx_ess_sup - (1 << ii):].mean()
                    logger.warning(f"Avg weight last {1 << ii} observations is  = {avg_xix:.5g} vs. last is {self.density_df[exi_xeqa{line}].iloc[idx_ess_sup]}:.5g")

                logger.warning('You want these values all to be consistent!')
            df['exi_xgtag_' + line] = (df[f"exeqa_{line}"] / df.loss * df.gp_total).shift(-1)[::-1].cumsum() / df.gS
            df.loc[(gSeq0, 'exi_xgtag_' + line)] = 0.0
            df[f"exag_{line}"] = (df[f"exi_xgtag_{line}"].shift(1) * df.gS.shift(1)).cumsum() * self.bs

        df['exag_sumparts'] = df.filter(regex='^exag_[^η]').sum(axis=1)
        df['exag_total'] = df.gS.shift(1, fill_value=0).cumsum() * self.bs
        df['M.M_total'] = df.gS - df.S
        df['M.Q_total'] = 1 - df.gS
        df['M.L_total'] = df['S']
        df['M.P_total'] = df['gS']
        df['M.ROE_total'] = df['M.M_total'] / df['M.Q_total']
        roe_zero = df['M.ROE_total'] == 0.0
        for line in self.line_names_ex:
            df[f"exa_{line}_pcttotal"] = df[('exa_' + line)] / df.exa_total
            df[f"exag_{line}_pcttotal"] = df[('exag_' + line)] / df.exag_total
            df[f"T.L_{line}"] = df[f"exa_{line}"]
            df[f"T.P_{line}"] = df[f"exag_{line}"]
            df.loc[(0, f"T.P_{line}")] = 0
            df[f"T.LR_{line}"] = df[f"exa_{line}"] / df[f"exag_{line}"]
            df[f"T.M_{line}"] = df[f"exag_{line}"] - df[f"exa_{line}"]
            df.loc[(0, f"T.M_{line}")] = 0
            df[f"M.M_{line}"] = df[f"T.M_{line}"].diff().shift(-1) / self.bs
            df[f"M.Q_{line}"] = df[f"M.M_{line}"] / df['M.ROE_total']
            df[f"M.Q_{line}"].iloc[-1] = 0
            df.loc[(roe_zero, f"M.Q_{line}")] = np.nan
            if line != 'total':
                df[f"M.L_{line}"] = df[f"exi_xgta_{line}"] * df['S']
                df[f"M.P_{line}"] = df[f"exi_xgtag_{line}"] * df['gS']
            df[f"M.LR_{line}"] = df[f"M.L_{line}"] / df[f"M.P_{line}"]
            df[f"T.Q_{line}"] = df[f"M.Q_{line}"].shift(1).cumsum() * self.bs
            df.loc[(0, f"T.Q_{line}")] = 0
            df[f"T.ROE_{line}"] = df[f"T.M_{line}"] / df[f"T.Q_{line}"]
            df[f"T.PQ_{line}"] = df[f"T.P_{line}"] / df[f"T.Q_{line}"]
            df[f"M.PQ_{line}"] = df[f"M.P_{line}"] / df[f"M.Q_{line}"]

        df['T.L_total'] = df['exa_total']
        df['T.P_total'] = df['exag_total']
        df['T.Q_total'] = df.loss - df['exag_total']
        df['T.M_total'] = df['exag_total'] - df['exa_total']
        df['T.PQ_total'] = df['T.P_total'] / df['T.Q_total']
        df['T.LR_total'] = df['T.L_total'] / df['T.P_total']
        df['T.ROE_total'] = df['T.M_total'] / df['T.Q_total']
        f_distortion = f_byline = f_bylineg = f_exas = None
        if plots == 'all':
            plots = [
             'basic', 'extended']
        if plots:
            if 'basic' in plots:
                f_distortion, ax = plt.subplots(1, 1, figsize=(4, 4))
                ax.plot((df.exag_sumparts), label='Sum of Parts')
                ax.plot((df.exag_total), label='Total')
                ax.plot((df.exa_total), label='Loss')
                ax.legend()
                ax.set_title(f"Mass audit for {dist.name}")
                ax.legend(loc='upper right')
                ax.grid()
            if 'extended' in plots:
                max_x = 1.1 * self.q(0.999999)
                df_plot = df.loc[0:max_x, :]
                f_exas, axs, axiter = AxisManager.make_figure(12, sharex=True)
                ax = next(axiter)
                df_plot.filter(regex='^p_').sort_index(axis=1).plot(ax=ax)
                ax.set_ylim(0, df_plot.filter(regex='p_[^η]').iloc[1:, :].max().max())
                ax.set_title('Densities')
                ax.legend(loc='upper right')
                ax.grid()
                ax = next(axiter)
                df_plot.loc[:, ['p_total', 'gp_total']].plot(ax=ax)
                ax.set_title('Total Density and Distortion')
                ax.legend(loc='upper right')
                ax.grid()
                ax = next(axiter)
                df_plot.loc[:, ['S', 'gS']].plot(ax=ax)
                ax.set_title('S, gS')
                ax.legend(loc='upper right')
                ax.grid()
                for prefix in ('exa', 'exag', 'exeqa', 'exgta', 'exi_xeqa', 'exi_xgta'):
                    ax = next(axiter)
                    df_plot.filter(regex=f"^{prefix}_(?!ημ)[a-zA-Z0-9]+$").sort_index(axis=1).plot(ax=ax)
                    ax.set_title(f"{prefix} by line")
                    ax.legend(loc='upper left')
                    ax.grid()
                    if prefix.find('xi_x') > 0:
                        ax.set_ylim(-0.025, 1.025)

                ax = next(axiter)
                df_plot.filter(regex='^exa_.*_pcttotal$').sort_index(axis=1).plot(ax=ax)
                ax.set_title('Proportion of loss: T.L_line / T.L_total')
                ax.set_ylim(0, 1.05)
                ax.legend(loc='upper left')
                ax.grid()
                ax = next(axiter)
                df_plot.filter(regex='^exag_.*_pcttotal$').sort_index(axis=1).plot(ax=ax)
                ax.set_title('Proportion of premium: T.P_line / T.P_total')
                ax.legend(loc='upper left')
                ax.grid()
                ax = next(axiter)
                df_plot.filter(regex='^M.LR_').sort_index(axis=1).plot(ax=ax)
                ax.set_title('LR with the Natural (constant layer ROE) Allocation')
                ax.legend(loc='lower right')
                ax.grid()
                nl = len(self.line_names_ex)
                f_byline, axs, axiter = AxisManager.make_figure(nl)
                for line in self.line_names:
                    ax = next(axiter)
                    df_plot.filter(regex=f"ex(le|eq|gt)a_{line}").sort_index(axis=1).plot(ax=ax)
                    ax.set_title(f"{line} EXs")
                    ax.set(ylim=[0, self.q(0.999, 'lower')])
                    ax.legend(loc='upper left')
                    ax.grid()

                AxisManager.tidy_up(f_byline, axiter)
                f_bylineg, axs, axiter = AxisManager.make_figure(nl)
                for line in self.line_names_ex:
                    ax = next(axiter)
                    df_plot.filter(regex=f"exa[g]?_{line}$").sort_index(axis=1).plot(ax=ax)
                    ax.set_title(f"{line} T.L and T.P")
                    ax.legend(loc='lower right')
                    ax.grid()

                AxisManager.tidy_up(f_bylineg, axiter)
        if create_augmented:
            self.augmented_df = df
            self._distortion = dist
        return Answer(augmented_df=df, f_distortion=f_distortion,
          f_byline=f_byline,
          f_bylineg=f_bylineg,
          f_exas=f_exas)

    def var_dict(self, p, kind):
        """
        make a dictionary of value at risks for each line and the whole portfolio.

         Returns: {line : var(p, kind)} and includes the total as self.name line

        :param p:
        :param kind:
        :return:
        """
        var_dict = {a.name:a.q(p, kind) for a in self.agg_list}
        var_dict[self.name] = self.q(p, kind)
        return var_dict

    def gamma(self, a=None, p=None, kind='', plot=False, compute_stand_alone=False, three_plot_xlim=-1, ylim_zoom=(1, 1000.0), extreme_var=0.99999998):
        """
        Return the vector gamma_a(x), the conditional layer effectiveness given assets a.
        Assets specified by percentile level and type (you need a in the index too hard to guess?)
        gamma can be created with no base and no calibration - it does not depend on a distortion.
        It only depends on total losses.
        It does NOT vary by line - because of equal priority.
        a must be in index?

        Originally in aggregate_extensions...but only involves one portfolio so should be in agg
        Note that you need upper and lower q's in aggs now too.

        :param a:     input a or p and kind as ususal
        :param p:     asset level percentile
        :param kind:  lower or upper
        :param plot:
        :param compute_stand_alone:
        :param three_plot_xlim:        if >0 do the three plot xlim=[0, loss_threshold] to show details
        :param ylim_zoom: now on a return period, 1/(1-p) basis so > 1
        :param extreme_var:
        :return:
        """
        if a is None:
            assert p is not None
            a = self.q(p, kind)
        else:
            p = self.cdf(a)
            kind = 'lower'
            ql = self.q(p, 'lower')
            qu = self.q(p, 'upper')
            logger.warning(f"Input a={a} to gamma; computed p={p:.8g}, lower and upper quantiles are {ql:.8g} and {qu:.8g}")
        temp = self.density_df.filter(regex='^p_|^e1xi_1gta_|exi_xgta_|exi_xeqa_|exeqa_|S|loss').copy()
        var_dict = self.var_dict(p, kind)
        extreme_var_dict = self.var_dict(extreme_var, kind)
        min_xa = np.minimum(temp.loss, a) / temp.loss
        temp['min_xa_x'] = min_xa
        ln = 'total'
        gam_name = f"gamma_{self.name}_{ln}"
        temp[f"exi_x1gta_{ln}"] = np.cumsum((temp['loss'] * temp.p_total / temp.loss)[::-1]) * self.bs
        temp[gam_name] = np.cumsum((min_xa * 1.0 * temp.p_total)[::-1]) / temp[f"exi_x1gta_{ln}"] * self.bs
        for ln in self.line_names:
            if compute_stand_alone:
                a_l = var_dict[ln]
                a_l_ = a_l - self.bs
                xinv = temp[f"e1xi_1gta_{ln}"].shift(-1)
                gam_name = f"gamma_{ln}_sa"
                s = 1 - temp[f"p_{ln}"].cumsum()
                temp[f"S_{ln}"] = s
                temp[gam_name] = 0
                temp.loc[0:a_l_, gam_name] = (s[0:a_l_] - s[a_l] + a_l * xinv[a_l]) / s[0:a_l_]
                temp.loc[a_l:, gam_name] = a_l * xinv[a_l:] / s[a_l:]
                temp[gam_name] = temp[gam_name].shift(1)
                temp.loc[extreme_var_dict[ln]:, gam_name] = np.nan
            gam_name = f"gamma_{self.name}_{ln}"
            temp[f"exi_x1gta_{ln}"] = np.cumsum((temp[f"exeqa_{ln}"] * temp.p_total / temp.loss)[::-1]) * self.bs
            temp[gam_name] = np.cumsum((min_xa * temp[f"exi_xeqa_{ln}"] * temp.p_total)[::-1]) / temp[f"exi_x1gta_{ln}"] * self.bs

        temp['BEST'] = 1
        temp.loc[a:, 'BEST'] = a / temp.loc[a:, 'loss']
        temp['WORST'] = np.maximum(0, 1 - temp.loc[(a, 'S')] / temp.S)
        f = spl = None
        if plot:
            renamer = self.renamer
            if three_plot_xlim > 0:
                spl = temp.filter(regex='gamma|BEST|WORST').rename(columns=renamer).sort_index(1).plot(ylim=[
                 -0.05, 1.05],
                  linewidth=1)
            else:
                spl = temp.filter(regex='gamma|BEST|WORST').sort_index(1).plot(ylim=[-0.05, 1.05], linewidth=1)
            for ln in spl.lines:
                lbl = ln.get_label()
                if lbl == lbl.upper():
                    ln.set(linewidth=1, linestyle='--', label=(lbl.title()))

            spl.grid('b')
            if three_plot_xlim > 0:
                spl.set(xlim=[0, three_plot_xlim])
            spl.legend()
            if three_plot_xlim > 0 and compute_stand_alone:
                temp_ex = temp.query(f"loss < {three_plot_xlim}").filter(regex='gamma_|p_')
                temp_ex[[f"S_{l[2:]}" for l in temp_ex.filter(regex='p_').columns]] = temp_ex.filter(regex='p_').shift((-1), fill_value=0).iloc[::-1].cumsum()
                f, axs = plt.subplots(3, 1, figsize=(8, 9), squeeze=False, constrained_layout=True)
                ax1 = axs[(0, 0)]
                ax2 = axs[(1, 0)]
                ax3 = axs[(2, 0)]
                btemp = temp_ex.filter(regex='gamma_').rename(columns=renamer).sort_index(axis=1)
                (1 / (1 - btemp.iloc[1:])).plot(logy=True, ylim=ylim_zoom, ax=ax1)
                btemp.plot(ax=ax2)
                ax1.set(ylim=ylim_zoom, title='Gamma Functions (Return Period Scale)')
                ax2.set(ylim=[0, 1.005], title='Gamma Functions')
                temp_ex.filter(regex='S_').rename(columns=renamer).sort_index(axis=1).plot(ax=ax3)
                col_by_line = {}
                for l in ax3.lines:
                    ls = l.get_label().split(' ')
                    col_by_line[ls[0]] = l.get_color()

                l_loc = dict(zip(axs.flatten(), ['upper right', 'lower left', 'upper right']))
                ax3.set(ylim=[0, 1.005], title=f"Survival Functions up to p={self.cdf(three_plot_xlim):.1%} Loss")
                for ax in axs.flatten():
                    for l in self.line_names + [self.name]:
                        ln = ax.plot([var_dict[l], var_dict[l]], [1 if ax is ax1 else 0, ylim_zoom[1]], label=f"{l} s/a assets {var_dict[l]:.0f}")
                        ln[0].set(linewidth=1, linestyle=':')

                try:
                    for ax in axs.flatten():
                        for line in ax.lines:
                            ln = line.get_label()
                            lns = ln.split(' ')
                            if ln.find('stand-alone') > 0:
                                line.set(linestyle='--')
                            else:
                                if lns[0] in col_by_line:
                                    line.set(color=(col_by_line[lns[0]]))
                            if lns[1] in col_by_line:
                                line.set(color=(col_by_line[lns[1]]))

                        ax.legend(loc=(l_loc[ax]))
                        ax.grid(which='major', axis='y')

                except Exception as e:
                    try:
                        logger.error(f"Errors in gamma plotting;, {e}")
                    finally:
                        e = None
                        del e

        return Answer(augmented_df=temp.sort_index(axis=1), fig_gamma=spl, base=(self.name), fig_gamma_three_part=f,
          assets=a,
          p=p,
          kind=kind)

    def price(self, reg_g, pricing_g=None):
        """
        Price using regulatory and pricing g functions
            Compute E_price (X wedge E_reg(X) ) where E_price uses the pricing distortion and E_reg uses
            the regulatory distortion

            regulatory capital distortion is applied on unlimited basis: ``reg_g`` can be:

            * if input < 1 it is a number interpreted as a p value and used to deterine VaR capital
            * if input > 1 it is a directly input  capital number
            * d dictionary: Distortion; spec { name = dist name | var | epd, shape=p value a distortion used directly

            ``pricing_g`` is  { name = ph|wang and shape= or lr= or roe= }, if shape and lr or roe shape is overwritten

            if ly it must include ro in spec

            if lr and roe then lr is used

        :param reg_g: a distortion function spec or just a number; if >1 assets if <1 a prob converted to quantile
        :param pricing_g: spec or CDistortion class or lr= or roe =; must have name= to define spec; if CDist that is
                          used
        :return:
        """
        F = interpolate.interp1d((self.density_df.loss), (self.density_df.F), kind='linear', assume_sorted=True,
          bounds_error=False,
          fill_value='extrapolate')
        Finv = interpolate.interp1d((self.density_df.F), (self.density_df.loss), kind='nearest', assume_sorted=True,
          fill_value='extrapolate',
          bounds_error=False)
        a_reg_ix = 0
        a_reg = 0
        if isinstance(reg_g, float) or isinstance(reg_g, int):
            if reg_g > 1:
                a_reg = reg_g
                a_reg_ix = self.density_df.iloc[(
                 self.density_df.index.get_loc(reg_g, 'ffill'), 0)]
            else:
                a_reg = a_reg_ix = float(Finv(reg_g))
        else:
            if isinstance(reg_g, dict):
                if reg_g['name'] == 'var':
                    a_reg = a_reg_ix = float(Finv(reg_g['shape']))
                else:
                    if reg_g['name'] == 'epd':
                        a_reg = float(self.epd_2_assets[('total', 0)](reg_g['shape']))
                        a_reg_ix = self.density_df.iloc[(
                         self.density_df.index.get_loc(a_reg, 'ffill'), 0)]
                    else:
                        reg_g = Distortion(**reg_g)
            elif a_reg == 0:
                assert isinstance(reg_g, Distortion)
                gS = reg_g.g(self.density_df.S)
                a_reg = self.bs * np.sum(gS)
                ix = self.density_df.index.get_loc(a_reg, method='ffill')
                a_reg_ix = self.density_df.index[ix]
            else:
                row = self.density_df.loc[a_reg_ix, :]
                prem = 0
                if isinstance(pricing_g, Distortion):
                    pass
                elif 'lr' in pricing_g:
                    prem = row['exa_total'] / pricing_g['lr']
                else:
                    if 'roe' in pricing_g:
                        roe = pricing_g['roe']
                        delta = roe / (1 + roe)
                        prem = row['exa_total'] + delta * (a_reg - row['exa_total'])
                    if prem > 0:
                        pricing_g = self.calibrate_distortion(name=(pricing_g['name']), premium_target=prem, assets=a_reg_ix)
                    else:
                        pricing_g = Distortion(**pricing_g)
            g_pri, g_pri_inv = pricing_g.g, pricing_g.g_inv
            df = pd.DataFrame(columns=['line', 'a_reg', 'exa', 'exag'], dtype=float)
            df.columns.name = 'statistic'
            df = df.set_index('line', drop=True)
            gS = pd.Series((g_pri(self.density_df.S)), index=(self.density_df.index))
            gp_total = -pd.Series((np.diff(np.hstack((1, gS)))), index=(self.density_df.index))
            mass = 0
            if pricing_g.has_mass:
                mass = pricing_g.mass
                mass *= a_reg_ix
                logger.info(f"CPortfolio.price | {self.name}, Using mass {mass}")
            for line in self.line_names:
                exag1 = np.sum(self.density_df.loc[0:a_reg_ix - self.bs, f"exeqa_{line}"] * gp_total.loc[0:a_reg_ix - self.bs])
                exag2 = np.sum(self.density_df.loc[a_reg_ix:, f"exeqa_{line}"] / self.density_df.loss.loc[a_reg_ix:] * gp_total.loc[a_reg_ix:]) * a_reg_ix
                exag = exag1 + exag2
                if mass > 0:
                    lim_xi_x = self.density_df.loc[(a_reg_ix, f"exi_xeqa_{line}")]
                    exag += lim_xi_x * mass
                df.loc[line, :] = [a_reg_ix, row[f"exa_{line}"], exag]

            line = 'total'
            exag = np.sum(g_pri(self.density_df.loc[0:a_reg_ix - self.bs, 'S'])) * self.bs
            assert np.isclose(exag, np.sum(gS.loc[0:a_reg_ix - self.bs]) * self.bs)
            df.loc[line, :] = [a_reg_ix, row[f"exa_{line}"], exag]
            df['lr'] = df.exa / df.exag
            df['profit'] = df.exag - df.exa
            df.loc[('total', 'ROE')] = df.loc[('total', 'profit')] / (df.loc[('total',
                                                                              'a_reg')] - df.loc[('total',
                                                                                                  'exag')])
            df.loc[('total', 'prDef')] = 1 - float(F(a_reg))
            df['pct_loss'] = df.exa / df.loc[('total', 'exa')]
            df['pct_prem'] = df.exag / df.loc[('total', 'exag')]
            df['lr'] = df.exa / df.exag
            df['levg'] = df.exag / df.a_reg
            df['ROE'] = df.profit / (df.a_reg - df.exag)
            logger.info(f"CPortfolio.price | {self.name} portfolio pricing g {pricing_g}")
            logger.info(f"CPortfolio.price | Capital sufficient to prob {float(F(a_reg)):7.4f}")
            logger.info(f"CPortfolio.price | Capital quantization error {(a_reg - a_reg_ix) / a_reg:7.5f}")
            if prem > 0:
                logger.info(f"CPortfolio.price | Premium calculated as {prem:18,.1f}")
                logger.info(f"CPortfolio.price | Pricing distortion shape calculated as {pricing_g.shape}")
            return (df, pricing_g)

    def analyze_distortion(self, dname, dshape=None, dr0=0.025, ddf=5.5, LR=None, ROE=None, p=None, kind='lower', A=None, use_self=False, plot=True, a_max_p=0.99999999):
        """

        Graphic and summary DataFrame for one distortion showing results that vary by asset levelm
        such as increasing or decreasing cumulative premium.

        Characterized by the need to know an asset level, vs. apply_distortion that produced
        values for all asset levels.

        Returns DataFrame with values upto the input asset level...differentiates from apply_distortion
        graphics that cover the full range.

        analyze_pricing will then zoom in and only look at one asset level for micro-dynamics...

        Logic of arguments:

            if data_in == 'self' use self.augmented_df; this implies a distortion self.distortion

            else need to build the distortion and apply it
                if dname is a distortion use it
                else built one calibrated to input data

            LR/ROE/a/p:
                if p then a=q(p, kind) else p = MESSY
                if LR then P and ROE; if ROE then Q to P to LR
                these are used to calibrate distortion

            A newly made distortion is run through apply_distortion with no plot

        Logic to determine assets similar to calibrate_distortions.

        Can pass in a pre-calibrated distortion in dname

        Must pass LR or ROE to determine profit

        Must pass p or A to determine assets

        Output is an `Answer` class object containing

                Answer(augmented_df=deets, trinity_df=df, distortion=dist, fig1=f1 if plot else None,
                      fig2=f2 if plot else None, pricing=pricing, exhibit=exhibit, roe_compare=exhibit2,
                      audit_df=audit_df)

        Originally `example_factory`.

        example_factory_exhibits included:

        do the work to extract the pricing, exhibit and exhibit 2 DataFrames from deets
        Can also accept an ans object with an augmented_df element (how to call from outside)
        POINT: re-run exhibits at different p/a thresholds without recalibrating
        add relevant items to audit_df
        a = q(p) if both given; if not both given derived as usual

        Figures show

        :param dname: name of distortion
        :param dshape:  if input use dshape and dr0 to make the distortion
        :param dr0:
        :param ddf:  r0 and df params for distortion
        :param LR: otherwise use loss ratio and p or a loss ratio
        :param ROE:
        :param p: p value to determine capital.
        :param kind: type of VaR, upper or lower
        :param A:
        :param use_self:  if true use self.augmented and self.distortion...else recompute
        :param plot:
        :param a_max_p: percentile to use to set the right hand end of plots
        :return: various dataframes in an Answer class object

        """
        a_max = self.q(a_max_p)
        a_min = self.q(0.0001)
        if use_self:
            dist = self.distortion
            augmented_df = self.augmented_df
            a_cal = self.q(p, kind)
            exa = self.density_df.loc[(a_cal, 'exa_total')]
            exag = augmented_df.loc[(a_cal, 'exag_total')]
            K = a_cal - exag
            LR = exa / exag
            ROE = (exag - exa) / K
        else:
            if p:
                a_cal = self.q(p, kind)
                exa = self.density_df.loc[(a_cal, 'exa_total')]
            else:
                assert A is not None
                p = self.cdf(A)
                a_cal = self.q(p)
                exa = self.density_df.loc[(a_cal, 'exa_total')]
                if a_cal != A:
                    logger.warning(f"a_cal:=q(p)={a_cal} is not equal to A={A} at p={p}")
                elif dshape or isinstance(dname, Distortion):
                    if isinstance(dname, Distortion):
                        dist = dname
                    else:
                        dist = Distortion(dname, dshape, dr0, ddf)
                    _x = self.apply_distortion(dist, create_augmented=False)
                    augmented_df = _x.augmented_df
                    exa = self.density_df.loc[(a_cal, 'exa_total')]
                    exag = augmented_df.loc[(a_cal, 'exag_total')]
                    profit = exag - exa
                    K = a_cal - exag
                    ROE = profit / K
                    LR = exa / exag
                else:
                    if LR is None:
                        assert ROE is not None
                        delta = ROE / (1 + ROE)
                        nu = 1 - delta
                        exag = nu * exa + delta * a_cal
                        LR = exa / exag
                    else:
                        exag = exa / LR
                    profit = exag - exa
                    K = a_cal - exag
                    ROE = profit / K
                    dist = self.calibrate_distortion(dname, r0=dr0, df=ddf, roe=ROE, assets=a_cal)
                    _x = self.apply_distortion(dist, create_augmented=False)
                    augmented_df = _x.augmented_df
        audit_df = pd.DataFrame(dict(stat=[p, LR, ROE, a_cal, K, dist.name, dist.shape]), index=[
         'p', 'LR', 'ROE', 'a_cal', 'K', 'dname', 'dshape'])
        for nc in ('L', 'P', 'M', 'Q', 'LR', 'ROE', 'PQ'):
            augmented_df[f"V.{nc}_total"] = 0

        augmented_df.loc[0:a_cal, 'V.L_total'] = augmented_df.at[(a_cal, 'T.L_total')] - augmented_df.loc[0:a_cal,
         'T.L_total']
        augmented_df.loc[0:a_cal, 'V.P_total'] = augmented_df.at[(a_cal, 'T.P_total')] - augmented_df.loc[0:a_cal,
         'T.P_total']
        augmented_df.loc[0:a_cal, 'V.M_total'] = augmented_df.at[(a_cal, 'T.M_total')] - augmented_df.loc[0:a_cal,
         'T.M_total']
        augmented_df.loc[0:a_cal, 'V.Q_total'] = augmented_df.at[(a_cal, 'T.Q_total')] - augmented_df.loc[0:a_cal,
         'T.Q_total']
        augmented_df.loc[0:a_cal, 'V.LR_total'] = augmented_df.loc[0:a_cal, 'V.L_total'] / augmented_df.loc[0:a_cal,
         'V.P_total']
        augmented_df.loc[0:a_cal, 'V.PQ_total'] = augmented_df.loc[0:a_cal, 'V.P_total'] / augmented_df.loc[0:a_cal,
         'V.Q_total']
        augmented_df.loc[0:a_cal, 'V.ROE_total'] = augmented_df.loc[0:a_cal, 'V.M_total'] / augmented_df.loc[0:a_cal,
         'V.Q_total']
        done = []
        ex = augmented_df.loc[[a_cal]].T
        pricing = augmented_df.loc[[a_cal]].T.filter(regex='^(T|M)\\.(L|P|M|Q|LR|ROE|PQ)|exi_xgtag?_[a-zA-Z]+(?<!sum)$',
          axis=0).copy()
        pricing.index = pricing.index.str.replace('exi_xgta_(.+)$', 'M_alpha_\\1').str.replace('exi_xgtag_(.+)$', 'M_beta_\\1').str.split('_|\\.',
          expand=True)
        pricing.index.set_names(['MT', 'stat', 'line'], inplace=True)
        pricing = pricing.sort_index(level=[0, 1, 2])
        exhibit = pricing.unstack(2).copy()
        exhibit.columns = exhibit.columns.droplevel(level=0)
        exhibit.loc['Assets', :] = a_cal
        try:
            p_t = self.tvar_threshold(p, kind)
        except ValueError as e:
            try:
                logger.warning(f"Error computing p_t threshold for VaR at p={p}")
                logger.warning(str(e))
                p_t = np.nan
            finally:
                e = None
                del e

        try:
            pv, pt = self.equal_risk_var_tvar(p, p_t)
        except (ZeroDivisionError, ValueError) as e:
            try:
                logger.warning(f"Error computing pv, pt equal_risk_var_tvar for VaR, p={p}, kind={kind}, p_t={p_t}")
                logger.warning(str(e))
                pv = np.nan
                pt = np.nan
            finally:
                e = None
                del e

        try:
            done = []
            exhibit.loc[('VaR', 'Q'), :] = [float(a.q(p, kind)) for a in self] + [self.q(p, kind)]
            done.append('var')
            exhibit.loc[('TVaR', 'Q'), :] = [float(a.tvar(p_t)) for a in self] + [self.tvar(p_t)]
            done.append('tvar')
            exhibit.loc[('ScaledVaR', 'Q'), :] = exhibit.loc[('VaR', 'Q'), :]
            exhibit.loc[('ScaledTVaR', 'Q'), :] = exhibit.loc[('TVaR', 'Q'), :]
            exhibit.loc[(('ScaledVaR', 'Q'), 'total')] = 0
            exhibit.loc[(('ScaledTVaR', 'Q'), 'total')] = 0
            sumvar = exhibit.loc[('ScaledVaR', 'Q'), :].sum()
            sumtvar = exhibit.loc[('ScaledTVaR', 'Q'), :].sum()
            exhibit.loc[('ScaledVaR', 'Q'), :] = exhibit.loc[('ScaledVaR', 'Q'), :] * exhibit.at[(('VaR', 'Q'),
                                                                                                  'total')] / sumvar
            exhibit.loc[('ScaledTVaR', 'Q'), :] = exhibit.loc[('ScaledTVaR', 'Q'), :] * exhibit.at[(('TVaR', 'Q'),
                                                                                                    'total')] / sumtvar
            exhibit.at[(('ScaledVaR', 'Q'), 'total')] = exhibit.at[(('VaR', 'Q'), 'total')]
            exhibit.at[(('ScaledTVaR', 'Q'), 'total')] = exhibit.at[(('TVaR', 'Q'),
                                                                     'total')]
            exhibit.at[(('VaR', 'Q'), 'total')] = sumvar
            exhibit.at[(('TVaR', 'Q'), 'total')] = sumtvar
            exhibit.loc[('EqRiskVaR', 'Q'), :] = [float(a.q(pv, kind)) for a in self] + [self.q(p)]
            done.append('eqvar')
            exhibit.loc[('EqRiskTVaR', 'Q'), :] = [float(a.tvar(pt)) for a in self] + [self.tvar(p_t)]
            done.append('eqtvar')
            exhibit.loc[('MerPer', 'Q'), :] = self.merton_perold(p)
            done.append('merper')
        except Exception as e:
            try:
                logger.warning(f"Some general out of bounds error on VaRs and TVaRs, setting all equal to zero. Last completed steps {done[(-1)] if len(done) else 'none'}, out of var, tvar, eqvar, eqtvar merper. ")
                logger.warning(f"The built in warning is type {type(e)} saying {e}")
                for c in ('VaR', 'TVaR', 'ScaledVaR', 'ScaledTVaR', 'EqRiskVaR', 'EqRiskTVaR',
                          'MerPer'):
                    if c.lower() in done:
                        continue
                    exhibit.loc[(c, 'Q'), :] = np.nan

            finally:
                e = None
                del e

        row = self.density_df.loc[a_cal, :]
        exhibit.loc[('T', 'EPD'), :] = [row.at[f"epd_{0 if l == 'total' else 1}_{l}"] for l in self.line_names_ex]
        exhibit = exhibit.sort_index()
        try:
            for m in ('VaR', 'TVaR', 'ScaledVaR', 'ScaledTVaR', 'EqRiskVaR', 'EqRiskTVaR',
                      'MerPer'):
                exhibit.loc[(m, 'Q'), :] -= exhibit.loc[('T', 'P'), :].values
                exhibit.loc[(m, 'L'), :] = exhibit.loc[('T', 'L'), :]
                exhibit.loc[(m, 'P'), :] = exhibit.loc[('T', 'L'), :] + ROE * exhibit.loc[(m, 'Q'), :]
                exhibit.loc[(m, 'M'), :] = exhibit.loc[(m, 'P'), :] - exhibit.loc[('T', 'L'), :].values
                exhibit.loc[(m, 'LR'), :] = exhibit.loc[('T', 'L'), :] / exhibit.loc[(m, 'P'), :]
                exhibit.loc[(m, 'ROE'), :] = exhibit.loc[(m, 'M'), :] / exhibit.loc[(m, 'Q'), :]
                exhibit.loc[(m, 'PQ'), :] = exhibit.loc[(m, 'P'), :] / exhibit.loc[(m, 'Q'), :]

        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        exhibit = exhibit.sort_index()
        audit_df.loc['TVaR@'] = p_t
        audit_df.loc['erVaR'] = pv
        audit_df.loc['erTVaR'] = pt
        audit_df.loc['a'] = a_cal
        audit_df.loc['kind'] = kind
        f_6_part = f_trinity = f_8_part = f_distortion = f_close = None
        if plot:
            f_distortion, ax = plt.subplots(1, 1)
            dist.plot(ax=ax)

            def tidy(a, y=True):
                """
                function to tidy up the graphics
                """
                n = 6
                a.set(xlabel='Assets')
                a.xaxis.set_major_locator(FixedLocator([a_cal]))
                ff = f"A={a_cal:,.0f}"
                a.xaxis.set_major_formatter(FixedFormatter([ff]))
                a.xaxis.set_minor_locator(MaxNLocator(n))
                a.xaxis.set_minor_formatter(StrMethodFormatter('{x:,.0f}'))
                if y:
                    a.yaxis.set_major_locator(MaxNLocator(n))
                    a.yaxis.set_minor_locator(AutoMinorLocator(4))
                a.grid(which='major', axis='x', c='cornflowerblue', alpha=1, linewidth=1)
                a.grid(which='major', axis='y', c='lightgrey', alpha=0.5, linewidth=1)
                a.grid(which='minor', axis='x', c='lightgrey', alpha=0.5, linewidth=1)
                a.grid(which='minor', axis='y', c='gainsboro', alpha=0.25, linewidth=0.5)
                a.tick_params('x', which='major', labelsize=7, length=10, width=0.75, color='cornflowerblue', direction='out')
                a.tick_params('y', which='major', labelsize=7, length=5, width=0.75, color='black', direction='out')
                a.tick_params('both', which='minor', labelsize=7, length=2, width=0.5, color='black', direction='out')

            f_6_part, axs = plt.subplots(3, 2, figsize=(8, 10), sharex=True, constrained_layout=True)
            axi = iter(axs.flatten())
            ax = next(axi)
            augmented_df.filter(regex='^F|^gS|^S').rename(columns=(self.renamer)).plot(xlim=[
             0, a_max],
              ylim=[-0.025, 1.025],
              logy=False,
              title='F, S, gS: marginal premium and loss',
              ax=ax)
            tidy(ax)
            ax.legend(frameon=True, loc='center right')
            ax = next(axi)
            augmented_df.filter(regex='^M\\.[QM]_total').rename(columns=(self.renamer)).plot(xlim=[
             0, a_max],
              ylim=[-0.05, 1.05],
              logy=False,
              title='Marginal Capital and Margin',
              ax=ax)
            tidy(ax)
            ax.legend(frameon=True, loc='center right')
            ax = next(axi)
            augmented_df.filter(regex='^V\\.(L|P|Q|M)_total').rename(columns=(self.renamer)).plot(xlim=[
             0, a_max],
              ylim=[0, a_max],
              logy=False,
              title=f"Decreasing LPMQ from {a_cal:.0f}",
              ax=ax)
            (a_cal - augmented_df.loc[:a_cal, 'loss']).plot(ax=ax, label='Assets')
            tidy(ax)
            ax.legend(frameon=True, loc='upper right')
            ax = next(axi)
            augmented_df.filter(regex='^(T|V|M)\\.LR_total').rename(columns=(self.renamer)).plot(xlim=[
             0, a_cal * 1.1],
              ylim=[-0.05, 1.05],
              ax=ax,
              title='Increasing, Decreasing and Marginal LRs')
            tidy(ax)
            ax.legend(frameon=True, loc='lower left')
            ax = next(axi)
            augmented_df.filter(regex='^T\\.(L|P|Q|M)_total|loss').rename(columns=(self.renamer)).plot(xlim=[
             0, a_max],
              ylim=[0, a_max],
              logy=False,
              title=f"Increasing LPMQ to {a_cal:.0f}",
              ax=ax)
            tidy(ax)
            ax.legend(frameon=True, loc='upper left')
            ax = next(axi)
            augmented_df.filter(regex='^(M|T|V)\\.ROE_(total)?$').rename(columns=(self.renamer)).plot(xlim=[
             0, a_max],
              logy=False,
              title=f"Increasing, Decreasing and Marginal ROE to {a_cal:.0f}",
              ax=ax)
            ax.plot([0, a_max], [ROE, ROE], ':', linewidth=2, alpha=0.75, label='Avg ROE')
            tidy(ax)
            ax.legend(loc='upper right')
            title = f"{self.name} with {str(dist)} Distortion\nCalibrated to LR={LR:.3f} and p={p:.3f}, Assets={a_cal:,.1f}, ROE={ROE:.3f}"
            f_6_part.suptitle(title, fontsize='x-large')

            def tidy2(a, k, xloc=0.25):
                n = 4
                a.xaxis.set_major_locator(MultipleLocator(xloc))
                a.xaxis.set_minor_locator(AutoMinorLocator(4))
                a.xaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
                a.yaxis.set_major_locator(MaxNLocator(2 * n))
                a.yaxis.set_minor_locator(AutoMinorLocator(4))
                a.grid(which='major', axis='x', c='lightgrey', alpha=0.5, linewidth=1)
                a.grid(which='major', axis='y', c='lightgrey', alpha=0.5, linewidth=1)
                a.grid(which='minor', axis='x', c='gainsboro', alpha=0.25, linewidth=0.5)
                a.grid(which='minor', axis='y', c='gainsboro', alpha=0.25, linewidth=0.5)
                a.tick_params('both', which='major', labelsize=7, length=4, width=0.75, color='black', direction='out')
                a.tick_params('both', which='minor', labelsize=7, length=2, width=0.5, color='black', direction='out')
                a.plot([0, 1], [k, k], linewidth=1, c='black', label='Assets')

            f_trinity, axs = plt.subplots(1, 5, figsize=(8, 3), constrained_layout=True, sharey=True)
            axi = iter(axs.flatten())
            xr = [-0.05, 1.05]
            audit = augmented_df.loc[:a_max, :]
            ax = next(axi)
            ax.plot((audit.gS), (audit.loss), label='M.P_total')
            ax.plot((audit.S), (audit.loss), label='M.L_total')
            ax.set(xlim=xr, title='Marginal Prem & Loss')
            ax.set(xlabel='Loss = S = Pr(X>a)\nPrem = g(S)', ylabel='Assets, a')
            tidy2(ax, a_cal)
            ax.legend(loc='upper right', frameon=True, edgecolor=None)
            ax = next(axi)
            m = audit.F - audit.gF
            ax.plot(m, (audit.loss), linewidth=2, label='M')
            ax.set(xlim=(-0.01), title='Marginal Margin', xlabel='M = g(S) - S')
            tidy2(ax, a_cal, m.max() * 1.05 / 4)
            ax = next(axi)
            ax.plot((1 - audit.gS), (audit.loss), label='Q')
            ax.set(xlim=xr, title='Marginal Equity')
            ax.set(xlabel='Q = 1 - g(S)')
            tidy2(ax, a_cal)
            ax = next(axi)
            temp = audit.loc[self.q(1e-05):, :]
            r = (temp.gS - temp.S) / (1 - temp.gS)
            ax.plot(r, (temp.loss), linewidth=2, label='ROE')
            ax.set(xlim=(-0.05), title='Layer ROE')
            ax.set(xlabel='ROE = M / Q')
            tidy2(ax, a_cal, r.max() * 1.05 / 4)
            ax = next(axi)
            ax.plot(audit.S / audit.gS, audit.loss)
            ax.set(xlim=xr, title='Layer LR')
            ax.set(xlabel='LR = S / g(S)')
            tidy2(ax, a_cal)
            temp = augmented_df.filter(regex='exi_xgtag?_(?!sum)|^S|^gS|^(M|T)\\.').copy()
            renamer = self.renamer
            augmented_df.index.name = 'Assets a'
            temp.index.name = 'Assets a'
            f_8_part, axs = plt.subplots(4, 2, figsize=(8, 10), constrained_layout=True, squeeze=False)
            ax = iter(axs.flatten())
            try:
                a = (1 - augmented_df.filter(regex='p_').cumsum()).rename(columns=renamer).sort_index(1).plot(ylim=[
                 0, 1],
                  xlim=[0, a_max],
                  title='Survival functions',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='exi_xgtag?').rename(columns=renamer).sort_index(1).plot(ylim=[
                 0, 1],
                  xlim=[0, a_max],
                  title='$\\alpha=E[X_i/X | X>a],\\beta=E_Q$ by Line',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='^T\\.M').rename(columns=renamer).sort_index(1).plot(xlim=[
                 0, a_max],
                  title='Total Margins by Line',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='^M\\.M').rename(columns=renamer).sort_index(1).iloc[:-1, :].plot(xlim=[
                 0, a_max],
                  title='Marginal Margins by Line',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='^M\\.Q|gF').rename(columns=renamer).sort_index(1).plot(xlim=[
                 0, a_max],
                  title='Capital = 1-gS = gF',
                  ax=(next(ax)))
                a.grid('b')
                for _ in a.lines:
                    if _.get_label() == 'gF':
                        _.set(linewidth=5, alpha=0.3)

                a.legend()
                a = augmented_df.filter(regex='^ROE$|exi_xeqa').rename(columns=renamer).sort_index(1).plot(xlim=[
                 0, a_max],
                  title='M.ROE Total and $E[X_i/X | X=a]$ by line',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='M\\.LR').rename(columns=renamer).sort_index(1).plot(ylim=[
                 -0.05, 1.5],
                  xlim=[0, a_max],
                  title='Marginal LR',
                  ax=(next(ax)))
                a.grid('b')
                a = augmented_df.filter(regex='T.LR_').rename(columns=renamer).sort_index(1).plot(ylim=[
                 -0.05, 1.25],
                  xlim=[0, a_max],
                  title='Increasing Total LR by Line',
                  ax=(next(ax)))
                a.grid('b')
                a.legend(loc='center right')
            except Exception as e:
                try:
                    print('Error', e)
                finally:
                    e = None
                    del e

            bit = augmented_df.query(f"loss < {a_max}").filter(regex='exi_xgtag?_.*(?<!sum)$')
            f_close, ax = plt.subplots(1, 1, figsize=(8, 5))
            ax = bit.rename(columns=renamer).plot(ylim=[-0.025, 1.025], ax=ax)
            ax.grid()
            nl = len(self.line_names)
            for i, l in enumerate(ax.lines[nl:]):
                ax.lines[i].set(linewidth=1, linestyle='--')
                l.set(color=(ax.lines[i].get_color()), linewidth=2)

            ax.legend(loc='upper left')
        return Answer(augmented_df=augmented_df, distortion=dist, fig_distortion=f_distortion,
          fig_six_up_down=f_6_part,
          fig_trinity=f_trinity,
          fig_eight=f_8_part,
          fig_close=f_close,
          pricing=pricing,
          exhibit=exhibit,
          audit_df=audit_df)

    def top_down(self, distortions, A_or_p):
        """
        DataFrame summary and nice plots showing marginal and average ROE, lr etc. as you write a layer from x to A
        If A=0 A=q(log) is used

        Not integrated into graphics format (plot)

        :param distortions: list or dictionary of CDistortion objects, or a single CDist object
        :param A_or_p: if <1 interpreted as a quantile, otherwise assets
        :return:
        """
        logger.warning('Portfolio.top_down is deprecated. It has been replaced by Portfolio.example_factory.')

    def analysis_priority(self, asset_spec, output='df'):
        """
        Create priority analysis report_ser.
        Can be called multiple times with different ``asset_specs``
        asset_spec either a float used as an epd percentage or a dictionary. Entering an epd percentage
        generates the dictionary

                base = {i: self.epd_2_assets[('not ' + i, 0)](asset_spec) for i in self.line_names}

        :param asset_spec: epd
        :param output: df = pandas data frame; html = nice report, markdown = raw markdown text
        :return:
        """
        ea = self.epd_2_assets
        ae = self.assets_2_epd
        if isinstance(asset_spec, dict):
            base = asset_spec
        else:
            if type(asset_spec) != float:
                raise ValueError('Input dictionary or float = epd target')
            base = {i:ea[('not ' + i, 0)](asset_spec) for i in self.line_names}
        if output == 'df':
            priority_analysis_df = pd.DataFrame(columns=[
             'a', 'chg a', 'not_line epd sa @a', 'line epd @a 2pri', 'not_line epd eq pri',
             'line epd eq pri', 'total epd'],
              index=pd.MultiIndex.from_arrays([[], []], names=['Line', 'Scenario']))
            for col in set(self.line_names).intersection(set(base.keys())):
                notcol = 'not ' + col
                a_base = base[col]
                a = a_base
                e0 = ae[(notcol, 0)](a_base)
                e = e0
                priority_analysis_df.loc[(col, 'base'), :] = (
                 a, a - a_base, e, ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a), ae[('total', 0)](a))
                a = ea[(col, 2)](e0)
                priority_analysis_df.loc[(col, '2pri line epd = not line sa'), :] = (
                 a, a - a_base, ae[(notcol, 0)](a), ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a),
                 ae[('total', 0)](a))
                a = ea[(col, 2)](priority_analysis_df.ix[((col, 'base'), 'line epd eq pri')])
                priority_analysis_df.loc[(col, 'thought buying (line 2pri epd = base not line eq pri epd'), :] = (
                 a, a - a_base, ae[(notcol, 0)](a), ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a),
                 ae[('total', 0)](a))
                a = ea[(notcol, 1)](e0)
                priority_analysis_df.loc[(col, 'fair to not line, not line eq pri epd = base sa epd'), :] = (
                 a, a - a_base, ae[(notcol, 0)](a), ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a),
                 ae[('total', 0)](a))
                a = ea[(col, 1)](e0)
                priority_analysis_df.loc[(col, 'line eq pri epd = base not line sa'), :] = (
                 a, a - a_base, ae[(notcol, 0)](a), ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a),
                 ae[('total', 0)](a))
                a = ea[('total', 0)](e0)
                priority_analysis_df.loc[(col, 'total epd = base sa not line epd'), :] = (
                 a, a - a_base, ae[(notcol, 0)](a), ae[(col, 2)](a), ae[(notcol, 1)](a), ae[(col, 1)](a),
                 ae[('total', 0)](a))

            priority_analysis_df.loc[:, 'pct chg'] = priority_analysis_df.loc[:, 'chg a'] / priority_analysis_df.a
            return priority_analysis_df
            ans = []
            for line in set(self.line_names).intersection(set(base.keys())):
                a = base[line]
                e = ae[(f"not {line}", 0)](a)
                a0 = float(ea[('total', 0)](e))
                eb0a0 = ae[(f"not {line}", 0)](a0)
                eba0 = ae[(f"not {line}", 1)](a0)
                e2a0 = ae[(line, 2)](a0)
                e1a0 = ae[(line, 1)](a0)
                e2 = ae[(line, 2)](a)
                e1 = float(ae[(line, 1)](a))
                a2 = float(ea[(line, 2)](e1))
                af = float(ea[(f"not {line}", 1)](e))
                af2 = float(ea[(line, 1)](e))
                a3 = float(ea[(line, 2)](e))
                a4 = float(ea[(f"not {line}", 1)](e))
                story = f"\nConsider adding **{line}** to the existing portfolio. The existing portfolio has capital {a:,.1f} and and epd of {e:.4g}.\n\n* If {line} is added as second priority to the existing lines with no increase in capital it has an epd of {e2:.4g}.\n* If the regulator requires the overall epd be a constant then the firm must increase capital to {a0:,.1f} or by {(a0 / a - 1) * 100:.2f} percent.\n    - At the higher capital {line} has an epd of {e2a0:.4g} as second priority and the existing lines have an epd of {eb0a0:.4g} as first priority.\n    - The existing and {line} epds under equal priority are {eba0:.4g} and {e1a0:.4g}.\n* If {line} *thought* it was added at equal priority it would have expected an epd of {e1:.4g}.\n  In order to achieve this epd as second priority would require capital of {a2:,.1f}, an increase of {(a2 / a - 1) * 100:.2f} percent.\n* In order for {line} to have an epd equal to the existing lines as second priority would require capital\n  of {a3:,.1f}, and increase of {(a3 / a - 1) * 100:.2f} percent.\n* In order for {line} to be added at equal priority and for the existing lines to have an unchanged epd requires capital of {af:,.1f}, an\n  increase of {(af / a - 1) * 100:.2f} percent.\n* In order for {line} to be added at equal priority and to have an epd equal to the existing line epd requires capital of {af2:,.1f}, an\n  increase of {(af2 / a - 1) * 100:.2f} percent.\n* In order for the existing lines to have an unchanged epd at equal priority requires capital of {a4:,.1f}, an increase of {(a4 / a - 1) * 100:.2f} percent.\n"
                ans.append(story)

            ans = '\n'.join(ans)
            if output == 'html':
                display(HTML(pypandoc.convert_text(ans, to='html', format='markdown')))
        else:
            return ans

    def analysis_collateral(self, line, c, a, debug=False):
        """
        E(C(a,c)) expected value of line against not line with collateral c and assets a, c <= a

        :param line: line of business with collateral, analyzed against not line
        :param c: collateral, c <= a required; c=0 reproduces exa, c=a reproduces lev
        :param a: assets, assumed less than the max loss (i.e. within the square)
        :param debug:
        :return:
        """
        if not c <= a:
            raise AssertionError
        else:
            xs = self.density_df.loc[:, 'loss'].values
            pline = self.density_df.loc[:, 'p_' + line].values
            notline = self.density_df.loc[:, 'ημ_' + line].values
            ans = []
            gt, incr, int1, int2, int3 = (0, 0, 0, 0, 0)
            c1, c2, c3 = (0, 0, 0)
            n_c = int(c / self.bs)
            n_max = len(xs)
            err_count = 0
            for loss in np.arange(a + self.bs, 2 * xs.max(), self.bs):
                n_loss = int(loss / self.bs)
                c1 = c / a * loss
                n_c1 = min(n_max, int(c1 / self.bs))
                la = max(0, n_loss - (n_max - 1))
                lc = min(n_loss, n_max - 1)
                lb = lc + 1
                if la == 0:
                    ld = None
                else:
                    ld = la - 1
                try:
                    s1 = slice(la, max(la, min(lb, n_c)))
                    s2 = slice(max(la, min(lb, n_c)), max(la, min(lb, n_c1)))
                    s3 = slice(max(la, min(lb, n_c1)), lb)
                    if ld is None:
                        s1r = slice(lc, min(lc, n_loss - n_c), -1)
                        s2r = slice(min(lc, n_loss - n_c), min(lc, n_loss - n_c1), -1)
                        s3r = slice(min(lc, n_loss - n_c1), ld, -1)
                    else:
                        s1r = slice(lc, max(ld, min(lc, n_loss - n_c)), -1)
                        s2r = slice(max(ld, min(lc, n_loss - n_c)), max(ld, min(lc, n_loss - n_c1)), -1)
                        s3r = slice(max(ld, min(lc, n_loss - n_c1)), ld, -1)
                    int1 = np.sum(xs[s1] * pline[s1] * notline[s1r])
                    int2 = c * np.sum(pline[s2] * notline[s2r])
                    int3 = a / loss * np.sum(xs[s3] * pline[s3] * notline[s3r])
                    ptot = np.sum(pline[s3] * notline[s3r])
                except ValueError as e:
                    try:
                        print(e)
                        print(f"Value error: loss={loss}, loss/b={loss / self.bs}, c1={c1}, c1/b={c1 / self.bs}")
                        print(f"n_loss {n_loss},  n_c {n_c}, n_c1 {n_c1}")
                        print(f"la={la}, lb={lb}, lc={lc}, ld={ld}")
                        print(*('ONE:', ), *map(len, [xs[s1], pline[s1], notline[s1r]]))
                        print(*('TWO:', ), *map(len, [pline[s2], notline[s2r]]))
                        print(*('THR:', ), *map(len, [xs[s3], pline[s3], notline[s3r]]))
                        err_count += 1
                        if err_count > 3:
                            break
                    finally:
                        e = None
                        del e

                if n_loss < n_max:
                    p = self.density_df.loc[(loss, 'p_total')]
                else:
                    p = np.nan
                incr = int1 + int2 + int3
                gt += incr
                c1 += int1
                c2 += int2
                c3 += int3
                if debug:
                    ans.append([loss, int1, int2, int3, int3 * loss / a / ptot, ptot, incr, c1, c2, c3, gt, p])
                if incr / gt < 1e-12:
                    if debug:
                        logger.info(f"incremental change {incr / gt:12.6f}, breaking")
                    break

            exlea = self.density_df.loc[(a, 'exlea_' + line)]
            exgta = self.density_df.loc[(a, 'exgta_' + line)]
            exix = self.density_df.loc[(a, 'exi_xgta_' + line)]
            exeqa = self.density_df.loc[(a, 'exeqa_' + line)]
            p_total = self.density_df.loc[(a, 'p_total')]
            F = self.density_df.loc[(a, 'F')]
            exa = self.density_df.loc[(a, 'exa_' + line)]
            lev = self.density_df.loc[(a, 'lev_' + line)]
            df = pd.DataFrame([
             (
              line, a, c, p_total, F, gt, a * exix * (1 - F), exeqa, exlea, exgta, exix, exa, gt + exlea * F, lev)],
              columns=[
             'line', 'a', 'c', 'p_total', 'F', 'gt', 'exa_delta', 'exeqa', 'exlea', 'exgta', 'exix', 'exa',
             'ecac', 'lev'])
            if debug:
                ans = pd.DataFrame(ans, columns=[
                 'loss', 'int1', 'int2', 'int3', 'exeqa', 'ptot', 'incr', 'c1', 'c2', 'c3', 'gt',
                 'log'])
                ans = ans.set_index('loss', drop=True)
                ans.index.name = 'loss'
            else:
                ans = None
        return (
         df, ans)

    def uat_differential(self, line):
        """
        Check the numerical and theoretical derivatives of exa agree for given line

        :param line:
        :return:
        """
        test = self.density_df[f"exa_{line}"]
        dtest = np.gradient(test, test.index)
        dtest2 = self.density_df.loc[:, f"exi_xgta_{line}"] * self.density_df.S
        ddtest = np.gradient(dtest)
        ddtest2 = -self.density_df.loc[:, f"exeqa_{line}"] / self.density_df.loss * self.density_df.p_total
        f, axs = plt.subplots(1, 3, figsize=(12, 4))
        axs[0].plot((test.index), test, label=f"exa_{line}")
        axs[1].plot((test.index), dtest, label='numdiff')
        axs[1].plot((test.index), dtest2, label='xi_xgta S(x)')
        axs[1].legend()
        axs[2].plot((test.index), ddtest, label='numdiff')
        axs[2].plot((test.index), ddtest2, label='-EXi(a)/a')
        axs[2].legend()

    def uat(self, As=None, Ps=[0.98], LRs=[0.965], r0=0.03, num_plots=1, verbose=False):
        """
        Reconcile apply_distortion(s) with price and calibrate

        :type Ps: object
        :param As:   Asset levels
        :param Ps:   probability levels used to determine asset levels using quantile function
        :param LRs:  loss ratios used to determine profitability
        :param r0:   r0 level for distortions
        :param verbose: controls level of output
        :return:
        """
        if As is None:
            As = []
            for p in Ps:
                As.append(self.q(p))

        else:
            params = self.calibrate_distortions(LRs=LRs, As=As, r0=r0)
            K = As[0]
            LR = LRs[0]
            idx = (K, LR)
            dd = Distortion.distortions_from_params(params, index=idx, r0=r0, plot=False)
            if num_plots == 2:
                axiter = axiter_factory(None, len(dd))
            else:
                if num_plots == 3:
                    axiter = axiter_factory(None, 30)
                else:
                    axiter = None
            table, stacked = self.apply_distortions(dd, As, axiter, num_plots)
            table['lr err'] = table['lr_total'] - LR
            pdfs = []
            for name in Distortion.available_distortions():
                pdf, _ = self.price(reg_g=K, pricing_g=(dd[name]))
                pdf['dist'] = name
                pdfs.append(pdf)

            p = pd.concat(pdfs)
            p['lr err'] = p['lr'] - LR
            a = table.query(f" loss=={K} ")
            logger.info(f"Portfolio.uat | {self.name} Sum of parts all close to total: {np.allclose(a.exag_total, a.exag_sumparts)}")
            logger.info(f"Portfolio.uat | {self.name} Sum of parts vs total: {np.sum(np.abs(a.exag_total - a.exag_sumparts)):15,.1f}")
            pp = p[['dist', 'exag']]
            pp = pp.pivot(columns='dist').T.loc['exag']
            aa = a.filter(regex='exa|method').set_index('method')
            test = pd.concat((aa, pp), axis=1, sort=True)
            for c in self.line_names_ex:
                test[f"err_{c}"] = test[c] / test[f"exag_{c}"] - 1

            test['err sum/total'] = test['exag_sumparts'] / test['exag_total'] - 1
            test = test[([f"{i}{j}" for j in self.line_names_ex for i in ('exag_',
                                                                          '', 'err_')] + ['exag_sumparts', 'err sum/total'])]
            lr_err = pd.DataFrame({'applyLR':a.lr_total,  'method':a.method,  'target':LR,  'errs':a.lr_total - LR})
            lr_err = lr_err.reset_index(drop=False).set_index('method')
            lr_err = lr_err.rename(columns={'index': 'a'})
            test = pd.concat((test, lr_err), axis=1, sort=True)
            overall_test = test.filter(regex='err').abs().sum().sum()
            if verbose:
                html_title(f"Combined, overall error {overall_test:.3e}")
                display(test)
            if lr_err.errs.abs().max() > 0.0001:
                logger.error('Portfolio.uat | {self.name} UAT Loss Ratio Error {lr_err.errs.abs().max()}')
            if overall_test < 1e-07:
                logger.info(f"Portfolio.uat | {self.name} UAT All good, total error {overall_test:6.4e}")
            else:
                s = f"{self.name} UAT total error {overall_test:6.4e}"
                logger.error(f"Portfolio.uat | {s}")
                logger.error(f"Portfolio.uat | {s}")
                logger.error(f"Portfolio.uat | {s}")
        return (
         a, p, test, params, dd, table, stacked)

    @property
    def renamer(self):
        """
        write a sensible renamer for the columns to use thusly

        self.density_df.rename(columns=renamer)

        write a tex version separately
        Create once per item...assume lines etc. never change

        :return: dictionary that can be used to rename columns
        """
        if self._renamer is None:
            self._renamer = {}
            meta_namer = dict(p_=('', ' density'), lev_=('LEV[', 'a]'),
              exag_=('EQ[', '(a)]'),
              exa_=('E[', '(a)]'),
              exlea_=('E[', ' | X<=a]'),
              exgta_=('E[', ' | X>a]'),
              exeqa_=('E[', ' | X=a]'),
              e1xi_1gta_=('E[1/', ' 1(X>a)]'),
              exi_x_=('E[', '/X]'),
              exi_xgta_sum=('Sum Xi/X gt', ''),
              exi_xeqa_sum=('Sum Xi/X eq', ''),
              exi_xgta_=('α=E[', '/X | X>a]'),
              exi_xeqa_=('E[', '/X | X=a]'),
              exi_xlea_=('E[', '/X | X<=a]'),
              epd_0_=('EPD(', ') stand alone'),
              epd_1_=('EPD(', ') within X'),
              epd_2_=('EPD(', ') second pri'),
              e2pri_=('E[X', '(a) second pri]'),
              ημ_=('All but ', ' density'))
            for l in self.density_df.columns:
                if re.search('^ημ_', l):
                    self._renamer[l] = re.sub('^ημ_([A-Za-z\\-_.,]+)', 'not \\1 density', l)
                else:
                    l0 = l.replace('ημ_', 'not ')
                    for k, v in meta_namer.items():
                        d1 = l0.find(k)
                        if d1 >= 0:
                            d1 += len(k)
                            b, a = v
                            self._renamer[l] = f"{b}{l0[d1:]}{a}".replace('total', 'X')
                            break

            for l in self.line_names_ex:
                self._renamer[f"exag_{l}"] = f"EQ[{l}(a)]"
                self._renamer[f"exi_xgtag_{l}"] = f"β=EQ[{l}/X | X>a]"
                self._renamer[f"exi_xleag_{l}"] = f"EQ[{l}/X | X<=a]"
                self._renamer[f"e1xi_1gta_{l}"] = f"E[{l}/X 1(X >a)]"

            self._renamer['exag_sumparts'] = 'Sum of EQ[Xi(a)]'
            for pre, m1 in zip(['M', 'T'], ['Marginal', 'Total']):
                for post, m2 in zip(['L', 'P', 'LR', 'Q', 'ROE', 'PQ', 'M'], [
                 'Loss', 'Premium', 'Loss Ratio', 'Equity', 'ROE', 'Leverage (P:S)', 'Margin']):
                    self._renamer[f"{pre}.{post}"] = f"{m1} {m2}"

            for line in self.line_names_ex:
                for pre, m1 in zip(['M', 'T'], ['Marginal', 'Total']):
                    for post, m2 in zip(['L', 'P', 'LR', 'Q', 'ROE', 'PQ', 'M'], [
                     'Loss', 'Premium', 'Loss Ratio', 'Equity', 'ROE', 'Leverage (P:S)', 'Margin']):
                        self._renamer[f"{pre}.{post}_{line}"] = f"{m1} {m2} {line}"

            self._renamer['A'] = 'Assets'
            self._renamer['exi/xgta'] = 'α=E[Xi/X | X > a]'
            self._renamer['exi/xgtag'] = 'β=E_Q[Xi/X | X > a]'
            for l in self.line_names:
                self._renamer[f"gamma_{l}_sa"] = f"γ {l} stand-alone"
                self._renamer[f"gamma_{self.name}_{l}"] = f"γ {l} part of {self.name}"
                self._renamer[f"p_{l}"] = f"{l} stand-alone density"
                self._renamer[f"S_{l}"] = f"{l} stand-alone survival"

            self._renamer['p_total'] = f"{self.name} total density"
            self._renamer['S_total'] = f"{self.name} total survival"
            self._renamer[f"gamma_{self.name}_total"] = f"γ {self.name} total"
        return self._renamer

    def cumintegral(self, v, bs_override=0):
        """
        cumulative integral of v with buckets size bs

        :param bs_override:
        :param v:
        :return:
        """
        if bs_override != 0:
            bs = bs_override
        else:
            bs = self.bs
        if type(v) == np.ndarray:
            logger.warning('CALLING cumintegral on a numpy array!!\nCALLING cumintegral on a numpy array!!\nCALLING cumintegral on a numpy array!!\nCALLING cumintegral on a numpy array!!\nCALLING cumintegral on a numpy array!!\n')
            return np.hstack((0, v[:-1])).cumsum() * bs
        return v.shift(1, fill_value=0).cumsum() * bs

    @staticmethod
    def from_DataFrame(name, df):
        """
        create portfolio from pandas dataframe
        uses columns with appropriate names

        Can be fed the agg output of uw.write_test( agg_program )

        :param name:
        :param df:
        :return:
        """
        spec_list = [g.dropna(axis=1).to_dict(orient='list') for n, g in df.groupby('name')]
        return Portfolio(name, spec_list)

    @staticmethod
    def from_Excel(name, ffn, sheet_name, **kwargs):
        """
        read in from Excel

        works via a Pandas dataframe; kwargs passed through to pd.read_excel
        drops all blank columns (mostly for auditing purposes)

        :param name:
        :param ffn: full file name, including path
        :param sheet_name:
        :param kwargs:
        :return:
        """
        df = (pd.read_excel)(ffn, sheet_name=sheet_name, **kwargs)
        df = df.dropna(axis=1, how='all')
        return Portfolio.from_DataFrame(name, df)

    @staticmethod
    def from_dict_of_aggs(prefix, agg_dict, sub_ports=None, uw=None, bs=0, log2=0, padding=2, **kwargs):
        """
        Create a portfolio from any iterable with values aggregate code snippets

        e.g.  agg_dict = {label: agg_snippet }

        will create all the portfolios specified in subsets, or all if subsets=='all'

        labels for subports are concat of keys in agg_dict, so recommend you use A:, B: etc.
        as the snippet names.  Portfolio names are prefix_[concat element names]

        agg_snippet is line agg blah without the tab or newline

        :param prefix:
        :param agg_dict:
        :param sub_ports:
        :param bs, log2, padding, kwargs: passed through to update; update if bs * log2 > 0
        :return:
        """
        agg_names = list(agg_dict.keys())
        ports = Answer()
        if sub_ports == 'all':
            sub_ports = subsets(agg_names)
        for sub_port in sub_ports:
            name = ''.join(sub_port)
            if prefix != '':
                name = f"{prefix}_{name}"
            else:
                pgm = f"port {name}\n"
                for l in agg_names:
                    if l in sub_port:
                        pgm += f"\t{agg_dict[l]}\n"

                if uw:
                    ports[name] = uw(pgm)
                else:
                    ports[name] = pgm
            if uw and bs * log2 > 0:
                (ports[name].update)(bs=bs, log2=log2, padding=padding, **kwargs)

        return ports