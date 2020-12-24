# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/_spm.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 21139 bytes
"""
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
"""
import sys, numpy as np
from scipy import stats
from .. import rft1d
from ..plot import plot_spm, plot_spm_design
from ..plot import plot_spmi, plot_spmi_p_values, plot_spmi_threshold_label
from ._clusters import Cluster

def df2str(df):
    if not df % 1:
        return str(df)
    else:
        return '%.3f' % df


def dflist2str(dfs):
    return '(%s, %s)' % (df2str(dfs[0]), df2str(dfs[1]))


def p2string(p):
    if p < 0.0005:
        return '<0.001'
    else:
        return '%.03f' % p


def plist2string(pList):
    s = ''
    if len(pList) > 0:
        for p in pList:
            s += p2string(p)
            s += ', '

        s = s[:-2]
    return s


def _set_docstr(childfn, parentfn, args2remove=None):
    docstr = parentfn.__doc__
    if args2remove != None:
        docstrlist0 = docstr.split('\n\t')
        docstrlist1 = []
        for s in docstrlist0:
            if not np.any([s.startswith('- *%s*' % argname) for argname in args2remove]):
                docstrlist1.append(s)

        docstrlist1 = [s + '\n\t' for s in docstrlist1]
        docstr = ''.join(docstrlist1)
    if sys.version_info.major == 2:
        childfn.__func__.__doc__ = docstr
    elif sys.version_info.major == 3:
        childfn.__doc__ = docstr


class _SPMParent(object):
    __doc__ = 'Parent class for all parametric SPM classes.'
    isanova = False
    isinference = False
    isregress = False
    isparametric = True
    dim = 0


class _SPMF(object):
    __doc__ = 'Additional attrubutes and methods specific to SPM{F} objects.'
    effect = 'Main A'
    effect_short = 'A'
    isanova = True

    def set_effect_label(self, label=''):
        self.effect = str(label)
        self.effect_short = self.effect.split(' ')[1]


class _SPM0D(_SPMParent):

    def __init__(self, STAT, z, df, beta=None, residuals=None, sigma2=None):
        self.STAT = STAT
        self.z = float(z)
        self.df = df
        self.beta = beta
        self.residuals = residuals
        self.sigma2 = sigma2

    def __repr__(self):
        stat = 't' if self.STAT == 'T' else self.STAT
        s = ''
        s += 'SPM{%s} (0D)\n' % stat
        if self.isanova:
            s += '   SPM.effect   :  %s\n' % self.effect
            s += '   SPM.SS       : (%s, %s)\n' % self.ss
            s += '   SPM.df       : (%s, %s)\n' % self.df
            s += '   SPM.MS       : (%s, %s)\n' % self.ms
            s += '   SPM.z        :  %.5f\n' % self.z
        else:
            s += '   SPM.z      :  %.5f\n' % self.z
            s += '   SPM.df     :  %s\n' % dflist2str(self.df)
        if self.isregress:
            s += '   SPM.r      :  %.5f\n' % self.r
        s += '\n'
        return s


class _SPM0Dinference(_SPM0D):
    isinference = True

    def __init__(self, spm, alpha, zstar, p, two_tailed=False):
        _SPM0D.__init__(self, (spm.STAT), (spm.z), (spm.df), beta=(spm.beta), residuals=(spm.residuals), sigma2=(spm.sigma2))
        self.alpha = alpha
        self.zstar = zstar
        self.h0reject = abs(spm.z) > zstar if two_tailed else spm.z > zstar
        self.p = p
        self.two_tailed = two_tailed
        self.isanova = spm.isanova
        self.isregress = spm.isregress
        if self.isanova:
            self.set_effect_label(spm.effect)
            self.ss = spm.ss
            self.ms = spm.ms
        if self.isregress:
            self.r = spm.r

    def __repr__(self):
        s = ''
        s += 'SPM{%s} (0D) inference\n' % self.STAT
        if self.isanova:
            s += '   SPM.effect   :  %s\n' % self.effect
            s += '   SPM.SS       : (%s, %s)\n' % self.ss
            s += '   SPM.df       : (%s, %s)\n' % self.df
            s += '   SPM.MS       : (%s, %s)\n' % self.ms
            s += '   SPM.z        :  %.5f\n' % self.z
        else:
            s += '   SPM.z        :  %.5f\n' % self.z
            s += '   SPM.df       :  %s\n' % dflist2str(self.df)
        if self.isregress:
            s += '   SPM.r        :  %.5f\n' % self.r
        s += 'Inference:\n'
        s += '   SPM.alpha    :  %.3f\n' % self.alpha
        s += '   SPM.zstar    :  %.5f\n' % self.zstar
        s += '   SPM.h0reject :  %s\n' % self.h0reject
        s += '   SPM.p        :  %.5f\n' % self.p
        s += '\n'
        return s


