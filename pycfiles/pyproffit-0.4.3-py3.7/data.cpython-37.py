# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyproffit/data.py
# Compiled at: 2020-04-23 04:51:54
# Size of source mod 2**32: 9181 bytes
import numpy as np
from astropy.io import fits
from astropy import wcs
from scipy.ndimage.filters import gaussian_filter
from scipy.interpolate import griddata

def get_extnum(fitsfile):
    next = 0
    if fitsfile[0].header['NAXIS'] == 2:
        return 0
    print('Primary HDU is not an image, moving on')
    nhdu = len(fitsfile)
    if nhdu == 1:
        print('Error: No IMAGE extension found in input file')
        return -1
    cont = 1
    next = 1
    while cont:
        if next < nhdu:
            extension = fitsfile[next].header['XTENSION']
            if extension == 'IMAGE':
                print('IMAGE HDU found in extension ', next)
                cont = 0
        else:
            next = next + 1

    if cont == 1:
        print('Error: No IMAGE extension found in input file')
        return -1
    return next


class Data:

    def __init__(self, imglink, explink=None, bkglink=None, voronoi=False, rmsmap=None):
        if imglink is None:
            print('Error: Image file not provided')
            return
        fimg = fits.open(imglink)
        next = get_extnum(fimg)
        self.img = fimg[next].data.astype(float)
        head = fimg[next].header
        self.header = head
        self.wcs_inp = wcs.WCS(head, relax=False)
        if 'CDELT2' in head:
            self.pixsize = head['CDELT2'] * 60.0
        else:
            if 'CD2_2' in head:
                self.pixsize = head['CD2_2'] * 60.0
            else:
                print('No pixel size could be found in header, will assume a pixel size of 2.5 arcsec')
                self.pixsize = 0.041666666666666664
        self.axes = self.img.shape
        if voronoi:
            self.errmap = fimg[1].data.astype(float)
        fimg.close()
        if explink is None:
            self.exposure = np.ones(self.axes)
        else:
            fexp = fits.open(explink)
            next = get_extnum(fexp)
            expo = fexp[next].data.astype(float)
            if expo.shape != self.axes:
                print('Error: Image and exposure map sizes do not match')
                return
            self.exposure = expo
            fexp.close()
        if bkglink is None:
            self.bkg = np.zeros(self.axes)
        else:
            fbkg = fits.open(bkglink)
            next = get_extnum(fbkg)
            bkg = fbkg[next].data.astype(float)
            if bkg.shape != self.axes:
                print('Error: Image and background map sizes do not match')
                return
                self.bkg = bkg
                fbkg.close()
            elif rmsmap is not None:
                frms = fits.open(rmsmap)
                next = get_extnum(frms)
                rms = frms[next].data.astype(float)
                if rms.shape != self.axes:
                    print('Error: Image and RMS map sizes do not match')
                    return
                self.rmsmap = rms
                frms.close()
            else:
                self.rmsmap = None
            self.filth = None

    def region(self, regfile):
        freg = open(regfile)
        lreg = freg.readlines()
        freg.close()
        nsrc = 0
        nreg = len(lreg)
        if self.exposure is None:
            print('No exposure given')
            return
        expo = np.copy(self.exposure)
        y, x = np.indices(self.axes)
        regtype = None
        for i in range(nreg):
            if 'fk5' in lreg[i]:
                regtype = 'fk5'

        if regtype is None:
            print('Error: invalid format')
            return
        for i in range(nreg):
            if 'circle' in lreg[i]:
                vals = lreg[i].split('(')[1].split(')')[0]
                if regtype == 'fk5':
                    xsrc = float(vals.split(',')[0])
                    ysrc = float(vals.split(',')[1])
                    rad = vals.split(',')[2]
                    if '"' in rad:
                        rad = float(rad.split('"')[0]) / self.pixsize / 60.0
                    else:
                        if "'" in rad:
                            rad = float(rad.split("'")[0]) / self.pixsize
                        else:
                            rad = float(rad) / self.pixsize * 60.0
                    wc = np.array([[xsrc, ysrc]])
                    pixcrd = self.wcs_inp.wcs_world2pix(wc, 1)
                    xsrc = pixcrd[0][0] - 1.0
                    ysrc = pixcrd[0][1] - 1.0
                else:
                    xsrc = float(vals.split(',')[0])
                    ysrc = float(vals.split(',')[1])
                    rad = float(vals.split(',')[2])
                boxsize = np.round(rad + 0.5).astype(int)
                intcx = np.round(xsrc).astype(int)
                intcy = np.round(ysrc).astype(int)
                xmin = np.max([intcx - boxsize, 0])
                xmax = np.min([intcx + boxsize + 1, self.axes[1]])
                ymin = np.max([intcy - boxsize, 0])
                ymax = np.min([intcy + boxsize + 1, self.axes[0]])
                rbox = np.hypot(x[ymin:ymax, xmin:xmax] - xsrc, y[ymin:ymax, xmin:xmax] - ysrc)
                src = np.where(rbox < rad)
                expo[ymin:ymax, xmin:xmax][src] = 0.0
                nsrc = nsrc + 1

        print('Excluded %d sources' % nsrc)
        self.exposure = expo

    def dmfilth(self, outfile=None):
        if self.img is None:
            print('No data given')
            return
        chimg = np.where(self.exposure == 0.0)
        imgc = np.copy(self.img)
        imgc[chimg] = 0.0
        print('Applying high-pass filter')
        smoothing_scale = 25
        gsb = gaussian_filter(imgc, smoothing_scale)
        gsexp = gaussian_filter(self.exposure, smoothing_scale)
        img_smoothed = np.nan_to_num(np.divide(gsb, gsexp)) * self.exposure
        print('Interpolating in the masked regions')
        y, x = np.indices(self.axes)
        nonz = np.where(img_smoothed > 0.0)
        p_ok = np.array([x[nonz], y[nonz]]).T
        vals = img_smoothed[nonz]
        int_vals = np.nan_to_num(griddata(p_ok, vals, (x, y), method='cubic'))
        print('Filling holes')
        area_to_fill = np.where(np.logical_and(int_vals > 0.0, self.exposure == 0))
        dmfilth = np.copy(self.img)
        dmfilth[area_to_fill] = np.random.poisson(int_vals[area_to_fill])
        self.filth = dmfilth
        if outfile is not None:
            hdu = fits.PrimaryHDU(dmfilth)
            hdu.header = self.header
            hdu.writeto(outfile, overwrite=True)
            print('Dmfilth image written to file ' + outfile)