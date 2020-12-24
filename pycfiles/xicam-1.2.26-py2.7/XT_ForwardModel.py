# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\tomography\tomocam\XT_ForwardModel.py
# Compiled at: 2018-08-27 17:21:07
import gnufft, math, numpy as np, afnumpy as afnp, afnumpy.fft as af_fft, scipy.special as sc_spl, tomopy, matplotlib.pyplot as plt
from XT_Common import padmat

def forward_project(x, params):
    qxyXrxy = params['fft2Dshift'] * af_fft.fft2(x * params['deapod_filt'] * params['fft2Dshift'])
    qtXqxy = gnufft.polarsample(params['gxy'], qxyXrxy, params['gkblut'], params['scale'], params['k_r']) / params['Ns'] ** 2
    rtXqt = params['fftshift1D'](af_fft.ifft(afnp.array(params['fftshift1D_center'](qtXqxy).T)).T) * params['sino_mask']
    return rtXqt


def back_project(y, params):
    qtXrt = params['giDq'].reshape((params['Ns'], 1)) * params['fftshift1Dinv_center'](af_fft.fft(params['fftshift1D'](y).T).T)
    qxyXqt = gnufft.polarsample_transpose(params['gxy'], qtXrt, params['grid'], params['gkblut'], params['scale'], params['k_r']) * (afnp.pi / (2 * params['Ns']))
    rxyXqxy = params['fft2Dshift'] * af_fft.ifft2(qxyXqt * params['fft2Dshift']) * params['deapod_filt']
    return rxyXqxy


def init_nufft_params(sino, geom):
    KBLUT_LENGTH = 256
    k_r = 3
    beta = 4 * math.pi
    Ns = sino['Ns']
    Ns_orig = sino['Ns_orig']
    ang = sino['angles']
    q_grid = np.arange(1, sino['Ns'] + 1) - np.floor((sino['Ns'] + 1) / 2) - 1
    sino['tt'], sino['qq'] = np.meshgrid(ang * 180 / math.pi, q_grid)
    kblut, KB, KB1D, KB2D = KBlut(k_r, beta, KBLUT_LENGTH)
    xi, yi = pol2cart(sino['qq'], sino['tt'] * math.pi / 180)
    xi = xi + np.floor((Ns + 1) / 2)
    yi = yi + np.floor((Ns + 1) / 2)
    params = {}
    params['k_r'] = k_r
    params['deapod_filt'] = afnp.array(deapodization(Ns, KB1D), dtype=afnp.float32)
    params['sino_mask'] = afnp.array(padmat(np.ones((Ns_orig, sino['qq'].shape[1])), np.array((Ns, sino['qq'].shape[1])), 0), dtype=afnp.float32)
    params['grid'] = [Ns, Ns]
    params['scale'] = (KBLUT_LENGTH - 1) / k_r
    params['center'] = afnp.array(sino['center'])
    params['Ns'] = Ns
    params['Ntheta'] = np.size(ang)
    params['gxi'] = afnp.array(np.single(xi))
    params['gyi'] = afnp.array(np.single(yi))
    params['gxy'] = params['gxi'] + complex(0.0, 1.0) * params['gyi']
    params['gkblut'] = afnp.array(np.single(kblut))
    params['det_grid'] = np.array(np.reshape(np.arange(0, sino['Ns']), (sino['Ns'], 1)))
    temp_mask = np.ones(Ns)
    kernel = np.ones(Ns)
    if 'filter' in sino:
        temp_r = np.linspace(-1, 1, Ns)
        kernel = Ns * np.fabs(temp_r) * np.sinc(temp_r / 2)
        temp_pos = (1 - sino['filter']) / 2
        temp_mask[0:(np.int16(temp_pos * Ns))] = 0
        temp_mask[(np.int16((1 - temp_pos) * Ns)):] = 0
    params['giDq'] = afnp.array(kernel * temp_mask, dtype=afnp.complex64)
    temp = afnp.array((-1) ** params['det_grid'], dtype=afnp.float32)
    temp2 = np.array((-1) ** params['det_grid'], dtype=afnp.float32)
    temp2 = afnp.array(temp2.reshape(1, sino['Ns']))
    temp3 = afnp.array(afnp.exp(complex(0.0, -2.0) * params['center'] * (afnp.pi / params['Ns']) * params['det_grid']).astype(afnp.complex64))
    temp4 = afnp.array(afnp.exp(complex(0.0, 2.0) * params['center'] * afnp.pi / params['Ns'] * params['det_grid']).astype(afnp.complex64))
    params['fft2Dshift'] = afnp.array(temp * temp2, dtype=afnp.complex64)
    params['fftshift1D'] = lambda x: temp * x
    params['fftshift1D_center'] = lambda x: temp3 * x
    params['fftshift1Dinv_center'] = lambda x: temp4 * x
    return params


def deapodization(Ns, KB1D):
    xx = np.arange(1, Ns + 1) - Ns / 2 - 1
    dpz = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(np.reshape(KB1D(xx), (np.size(xx), 1)) * KB1D(xx))))
    dpz = dpz.real
    dpz = 1 / dpz
    return dpz


def KBlut(k_r, beta, nlut):
    kk = np.linspace(0, k_r, nlut)
    kblut = KB2(kk, 2 * k_r, beta)
    scale = (nlut - 1) / k_r
    kbcrop = lambda x: np.abs(x) <= k_r
    KBI = lambda x: np.int16(np.abs(x) * scale - np.floor(np.abs(x) * scale))
    KB1D = lambda x: (np.reshape(kblut[np.int16(np.floor(np.abs(x) * scale) * kbcrop(x))], x.shape) * KBI(x) + np.reshape(kblut[np.int16(np.ceil(np.abs(x) * scale) * kbcrop(x))], x.shape) * (1 - KBI(x))) * kbcrop(x)
    KB = lambda x, y: KB1D(x) * KB1D(y)
    KB2D = lambda x, y: KB1D(x) * KB1D(y)
    return (kblut, KB, KB1D, KB2D)


def KB2(x, k_r, beta):
    w = sc_spl.iv(0, beta * np.sqrt(1 - (2 * x / k_r) ** 2))
    w = w * (x <= k_r)
    return w


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)