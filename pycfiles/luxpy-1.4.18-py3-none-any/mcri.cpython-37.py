# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cri\indices\mcri.py
# Compiled at: 2019-01-25 08:03:04
# Size of source mod 2**32: 8864 bytes
"""
###############################################################################
# Module for the memory color rendition index (MCRI), Rm
###############################################################################

 :_MCRI_DEFAULTS: default settings for MCRI 
                  (major dict has 9 keys (04-Jul-2017): 
                  sampleset [str/dict], 
                  ref_type [str], 
                  cieobs [str], 
                  avg [fcn handle], 
                  scale [dict], 
                  cspace [dict], 
                  catf [dict], 
                  rg_pars [dict], 
                  cri_specific_pars [dict])

 :spd_to_mcri(): Calculates the memory color rendition index, Rm:
    
Reference
    1. `K.A.G. Smet, W.R. Ryckaert, M.R. Pointer, G. Deconinck, P. Hanselaer,(2012)
    “A memory colour quality metric for white light sources,” 
    Energy Build., vol. 49, no. C, pp. 216–225.
    <http://www.sciencedirect.com/science/article/pii/S0378778812000837>`_

"""
from luxpy import np, cat, math, _CRI_RFL, _S_INTERP_TYPE, spd, np2d, asplit, spd_to_xyz, xyz_to_ipt, xyz_to_cct
from utils.DE_scalers import psy_scale
from utils.helpers import jab_to_rg
_MCRI_DEFAULTS = {'sampleset':"_CRI_RFL['mcri']", 
 'ref_type':None, 
 'cieobs':{'xyz':'1964_10', 
  'cct':'1931_2'}, 
 'avg':math.geomean, 
 'scale':{'fcn':psy_scale, 
  'cfactor':[21.7016, 4.2106, 2.4154]}, 
 'cspace':{'type':'ipt', 
  'Mxyz2lms':[[0.40007, 0.70727, -0.080674], [-0.228111, 1.150561, 0.06123], [0.0, 0.0, 0.931757]]}, 
 'catf':{'xyzw':[
   94.81, 100.0, 107.32], 
  'mcat':'cat02',  'cattype':'vonkries',  'F':1,  'Yb':20.0,  'Dtype':'cat02',  'catmode':'1>2'}, 
 'rg_pars':{'nhbins':None, 
  'start_hue':0.0,  'normalize_gamut':False,  'normalized_chroma_ref':100}, 
 'cri_specific_pars':{'similarity_ai': np.array([[-0.09651, 0.41354, 40.64, 16.55, -0.17],
                    [
                     0.16548, 0.38877, 58.27, 20.37, -0.59],
                    [
                     0.32825, 0.49673, 35.97, 18.05, -6.04],
                    [
                     0.02115, -0.13658, 261.62, 110.99, -44.86],
                    [
                     -0.12686, -0.22593, 99.06, 55.9, -39.86],
                    [
                     0.18488, 0.01172, 58.23, 62.55, -22.86],
                    [
                     -0.0344, 0.2348, 94.71, 32.12, 2.9],
                    [
                     0.04258, 0.0504, 205.54, 53.08, -35.2],
                    [
                     0.15829, 0.13624, 90.21, 70.83, -19.01],
                    [
                     -0.01933, -0.02168, 742.97, 297.66, -227.3]])}}

