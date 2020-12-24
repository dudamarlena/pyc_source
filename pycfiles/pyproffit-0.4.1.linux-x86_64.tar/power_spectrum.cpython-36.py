# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyproffit/power_spectrum.py
# Compiled at: 2019-11-19 08:35:18
# Size of source mod 2**32: 19715 bytes
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from astropy.io import fits
from astropy.cosmology import WMAP9 as cosmo
from scipy.signal import convolve
from scipy.special import gamma
import matplotlib.pyplot as plt, time
epsilon = 0.001
Yofn = np.pi
alpha = 3.6666666666666665
cf = np.power(2.0, alpha / 2.0) * gamma(3.0 - alpha / 2.0) / gamma(3.0)
a3d = 0.1

def calc_mexicanhat(sc, img, mask, simmod):
    gf = np.zeros(img.shape)
    cx = int(img.shape[0] / 2 + 0.5)
    cy = int(img.shape[1] / 2 + 0.5)
    gf[(cx, cy)] = 1.0
    gfm = gaussian_filter(gf, sc / np.sqrt(1.0 + epsilon))
    gfp = gaussian_filter(gf, sc * np.sqrt(1.0 + epsilon))
    gsigma1 = convolve(img, gfm, mode='same')
    gsigma2 = convolve(img, gfp, mode='same')
    gmask1 = convolve(mask, gfm, mode='same')
    gmask2 = convolve(mask, gfp, mode='same')
    gbeta1 = convolve(simmod, gfm, mode='same')
    gbeta2 = convolve(simmod, gfp, mode='same')
    fout1 = np.nan_to_num(np.divide(gsigma1, gmask1))
    fout2 = np.nan_to_num(np.divide(gsigma2, gmask2))
    fout = (fout1 - fout2) * mask
    bout1 = np.nan_to_num(np.divide(gbeta1, gmask1))
    bout2 = np.nan_to_num(np.divide(gbeta2, gmask2))
    bout = (bout1 - bout2) * mask
    return (fout, bout)


def do_bootstrap(vals, nsample):
    nval = len(vals[0])
    nsc = len(vals)
    vout = np.zeros([nsc, nsample])
    for ns in range(nsample):
        idb = [int(np.floor(np.random.rand() * nval)) for i in range(nval)]
        for k in range(nsc):
            vout[(k, ns)] = np.mean(vals[k][idb])

    cov = np.cov(vout)
    return cov


def calc_ps(region, img, mod, kr, nreg):
    var = np.var(img[region])
    vmod = np.var(mod[region])
    ps = (var - vmod) / epsilon ** 2 / Yofn / kr ** 2
    psnoise = vmod / epsilon ** 2 / Yofn / kr ** 2
    nptot = len(img[region])
    vals = np.empty(nreg)
    for l in range(nreg):
        step = np.double(nptot / nreg)
        imin = int(l * step)
        imax = int((l + 1) * step - 1)
        vals[l] = (np.var(img[region][imin:imax]) - np.var(mod[region][imin:imax])) / (epsilon ** 2 * Yofn * kr ** 2)

    return (
     ps, psnoise, vals)


def betamodel(x, par):
    beta = par[0]
    rc = par[1]
    norm = np.power(10.0, par[2])
    y = norm * np.power(1.0 + (x / rc) ** 2, -3.0 * beta / 2.0)
    return y


def doublebeta(x, pars):
    beta = pars[0]
    rc1 = pars[1]
    rc2 = pars[2]
    ratio = pars[3]
    norm = np.power(10.0, pars[4])
    base1 = 1 + x ** 2 / rc1 ** 2
    base2 = 1 + x ** 2 / rc2 ** 2
    xx = norm * (np.power(base1, -3 * beta) + ratio * np.power(base2, -3 * beta))
    return np.sqrt(xx)


