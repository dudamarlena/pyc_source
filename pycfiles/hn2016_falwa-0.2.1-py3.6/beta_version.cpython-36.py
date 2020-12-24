# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/hn2016_falwa/beta_version.py
# Compiled at: 2017-12-21 21:42:42
# Size of source mod 2**32: 20464 bytes


def input_jk_output_index(j, k, kmax):
    return j * kmax + k


def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0] + (x - xs[0]) * (ys[1] - ys[0]) / (xs[1] - xs[0])
        else:
            if x > xs[(-1)]:
                return ys[(-1)] + (x - xs[(-1)]) * (ys[(-1)] - ys[(-2)]) / (xs[(-1)] - xs[(-2)])
            return interpolator(x)

    def ufunclike(xs):
        from scipy import array
        return array(map(pointwise, array(xs)))

    return ufunclike


def solve_uref_both_bc(tstamp, zmum, FAWA_cos, ylat, ephalf2, Delta_PT, zm_PT, Input_B0, Input_B1, use_real_Data=True, plot_all_ref_quan=False):
    r"""
    Compute equivalent latitude and wave activity on a barotropic sphere.

    Parameters
    ----------
    tstamp : string
        Time stamp of the snapshot of the field.
    znum : ndarray
        Zonal mean wind.
    FAWA_cos : ndarray
        Zonal mean finite-amplitude wave activity.
    ylat : sequence or array_like
        1-d numpy array of latitude (in degree) with equal spacing in ascending order; dimension = nlat.
    ephalf2 : ndarray
        Epsilon in Nakamura and Solomon (2010).
    Delta_PT : ndarray
        \Delta \Theta in Nakamura and Solomon (2010); upper-boundary conditions.
    zm_PT : ndarray
        Zonal mean potential temperature.
    Input_B0 : sequence or array_like
        Zonal-mean surface wave activity for the lowest layer (k=0). Part of the lower-boundary condition.
    Input_B1 : sequence or array_like
        Zonal-mean surface wave activity for the second lowest layer (k=1). Part of the lower-boundary condition.
    use_real_Data : boolean
        Whether to use input data to compute the reference states. By detault True. If false, randomly generated arrays will be used.
    plot_all_ref_quan : boolean
        Whether to plot the solved reference states using matplotlib library. By default False. For debugging.

    Returns
    -------
    u_MassCorr_regular_noslip : ndarray
        2-d numpy array of mass correction \Delta u in NS10 with no-slip lower boundary conditions; dimension = (kmax,nlat).
    u_Ref_regular_noslip : ndarray
        2-d numpy array of zonal wind reference state u_ref in NS10 with no-slip lower boundary conditions; dimension = (kmax,nlat).
    T_MassCorr_regular_noslip : ndarray
        2-d numpy array of adjustment in reference temperature \Delta T in NS10 with no-slip lower boundary conditions; dimension = (kmax,nlat).
    T_Ref_regular_noslip : ndarray
        2-d numpy array of adjustment in reference temperature T_ref in NS10 with no-slip lower boundary conditions; dimension = (kmax,nlat).
    u_MassCorr_regular_adiab : ndarray
        2-d numpy array of mass correction \Delta u in NS10 with adiabatic lower boundary conditions; dimension = (kmax,nlat).
    u_Ref_regular_adiab : ndarray
        2-d numpy array of zonal wind reference state u_ref in NS10 with adiabatic lower boundary conditions; dimension = (kmax,nlat).
    T_MassCorr_regular_adiab : ndarray
        2-d numpy array of adjustment in reference temperature \Delta T in NS10 with adiabatic lower boundary conditions; dimension = (kmax,nlat).
    T_Ref_regular_adiab : ndarray
        2-d numpy array of adjustment in reference temperature T_ref in NS10 with adiabatic lower boundary conditions; dimension = (kmax,nlat).

    """
    from math import pi, exp
    from scipy import interpolate
    from scipy.sparse import csc_matrix
    from scipy.sparse.linalg import spsolve
    from copy import copy
    import numpy as np, itertools
    if plot_all_ref_quan:
        import matplotlib.pyplot as plt
    else:
        dz = 1000.0
        aa = 6378000.0
        r0 = 287.0
        hh = 7000.0
        cp = 1004.0
        rkappa = r0 / cp
        om = 7.29e-05
        nlat = FAWA_cos.shape[(-1)]
        jmax1 = nlat // 4
        dm = 1.0 / float(jmax1 + 1)
        gl = np.array([(j + 1) * dm for j in range(jmax1)])
        gl_2 = np.array([j * dm for j in range(jmax1 + 2)])
        cosl = np.sqrt(1.0 - gl ** 2)
        alat = np.arcsin(gl) * 180.0 / pi
        alat_2 = np.arcsin(gl_2) * 180.0 / pi
        dmdz = dm / dz
        kmax = FAWA_cos.shape[0]
        c_a = np.zeros((jmax1, kmax))
        c_b = np.zeros((jmax1, kmax))
        c_c = np.zeros((jmax1, kmax))
        c_d = np.zeros((jmax1, kmax))
        c_e = np.zeros((jmax1, kmax))
        c_f = np.zeros((jmax1, kmax))
        zmu1 = np.zeros((jmax1, kmax))
        cx1 = np.zeros((jmax1, kmax))
        cor1 = np.zeros((jmax1, kmax))
        ephalf = np.zeros((jmax1, kmax))
        Delta_PT1 = np.zeros(jmax1 + 2)
        zm_PT1 = np.zeros((jmax1, kmax))
        Input_B0_1 = np.zeros(jmax1 + 2)
        Input_B1_1 = np.zeros(jmax1 + 2)
        if use_real_Data:
            for vv1, vvm in zip([zmu1, cx1, zm_PT1], [zmum, FAWA_cos, zm_PT]):
                f_toGaussian = interpolate.interp1d((ylat[:]), (vvm[:, :].T), axis=0, kind='linear')
                vv1[:, :] = f_toGaussian(alat[:])

            f_ep_toGaussian = interpolate.interp1d((ylat[:]), (ephalf2[:, :].T), axis=0, kind='linear')
            ephalf[:, :] = f_ep_toGaussian(alat[:])
            f_DT_toGaussian = interpolate.interp1d((ylat[:]), (Delta_PT[:]), kind='linear',
              fill_value='extrapolate')
            Delta_PT1[:] = f_DT_toGaussian(alat_2[:])
            f_B0_toGaussian = interpolate.interp1d((ylat[:]), (Input_B0[:]), kind='linear',
              fill_value='extrapolate')
            Input_B0_1[:] = f_B0_toGaussian(alat_2[:])
            f_B1_toGaussian = interpolate.interp1d((ylat[:]), (Input_B1[:]), kind='linear',
              fill_value='extrapolate')
            Input_B1_1[:] = f_B1_toGaussian(alat_2[:])
        else:
            zmu1 = np.random.rand(jmax1, kmax) + np.ones((jmax1, kmax)) * 1e-08
        cx1 = np.random.rand(jmax1, kmax) + np.ones((jmax1, kmax)) * 1e-08
    cor1 = 2.0 * om * gl[:, np.newaxis] * np.ones((jmax1, kmax))
    qxx0 = -cx1 / cor1
    c_f[0, :] = qxx0[1, :] - 2 * qxx0[0, :]
    c_f[-1, :] = qxx0[-2, :] - 2 * qxx0[-1, :]
    c_f[1:-1, :] = qxx0[:-2, :] + qxx0[2:, :] - 2 * qxx0[1:-1, :]
    Input_dB0 = np.zeros(jmax1)
    Input_dB1 = np.zeros(jmax1)
    uz1 = np.zeros(jmax1)
    Input_dB0[:] = Input_B0_1[:-2] + Input_B0_1[2:] - 2 * Input_B0_1[1:-1]
    Input_dB1[:] = Input_B1_1[:-2] + Input_B1_1[2:] - 2 * Input_B1_1[1:-1]
    uz1[:] = -r0 * cosl[:] ** 2 * Input_dB1[:] * 2 * dz / (cor1[:, 1] ** 2 * aa ** 2 * hh * dm ** 2) * exp(-rkappa * 1.0 / 7.0) - r0 * cosl[:] ** 2 * Input_dB0[:] * 2 * dz / (cor1[:, 0] ** 2 * aa ** 2 * hh * dm ** 2) * exp(-rkappa * 0.0 / 7.0)
    uz2 = np.zeros(jmax1)
    dDelta_PT1 = Delta_PT1[2:] - Delta_PT1[:-2]
    uz2[:] = -r0 * cosl[:] ** 2 * exp(-rkappa * (kmax - 2.0) / 7.0) * dDelta_PT1 / (cor1[:, -2] ** 2 * aa * hh * dmdz)
    c_a[:, :] = 1.0
    c_b[:, :] = 1.0
    c_c[:, 1:-1] = dmdz ** 2 * ephalf[:, 1:-1] * exp(-dz / (2 * hh))
    c_d[:, 1:-1] = dmdz ** 2 * ephalf[:, 0:-2] * exp(dz / (2 * hh))
    c_e[:, 1:-1] = -(c_a[:, 1:-1] + c_b[:, 1:-1] + c_c[:, 1:-1] + c_d[:, 1:-1])
    b = np.zeros(jmax1 * kmax)
    row_index = []
    col_index = []
    coeff = []
    jrange = range(jmax1)
    krange = range(1, kmax - 1)
    for j, k in itertools.product(jrange, krange):
        ind = input_jk_output_index(j, k, kmax)
        b[ind] = c_f[(j, k)]
        if j < jmax1 - 1:
            row_index.append(ind)
            col_index.append(input_jk_output_index(j + 1, k, kmax))
            coeff.append(c_a[(j, k)])
        if j > 0:
            row_index.append(ind)
            col_index.append(input_jk_output_index(j - 1, k, kmax))
            coeff.append(c_b[(j, k)])
        row_index.append(ind)
        col_index.append(input_jk_output_index(j, k + 1, kmax))
        coeff.append(c_c[(j, k)])
        row_index.append(ind)
        col_index.append(input_jk_output_index(j, k - 1, kmax))
        coeff.append(c_d[(j, k)])
        row_index.append(ind)
        col_index.append(input_jk_output_index(j, k, kmax))
        coeff.append(c_e[(j, k)])

    for j in range(jmax1):
        ind1 = input_jk_output_index(j, kmax - 1, kmax)
        b[ind1] = uz2[j]
        row_index.append(ind1)
        col_index.append(ind1)
        coeff.append(1.0)
        row_index.append(ind1)
        col_index.append(input_jk_output_index(j, kmax - 3, kmax))
        coeff.append(-1.0)

    row_index_adiab = copy(row_index)
    col_index_adiab = copy(col_index)
    coeff_adiab = copy(coeff)
    b_adiab = np.copy(b)
    for j in range(jmax1):
        ind0 = input_jk_output_index(j, 0, kmax)
        b_adiab[ind0] = uz1[j]
        row_index_adiab.append(ind0)
        col_index_adiab.append(ind0)
        coeff_adiab.append(-1.0)
        row_index_adiab.append(ind0)
        col_index_adiab.append(input_jk_output_index(j, 2, kmax))
        coeff_adiab.append(1.0)

    A_adiab = csc_matrix((coeff_adiab, (row_index_adiab, col_index_adiab)), shape=(jmax1 * kmax, jmax1 * kmax))
    for j in range(jmax1):
        ind = input_jk_output_index(j, 0, kmax)
        b[ind] = zmu1[(j, 0)] * cosl[j] / cor1[(j, 0)]
        row_index.append(ind)
        col_index.append(ind)
        coeff.append(1.0)

    A = csc_matrix((coeff, (row_index, col_index)), shape=(jmax1 * kmax, jmax1 * kmax))
    u2_adiab = spsolve(A_adiab, b_adiab)
    u2 = spsolve(A, b)
    u_adiab = np.zeros((jmax1 + 2, kmax))
    u = np.zeros((jmax1 + 2, kmax))
    for j in range(jmax1):
        for k in range(kmax):
            u_adiab[(j + 1, k)] = u2_adiab[(j * kmax + k)]
            u[(j + 1, k)] = u2[(j * kmax + k)]

    u_MassCorr_adiab = np.zeros_like(u_adiab)
    u_MassCorr_noslip = np.zeros_like(u)
    u_MassCorr_adiab[1:-1, :] = u_adiab[1:-1, :] * cor1 / cosl[:, np.newaxis]
    u_MassCorr_noslip[1:-1, :] = u[1:-1, :] * cor1 / cosl[:, np.newaxis]
    u_Ref_regular_adiab = np.zeros_like(zmum)
    u_Ref_regular_noslip = np.zeros_like(zmum)
    u_MassCorr_regular_adiab = np.zeros_like(zmum)
    u_MassCorr_regular_noslip = np.zeros_like(zmum)
    T_Ref_regular_adiab = np.zeros_like(zmum)
    T_Ref_regular_noslip = np.zeros_like(zmum)
    T_MassCorr_regular_adiab = np.zeros_like(zmum)
    T_MassCorr_regular_noslip = np.zeros_like(zmum)
    for u_MassCorr, u_MassCorr_regular, u_Ref_regular, T_MassCorr_regular, T_Ref_regular, BCstring in zip([u_MassCorr_adiab, u_MassCorr_noslip], [
     u_MassCorr_regular_adiab, u_MassCorr_regular_noslip], [
     u_Ref_regular_adiab, u_Ref_regular_noslip], [
     T_MassCorr_regular_adiab, T_MassCorr_regular_noslip], [
     T_Ref_regular_adiab, T_Ref_regular_noslip], [
     'Adiabatic', 'Noslip']):
        T_MassCorr = np.zeros_like(u_MassCorr)
        for k in range(1, kmax - 2):
            for j in range(2, jmax1, 2):
                T_MassCorr[(j, k)] = T_MassCorr[(j - 2, k)] - 2.0 * om * gl[(j - 1)] * aa * hh * dmdz / (r0 * cosl[(j - 1)]) * (u_MassCorr[(j - 1, k + 1)] - u_MassCorr[(j - 1, k - 1)])

            f_Todd = interpolate.interp1d((gl_2[::2]), (T_MassCorr[::2, k]), kind='linear',
              fill_value='extrapolate')
            T_MassCorr[:, k] = f_Todd(gl_2[:])
            T_MC_mean = np.mean(T_MassCorr[:, k])
            T_MassCorr[:, k] -= T_MC_mean

        f_u_MassCorr = interpolate.interp1d(alat_2, u_MassCorr, axis=0, kind='linear')
        u_MassCorr_regular[:, -nlat // 2:] = f_u_MassCorr(ylat[-nlat // 2:]).T
        f_T_MassCorr = interpolate.interp1d(alat_2, T_MassCorr, axis=0, kind='linear')
        T_MassCorr_regular[:, -nlat // 2:] = f_T_MassCorr(ylat[-nlat // 2:]).T
        u_Ref = zmum[:, -nlat // 2:] - u_MassCorr_regular[:, -nlat // 2:]
        T_ref = zm_PT[:, -nlat // 2:] * np.exp(-np.arange(kmax) / 7.0 * rkappa)[:, np.newaxis] - T_MassCorr_regular[:, -nlat // 2:]
        u_Ref_regular[:, -nlat // 2:] = u_Ref
        T_Ref_regular[:, -nlat // 2:] = T_ref
        if plot_all_ref_quan:
            height = np.array([i for i in range(kmax)])
            contour_int = np.arange(-120, 145, 5)
            dT_contour_int = np.arange(-120, 81, 5)
            T_contour_int = np.arange(160, 321, 5)
            fig = plt.subplots(figsize=(12, 12))
            plt.subplot(221)
            plt.contourf(ylat[-nlat // 2:], height[:-2], u_MassCorr_regular[:-2, -nlat // 2:], contour_int)
            plt.colorbar()
            c1 = plt.contour((ylat[-nlat // 2:]), (height[:-2]), (u_MassCorr_regular[:-2, -nlat // 2:]), (contour_int[::2]), colors='k')
            plt.clabel(c1, (c1.levels), inline=True, fmt='%d', fontsize=10)
            plt.title('$\\Delta$ u ' + tstamp)
            plt.ylabel('height (km)')
            plt.subplot(222)
            plt.contourf(ylat[-nlat // 2:], height[:-2], u_Ref[:-2, :], contour_int)
            plt.colorbar()
            c2 = plt.contour((ylat[-nlat // 2:]), (height[:-2]), (u_Ref[:-2, :]), (contour_int[::2]), colors='k')
            plt.clabel(c2, (c2.levels), inline=True, fmt='%d', fontsize=10)
            plt.title('$u_{REF}$ (' + BCstring + ' BC)')
            plt.subplot(223)
            plt.contourf(ylat[-nlat // 2:], height[:-2], T_MassCorr_regular[:-2, -nlat // 2:], dT_contour_int)
            plt.colorbar()
            c3 = plt.contour((ylat[-nlat // 2:]), (height[:-2]), (T_MassCorr_regular[:-2, -nlat // 2:]), dT_contour_int, colors='k')
            plt.clabel(c3, (c3.levels), inline=True, fmt='%d', fontsize=10)
            plt.title('$\\Delta$ T')
            plt.ylabel('height (km)')
            plt.subplot(224)
            plt.contourf(ylat[-nlat // 2:], height[:-2], T_ref[:-2, :], T_contour_int)
            plt.colorbar()
            c4 = plt.contour((ylat[-nlat // 2:]), (height[:-2]), (T_ref[:-2, :]), (T_contour_int[::2]), colors='k')
            plt.clabel(c4, (c4.levels), inline=True, fmt='%d', fontsize=10)
            plt.title('$T_{REF}$')
            plt.ylabel('height (km)')
            plt.tight_layout()
            plt.show()
            plt.close()

    return (u_MassCorr_regular_noslip, u_Ref_regular_noslip, T_MassCorr_regular_noslip, T_Ref_regular_noslip, u_MassCorr_regular_adiab, u_Ref_regular_adiab, T_MassCorr_regular_adiab, T_Ref_regular_adiab)


if __name__ == '__main__':
    import matplotlib.pyplot as plt, numpy as np
    nlat = 121
    kmax = 49
    jmax1 = nlat
    tstamp = 'random'
    ylat = np.linspace((-90), 90, 121, endpoint=True)
    t1 = np.random.rand(nlat, kmax) + np.ones((nlat, kmax)) * 0.001
    t2 = np.random.rand(nlat, kmax) + np.ones((nlat, kmax)) * 0.001
    t3 = np.random.rand(nlat, kmax) + np.ones((nlat, kmax)) * 0.001
    Delta_PT = np.random.rand(nlat) + np.ones(nlat) * 0.001
    zm_PT = np.random.rand(nlat, kmax) + np.ones((nlat, kmax)) * 0.001
    Input_B0 = np.random.rand(nlat) + np.ones(nlat) * 0.001
    Input_B1 = np.random.rand(nlat) + np.ones(nlat) * 0.001
    eh = np.random.rand(jmax1, kmax) + np.ones((jmax1, kmax)) * 0.001
    Delta_PT = np.sort(np.random.rand(jmax1))
    xxx = solve_uref_both_bc(tstamp, t1, t2, ylat, t3, Delta_PT, zm_PT, Input_B0, Input_B1, use_real_Data=True)
    print(xxx)