class SPM0D_F(_SPMF, _SPM0D):

    def __init__(self, z, df, ss=(0, 0), ms=(0, 0), eij=0, X0=None):
        _SPM0D.__init__(self, 'F', z, df)
        self.ss = tuple(map(float, ss))
        self.ms = tuple(map(float, ms))
        self.eij = eij
        self.residuals = np.asarray(eij).flatten()
        self.X0 = X0

    def _repr_summ(self):
        return '{:<5} F = {:<8} df = {}\n'.format(self.effect_short, '%.3f' % self.z, dflist2str(self.df))

    def inference(self, alpha=0.05):
        zstar = stats.f.isf(alpha, self.df[0], self.df[1])
        p = stats.f.sf(self.z, self.df[0], self.df[1])
        return SPM0Di_F(self, alpha, zstar, p)


class SPM0D_T(_SPM0D):

    def __init__(self, z, df, beta=None, residuals=None, sigma2=None):
        _SPM0D.__init__(self, 'T', z, df, beta=beta, residuals=residuals, sigma2=sigma2)

    def inference(self, alpha=0.05, two_tailed=True):
        a = 0.5 * alpha if two_tailed else alpha
        z = abs(self.z) if two_tailed else self.z
        zstar = stats.t.isf(a, self.df[1])
        p = stats.t.sf(z, self.df[1])
        p = min(1, 2 * p) if two_tailed else p
        return SPM0Di_T(self, alpha, zstar, p, two_tailed)


class SPM0D_T2(_SPM0D):

    def __init__(self, z, df):
        _SPM0D.__init__(self, 'T2', z, df)

    def inference(self, alpha=0.05):
        zstar = rft1d.T2.isf0d(alpha, self.df)
        p = rft1d.T2.sf0d(self.z, self.df)
        return SPM0Di_T2(self, alpha, zstar, p)


class SPM0D_X2(_SPM0D):

    def __init__(self, z, df, residuals=None):
        _SPM0D.__init__(self, 'X2', z, df, residuals=residuals)

    def inference(self, alpha=0.05):
        zstar = rft1d.chi2.isf0d(alpha, self.df[1])
        p = rft1d.chi2.sf0d(self.z, self.df[1])
        return SPM0Di_X2(self, alpha, zstar, p)


class SPM0Di_F(_SPMF, _SPM0Dinference):
    __doc__ = 'An SPM{F} (0D) inference object.'

    def _repr_summ(self):
        return '{:<5} F = {:<8} df = {:<9} p = {}\n'.format(self.effect.split(' ')[1], '%.3f' % self.z, dflist2str(self.df), p2string(self.p))


class SPM0Di_T(_SPM0Dinference):
    __doc__ = 'An SPM{T} (0D) inference object.'


class SPM0Di_T2(_SPM0Dinference):
    __doc__ = 'An SPM{T2} (0D) inference object.'


class SPM0Di_X2(_SPM0Dinference):
    __doc__ = 'An SPM{X2} (0D) inference object.'