def calc_projection_factor(nn, mask, betaparams, scale):
    tinit = time.time()
    wave_cutoff_largek = nn / 2.0
    wave_cutoff_smallk = 2.0
    tinit = time.time()
    print('Initializing 3D k-space ... ')
    kxq, kyq, kzq = np.indices((nn, nn, nn))
    lfr = np.where(kxq > nn / 2.0)
    kxq[lfr] = kxq[lfr] - nn
    mfr = np.where(kyq > nn / 2.0)
    kyq[mfr] = kyq[mfr] - nn
    nfr = np.where(kzq > nn / 2.0)
    kzq[nfr] = kzq[nfr] - nn
    k3D = np.sqrt(kxq ** 2 + kyq ** 2 + kzq ** 2)
    print('Initializing fluctuations in the k-space ... ')
    cube = nn * nn * nn
    amp = np.sqrt(np.power(k3D, -alpha))
    cut = np.where(np.logical_or(k3D <= wave_cutoff_smallk, k3D > wave_cutoff_largek))
    amp[cut] = 0.0
    gauss1 = np.random.randn(nn ** 3).reshape(nn, nn, nn)
    gauss2 = np.random.randn(nn ** 3).reshape(nn, nn, nn)
    akx = amp * (gauss1 + complex(0.0, 1.0) * gauss2)
    print('Computing inverse 3D FFT  ... ')
    bx = np.fft.ifftn(akx)
    avbx = np.sqrt(np.sum(np.real(bx) ** 2) / cube)
    fluct = np.real(bx) / avbx
    print('RMS (= 1 sigma) delta_x is: ', avbx)
    print('Minimum (real) delta_x/rms is: ', np.min(fluct))
    print('Maximum (real) delta_x/rms is: ', np.max(fluct))
    hdu = fits.PrimaryHDU(fluct)
    hdulist = fits.HDUList([hdu])
    hdulist.writeto('fluctuations.fits', overwrite=True)
    print('3D fluctuations field saved to fluctuations.fits')
    print('Now computing 2D and 3D power spectra...')

    def project(cone, ax):
        image = np.sum(cone, axis=ax)
        return image

    c = [
     nn / 2.0, nn / 2.0, nn / 2.0]
    x, y, z = np.indices((nn, nn, nn))
    rads = np.sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2 + (z - c[2]) ** 2)
    npar = len(betaparams)
    if npar == 4:
        rho_unpert = betamodel(rads, betaparams)
    else:
        rho_unpert = doublebeta(rads, betaparams)
    em = np.power(rho_unpert * (1.0 + a3d * fluct), 2.0)
    em3d = em / np.power(rho_unpert, 2.0)
    mod = project(np.power(rho_unpert, 2.0), 0)
    imgo = project(em, 0)
    img = np.nan_to_num(np.divide(imgo, mod))
    nsc = len(scale)
    imgs = []
    flucts = []
    print('Convolving images with Mexican Hat filters')
    for i in range(nsc):
        sc = scale[i]
        print('Convolving with scale ', sc)
        gf = np.zeros((nn, nn))
        center = int(nn / 2)
        gf[(center, center)] = 1.0
        gfm = gaussian_filter(gf, sc / np.sqrt(1.0 + epsilon))
        gfp = gaussian_filter(gf, sc * np.sqrt(1.0 + epsilon))
        gsigma1 = convolve(img, gfm, mode='same')
        gsigma2 = convolve(img, gfp, mode='same')
        gf = np.zeros((nn, nn, nn))
        gf[(center, center, center)] = 1.0
        gfm = gaussian_filter(gf, sc / np.sqrt(1.0 + epsilon))
        gfp = gaussian_filter(gf, sc * np.sqrt(1.0 + epsilon))
        gfluct1 = convolve(em3d, gfm, mode='same')
        gfluct2 = convolve(em3d, gfp, mode='same')
        fout = gsigma1 - gsigma2
        imgs.append(fout)
        ffluct = gfluct1 - gfluct2
        flucts.append(ffluct)

    print('Computing 2D and 3D power spectra...')
    kr = 1.0 / np.sqrt(2.0 * np.pi ** 2) * np.divide(1.0, scale)
    Yofn = np.pi
    Yofn3d = 15.0 * np.power(np.pi, 1.5) / 8.0 / np.sqrt(2.0)
    nonzero = np.where(mask > 0.0)
    ps, ps3d, amp = np.empty(nsc), np.empty(nsc), np.empty(nsc)
    for i in range(nsc):
        tkr = kr[i]
        timg = imgs[i][nonzero]
        var = np.var(timg)
        tp = var / epsilon ** 2 / Yofn / tkr ** 2
        ps[i] = tp
        amp[i] = np.sqrt(tp * 2.0 * np.pi * tkr ** 2)
        t3d = flucts[i]
        v3d = np.var(t3d) / epsilon ** 2 / Yofn3d / tkr ** 3
        ps3d[i] = v3d

    pout = np.transpose([kr, ps, amp, ps3d])[::-1]
    np.savetxt('conv2d3d.txt', pout)
    print('Results written in file conv2d3d.txt')
    tend = time.time()
    print(' Total computing time is: ', (tend - tinit) / 60.0, ' minutes')
    return pout


