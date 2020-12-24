# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/_helper/helper.py
# Compiled at: 2018-06-14 04:07:03
"""
Helper functions
=======================================

bugfix: mm = numpy.tile(mm, [numpy.prod(Jd).astype(int), 1])  to fix wrong type when numpy.prod(Jd) is not casted as int
bugfix: fix rcond=None -> rcond = 0 because rcond cannot be None in Python 3.6.5 and numpy 1.13.1 
            
"""
import numpy
dtype = numpy.complex64
import scipy

def create_laplacian_kernel(nufft):
    """
    Create the multi-dimensional laplacian kernel in k-space
    
    :param nufft: the NUFFT object
    :returns: uker: the multi-dimensional laplacian kernel in k-space (no fft shift used)
    :rtype: numpy ndarray
    """
    uker = numpy.zeros(nufft.st['Kd'][:], dtype=numpy.complex64, order='C')
    n_dims = numpy.size(nufft.st['Nd'])
    indx = [ slice(0, 1) for ss in range(0, n_dims) ]
    uker[indx] = -2.0 * n_dims
    for pp in range(0, n_dims):
        indx1 = indx.copy()
        indx1[pp] = 1
        uker[indx1] = 1
        indx1 = indx.copy()
        indx1[pp] = -1
        uker[indx1] = 1

    uker = numpy.fft.fftn(uker)
    return uker


def indxmap_diff(Nd):
    """
    Preindixing for rapid image gradient ()
    
    Diff(x) = x.flat[d_indx[0]] - x.flat
    
    Diff_t(x) =  x.flat[dt_indx[0]] - x.flat
                            
    :param Nd: the dimension of the image
    :type Nd: tuple with integers
    :returns d_indx: iamge gradient
    :returns  dt_indx:  the transpose of the image gradient 
    :rtype: d_indx: lists with numpy ndarray
    :rtype: dt_indx: lists with numpy ndarray
    """
    ndims = len(Nd)
    Ndprod = numpy.prod(Nd)
    mylist = numpy.arange(0, Ndprod).astype(numpy.int32)
    mylist = numpy.reshape(mylist, Nd)
    d_indx = []
    dt_indx = []
    for pp in range(0, ndims):
        d_indx = d_indx + [numpy.reshape(numpy.roll(mylist, +1, pp), (Ndprod,), order='C').astype(numpy.int32)]
        dt_indx = dt_indx + [numpy.reshape(numpy.roll(mylist, -1, pp), (Ndprod,), order='C').astype(numpy.int32)]

    return (d_indx, dt_indx)