def spd_to_mcri(SPD, D=0.9, E=None, Yb=20.0, out='Rm', wl=None):
    """
    Calculates the MCRI or Memory Color Rendition Index, Rm
    
    Args: 
        :SPD: 
            | ndarray with spectral data (can be multiple SPDs, 
              first axis are the wavelengths)
        :D: 
            | 0.9, optional
            | Degree of adaptation.
        :E: 
            | None, optional
            | Illuminance in lux 
            |  (used to calculate La = (Yb/100)*(E/pi) to then calculate D 
            |  following the 'cat02' model). 
            | If None: the degree is determined by :D:
            |  If (:E: is not None) & (:Yb: is None):  :E: is assumed to contain 
               the adapting field luminance La (cd/m²).
        :Yb: 
            | 20.0, optional
            | Luminance factor of background. (used when calculating La from E)
            | If None, E contains La (cd/m²).
        :out: 
            | 'Rm' or str, optional
            | Specifies requested output (e.g. 'Rm,Rmi,cct,duv') 
        :wl: 
            | None, optional
            | Wavelengths (or [start, end, spacing]) to interpolate the SPDs to. 
            | None: default to no interpolation   
    
    Returns:
        :returns: 
            | float or ndarray with MCRI Rm for :out: 'Rm'
            | Other output is also possible by changing the :out: str value.        
          
    References:
        1. `K.A.G. Smet, W.R. Ryckaert, M.R. Pointer, G. Deconinck, P. Hanselaer,(2012)
        “A memory colour quality metric for white light sources,” 
        Energy Build., vol. 49, no. C, pp. 216–225.
        <http://www.sciencedirect.com/science/article/pii/S0378778812000837>`_
    """
    SPD = np2d(SPD)
    if wl is not None:
        SPD = spd(data=SPD, interpolation=_S_INTERP_TYPE, kind='np', wl=wl)
    else:
        avg, catf, cieobs, cri_specific_pars, cspace, ref_type, rg_pars, sampleset, scale = [_MCRI_DEFAULTS[x] for x in sorted(_MCRI_DEFAULTS.keys())]
        similarity_ai = cri_specific_pars['similarity_ai']
        Mxyz2lms = cspace['Mxyz2lms']
        scale_fcn = scale['fcn']
        scale_factor = scale['cfactor']
        sampleset = eval(sampleset)
        xyzti, xyztw = spd_to_xyz(SPD, cieobs=(cieobs['xyz']), rfl=sampleset, out=2)
        if 'cct' in out.split(','):
            cct, duv = xyz_to_cct(xyztw, cieobs=(cieobs['cct']), out='cct,duv', mode='lut')
        if catf is not None:
            Dtype_cat, F, Yb_cat, catmode_cat, cattype_cat, mcat_cat, xyzw_cat = [catf[x] for x in sorted(catf.keys())]
            if E is not None:
                if Yb is not None:
                    La = Yb / 100.0 * (E / np.pi)
                else:
                    La = E
                D = cat.get_degree_of_adaptation(Dtype=Dtype_cat, F=F, La=La)
            else:
                Dtype_cat = None
            if E is None:
                if D is None:
                    D = 1.0
            if D > 1.0:
                D = 1.0
            if D < 0.6:
                D = 0.6
            xyzti = cat.apply(xyzti, cattype=cattype_cat, catmode=catmode_cat, xyzw1=xyztw, xyzw0=None, xyzw2=xyzw_cat, D=D, mcat=[mcat_cat], Dtype=Dtype_cat)
            xyztw = cat.apply(xyztw, cattype=cattype_cat, catmode=catmode_cat, xyzw1=xyztw, xyzw0=None, xyzw2=xyzw_cat, D=D, mcat=[mcat_cat], Dtype=Dtype_cat)
        ipt = xyz_to_ipt(xyzti, cieobs=(cieobs['xyz']), M=Mxyz2lms)
        I, P, T = asplit(ipt)
        if len(xyzti.shape) == 3:
            ai = np.expand_dims(similarity_ai, axis=1)
        else:
            ai = similarity_ai
    a1, a2, a3, a4, a5 = asplit(ai)
    mahalanobis_d2 = a3 * np.power(P - a1, 2.0) + a4 * np.power(T - a2, 2.0) + 2.0 * a5 * (P - a1) * (T - a2)
    if (len(mahalanobis_d2.shape) == 3) & (mahalanobis_d2.shape[(-1)] == 1):
        mahalanobis_d2 = mahalanobis_d2[:, :, 0].T
    Si = np.exp(-0.5 * mahalanobis_d2)
    Sa = avg(Si, axis=0, keepdims=True)
    Rmi = scale_fcn((np.log(Si)), scale_factor=scale_factor)
    Rm = np2d(scale_fcn((np.log(Sa)), scale_factor=scale_factor))
    if 'Rg' in out.split(','):
        I = I[(Ellipsis, None)]
        a1 = a1[:, None] * np.ones(I.shape)
        a2 = a2[:, None] * np.ones(I.shape)
        a12 = np.concatenate((a1, a2), axis=2)
        ipt_mc = np.concatenate((I, a12), axis=2)
        nhbins, normalize_gamut, normalized_chroma_ref, start_hue = [rg_pars[x] for x in sorted(rg_pars.keys())]
        Rg = jab_to_rg(ipt, ipt_mc, ordered_and_sliced=False, nhbins=nhbins, start_hue=start_hue, normalize_gamut=normalize_gamut)
    if out != 'Rm':
        return eval(out)
    return Rm