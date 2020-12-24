# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\tomography\tomocam\tomoCam.py
# Compiled at: 2018-08-27 17:21:07
import tomopy, argparse, numpy as np, afnumpy as afnp, arrayfire as af
from gnufft import tvd_update, add_hessian
from XT_ForwardModel import forward_project, init_nufft_params, back_project

def gpuGridrec(tomo, angles, center, input_params):
    """
        Gridrec reconstruction using GPU based gridding
        Inputs: tomo : 3D numpy sinogram array with dimensions same as tomopy
        angles : Array of angles in radians
        center : Floating point center of rotation
        input_params : A dictionary with the keys
        'gpu_device' : Device id of the gpu (For a 4 GPU cluster ; 0-3)
        'oversamp_factor': A factor by which to pad the image/data for FFT
        'fbp_filter_param' : A number between 0-1 for setting the filter cut-off for FBP
        """
    print 'Starting GPU NUFFT recon'
    af.set_device(input_params['gpu_device'])
    new_tomo = np.transpose(tomo, (1, 2, 0))
    im_size = new_tomo.shape[1]
    num_slice = new_tomo.shape[0]
    num_angles = new_tomo.shape[2]
    pad_size = np.int16(im_size * input_params['oversamp_factor'])
    sino = {}
    geom = {}
    sino['Ns'] = pad_size
    sino['Ns_orig'] = im_size
    sino['center'] = center + (sino['Ns'] / 2 - sino['Ns_orig'] / 2)
    sino['angles'] = angles
    sino['filter'] = input_params['fbp_filter_param']
    nufft_params = init_nufft_params(sino, geom)
    rec_nufft = afnp.zeros((num_slice / 2, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    Ax = afnp.zeros((sino['Ns'], num_angles), dtype=afnp.complex64)
    pad_idx = slice(sino['Ns'] / 2 - sino['Ns_orig'] / 2, sino['Ns'] / 2 + sino['Ns_orig'] / 2)
    rec_nufft_final = np.zeros((num_slice, sino['Ns_orig'], sino['Ns_orig']), dtype=np.float32)
    slice_1 = slice(0, num_slice, 2)
    slice_2 = slice(1, num_slice, 2)
    gdata = afnp.array(new_tomo[slice_1] + complex(0.0, 1.0) * new_tomo[slice_2], dtype=afnp.complex64)
    x_recon = afnp.zeros((sino['Ns'], sino['Ns']), dtype=afnp.complex64)
    for i in range(0, num_slice / 2):
        Ax[pad_idx, :] = gdata[i]
        rec_nufft[i] = back_project(Ax, nufft_params)[(pad_idx, pad_idx)]

    rec_nufft = np.array(rec_nufft, dtype=np.complex64)
    rec_nufft_final[slice_1] = np.array(rec_nufft.real, dtype=np.float32)
    rec_nufft_final[slice_2] = np.array(rec_nufft.imag, dtype=np.float32)
    return rec_nufft_final


def gpuSIRT(tomo, angles, center, input_params):
    """
        SIRT reconstruction using GPU based gridding operators
        Inputs: tomo : 3D numpy sinogram array with dimensions same as tomopy
        angles : Array of angles in radians
        center : Floating point center of rotation
        input_params : A dictionary with the keys
        'gpu_device' : Device id of the gpu (For a 4 GPU cluster ; 0-3)
        'oversamp_factor': A factor by which to pad the image/data for FFT
        'num_iter' : Number of SIRT iterations
        """
    print 'Starting GPU SIRT recon'
    af.set_device(input_params['gpu_device'])
    new_tomo = np.transpose(tomo, (1, 2, 0))
    im_size = new_tomo.shape[1]
    num_slice = new_tomo.shape[0]
    num_angles = new_tomo.shape[2]
    pad_size = np.int16(im_size * input_params['oversamp_factor'])
    num_iter = input_params['num_iter']
    sino = {}
    geom = {}
    sino['Ns'] = pad_size
    sino['Ns_orig'] = im_size
    sino['center'] = center + (sino['Ns'] / 2 - sino['Ns_orig'] / 2)
    sino['angles'] = angles
    nufft_params = init_nufft_params(sino, geom)
    temp_y = afnp.zeros((sino['Ns'], num_angles), dtype=afnp.complex64)
    temp_x = afnp.zeros((sino['Ns'], sino['Ns']), dtype=afnp.complex64)
    x_recon = afnp.zeros((num_slice / 2, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    pad_idx = slice(sino['Ns'] / 2 - sino['Ns_orig'] / 2, sino['Ns'] / 2 + sino['Ns_orig'] / 2)
    rec_sirt_final = np.zeros((num_slice, sino['Ns_orig'], sino['Ns_orig']), dtype=np.float32)
    x_ones = afnp.ones((sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    temp_x[(pad_idx, pad_idx)] = x_ones
    temp_proj = forward_project(temp_x, nufft_params)
    R = 1 / afnp.abs(temp_proj)
    R[afnp.isnan(R)] = 0
    R[afnp.isinf(R)] = 0
    R = afnp.array(R, dtype=afnp.complex64)
    y_ones = afnp.ones((sino['Ns_orig'], num_angles), dtype=afnp.complex64)
    temp_y[pad_idx] = y_ones
    temp_backproj = back_project(temp_y, nufft_params)
    C = 1 / afnp.abs(temp_backproj)
    C[afnp.isnan(C)] = 0
    C[afnp.isinf(C)] = 0
    C = afnp.array(C, dtype=afnp.complex64)
    slice_1 = slice(0, num_slice, 2)
    slice_2 = slice(1, num_slice, 2)
    gdata = afnp.array(new_tomo[slice_1] + complex(0.0, 1.0) * new_tomo[slice_2], dtype=afnp.complex64)
    for i in range(num_slice / 2):
        for iter_num in range(num_iter):
            temp_x[(pad_idx, pad_idx)] = x_recon[i]
            Ax = forward_project(temp_x, nufft_params)
            temp_y[pad_idx] = gdata[i]
            x_recon[i] = x_recon[i] + (C * back_project(R * (temp_y - Ax), nufft_params))[(pad_idx, pad_idx)]

    rec_sirt = np.array(x_recon, dtype=np.complex64)
    rec_sirt_final[slice_1] = np.array(rec_sirt.real, dtype=np.float32)
    rec_sirt_final[slice_2] = np.array(rec_sirt.imag, dtype=np.float32)
    return rec_sirt_final


def gpuMBIR(tomo, angles, center, input_params):
    """
        MBIR reconstruction using GPU based gridding operators
        Inputs: tomo : 3D numpy sinogram array with dimensions same as tomopy
        angles : Array of angles in radians
        center : Floating point center of rotation
        input_params : A dictionary with the keys
        'gpu_device' : Device id of the gpu (For a 4 GPU cluster ; 0-3)
        'oversamp_factor': A factor by which to pad the image/data for FFT
        'num_iter' : Max number of MBIR iterations
        'smoothness' : Regularization constant
        'p': MRF shape param
        """
    print 'Starting GPU MBIR recon'
    af.set_device(input_params['gpu_device'])
    new_tomo = np.transpose(tomo, (1, 2, 0))
    im_size = new_tomo.shape[1]
    num_slice = new_tomo.shape[0]
    num_angles = new_tomo.shape[2]
    pad_size = np.int16(im_size * input_params['oversamp_factor'])
    num_iter = input_params['num_iter']
    mrf_sigma = input_params['smoothness']
    mrf_p = input_params['p']
    print 'MRF params p=%f sigma=%f' % (mrf_p, mrf_sigma)
    sino = {}
    geom = {}
    sino['Ns'] = pad_size
    sino['Ns_orig'] = im_size
    sino['center'] = center + (sino['Ns'] / 2 - sino['Ns_orig'] / 2)
    sino['angles'] = angles
    print 'Initialize NUFFT params'
    nufft_params = init_nufft_params(sino, geom)
    temp_y = afnp.zeros((sino['Ns'], num_angles), dtype=afnp.complex64)
    temp_x = afnp.zeros((sino['Ns'], sino['Ns']), dtype=afnp.complex64)
    x_recon = afnp.zeros((num_slice / 2, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    pad_idx = slice(sino['Ns'] / 2 - sino['Ns_orig'] / 2, sino['Ns'] / 2 + sino['Ns_orig'] / 2)
    rec_mbir_final = np.zeros((num_slice, sino['Ns_orig'], sino['Ns_orig']), dtype=np.float32)
    print 'Moving data to GPU'
    slice_1 = slice(0, num_slice, 2)
    slice_2 = slice(1, num_slice, 2)
    gdata = afnp.array(new_tomo[slice_1] + complex(0.0, 1.0) * new_tomo[slice_2], dtype=afnp.complex64)
    gradient = afnp.zeros((num_slice / 2, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    z_recon = afnp.zeros((num_slice / 2, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    t_nes = 1
    print 'Computing Lipschitz of gradient'
    x_ones = afnp.ones((1, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    temp_x[(pad_idx, pad_idx)] = x_ones[0]
    temp_proj = forward_project(temp_x, nufft_params)
    temp_backproj = back_project(temp_proj, nufft_params)[(pad_idx, pad_idx)]
    print 'Adding Hessian of regularizer'
    temp_backproj2 = afnp.zeros((1, sino['Ns_orig'], sino['Ns_orig']), dtype=afnp.complex64)
    temp_backproj2[0] = temp_backproj
    add_hessian(mrf_sigma, x_ones, temp_backproj2)
    L = np.max([temp_backproj2.real.max(), temp_backproj2.imag.max()])
    print 'Lipschitz constant = %f' % L
    del x_ones
    del temp_proj
    del temp_backproj
    del temp_backproj2
    for iter_num in range(num_iter):
        print 'Iteration %d of %d' % (iter_num, num_iter)
        for i in range(num_slice / 2):
            temp_x[(pad_idx, pad_idx)] = x_recon[i]
            Ax = forward_project(temp_x, nufft_params)
            temp_y[pad_idx] = gdata[i]
            gradient[i] = back_project(Ax - temp_y, nufft_params)[(pad_idx, pad_idx)]

        tvd_update(mrf_p, mrf_sigma, x_recon, gradient)
        x_recon, z_recon, t_nes = nesterovOGM2update(x_recon, z_recon, t_nes, gradient, L)

    rec_mbir = np.array(x_recon, dtype=np.complex64)
    rec_mbir_final[slice_1] = np.array(rec_mbir.real, dtype=np.float32)
    rec_mbir_final[slice_2] = np.array(rec_mbir.imag, dtype=np.float32)
    return rec_mbir_final


def nesterovOGM1update(x, z, t, grad, L):
    tNew = 0.5 * (1 + np.sqrt(1 + 4 * t ** 2))
    zNew = x - grad / L
    xNew = zNew + (t - 1) / tNew * (zNew - z)
    return (xNew, zNew, tNew)


def nesterovOGM2update(x, z, t, grad, L):
    zNew = x - grad / L
    tNew = 0.5 * (1 + np.sqrt(1 + 4 * t ** 2))
    xNew = zNew + (t - 1) / tNew * (zNew - z) + t / tNew * (zNew - x)
    return (xNew, zNew, tNew)