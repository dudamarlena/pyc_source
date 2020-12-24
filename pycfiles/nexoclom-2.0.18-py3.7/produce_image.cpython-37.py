# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/produce_image.py
# Compiled at: 2019-02-21 11:38:12
# Size of source mod 2**32: 13699 bytes
import os.path, numpy as np
import numpy.matlib as npmat
import psycopg2, pandas as pd, pickle
import astropy.units as u
from solarsystem import SSObject
from mathMB import rotation_matrix
from .ModelResults import ModelResult, read_format, results_loadfile, results_packet_weighting
quantities = [
 'column', 'intensity', 'density']

def image_rotation(image):
    slong = image.subobslongitude
    slat = image.subobslatitude
    pSun = np.array([0.0, -1.0, 0.0])
    pObs = np.array([np.sin(slong) * np.cos(slat),
     -np.cos(slong) * np.cos(slat),
     np.sin(slat)])
    if np.array_equal(pSun, pObs):
        M = npmat.identity(3)
    else:
        costh = np.dot(pSun, pObs) / np.linalg.norm(pSun) / np.linalg.norm(pObs)
        theta = np.arccos(np.clip(costh, -1, 1))
        axis = np.cross(pSun, pObs)
        M = rotation_matrix(theta, axis)
    return M


class ModelImage(ModelResult):

    def __init__(self, inputs, formatfile, filenames=None):
        self.type = 'image'
        if isinstance(formatfile, str):
            format_ = read_format(formatfile)
            quantities = [
             'column', 'radiance']
            if format_['quantity'] in quantities:
                self.quantity = format_['quantity']
            else:
                assert 0, 'Quantity not specified'
            if format_['quantity'] == 'radiance':
                self.mechanism = tuple((m.strip() for m in format_['mechanism'].split(',')))
                if 'wavelength' in format_:
                    self.wavelength = tuple((int(m.strip()) * u.AA for m in format_['wavelength'].split(',')))
                else:
                    if inputs.options.atom == 'Na':
                        self.wavelength = (
                         5891 * u.AA, 5897 * u.AA)
                    else:
                        if inputs.options.atom == 'Ca':
                            self.wavelength = (
                             4227 * u.AA,)
                        else:
                            if inputs.options.atom == 'Mg':
                                self.wavelength = (
                                 2852 * u.AA,)
                            else:
                                assert 0, f"No default wavelength for {input.options.atom}"
            else:
                self.origin = SSObject(format_['origin'])
                self.unit = u.def_unit('R_' + self.origin.object, self.origin.radius)
                dimtemp = format_['dims'].split(',')
                self.dims = np.array((int(dimtemp[0]), int(dimtemp[1])))
                centtemp = format_['center'].split(',')
                self.center = np.array((float(centtemp[0]), float(centtemp[1])))
                self.center *= self.unit
                widtemp = format_['width'].split(',')
                self.width = np.array((float(widtemp[0]), float(widtemp[1])))
                self.width *= self.unit
                self.subobslongitude = float(format_['subobslongitude']) * u.rad
                self.subobslatitude = float(format_['subobslatitude']) * u.rad
        else:
            if isinstance(formatfile, dict):
                assert 0, 'Not working right yet'
                format_ = formatfile
                if format_['quantity'] in quantities:
                    self.quantity = format_['quantity']
                else:
                    assert 0, 'Quantity not specified'
                    self.origin = SSObject(format_['origin'])
                    unit = u.def_unit('R_' + self.origin.object, self.origin.radius)
                    self.dims = format_['dims']
                    self.center = format_['center']
                    self.width = format_['width']
                if isinstance(format_['subobslongitude'][0], (int, float)):
                    self.subobslongitude = (
                     format_['subobslongitude'][0] * u.rad,
                     format_['subobslongitude'][1] * u.rad)
                else:
                    if isinstance(format_['subobslongitude'][0], type(1 * u.rad)):
                        self.subobslongitude = format_['subobslongitude']
                    if isinstance(format_['subobslatitude'][0], (int, float)):
                        self.subobslatitude = (
                         format_['subobslatitude'][0] * u.rad,
                         format_['subobslatitude'][1] * u.rad)
                    else:
                        if isinstance(format_['subobslatitude'][0], type(1 * u.rad)):
                            self.subobslatitude = format_['subobslatitude']
            else:
                assert 0, 'Format problem.'
                ModelResult.__init__(self, inputs)
                if isinstance(filenames, str):
                    print('Setting filenames breaks calibration.')
                    self.filenames = [filenames]
                else:
                    if isinstance(filenames, list):
                        print('Setting filenames breaks calibration.')
                        self.filenames = filenames
                    else:
                        self.image = np.zeros(self.dims)
                        self.packet_image = np.zeros(self.dims)
                        self.blimits = None
                        immin = self.center - self.width / 2.0
                        immax = self.center + self.width / 2.0
                        scale = self.width / (self.dims - 1)
                        self.Apix = (scale[0] * scale[1]).to(u.cm ** 2)
                        self.xaxis = np.linspace(immin[0], immax[0], self.dims[0])
                        self.zaxis = np.linspace(immin[1], immax[1], self.dims[1])
                        for i, fname in enumerate(self.filenames):
                            image_, packets_ = self.restore(fname)
                            if image_ is None:
                                image_, packets_ = self.create_image(fname)
                                print(f"Completed image {i + 1} of {len(self.filenames)}")
                            else:
                                print(f"Image {i + 1} of {len(self.filenames)} previously completed.")
                            self.image += image_
                            self.packet_image += packets_

                self.image = self.image * self.atoms_per_packet

    def save(self, fname, image, packets):
        con = psycopg2.connect(database=(self.inputs.database))
        con.autocommit = True
        cur = con.cursor()
        idnum_ = pd.read_sql(f"SELECT idnum\n                                FROM outputfile\n                                WHERE filename='{fname}' ", con)
        idnum = int(idnum_.idnum[0])
        if self.quantity == 'radiance':
            mech = ', '.join(sorted([m for m in self.mechanism]))
            wave_ = sorted([w.value for w in self.wavelength])
            wave = ', '.join([str(w) for w in wave_])
        else:
            mech = None
            wave = None
        dims = f"ARRAY[{self.dims[0]}, {self.dims[1]}]"
        center = f"ARRAY[{self.center[0].value}, {self.center[1].value}]"
        width = f"ARRAY[{self.width[0].value}, {self.width[1].value}]"
        cur.execute(f"INSERT into modelimages (out_idnum, quantity,\n                            origin, dims, center, width, subobslongitude,\n                            subobslatitude, mechanism, wavelength)\n                        values (%s, %s, %s, {dims}, {center}, {width},\n                            %s, %s, %s, %s)", (
         idnum, self.quantity, self.origin.object,
         self.subobslongitude.value, self.subobslatitude.value,
         mech, wave))
        idnum_ = pd.read_sql('SELECT idnum\n                                FROM modelimages\n                                WHERE filename is NULL', con)
        assert len(idnum_) == 1
        idnum = int(idnum_.idnum[0])
        savefile = os.path.join(os.path.dirname(fname), f"image.{idnum}.pkl")
        with open(savefile, 'wb') as (f):
            pickle.dump((image, packets), f)
        cur.execute('UPDATE modelimages\n                        SET filename=%s\n                        WHERE idnum = %s', (savefile, idnum))

    def restore(self, fname):
        con = psycopg2.connect(database=(self.inputs.database))
        con.autocommit = True
        idnum_ = pd.read_sql(f"SELECT idnum\n                                FROM outputfile\n                                WHERE filename='{fname}' ", con)
        oid = idnum_.idnum[0]
        if self.quantity == 'radiance':
            mech = "mechanism = '" + ', '.join(sorted([m for m in self.mechanism])) + "'"
            wave_ = sorted([w.value for w in self.wavelength])
            wave = "wavelength = '" + ', '.join([str(w) for w in wave_]) + "'"
        else:
            mech = 'mechanism is NULL'
            wave = 'wavelength is NULL'
        result = pd.read_sql(f"SELECT filename FROM modelimages\n                WHERE out_idnum = {oid} and\n                      quantity = '{self.quantity}' and\n                      origin = '{self.origin.object}' and\n                      dims[1] = {self.dims[0]} and\n                      dims[2] = {self.dims[1]} and\n                      center[1] = {self.center[0].value} and\n                      center[2] = {self.center[1].value} and\n                      width[1] = {self.width[0].value} and\n                      width[2] = {self.width[1].value} and\n                      subobslongitude = {self.subobslongitude.value} and\n                      subobslatitude = {self.subobslatitude.value} and\n                      {mech} and\n                      {wave}", con)
        if not len(result) <= 1:
            raise AssertionError
        elif len(result) == 1:
            savefile = result.filename[0]
            image, packets = pickle.load(open(savefile, 'rb'))
        else:
            image, packets = (None, None)
        return (image, packets)

    def create_image(self, fname):
        M = image_rotation(self)
        output = results_loadfile(fname)
        radvel_sun = output.vy + output.vrplanet
        pts_sun = np.array((output.x, output.y, output.z)) * output.x.unit
        frac = output.frac
        pts_obs = np.matmul(M, pts_sun)
        rhosqr_obs = pts_obs[0, :] ** 2 + pts_obs[2, :] ** 2
        inview = (rhosqr_obs.value > 1) | (pts_obs[1, :].value < 0)
        frac *= inview
        rhosqr_sun = pts_sun[0, :] ** 2 + pts_sun[2, :] ** 2
        out_of_shadow = (rhosqr_sun.value > 1) | (pts_sun[1, :].value < 0)
        weight = results_packet_weighting(self, radvel_sun, frac, out_of_shadow, output.aplanet) / self.Apix
        assert pts_obs.unit == self.xaxis.unit
        dx = (self.xaxis[1] - self.xaxis[0]) / 2.0
        bx = np.append(self.xaxis.value - dx.value, self.xaxis[(-1)].value + dx.value) * self.xaxis.unit
        dz = (self.zaxis[1] - self.zaxis[0]) / 2.0
        bz = np.append(self.zaxis.value - dz.value, self.zaxis[(-1)].value + dz.value) * self.zaxis.unit
        image, _, _ = np.histogram2d((pts_obs[0, :]), (pts_obs[2, :]), weights=weight,
          bins=(bx, bz))
        packets, _, _ = np.histogram2d((pts_obs[0, :]), (pts_obs[2, :]), bins=(
         bx, bz))
        self.save(fname, image, packets)
        del output
        return (
         image, packets)

    def display(self, savefile='image.png', limits=None, show=True):
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        from matplotlib.colors import LogNorm
        from astropy.visualization import PercentileInterval, LogStretch, ImageNormalize
        extent = (
         np.min(self.xaxis.value), np.max(self.xaxis.value),
         np.min(self.zaxis.value), np.max(self.zaxis.value))
        if self.unit.__str__() == 'R_Mercury':
            ustr = '$R_{M}$'
        else:
            ustr = '$R_{obj}$'
        if limits is None:
            interval = PercentileInterval(95)
            self.blimits = interval.get_limits(self.image[(self.image > 0)])
        else:
            if len(limits) == 2:
                self.blimits = limits
            else:
                if not 0:
                    raise AssertionError('Problem with the display limits')
                else:
                    fig, ax = plt.subplots(figsize=(12, 12))
                    im = ax.imshow((self.image.transpose()), cmap='afmhot', extent=extent, norm=LogNorm(vmin=(self.blimits[0]), vmax=(self.blimits[1])))
                    ax.set_xlabel(f"Distance ({ustr})")
                    ax.set_ylabel(f"Distance ({ustr})")
                    ax.set_title(f"{self.inputs.options.atom} {self.quantity.title()}")
                    if self.quantity == 'column':
                        clabel = f"$N_{{ {self.inputs.options.atom} }}\\ cm^{{-2}}$"
                    else:
                        clabel = f"$I_{{ {self.inputs.options.atom} }} R$"
                cbar = fig.colorbar(im, shrink=0.7, label=clabel)
                xc, yc = np.cos(np.linspace(0, 2 * np.pi, 1000)), np.sin(np.linspace(0, 2 * np.pi, 1000))
                ax.fill(xc, yc, 'y')
                if show:
                    plt.show()
                plt.savefig(savefile)
                plt.close()
                return (
                 fig, ax, cbar)