class PowerSpectrum:

    def __init__(self, data, profile):
        self.data = data
        self.profile = profile

    def MexicanHat(self, modimg_file, z, region_size=1.0, factshift=1.5):
        imgo = self.data.img
        expo = self.data.exposure
        bkg = self.data.bkg
        pixsize = self.data.pixsize
        fmod = fits.open(modimg_file)
        modimg = fmod[0].data.astype(float)
        nonz = np.where(expo > 0.0)
        masko = np.copy(expo)
        masko[nonz] = 1.0
        imgt = np.copy(imgo)
        noexp = np.where(expo == 0.0)
        imgt[noexp] = 0.0
        x_c = self.profile.cx
        y_c = self.profile.cy
        kpcp = cosmo.kpc_proper_per_arcmin(z).value
        Mpcpix = 1000.0 / kpcp / pixsize
        regsizepix = region_size * Mpcpix
        self.regsize = regsizepix
        minx = int(np.round(x_c - factshift * regsizepix))
        maxx = int(np.round(x_c + factshift * regsizepix + 1))
        miny = int(np.round(y_c - factshift * regsizepix))
        maxy = int(np.round(y_c + factshift * regsizepix + 1))
        if minx < 0:
            minx = 0
        if miny < 0:
            miny = 0
        if maxx > self.data.axes[1]:
            maxx = self.data.axes[1]
        if maxy > self.data.axes[0]:
            maxy = self.data.axes[0]
        img = np.nan_to_num(np.divide(imgt[miny:maxy, minx:maxx], modimg[miny:maxy, minx:maxx]))
        mask = masko[miny:maxy, minx:maxx]
        self.size = img.shape
        self.mask = mask
        fmod[0].data = mask
        fmod.writeto('mask.fits', overwrite=True)
        randmod = np.random.poisson(modimg[miny:maxy, minx:maxx])
        simmod = np.nan_to_num(np.divide(randmod, modimg[miny:maxy, minx:maxx]))
        minscale = 2
        maxscale = regsizepix / 2.0
        scale = np.logspace(np.log10(minscale), np.log10(maxscale), 10)
        sckpc = scale * pixsize * kpcp
        for i in range(len(scale)):
            sc = scale[i]
            print('Convolving with scale', sc)
            convimg, convmod = calc_mexicanhat(sc, img, mask, simmod)
            fmod[0].data = convimg
            fmod.writeto(('conv_scale_%d_kpc.fits' % int(np.round(sckpc[i]))), overwrite=True)
            fmod[0].data = convmod
            fmod.writeto(('conv_model_%d_kpc.fits' % int(np.round(sckpc[i]))), overwrite=True)

        fmod.close()

    def PS(self, z, region_size=1.0, radius_in=0.0, radius_out=1.0):
        kpcp = cosmo.kpc_proper_per_arcmin(z).value
        Mpcpix = 1000.0 / kpcp / self.data.pixsize
        regsizepix = region_size * Mpcpix
        minscale = 2
        maxscale = regsizepix / 2.0
        scale = np.logspace(np.log10(minscale), np.log10(maxscale), 10)
        sckpc = scale * self.data.pixsize * kpcp
        kr = 1.0 / np.sqrt(2.0 * np.pi ** 2) * np.divide(1.0, scale)
        fmask = fits.open('mask.fits')
        mask = fmask[0].data
        data_size = mask.shape
        fmask.close()
        y, x = np.indices(data_size)
        rads = np.hypot(y - data_size[0] / 2.0, x - data_size[1] / 2.0)
        region = np.where(np.logical_and(np.logical_and(rads > radius_in * Mpcpix, rads <= radius_out * Mpcpix), mask > 0.0))
        nsc = len(scale)
        ps, psnoise, amp, eamp = (np.empty(nsc), np.empty(nsc), np.empty(nsc), np.empty(nsc))
        vals = []
        nreg = 20
        for i in range(nsc):
            fco = fits.open('conv_scale_%d_kpc.fits' % int(np.round(sckpc[i])))
            convimg = fco[0].data.astype(float)
            fco.close()
            fmod = fits.open('conv_model_%d_kpc.fits' % int(np.round(sckpc[i])))
            convmod = fmod[0].data.astype(float)
            fmod.close()
            print('Computing the power at scale', sckpc[i], 'kpc')
            ps[i], psnoise[i], vps = calc_ps(region, convimg, convmod, kr[i], nreg)
            vals.append(vps)

        print('Computing the covariance matrix...')
        nboot = int(10000.0)
        cov = do_bootstrap(vals, nboot)
        la, v = np.linalg.eig(cov)
        print('Eigenvalues: ', la)
        eps = np.empty(nsc)
        for i in range(nsc):
            eps[i] = np.sqrt(cov[(i, i)])

        amp = np.sqrt(np.abs(ps) * 2.0 * np.pi * kr ** 2 / cf)
        eamp = 0.5 * np.power(np.abs(ps) * 2.0 * np.pi * kr ** 2 / cf, -0.5) * 2.0 * np.pi * kr ** 2 / cf * eps
        self.kpix = kr
        self.k = 1.0 / np.sqrt(2.0 * np.pi ** 2) * np.divide(1.0, sckpc)
        self.ps = ps
        self.eps = eps
        self.psnoise = psnoise
        self.amp = amp
        self.eamp = eamp
        self.cov = cov

    def Plot(self, save_plots=True, outps='power_spectrum.pdf', outamp='a2d.pdf', plot_3d=False, cfact=None):
        if self.ps is None:
            print('Error: No power spectrum exists in structure')
            return
        else:
            plt.clf()
            fig = plt.figure(figsize=(13, 10))
            ax_size = [0.1, 0.1,
             0.87, 0.87]
            ax = fig.add_axes(ax_size)
            ax.minorticks_on()
            ax.tick_params(length=20, width=1, which='major', direction='in', right=True, top=True)
            ax.tick_params(length=10, width=1, which='minor', direction='in', right=True, top=True)
            for item in ax.get_xticklabels() + ax.get_yticklabels():
                item.set_fontsize(18)

            plt.xlabel('k [kpc$^{-1}$]', fontsize=40)
            plt.ylabel('2D Power', fontsize=40)
            plt.xscale('log')
            plt.yscale('log')
            plt.plot((self.k), (self.ps), color='red', linewidth=2, label='P$_{2D}$')
            plt.plot((self.k), (self.psnoise), color='blue', label='Poisson noise')
            plt.fill_between((self.k), (self.ps - self.eps), (self.ps + self.eps), color='red', alpha=0.4)
            if plot_3d:
                kcf = cfact[:, 0]
                cf = cfact[:, 3] / cfact[:, 1]
                interp_cf = np.interp(self.kpix, kcf, cf)
                ps3d = self.ps * interp_cf
                eps3d = self.eps * interp_cf
                plt.plot((self.k), ps3d, color='green', linewidth=2, label='P$_{3D}$')
                plt.fill_between((self.k), (ps3d - eps3d), (ps3d + eps3d), color='green', alpha=0.4)
            plt.legend(fontsize=22)
            if save_plots:
                plt.savefig(outps)
            else:
                plt.show()
            plt.clf()
            fig = plt.figure(figsize=(13, 10))
            ax_size = [0.1, 0.1,
             0.87, 0.87]
            ax = fig.add_axes(ax_size)
            ax.minorticks_on()
            ax.tick_params(length=20, width=1, which='major', direction='in', right=True, top=True)
            ax.tick_params(length=10, width=1, which='minor', direction='in', right=True, top=True)
            for item in ax.get_xticklabels() + ax.get_yticklabels():
                item.set_fontsize(18)

            plt.xlabel('k [kpc$^{-1}$]', fontsize=40)
            plt.ylabel('$A_{2D}$', fontsize=40)
            plt.xscale('log')
            plt.yscale('log')
            plt.plot((self.k), (self.amp), color='red', linewidth=2, label='A$_{2D}$')
            plt.fill_between((self.k), (self.amp - self.eamp), (self.amp + self.eamp), color='red', alpha=0.4)
            if plot_3d:
                a3d = np.sqrt(ps3d * 4.0 * np.pi * self.kpix ** 3) / 2.0
                ea3d = 0.5 * np.power(ps3d * 4.0 * np.pi * self.kpix ** 3, -0.5) * 4.0 * np.pi * self.kpix ** 3 * eps3d / 2.0
                plt.plot((self.k), a3d, color='green', linewidth=2, label='A$_{3D}$')
                plt.fill_between((self.k), (a3d - ea3d), (a3d + ea3d), color='green', alpha=0.4)
            plt.legend(fontsize=22)
            if save_plots:
                plt.savefig(outamp)
            else:
                plt.show()

    def Save(self, outfile, outcov='covariance.txt'):
        if self.ps is None:
            print('Error: Nothing to save')
            return
        np.savetxt(outfile, (np.transpose([self.k, self.ps, self.eps, self.psnoise, self.amp, self.eamp])[::-1]), header='k/kpc-1  PS2D  dPS2D  Noise  A2D  dA2D')
        np.savetxt(outcov, self.cov)

    def ProjectionFactor(self, z, betaparams, region_size=1.0):
        pixsize = self.data.pixsize
        npar = len(betaparams)
        if npar == 4:
            print('We will use a single beta profile')
            betaparams[1] = betaparams[1] / pixsize
            betaparams[2] = 0.0
        else:
            if npar == 6:
                print('We will use a double beta profile')
                betaparams[1] = betaparams[1] / pixsize
                betaparams[2] = betaparams[2] / pixsize
                betaparams[4] = 0.0
            else:
                print('Invalid number of SB parameters')
                return
        fmask = fits.open('mask.fits')
        mask = fmask[0].data
        data_size = mask.shape
        fmask.close()
        kpcp = cosmo.kpc_proper_per_arcmin(z).value
        Mpcpix = 1000.0 / kpcp / self.data.pixsize
        regsizepix = region_size * Mpcpix
        if regsizepix > data_size[0] / 2:
            print('Error: region size larger than image size')
            return
        else:
            minx = int(np.round(data_size[1] / 2 - regsizepix))
            maxx = int(np.round(data_size[1] / 2 + regsizepix))
            miny = int(np.round(data_size[0] / 2 - regsizepix))
            maxy = int(np.round(data_size[0] / 2 + regsizepix))
            msk = mask[miny:maxy, minx:maxx]
            npix = len(msk)
            minscale = 2
            maxscale = regsizepix / 2.0
            scale = np.logspace(np.log10(minscale), np.log10(maxscale), 10)
            self.cfact = calc_projection_factor(npix, msk, betaparams, scale)
            return self.cfact