def plan(om, Nd, Kd, Jd):
    if type(Nd) != tuple:
        raise TypeError('Nd must be tuple, e.g. (256, 256)')
    if type(Kd) != tuple:
        raise TypeError('Kd must be tuple, e.g. (512, 512)')
    if type(Jd) != tuple:
        raise TypeError('Jd must be tuple, e.g. (6, 6)')
    if (len(Nd) != len(Kd)) | (len(Nd) != len(Jd)) | len(Kd) != len(Jd):
        raise KeyError('Nd, Kd, Jd must be in the same length, e.g. Nd=(256,256),Kd=(512,512),Jd=(6,6)')
    dd = numpy.size(Nd)
    st = {}
    ud = {}
    kd = {}
    for dimid in range(0, dd):
        tmp_alpha, tmp_beta = nufft_alpha_kb_fit(Nd[dimid], Jd[dimid], Kd[dimid])
        st.setdefault('alpha', []).append(tmp_alpha)
        st.setdefault('beta', []).append(tmp_beta)

    st['tol'] = 0
    st['Jd'] = Jd
    st['Nd'] = Nd
    st['Kd'] = Kd
    M = om.shape[0]
    st['M'] = numpy.int32(M)
    st['om'] = om
    st['sn'] = numpy.array(complex(1.0, 0.0))
    dimid_cnt = 1
    for dimid in range(0, dd):
        tmp = nufft_scale(Nd[dimid], Kd[dimid], st['alpha'][dimid], st['beta'][dimid])
        dimid_cnt = Nd[dimid] * dimid_cnt
        st['sn'] = numpy.dot(st['sn'], tmp.T)
        st['sn'] = numpy.reshape(st['sn'], (dimid_cnt, 1), order='C')

    st['sn'] = st['sn'].reshape(Nd, order='C')
    st['sn'] = numpy.real(st['sn'])
    for dimid in range(0, dd):
        N = Nd[dimid]
        J = Jd[dimid]
        K = Kd[dimid]
        alpha = st['alpha'][dimid]
        beta = st['beta'][dimid]
        T = nufft_T(N, J, K, alpha, beta)
        r, arg = nufft_r(om[:, dimid], N, J, K, alpha, beta)
        c = numpy.dot(T, r)
        gam = 2.0 * numpy.pi / (K * 1.0)
        phase_scale = complex(0.0, 1.0) * gam * (N - 1.0) / 2.0
        phase = numpy.exp(phase_scale * arg)
        ud[dimid] = phase * c
        koff = nufft_offset(om[:, dimid], J, K)
        kd[dimid] = numpy.mod(outer_sum(numpy.arange(1, J + 1) * 1.0, koff), K)
        if dimid < dd - 1:
            kd[dimid] = kd[dimid] * numpy.prod(Kd[dimid + 1:dd]) - 1

    kk = kd[0]
    uu = ud[0]
    Jprod = Jd[0]
    Kprod = Kd[0]
    for dimid in range(1, dd):
        Jprod = numpy.prod(Jd[:dimid + 1])
        Kprod = numpy.prod(Kd[:dimid + 1])
        kk = block_outer_sum(kk, kd[dimid]) + 1
        kk = kk.reshape((Jprod, M), order='C')
        uu = block_outer_prod(uu, ud[dimid])
        uu = uu.reshape((Jprod, M), order='C')

    uu = uu.conj()
    mm = numpy.arange(0, M)
    mm = numpy.tile(mm, [numpy.prod(Jd).astype(int), 1])
    csrdata = numpy.reshape(uu.T, (Jprod * M,), order='C')
    rowindx = numpy.reshape(mm.T, (Jprod * M,), order='C')
    colindx = numpy.reshape(kk.T, (Jprod * M,), order='C')
    csrshape = (
     M, numpy.prod(Kd))
    st['p'] = scipy.sparse.csr_matrix((csrdata, (rowindx, colindx)), shape=csrshape)
    om = st['om']
    M = st['M']
    n_shift = tuple(0 * x for x in st['Nd'])
    final_shifts = tuple(numpy.array(n_shift) + numpy.array(st['Nd']) / 2)
    phase = numpy.exp(complex(0.0, 1.0) * numpy.sum(om * numpy.tile(final_shifts, (
     M,
     1)), 1))
    st['p'] = scipy.sparse.diags(phase, 0).dot(st['p'])
    return st


def preindex_copy(Nd, Kd):
    """
    Building the array index for copying two arrays of sizes Nd and Kd
    
    Only the front part of the input/output arrays are copied. 
    
    The oversize  parts of the input array are truncated (if Nd > Kd). 
    
    And the smaller size are zero-padded (if Nd < Kd)
    
    :param Nd: tuple, the dimensions of array1
    :param Kd: tuple, the dimensions of array2
    :type Nd: tuple with integer elements
    :type Kd: tuple with integer elements
    :returns: inlist: the index of the input array
    :returns: outlist: the index of the output array
    :returns: nelem: the length of the inlist and outlist (equal length)
    :rtype: inlist: list with integer elements
    :rtype: outlist: list with integer elements
    :rtype: nelem: int
    """
    ndim = len(Nd)
    kdim = len(Kd)
    if ndim != kdim:
        print 'mismatched dimensions!'
        print 'Nd and Kd must have the same dimensions'
        raise
    else:
        nelem = 1
        min_dim = ()
        for pp in range(ndim - 1, -1, -1):
            YY = numpy.minimum(Nd[pp], Kd[pp])
            nelem *= YY
            min_dim = (YY,) + min_dim

        mylist = numpy.arange(0, nelem).astype(numpy.int32)
        BB = ()
        for pp in range(ndim - 1, 0, -1):
            a = numpy.floor(mylist / min_dim[pp])
            b = mylist % min_dim[pp]
            mylist = a
            BB = (b,) + BB

        inlist = mylist
        outlist = mylist
        for pp in range(0, ndim - 1):
            inlist = inlist * Nd[(pp + 1)] + BB[pp]
            outlist = outlist * Kd[(pp + 1)] + BB[pp]

    return (
     inlist.astype(numpy.int32), outlist.astype(numpy.int32), nelem.astype(numpy.int32))


def dirichlet(x):
    return numpy.sinc(x)


def outer_sum(xx, yy):
    """
    Superseded by numpy.add.outer() function
    """
    return numpy.add.outer(xx, yy)


def nufft_offset(om, J, K):
    """
    For every om points(outside regular grids), find the nearest
    central grid (from Kd dimension)
    """
    gam = 2.0 * numpy.pi / (K * 1.0)
    k0 = numpy.floor(1.0 * om / gam - 1.0 * J / 2.0)
    return k0


