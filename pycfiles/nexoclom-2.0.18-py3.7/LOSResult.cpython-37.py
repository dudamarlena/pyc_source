# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/LOSResult.py
# Compiled at: 2019-02-19 11:16:26
# Size of source mod 2**32: 10897 bytes
import os.path, numpy as np, pandas as pd, psycopg2, pickle
import astropy.units as u
from solarsystem import SSObject
from MESSENGERuvvs import MESSENGERdata
from .ModelResults import ModelResult, read_format, results_loadfile, results_packet_weighting

class LOSResult(ModelResult):

    def __init__(self, inputs, data, quantity, dphi=3 * u.deg, filenames=None):
        self.type = 'LineOfSight'
        self.species = inputs.options.atom
        self.quantity = quantity
        self.origin = inputs.geometry.planet
        self.unit = u.def_unit('R_' + self.origin.object, self.origin.radius)
        self.dphi = dphi
        ModelResult.__init__(self, inputs)
        if isinstance(filenames, str):
            print('Setting filenames breaks calibration.')
            self.filenames = [filenames]
        else:
            if isinstance(filenames, list):
                print('Setting filenames breaks calibration.')
                self.filenames = filenames
            else:
                if self.quantity == 'radiance':
                    self.mechanism = ('resscat', )
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
                    nspec = len(data.x)
                    self.radiance = np.zeros(nspec)
                    self.ninview = np.zeros(nspec, dtype=int)
                    for j, outfile in enumerate(self.filenames):
                        radiance_, packets_ = self.restore(data, outfile)
                        if radiance_ is None:
                            radiance_, packets_ = self.create_model(data, outfile)
                            print(f"Completed model {j + 1} of {len(self.filenames)}")
                        else:
                            print(f"Model {j + 1} of {len(self.filenames)} previously completed.")
                        self.radiance += radiance_
                        self.packets += packets_

                    self.radiance = self.radiance * self.atoms_per_packet.value * u.R

    def save(self, data, fname, radiance, packets):
        orbits = set(data.orbit)
        orb = orbits.pop()
        if len(orbits) != 0:
            print('Model spans more than one orbit. Cannot be saved.')
        else:
            mdata = MESSENGERdata(self.species, f"orbit = {orb}")
            if len(mdata) != len(data):
                print('Model does not contain the complete orbit. Cannot be saved.')
            else:
                con = psycopg2.connect(database=(self.inputs.database))
                con.autocommit = True
                cur = con.cursor()
                idnum_ = pd.read_sql(f"SELECT idnum\n                                        FROM outputfile\n                                        WHERE filename='{fname}' ", con)
                idnum = int(idnum_.idnum[0])
                if self.quantity == 'radiance':
                    mech = ', '.join(sorted([m for m in self.mechanism]))
                    wave_ = sorted([w.value for w in self.wavelength])
                    wave = ', '.join([str(w) for w in wave_])
                else:
                    mech = None
                    wave = None
                cur.execute('INSERT into uvvsmodels (out_idnum, quantity,\n                                    orbit, dphi, mechanism, wavelength)\n                                values (%s, %s, %s, %s, %s, %s)', (
                 idnum, self.quantity, orb, self.dphi.value,
                 mech, wave))
                idnum_ = pd.read_sql('SELECT idnum\n                                        FROM uvvsmodels\n                                        WHERE filename is NULL', con)
                assert len(idnum_) == 1
                idnum = int(idnum_.idnum[0])
                savefile = os.path.join(os.path.dirname(fname), f"model.orbit{orb:04}.{idnum}.pkl")
                with open(savefile, 'wb') as (f):
                    pickle.dump((radiance, packets), f)
                cur.execute('UPDATE uvvsmodels\n                                SET filename=%s\n                                WHERE idnum=%s', (savefile, idnum))

    def restore(self, data, fname):
        orbits = set(data.orbit)
        orb = orbits.pop()
        if len(orbits) != 0:
            print('Model spans more than one orbit. Cannot be saved.')
            radiance, packets = (None, None)
        else:
            mdata = MESSENGERdata(self.species, f"orbit = {orb}")
            if len(mdata) != len(data):
                print('Model does not contain the complete orbit. Cannot be saved.')
                radiance, packets = (None, None)
            else:
                con = psycopg2.connect(database=(self.inputs.database))
                con.autocommit = True
                idnum_ = pd.read_sql(f"SELECT idnum\n                                        FROM outputfile\n                                        WHERE filename='{fname}' ", con)
                oid = idnum_.idnum[0]
                if self.quantity == 'radiance':
                    mech = "mechanism = '" + ', '.join(sorted([m for m in self.mechanism])) + "'"
                    wave_ = sorted([w.value for w in self.wavelength])
                    wave = "wavelength = '" + ', '.join([str(w) for w in wave_]) + "'"
                else:
                    mech = 'mechanism is NULL'
                    wave = 'wavelength is NULL'
                result = pd.read_sql(f"SELECT filename FROM uvvsmodels\n                        WHERE out_idnum={oid} and\n                              quantity = '{self.quantity}' and\n                              orbit = {orb} and\n                              dphi = {self.dphi.value} and\n                              {mech} and\n                              {wave}", con)
                if not len(result) <= 1:
                    raise AssertionError
                elif len(result) == 1:
                    savefile = result.filename[0]
                    with open(savefile, 'rb') as (f):
                        radiance, packets = pickle.load(f)
                else:
                    radiance, packets = (None, None)
            return (
             radiance, packets)

    def create_model(self, data, outfile):
        dist_from_plan = np.sqrt(data.x ** 2 + data.y ** 2 + data.z ** 2)
        ang = np.arccos((-data.x * data.xbore - data.y * data.ybore - data.z * data.zbore) / dist_from_plan)
        asize_plan = np.arcsin(1.0 / dist_from_plan)
        dist_from_plan[ang > asize_plan] = 1e+30
        output = results_loadfile(outfile)
        radvel_sun = output.vy + output.vrplanet
        out_of_shadow = np.ones_like(output.x)
        weight = results_packet_weighting(self, radvel_sun, output.frac, out_of_shadow, output.aplanet)
        xx_, yy_, zz_ = np.zeros((2, len(data))), np.zeros((2, len(data))), np.zeros((2, len(data)))
        xx_[1, :], yy_[1, :], zz_[1, :] = data.xbore * 10, data.ybore * 10, data.zbore * 10
        xx = data.x[np.newaxis, :] + xx_
        yy = data.y[np.newaxis, :] + yy_
        zz = data.z[np.newaxis, :] + zz_
        xx_min = np.min((xx - 0.5), axis=0) * self.unit
        yy_min = np.min((yy - 0.5), axis=0) * self.unit
        zz_min = np.min((zz - 0.5), axis=0) * self.unit
        xx_max = np.max((xx + 0.5), axis=0) * self.unit
        yy_max = np.max((yy + 0.5), axis=0) * self.unit
        zz_max = np.max((zz + 0.5), axis=0) * self.unit
        radiance, packets = np.zeros(len(data)), np.zeros(len(data))
        for i, row in data.iterrows():
            mask = (output.x >= xx_min[i]) & (output.x <= xx_max[i]) & (output.y >= yy_min[i]) & (output.y <= yy_max[i]) & (output.z >= zz_min[i]) & (output.z <= zz_max[i])
            x_, y_, z_, w_, rvsun_ = (output.x[mask], output.y[mask],
             output.z[mask], weight[mask],
             radvel_sun[mask])
            xpr = x_ - row.x * self.unit
            ypr = y_ - row.y * self.unit
            zpr = z_ - row.z * self.unit
            rpr = np.sqrt(xpr ** 2 + ypr ** 2 + zpr ** 2)
            costheta = (xpr * row.xbore + ypr * row.ybore + zpr * row.zbore) / rpr
            costheta[costheta > 1] = 1.0
            costheta[costheta < -1] = -1.0
            inview = (costheta >= np.cos(self.dphi)) & (w_ > 0) & (rpr < dist_from_plan[i] * self.unit)
            if np.any(inview):
                Apix = np.pi * (rpr[inview] * np.sin(self.dphi)) ** 2
                wtemp = w_[inview] / Apix.to(u.cm ** 2)
                wtemp = wtemp.value
                if self.quantity == 'radiance':
                    losrad = rpr[inview] * costheta[inview]
                    xhit = row.x + row.xbore * losrad.value
                    yhit = row.y + row.ybore * losrad.value
                    zhit = row.z + row.zbore * losrad.value
                    rhohit = xhit ** 2 + zhit ** 2
                    out_of_shadow = (rhohit > 1) | (yhit < 0)
                    wtemp *= out_of_shadow
                    radiance[i] = np.sum(wtemp)
                    packets[i] = np.sum(inview)

        del output
        self.save(data, outfile, radiance, packets)
        return (
         radiance, packets)