class _SPM(_SPMParent):
    dim = 1

    def __init__(self, STAT, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
        self.STAT = STAT
        self.Q = z.size
        self.Qmasked = z.size
        self.X = X
        self.beta = beta
        self.residuals = residuals
        self.sigma2 = sigma2
        self.z = z
        self.df = df
        self.fwhm = fwhm
        self.resels = resels
        self.roi = roi
        self._ClusterClass = Cluster
        if roi is not None:
            self.Qmasked = self.z.count()

    def __repr__(self):
        stat = self.STAT
        if stat == 'T':
            stat = 't'
        s = ''
        s += 'SPM{%s}\n' % stat
        if self.isanova:
            s += '   SPM.effect :   %s\n' % self.effect
        s += '   SPM.z      :  %s\n' % self._repr_teststat()
        s += '   SPM.df     :  %s\n' % dflist2str(self.df)
        s += '   SPM.fwhm   :  %.5f\n' % self.fwhm
        s += '   SPM.resels :  (%d, %.5f)\n\n\n' % tuple(self.resels)
        return s

    def _repr_teststat(self):
        return '(1x%d) test stat field' % self.Q

    def _repr_teststat_short(self):
        return '(1x%d) array' % self.Q

    def _build_spmi(self, alpha, zstar, clusters, p_set, two_tailed):
        p_clusters = [c.P for c in clusters]
        if self.STAT == 'T':
            spmi = SPMi_T(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
        else:
            if self.STAT == 'F':
                spmi = SPMi_F(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
            else:
                if self.STAT == 'T2':
                    spmi = SPMi_T2(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
                else:
                    if self.STAT == 'X2':
                        spmi = SPMi_X2(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
        return spmi

    def _cluster_geom(self, u, interp, circular, csign=1, z=None):
        Q = self.Q
        Z = self.z if z is None else z
        X = np.arange(Q)
        if np.ma.is_masked(Z):
            i = Z.mask
            Z = np.array(Z)
            B = csign * Z >= u
            B[i] = False
            Z[i] = np.nan
        else:
            B = csign * Z >= u
        Z = csign * Z
        L, n = rft1d.geom.bwlabel(B)
        clusters = []
        for i in range(n):
            b = L == i + 1
            x, z = X[b].tolist(), Z[b].tolist()
            if x[0] > 0 and not np.isnan(Z[(x[0] - 1)]):
                z0, z1 = Z[(x[0] - 1)], Z[x[0]]
                dx = (z1 - u) / (z1 - z0)
                x = [x[0] - dx] + x
                z = [u] + z
            if x[(-1)] < Q - 1:
                if not np.isnan(Z[(x[(-1)] + 1)]):
                    z0, z1 = Z[x[(-1)]], Z[(x[(-1)] + 1)]
                    dx = (z0 - u) / (z0 - z1)
                    x += [x[(-1)] + dx]
                    z += [u]
            x, z = np.array(x), csign * np.array(z)
            clusters.append(self._ClusterClass(x, z, csign * u, interp))

        if circular:
            if clusters != []:
                xy = np.array([c.endpoints for c in clusters])
                i0, i1 = xy[:, 0] == 0, xy[:, 1] == Q - 1
                ind0, ind1 = np.argwhere(i0), np.argwhere(i1)
                if len(ind0) > 0:
                    if len(ind1) > 0:
                        ind0, ind1 = ind0[0][0], ind1[0][0]
                        if ind0 != ind1:
                            if clusters[ind0].csign == clusters[ind1].csign:
                                clusters[ind0].merge(clusters[ind1])
                                clusters.pop(ind1)
        return clusters

    def _cluster_inference(self, clusters, two_tailed, withBonf):
        for cluster in clusters:
            cluster.inference(self.STAT, self.df, self.fwhm, self.resels, two_tailed, withBonf, self.Q)

        return clusters

    def _get_clusters(self, zstar, check_neg, interp, circular, z=None):
        clusters = self._cluster_geom(zstar, interp, circular, csign=1, z=z)
        if check_neg:
            clustersn = self._cluster_geom(zstar, interp, circular, csign=(-1), z=z)
            clusters += clustersn
            if len(clusters) > 1:
                x = [c.xy[0] for c in clusters]
                ind = np.argsort(x).flatten()
                clusters = np.array(clusters)[ind].tolist()
        return clusters

    def _isf(self, a, withBonf):
        if self.STAT == 'T':
            zstar = rft1d.t.isf_resels(a, (self.df[1]), (self.resels), withBonf=withBonf, nNodes=(self.Q))
        else:
            if self.STAT == 'F':
                zstar = rft1d.f.isf_resels(a, (self.df), (self.resels), withBonf=withBonf, nNodes=(self.Q))
            else:
                if self.STAT == 'T2':
                    zstar = rft1d.T2.isf_resels(a, (self.df), (self.resels), withBonf=withBonf, nNodes=(self.Q))
                else:
                    if self.STAT == 'X2':
                        zstar = rft1d.chi2.isf_resels(a, (self.df[1]), (self.resels), withBonf=withBonf, nNodes=(self.Q))
        return zstar

    def _setlevel_inference(self, zstar, clusters, two_tailed, withBonf):
        nUpcrossings = len(clusters)
        p_set = 1.0
        if nUpcrossings > 0:
            extents = [c.extentR for c in clusters]
            minextent = min(extents)
            if self.STAT == 'T':
                p_set = rft1d.t.p_set_resels(nUpcrossings, minextent, zstar, (self.df[1]), (self.resels), withBonf=withBonf, nNodes=(self.Q))
                p_set = min(1, 2 * p_set) if two_tailed else p_set
            else:
                if self.STAT == 'F':
                    p_set = rft1d.f.p_set_resels(nUpcrossings, minextent, zstar, (self.df), (self.resels), withBonf=withBonf, nNodes=(self.Q))
                else:
                    if self.STAT == 'T2':
                        p_set = rft1d.T2.p_set_resels(nUpcrossings, minextent, zstar, (self.df), (self.resels), withBonf=withBonf, nNodes=(self.Q))
                    elif self.STAT == 'X2':
                        p_set = rft1d.chi2.p_set_resels(nUpcrossings, minextent, zstar, (self.df[1]), (self.resels), withBonf=withBonf, nNodes=(self.Q))
        return p_set

    def inference(self, alpha=0.05, cluster_size=0, two_tailed=False, interp=True, circular=False, withBonf=True):
        check_neg = two_tailed
        if self.roi is not None:
            if self.roi.dtype != bool:
                if two_tailed:
                    raise ValueError('If the ROI contains directional predictions two_tailed must be FALSE.')
                else:
                    check_neg = np.any(self.roi == -1)
        a = 0.5 * alpha if two_tailed else alpha
        zstar = self._isf(a, withBonf)
        clusters = self._get_clusters(zstar, check_neg, interp, circular)
        clusters = self._cluster_inference(clusters, two_tailed, withBonf)
        p_set = self._setlevel_inference(zstar, clusters, two_tailed, withBonf)
        spmi = self._build_spmi(alpha, zstar, clusters, p_set, two_tailed)
        return spmi

    def plot(self, **kwdargs):
        return plot_spm(self, **kwdargs)

    def plot_design(self, **kwdargs):
        plot_spm_design(self, **kwdargs)

    def toarray(self):
        return self.z.copy()


class SPM_F(_SPMF, _SPM):
    __doc__ = '\n\tCreate an SPM{F} continuum.\n\tSPM objects are instantiated in the **spm1d.stats** module.\n\t\n\t:Parameters:\n\t\n\ty : the SPM{F} continuum\n\t\n\tfwhm: estimated field smoothness (full-width at half-maximium)\n\t\n\tdf : 2-tuple specifying the degrees of freedom (interest,error)\n\t\n\tresels : 2-tuple specifying the resel counts\n\t\n\tX : experimental design matrix\n\t\n\tbeta : array of fitted model parameters\n\t\n\tresiduals : array of residuals (used for smoothness estimation)\n\t\n\t:Returns:\n\t\n\tA **spm1d._spm.SPM_F** instance.\n\t\n\t:Methods:\n\t'

    def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, X0=None, sigma2=None, roi=None):
        _SPM.__init__(self, 'F', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)
        self.X0 = X0

    def _repr_summ(self):
        return '{:<5} z = {:<18} df = {}\n'.format(self.effect_short, self._repr_teststat_short(), dflist2str(self.df))

    def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
        """
                Conduct statistical inference using random field theory.
                
                :Parameters:
                
                alpha        : Type I error rate (default: 0.05)
                
                cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
                :Returns:
                
                A **spm1d._spm.SPMi_F** instance.
                """
        return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)


class SPM_T(_SPM):
    __doc__ = '\n\tCreate an SPM{T} continuum.\n\tSPM objects are instantiated in the **spm1d.stats** module.\n\t\n\t:Parameters:\n\t\n\ty : the SPM{T} continuum\n\t\n\tfwhm: estimated field smoothness (full-width at half-maximium)\n\t\n\tdf : a 2-tuple specifying the degrees of freedom (interest,error)\n\t\n\tresels : a 2-tuple specifying the resel counts\n\t\n\tX : experimental design matrix\n\t\n\tbeta : array of fitted model parameters\n\t\n\tresiduals : array of residuals (used for smoothness estimation)\n\t\n\t:Returns:\n\t\n\tA **spm1d._spm.SPM_t** instance.\n\t\n\t:Methods:\n\t'

    def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
        _SPM.__init__(self, 'T', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)

    def inference(self, alpha=0.05, cluster_size=0, two_tailed=True, interp=True, circular=False):
        """
                Conduct statistical inference using random field theory.
                
                :Parameters:
                
                alpha        : Type I error rate (default: 0.05)
                
                cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
                
                two_tailed   : Conduct two-tailed inference (default: False)
                
                :Returns:
                
                A **spm1d._spm.SPMi_T** instance.
                """
        return _SPM.inference(self, alpha, cluster_size, two_tailed, interp, circular)


class SPM_T2(_SPM):

    def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
        super(SPM_T2, self).__init__('T2', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)

    def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
        """
                Conduct statistical inference using random field theory.
                
                :Parameters:
                
                alpha        : Type I error rate (default: 0.05)
                
                cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
                :Returns:
                
                A **spm1d._spm.SPMi_F** instance.
                """
        return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)


class SPM_X2(_SPM):

    def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
        super(SPM_X2, self).__init__('X2', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)

    def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
        """
                Conduct statistical inference using random field theory.
                
                :Parameters:
                
                alpha        : Type I error rate (default: 0.05)
                
                cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
                :Returns:
                
                A **spm1d._spm.SPMi_F** instance.
                """
        return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)


class _SPMinference(_SPM):
    __doc__ = 'Parent class for SPM inference objects.'
    isinference = True

    def __init__(self, spm, alpha, zstar, clusters, p_set, p, two_tailed=False):
        _SPM.__init__(self, (spm.STAT), (spm.z), (spm.df), (spm.fwhm), (spm.resels), X=(spm.X), beta=(spm.beta), residuals=(spm.residuals), sigma2=(spm.sigma2), roi=(spm.roi))
        self.alpha = alpha
        self.zstar = zstar
        self.clusters = clusters
        self.nClusters = len(clusters)
        self.h0reject = self.nClusters > 0
        self.p_set = p_set
        self.p = p
        self.two_tailed = two_tailed
        if self.isanova:
            self.set_effect_label(spm.effect)

    def __repr__(self):
        stat = 't' if self.STAT == 'T' else self.STAT
        s = ''
        s += 'SPM{%s} inference field\n' % stat
        if self.isanova:
            s += '   SPM.effect    :   %s\n' % self.effect
        s += '   SPM.z         :  (1x%d) raw test stat field\n' % self.Q
        s += '   SPM.df        :  %s\n' % dflist2str(self.df)
        s += '   SPM.fwhm      :  %.5f\n' % self.fwhm
        s += '   SPM.resels    :  (%d, %.5f)\n' % tuple(self.resels)
        s += 'Inference:\n'
        s += '   SPM.alpha     :  %.3f\n' % self.alpha
        s += '   SPM.zstar     :  %.5f\n' % self.zstar
        s += '   SPM.h0reject  :  %s\n' % self.h0reject
        s += '   SPM.p_set     :  %s\n' % p2string(self.p_set)
        s += '   SPM.p_cluster :  (%s)\n\n\n' % plist2string(self.p)
        return s

    def plot(self, **kwdargs):
        return plot_spmi(self, **kwdargs)

    def plot_p_values(self, **kwdargs):
        plot_spmi_p_values(self, **kwdargs)

    def plot_threshold_label(self, **kwdargs):
        return plot_spmi_threshold_label(self, **kwdargs)


class SPMi_T(_SPMinference):
    __doc__ = 'An SPM{t} inference continuum.'


class SPMi_F(_SPMF, _SPMinference):
    __doc__ = 'An SPM{F} inference continuum.'

    def _repr_summ(self):
        return '{:<5} z={:<18} df={:<9} h0reject={}\n'.format(self.effect_short, self._repr_teststat_short(), dflist2str(self.df), self.h0reject)


class SPMi_T2(_SPMinference):
    __doc__ = 'An SPM{T2} inference continuum.'


class SPMi_X2(_SPMinference):
    __doc__ = 'An SPM{X2} inference continuum.'


_set_docstr((_SPM.plot), plot_spm, args2remove=['spm'])
_set_docstr((_SPMinference.plot), plot_spmi, args2remove=['spmi'])
_set_docstr((_SPMinference.plot_p_values), plot_spmi_p_values, args2remove=['spmi'])
_set_docstr((_SPMinference.plot_threshold_label), plot_spmi_threshold_label, args2remove=['spmi'])