def nufft_alpha_kb_fit(N, J, K):
    """
    Find parameters alpha and beta for scaling factor st['sn']
    The alpha is hardwired as [1,0,0...] when J = 1 (uniform scaling factor)
    
    :param int N: the size of image
    :param int J:the size of interpolator
    :param int K: the size of oversampled k-space
    
    
    
    """
    beta = 1
    Nmid = (N - 1.0) / 2.0
    if N > 40:
        L = 13
    else:
        L = numpy.ceil(N / 3).astype(numpy.int16)
    nlist = numpy.arange(0, N) * 1.0 - Nmid
    kb_a, kb_m = kaiser_bessel('string', J, 'best', 0, K / N)
    if J > 1:
        sn_kaiser = 1 / kaiser_bessel_ft(nlist / K, J, kb_a, kb_m, 1.0)
    elif J == 1:
        sn_kaiser = numpy.ones((1, N), dtype=dtype)
    gam = 2 * numpy.pi / K
    X_ant = beta * gam * nlist.reshape((N, 1), order='F')
    X_post = numpy.arange(0, L + 1)
    X_post = X_post.reshape((1, L + 1), order='F')
    X = numpy.dot(X_ant, X_post)
    X = numpy.cos(X)
    sn_kaiser = sn_kaiser.reshape((N, 1), order='F').conj()
    X = numpy.array(X, dtype=dtype)
    sn_kaiser = numpy.array(sn_kaiser, dtype=dtype)
    coef = numpy.linalg.lstsq(numpy.nan_to_num(X), numpy.nan_to_num(sn_kaiser), rcond=-1)[0]
    alphas = coef
    if J > 1:
        alphas[0] = alphas[0]
        alphas[1:] = alphas[1:] / 2.0
    elif J == 1:
        alphas[0] = 1.0
        alphas[1:] = 0.0
    alphas = numpy.real(alphas)
    return (alphas, beta)


def kaiser_bessel(x, J, alpha, kb_m, K_N):
    if K_N != 2:
        kb_m = 0
        alpha = 2.34 * J
    else:
        kb_m = 0
        jlist_bestzn = {2: 2.5, 3: 2.27, 
           4: 2.31, 
           5: 2.34, 
           6: 2.32, 
           7: 2.32, 
           8: 2.35, 
           9: 2.34, 
           10: 2.34, 
           11: 2.35, 
           12: 2.34, 
           13: 2.35, 
           14: 2.35, 
           15: 2.35, 
           16: 2.33}
        if J in jlist_bestzn:
            alpha = J * jlist_bestzn[J]
        else:
            tmp_key = jlist_bestzn.keys()
            min_ind = numpy.argmin(abs(tmp_key - J * numpy.ones(len(tmp_key))))
            p_J = tmp_key[min_ind]
            alpha = J * jlist_bestzn[p_J]
    kb_a = alpha
    return (kb_a, kb_m)


def kaiser_bessel_ft(u, J, alpha, kb_m, d):
    """
    Interpolation weight for given J/alpha/kb-m
    """
    u = u * complex(1.0, 0.0)
    import scipy.special
    z = numpy.sqrt((2 * numpy.pi * (J / 2) * u) ** 2.0 - alpha ** 2.0)
    nu = d / 2 + kb_m
    y = (2 * numpy.pi) ** (d / 2) * (J / 2) ** d * alpha ** kb_m / scipy.special.iv(kb_m, alpha) * scipy.special.jv(nu, z) / z ** nu
    y = numpy.real(y)
    return y


def nufft_scale1(N, K, alpha, beta, Nmid):
    """
    Calculate image space scaling factor
    """
    alpha = numpy.real(alpha)
    L = len(alpha) - 1
    if L > 0:
        sn = numpy.zeros((N, 1))
        n = numpy.arange(0, N).reshape((N, 1), order='F')
        i_gam_n_n0 = complex(0.0, 1.0) * (2 * numpy.pi / K) * (n - Nmid) * beta
        for l1 in range(-L, L + 1):
            alf = alpha[abs(l1)]
            if l1 < 0:
                alf = numpy.conj(alf)
            sn = sn + alf * numpy.exp(i_gam_n_n0 * l1)

    else:
        sn = numpy.dot(alpha, numpy.ones((N, 1)))
    return sn


def nufft_scale(Nd, Kd, alpha, beta):
    dd = numpy.size(Nd)
    Nmid = (Nd - 1) / 2.0
    if dd == 1:
        sn = nufft_scale1(Nd, Kd, alpha, beta, Nmid)
    else:
        sn = 1
        for dimid in numpy.arange(0, dd):
            tmp = nufft_scale1(Nd[dimid], Kd[dimid], alpha[dimid], beta[dimid], Nmid[dimid])
            sn = numpy.dot(list(sn), tmp.H)

    return sn


