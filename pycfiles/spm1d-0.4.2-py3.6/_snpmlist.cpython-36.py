# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/nonparam/_snpmlist.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 4974 bytes
import numpy as np
from . import _snpm
from .. import _spmlist

class SnPMFList0D(_spmlist.SPMFList, _snpm._SnPM0D):
    name = 'SnPM{F} list'
    isparametric = False

    def __init__(self, z, perm, nFactors=2):
        z = [0 if np.isnan(zz) else zz for zz in z]
        FF = [_snpm.SnPM0D_F(zz, isinlist=True) for zz in z]
        super(SnPMFList0D, self).__init__(FF)
        self.permuter = perm
        self.nPermUnique = perm.nPermTotal
        self.nFactors = nFactors
        self.z = z
        self.set_design_label(perm.get_design_label())
        self.set_effect_labels(perm.get_effect_labels())

    def _repr_get_header(self):
        s = '%s\n' % self.name
        s += '   design      :  %s\n' % self.design
        s += '   nEffects    :  %d\n' % self.nEffects
        s += '   nPermUnique :  %s\n' % self.get_nPermUnique_asstr()
        return s

    def inference(self, alpha=0.05, iterations=-1, force_iterations=False):
        self._check_iterations(iterations, alpha, force_iterations)
        self.permuter.build_pdf(iterations)
        zstarlist = self.permuter.get_z_critical_list(alpha)
        plist = self.permuter.get_p_value_list(self.z, zstarlist, alpha)
        return SnPMFiList0D(self, alpha, zstarlist, plist, iterations)


class SnPMFiList0D(_spmlist.SPMFiList, _snpm._SnPM):
    name = 'SnPM{F} inference list'
    isparametric = False

    def __init__(self, snpmlist, alpha, zstarvalues, pvalues, iterations):
        FFi = []
        for F, zstar, p in zip(snpmlist, zstarvalues, pvalues):
            Fi = _snpm.SnPM0DiF(F, alpha, zstar, p, isinlist=True)
            FFi.append(Fi)

        super(SnPMFiList0D, self).__init__(FFi)
        self.alpha = alpha
        self.permuter = snpmlist.permuter
        self.nPermUnique = snpmlist.permuter.nPermTotal
        self.nPermActual = snpmlist.permuter.Z.shape[0]
        self.nFactors = snpmlist.nFactors
        self.z = [Fi.z for Fi in self]
        self.set_design_label(self.permuter.get_design_label())
        self.set_effect_labels(self.permuter.get_effect_labels())

    def _repr_get_header(self):
        s = '%s\n' % self.name
        s += '   design      :  %s\n' % self.design
        s += '   nEffects    :  %d\n' % self.nEffects
        s += '   nPermUnique :  %s\n' % self.get_nPermUnique_asstr()
        s += '   nPermActual :  %d\n' % self.nPermActual
        return s


class SnPMFList(_spmlist.SPMFList, _snpm._SnPM1D):
    name = 'SnPM{F} list'
    isparametric = False

    def __init__(self, z, perm, nFactors=2):
        FF = [_snpm.SnPM_F(zz, perm, isinlist=True) for zz in z]
        super(SnPMFList, self).__init__(FF)
        self.permuter = perm
        self.nPermUnique = perm.nPermTotal
        self.nFactors = nFactors
        self.z = z
        self.set_design_label(perm.get_design_label())
        self.set_effect_labels(perm.get_effect_labels())

    def _repr_get_header(self):
        s = '%s\n' % self.name
        s += '   design      :  %s\n' % self.design
        s += '   nEffects    :  %d\n' % self.nEffects
        s += '   nPermUnique :  %s\n' % self.get_nPermUnique_asstr()
        return s

    def build_secondary_pdf(self, zstarlist, circular=False):
        self.permuter.build_secondary_pdf(zstar, circular)

    def inference(self, alpha=0.05, iterations=-1, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
        self._check_iterations(iterations, alpha, force_iterations)
        self.permuter.build_pdf(iterations)
        zstarlist = self.permuter.get_z_critical_list(alpha)
        self.permuter.set_metric(cluster_metric)
        self.permuter.build_secondary_pdfs(zstarlist, circular)
        FFi = []
        for F, zstar in zip(self, zstarlist):
            clusters = F._get_clusters(zstar, False, interp, circular, iterations, cluster_metric)
            clusters = F._cluster_inference(clusters, False)
            Fi = _snpm.SnPMiF(F, alpha, zstar, clusters)
            FFi.append(Fi)

        return SnPMFiList(self, FFi)


class SnPMFiList(SnPMFList):
    name = 'SnPM{F} inference list'
    isparametric = False

    def __init__(self, snpmlist, FFi, nFactors=2):
        super(SnPMFList, self).__init__(FFi)
        self.permuter = snpmlist.permuter
        self.nPermUnique = snpmlist.nPermUnique
        self.nFactors = snpmlist.nFactors
        self.set_design_label(self.permuter.get_design_label())
        self.set_effect_labels(self.permuter.get_effect_labels())