def mat_inv(A):
    B = scipy.linalg.pinv2(A)
    return B


def nufft_T(N, J, K, alpha, beta):
    """
     The Equation (29) and (26) in Fessler and Sutton 2003.
     Create the overlapping matrix CSSC (diagonal dominent matrix)
     of J points and find out the pseudo-inverse of CSSC """
    L = numpy.size(alpha) - 1
    cssc = numpy.zeros((J, J))
    j1, j2 = numpy.mgrid[1:J + 1, 1:J + 1]
    overlapping_mat = j2 - j1
    for l1 in range(-L, L + 1):
        for l2 in range(-L, L + 1):
            alf1 = alpha[abs(l1)]
            alf2 = alpha[abs(l2)]
            tmp = overlapping_mat + beta * (l1 - l2)
            tmp = dirichlet(1.0 * tmp / (1.0 * K / N))
            cssc = cssc + alf1 * alf2 * tmp

    return mat_inv(cssc)


def nufft_r(om, N, J, K, alpha, beta):
    """
    equation (30) of Fessler's paper

    """

    def iterate_sum(rr, alf, r1):
        rr = rr + alf * r1
        return rr

    def iterate_l1(L, alpha, arg, beta, K, N, rr):
        oversample_ratio = 1.0 * K / N
        import time
        t0 = time.time()
        for l1 in range(-L, L + 1):
            alf = alpha[abs(l1)] * 1.0
            input_array = (arg + 1.0 * l1 * beta) / oversample_ratio
            r1 = dirichlet(input_array)
            rr = iterate_sum(rr, alf, r1)

        return rr

    M = numpy.size(om)
    gam = 2.0 * numpy.pi / (K * 1.0)
    nufft_offset0 = nufft_offset(om, J, K)
    dk = 1.0 * om / gam - nufft_offset0
    arg = outer_sum(-numpy.arange(1, J + 1) * 1.0, dk)
    L = numpy.size(alpha) - 1
    rr = numpy.zeros((J, M), dtype=numpy.float32)
    rr = iterate_l1(L, alpha, arg, beta, K, N, rr)
    return (rr, arg)


def block_outer_prod(x1, x2):
    """
    Multiply x1 (J1 x M) and x2 (J2xM) and extend the dimension to 3D (J1xJ2xM)
    """
    J1, M = x1.shape
    J2, M = x2.shape
    xx1 = x1.reshape((J1, 1, M), order='F')
    xx1 = numpy.tile(xx1, (1, J2, 1))
    xx2 = x2.reshape((1, J2, M), order='F')
    xx2 = numpy.tile(xx2, (J1, 1, 1))
    y = xx1 * xx2
    return y


def block_outer_sum(x1, x2):
    """
    Update the new index after adding a new axis
    """
    J1, M = x1.shape
    J2, M = x2.shape
    xx1 = x1.reshape((J1, 1, M), order='F')
    xx1 = numpy.tile(xx1, (1, J2, 1))
    xx2 = x2.reshape((1, J2, M), order='F')
    xx2 = numpy.tile(xx2, (J1, 1, 1))
    y = xx1 + xx2
    return y


def crop_slice_ind(Nd):
    """
    (Deprecated in v.0.3.4) 
    Return the "slice" of Nd size to index multi-dimensional array.  "Slice" functions as the index of the array.
    Superseded by preindex_copy() which avoid run-time indexing.    
    """
    return [ slice(0, Nd[ss]) for ss in range(0, len(Nd)) ]


def diagnose():
    """
    Diagnosis function
    Find available device when NUFFT.offload() failed
    """
    from reikna import cluda
    import reikna.transformations
    from reikna.cluda import functions, dtypes
    try:
        api = cluda.cuda_api()
        print 'cuda interface is available'
        available_cuda_device = cluda.find_devices(api)
        print (api, available_cuda_device)
        cuda_flag = 1
        print 'try to load cuda interface:'
        for api_n in available_cuda_device.keys():
            print (
             "API='cuda',  ", 'platform_number=', api_n, ', device_number=', available_cuda_device[api_n][0])

    except:
        cuda_flag = 0
        print 'cuda interface is not available'

    try:
        api = cluda.ocl_api()
        print 'ocl interface is available'
        available_ocl_device = cluda.find_devices(api)
        print (api, available_ocl_device)
        ocl_flag = 1
        print 'try to load ocl interface with:'
        for api_n in available_ocl_device.keys():
            print (
             "API='ocl',  ", 'platform_number=', api_n, ', device_number=', available_ocl_device[api_n][0])

    except:
        print 'ocl interface is not available'
        ocl_flag = 0