# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/Output.py
# Compiled at: 2019-03-29 14:14:08
# Size of source mod 2**32: 25975 bytes
import os, os.path, numpy as np, pickle
import astropy.units as u
import psycopg2
from solarsystem import planet_dist
import mathMB
from .satellite_initial_positions import satellite_initial_positions
from atomicdataMB import RadPresConst
from .LossInfo import LossInfo
from .rk5 import rk5
from .bouncepackets import bouncepackets
from .source_distribution import surface_distribution, speed_distribution, angular_distribution, surface_spot, idlversion
from mathMB import minmaxmean

class Output:
    __doc__ = 'Keep track of packets initial and final positions\n    x0, y0, z0, f0, vx0, vy0, vz0\n    phi0, lat0, lon0\n    time, x, y, z, vx, vy, vz\n    index, npackets, totalsource\n    '

    def __init__(self, inputs, npackets, compress=True):
        self.inputs = inputs
        self.planet = inputs.geometry.planet
        self.compress = compress
        self.unit = u.def_unit('R_' + self.planet.object, self.planet.radius)
        self.GM = self.planet.GM.to(self.unit ** 3 / u.s ** 2).value
        r, v_r = planet_dist(self.planet, self.inputs.geometry.taa)
        self.aplanet = r.value
        self.vrplanet = v_r.to(self.unit / u.s).value
        if inputs.options.lifetime.value <= 0:
            self.loss_info = LossInfo(inputs.options.atom, inputs.options.lifetime, self.aplanet, inputs.database)
        else:
            self.loss_info = None
        if inputs.forces.radpres:
            radpres = RadPresConst(inputs.options.atom, self.aplanet, inputs.database)
            radpres.velocity = radpres.velocity.to(self.unit / u.s).value
            radpres.accel = radpres.accel.to(self.unit / u.s ** 2).value
            self.radpres = radpres
        else:
            self.radpres = None
        if inputs.options.at_once:
            time = np.ones(npackets) * inputs.options.endtime
        else:
            time = np.random.rand(npackets) * inputs.options.endtime
        self.time0 = time.copy()
        self.time = time.copy()
        self.f0 = np.ones(npackets)
        self.frac = np.ones(npackets)
        self.npackets = npackets
        self.totalsource = np.sum(self.f0)
        self.LossFrac = np.zeros(npackets)
        if self.planet.moons is not None:
            sat_init_pos = satellite_initial_positions(inputs)
        else:
            self.source_distribution()

    def __str__(self):
        print('Contents of output:')
        print('\tPlanet = {}'.format(self.planet.object))
        print('\ta_planet = {}'.format(self.aplanet))
        print('\tvr_planet = {}'.format(self.vrplanet))
        return ''

    def __len__(self):
        return self.npackets

    def __getitem__(self, keys):
        self.time = self.time[keys]
        self.frac = self.frac[keys]
        self.x = self.x[keys]
        self.y = self.y[keys]
        self.z = self.z[keys]
        self.vx = self.vx[keys]
        self.vy = self.vy[keys]
        self.vz = self.vz[keys]
        if 'index' in self.__dict__.keys():
            self.index = self.index[keys]

    def source_distribution(self):
        if self.inputs.spatialdist.type == 'surface':
            X0, lon, lat = surface_distribution(self.inputs, self.npackets, self.unit)
        else:
            if self.inputs.spatialdist.type == 'surfacespot':
                X0, lon, lat = surface_spot(self.inputs, self.npackets, self.unit)
            else:
                if self.inputs.spatialdist.type == 'idlversion':
                    X0, V0_, _ = idlversion(self.inputs, self.unit)
                else:
                    if not 0:
                        raise AssertionError('Spatial Distribution {} not supported.'.format(self.inputs.spatialdist.type))
                    else:
                        v0 = speed_distribution(self.inputs, self.npackets)
                        if v0 is not None:
                            v0 = v0.to(self.unit / u.s)
                            V0 = angular_distribution(self.inputs, X0.value, v0.value)
                            if V0 is not None:
                                V0 *= self.unit / u.s
                        else:
                            V0 = None
                    if self.inputs.geometry.planet.object != self.inputs.geometry.startpoint and not 0:
                        raise AssertionError('Not set up yet')
                    else:
                        if V0 is None:
                            V0 = V0_
                        else:
                            self.x0 = X0[0, :]
                    self.y0 = X0[1, :]
                    self.z0 = X0[2, :]
                    self.vx0 = V0[0, :]
                    self.vy0 = V0[1, :]
                    self.vz0 = V0[2, :]
                    self.x = X0[0, :]
                    self.y = X0[1, :]
                    self.z = X0[2, :]
                    self.vx = V0[0, :]
                    self.vy = V0[1, :]
                    self.vz = V0[2, :]

    def driver(self):
        hall = np.zeros(self.npackets) + 1000.0
        count = 0
        eps = 1e-10
        safety = 0.95
        shrink = -0.25
        grow = -0.2
        rest = self.inputs.options.resolution
        resx = self.inputs.options.resolution
        resv = 0.1 * self.inputs.options.resolution
        resf = self.inputs.options.resolution
        T = self.time.value
        X = np.array([self.x, self.y, self.z])
        V = np.array([self.vx, self.vy, self.vz])
        Frac = self.frac
        LossFrac = self.LossFrac
        numb = []
        moretogo = (T > rest) & (Frac > 0.0)
        while moretogo.any():
            oldT = T[moretogo].copy()
            oldX = X[:, moretogo].copy()
            oldV = V[:, moretogo].copy()
            oldFrac = Frac[moretogo].copy()
            T0 = T[moretogo]
            X0 = X[:, moretogo]
            V0 = V[:, moretogo]
            F0 = Frac[moretogo]
            Loss0 = LossFrac[moretogo]
            h = hall[moretogo]
            assert np.all(h >= 0), '\n\tNegative values of h'
            h = (T0 >= h) * h + (T0 < h) * T0
            t1, x1, v1, f1, delx, delv, delf = rk5(T0, X0, V0, F0, h, self)
            scalex = resx + np.abs(x1) * resx
            scalev = resv + np.abs(v1) * resv
            scalef = resf + np.abs(f1) * resf
            delx /= scalex
            delv /= scalev
            delf /= scalef
            xerrmax = delx.max(axis=0)
            verrmax = delv.max(axis=0)
            errmax = np.maximum(xerrmax, verrmax)
            errmax = np.maximum(errmax, delf)
            assert np.all(np.isfinite(errmax)), '\n\tInfinite values of emax'
            m = (f1 < 0) & (errmax < 1)
            if np.any(m):
                raise AssertionError('Found new values of frac that are negative')
            m = (f1 - oldFrac > scalef) & (errmax > 1)
            if np.any(m):
                errmax[m] = 1.1
            noerr = errmax < 1e-07
            errmax[noerr] = 1
            h[noerr] *= 10
            g = errmax < 1.0
            b = errmax >= 1.0
            numb.append(np.sum(b))
            if np.any(g):
                t_ = t1[g]
                x_ = x1[:, g]
                v_ = v1[:, g]
                f_ = f1[g]
                h_ = safety * h[g] * errmax[g] ** grow
                tempR = np.linalg.norm(x_, axis=0)
                hhh = tempR.value - 1 < 0
                if np.any(hhh):
                    if self.inputs.sticking_info.stickcoef == 1.0:
                        f_[hhh] = 0.0
                    else:
                        bouncepackets(self, t_, x_, v_, f_, hhh)
                if not self.inputs.options.fullsystem:
                    f_[tempR > self.inputs.options.outeredge] = 0
                f_[f_ < 1e-10] = 0
                t_[f_ == 0] = 0.0
                T0[g] = t_
                X0[:, g] = x_
                V0[:, g] = v_
                F0[g] = f_
                h[g] = h_
            if np.any(b):
                htemp = safety * h[b] * errmax[b] ** shrink
                assert np.all(np.isfinite(htemp)), '\n\tInfinite values of h'
                h[b] = np.maximum(htemp, 0.1 * h[b])
            assert np.all(h >= 0), '\n\tNegative values of h'
            T[moretogo] = T0
            X[:, moretogo] = X0
            V[:, moretogo] = V0
            Frac[moretogo] = F0
            LossFrac[moretogo] = Loss0
            hall[moretogo] = h
            moretogo = (T > rest) & (Frac > 0.0)
            if count % 100 == 0:
                print(f"Step {count}. {np.sum(moretogo)} more to go\n\th: {mathMB.minmaxmean(h)}")
            count += 1

        self.time = T * u.s
        self.x = X[0, :] * self.unit
        self.y = X[1, :] * self.unit
        self.z = X[2, :] * self.unit
        self.vx = V[0, :] * self.unit / u.s
        self.vy = V[1, :] * self.unit / u.s
        self.vz = V[2, :] * self.unit / u.s
        self.frac = Frac
        self.aplanet *= self.unit
        self.vrplanet *= self.unit / u.s
        self.GM *= self.unit ** 3 / u.s ** 2

    def stream_driver(self):
        T = self.time.value
        X = np.array([self.x, self.y, self.z])
        V = np.array([self.vx, self.vy, self.vz])
        Frac = self.frac
        LossFrac = self.LossFrac
        npack = len(T)
        xx0 = np.zeros((3, npack, self.inputs.options.nsteps))
        vv0 = np.zeros((3, npack, self.inputs.options.nsteps))
        ff0 = np.zeros((npack, self.inputs.options.nsteps))
        tt0 = np.zeros((npack, self.inputs.options.nsteps))
        tt0[:, 0] = T
        xx0[:, :, 0] = X
        vv0[:, :, 0] = V
        ff0[:, 0] = Frac
        dt = self.inputs.options.endtime.value / (self.inputs.options.nsteps - 1)
        h = dt
        curtime = self.inputs.options.endtime.value
        ct = 1
        eps = 1e-10
        moretogo = Frac > 0
        while curtime > 0:
            if moretogo.any():
                t0 = T[moretogo]
                x0 = X[:, moretogo]
                v0 = V[:, moretogo]
                f0 = Frac[moretogo]
                oldF = f0.copy()
                assert (f0 != 0).all(), 'Should not have 0 frac'
                assert np.isfinite(x0).all(), 'Infinite X values'
                assert np.isfinite(v0).all(), 'Infinite V values'
                t1, x1, v1, f1, _, _, _ = rk5(t0, x0, v0, f0, h, self)
                tempR = np.linalg.norm(x1, axis=0)
                hhh = tempR - 1.0 < 0
                if np.any(hhh):
                    if self.inputs.sticking_info.stickcoef == 1:
                        f1[hhh] = 0.0
            else:
                bouncepackets(self, t1, x1, v1, f1, hhh)
            if not self.inputs.options.fullsystem:
                f1[tempR > self.inputs.options.outeredge] = 0
            f1[f1 < 1e-10] = 0.0
            t1[f1 == 0] = 0.0
            T[moretogo] = t1
            X[:, moretogo] = x1
            V[:, moretogo] = v1
            Frac[moretogo] = f1
            tt0[:, ct] = T
            xx0[:, :, ct] = X
            vv0[:, :, ct] = V
            ff0[:, ct] = Frac
            moretogo = Frac > 0
            done = moretogo.any() is False
            if ct % 100 == 0:
                print(ct, curtime, np.sum(moretogo))
            ct += 1
            curtime -= dt

        allpacks = npack * self.inputs.options.nsteps
        self.time = tt0.reshape(allpacks) * u.s
        self.x = xx0[0, :, :].reshape(allpacks) * self.unit
        self.y = xx0[1, :, :].reshape(allpacks) * self.unit
        self.z = xx0[2, :, :].reshape(allpacks) * self.unit
        self.vx = vv0[0, :, :].reshape(allpacks) * self.unit / u.s
        self.vy = vv0[1, :, :].reshape(allpacks) * self.unit / u.s
        self.vz = vv0[2, :, :].reshape(allpacks) * self.unit / u.s
        self.frac = ff0.reshape(allpacks)
        self.totalsource *= self.inputs.options.nsteps
        index = np.mgrid[0:npack, 0:self.inputs.options.nsteps]
        self.index = index[0, :, :].reshape(allpacks)
        self.aplanet *= self.unit
        self.vrplanet *= self.unit / u.s
        self.GM *= self.unit ** 3 / u.s ** 2

    def determine_filename(self):
        """Come up with a filename for the model"""
        if self.planet.object == 'Mercury':
            taastr = '{:03.0f}'.format(np.round(self.inputs.geometry.taa.to(u.deg).value))
        else:
            assert 0, 'Filename not set up for anything but Mercury'
        pathname = os.path.join(self.inputs.savepath, self.planet.object, self.inputs.options.atom, self.inputs.spatialdist.type, self.inputs.speeddist.type, taastr)
        if os.path.exists(pathname) == 0:
            os.makedirs(pathname)
        numstr = '{:010d}'.format(self.idnum)
        filename = f"{numstr}.pkl"
        return (
         pathname, filename)

    def save(self):
        con = psycopg2.connect(database=(self.inputs.database))
        con.autocommit = True
        cur = con.cursor()
        cur.execute('INSERT into outputfile (npackets,\n                                               totalsource,\n                                               creationtime)\n                       VALUES (%s, %s, NOW())', (self.npackets,
         self.totalsource))
        cur.execute('SELECT idnum\n                       FROM outputfile\n                       WHERE filename is Null')
        if not cur.rowcount == 1:
            raise AssertionError('Outputs with NULL filename')
        else:
            self.idnum = cur.fetchone()[0]
            geometry = self.inputs.geometry
            objs = [obj.object for obj in geometry.objects]
            objs.sort()
            phi = [p.value for p in geometry.phi]
            cur.execute("INSERT into geometry\n                       VALUES (%s, %s, %s, %s::SSObject[],\n                               %s, %s, '(%s, %s)', %s)", (
             self.idnum,
             geometry.planet.object,
             geometry.startpoint,
             objs,
             geometry.time,
             phi,
             geometry.subsolarpoint[0].value,
             geometry.subsolarpoint[1].value,
             geometry.taa.value))
            con.commit()
            sticking_info = self.inputs.sticking_info
            cur.execute('INSERT into sticking_info\n                       VALUES (%s, %s, %s, %s, %s, %s,\n                               %s, %s, %s, %s, %s)', (
             self.idnum,
             sticking_info.stickcoef,
             sticking_info.tsurf,
             sticking_info.stickfn,
             sticking_info.stick_mapfile,
             sticking_info.epsilon,
             sticking_info.n,
             sticking_info.tmin,
             sticking_info.emitfn,
             sticking_info.accom_mapfile,
             sticking_info.accom_factor))
            con.commit()
            forces = self.inputs.forces
            cur.execute('INSERT into forces\n                       VALUES (%s, %s, %s)', (
             self.idnum, forces.gravity, forces.radpres))
            con.commit()
            spatdist = self.inputs.spatialdist
            if spatdist.longitude is None:
                lon = (0.0, 0.0)
            else:
                lon = (
                 spatdist.longitude[0].value, spatdist.longitude[1].value)
            if spatdist.latitude is None:
                lat = (0.0, 0.0)
            else:
                lat = (
                 spatdist.latitude[0].value, spatdist.latitude[1].value)
            cur.execute('INSERT into spatialdist\n                       VALUES (%s, %s, %s, %s, %s,\n                               ARRAY[%s,%s], ARRAY[%s,%s])', (
             self.idnum,
             spatdist.type,
             spatdist.exobase,
             spatdist.use_map,
             spatdist.mapfile,
             lon[0], lon[1],
             lat[0], lat[1]))
            con.commit()
            speeddist = self.inputs.speeddist
            vprob = None if speeddist.vprob is None else speeddist.vprob.value
            sigma = None if speeddist.sigma is None else speeddist.sigma.value
            U = None if speeddist.U is None else speeddist.U.value
            temperature = None if speeddist.temperature is None else speeddist.temperature.value
            delv = None if speeddist.delv is None else speeddist.delv.value
            cur.execute('INSERT into speeddist\n                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (
             self.idnum,
             speeddist.type,
             vprob,
             sigma,
             U,
             speeddist.alpha,
             speeddist.beta,
             temperature,
             delv))
            con.commit()
            angdist = self.inputs.angulardist
            if angdist.azimuth is None:
                az = 'NULL'
            else:
                az0 = angdist.azimuth[0].value
                az1 = angdist.azimuth[1].value
                az = f"ARRAY[{az0}, {az1}]"
            if angdist.altitude is None:
                alt = 'NULL'
            else:
                alt0 = angdist.altitude[0].value
            alt1 = angdist.altitude[1].value
            alt = f"ARRAY[{alt0}, {alt1}]"
        n = None if angdist.n is None else angdist.n
        cur.execute(f"INSERT into angulardist\n                        VALUES (%s, %s, {az}, {alt}, %s)", (
         self.idnum,
         angdist.type,
         n))
        con.commit()
        options = self.inputs.options
        cur.execute('INSERT into options\n                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
         self.idnum,
         options.endtime.value,
         options.resolution,
         options.at_once,
         options.atom,
         options.lifetime.value,
         options.fullsystem,
         options.outeredge,
         options.motion,
         options.streamlines,
         options.nsteps))
        con.commit()
        savefile = (os.path.join)(*self.determine_filename())
        print('Saving output as {}'.format(savefile))
        cur.execute('UPDATE outputfile\n                       SET filename=%s\n                       WHERE idnum=%s', (savefile, self.idnum))
        con.commit()
        con.close()
        if self.compress:
            self[(self.frac > 0)]
        self.time0 = self.time0.value.astype(np.float32)
        self.f0 = self.f0.astype(np.float32)
        self.x0 = self.x0.value.astype(np.float32)
        self.y0 = self.y0.value.astype(np.float32)
        self.z0 = self.z0.value.astype(np.float32)
        self.vx0 = self.vx0.value.astype(np.float32)
        self.vy0 = self.vy0.value.astype(np.float32)
        self.vz0 = self.vz0.value.astype(np.float32)
        self.time = self.time.value.astype(np.float32)
        self.frac = self.frac.astype(np.float32)
        self.x = self.x.value.astype(np.float32)
        self.y = self.y.value.astype(np.float32)
        self.z = self.z.value.astype(np.float32)
        self.vx = self.vx.value.astype(np.float32)
        self.vy = self.vy.value.astype(np.float32)
        self.vz = self.vz.value.astype(np.float32)
        self.LossFrac = self.LossFrac.astype(np.float32)
        with open(savefile, 'wb') as (f):
            pickle.dump(self, f, protocol=(pickle.HIGHEST_PROTOCOL))

    @classmethod
    def restore(cls, filename, reform=False):
        output = pickle.load(open(filename, 'rb'))
        output.time0 *= u.s
        output.time *= u.s
        output.x0 *= output.unit
        output.y0 *= output.unit
        output.z0 *= output.unit
        output.vx0 *= output.unit / u.s
        output.vy0 *= output.unit / u.s
        output.vz0 *= output.unit / u.s
        output.x *= output.unit
        output.y *= output.unit
        output.z *= output.unit
        output.vx *= output.unit / u.s
        output.vy *= output.unit / u.s
        output.vz *= output.unit / u.s
        if reform:
            index_ = list(set(output.index))
            n, m = len(index_), output.inputs.options.nsteps
            x = np.ndarray((n, m))
            y = np.ndarray((n, m))
            z = np.ndarray((n, m))
            vx = np.ndarray((n, m))
            vy = np.ndarray((n, m))
            vz = np.ndarray((n, m))
            frac, index = np.ndarray((n, m)), np.ndarray((n, m))
            time = np.ndarray((n, m))
            for i, ind in enumerate(index_):
                q = output.index == ind
                x[i, :sum(q)] = output.x[q]
                y[i, :sum(q)] = output.y[q]
                z[i, :sum(q)] = output.z[q]
                vx[i, :sum(q)] = output.vx[q]
                vy[i, :sum(q)] = output.vy[q]
                vz[i, :sum(q)] = output.vz[q]
                frac[i, :sum(q)] = output.frac[q]
                index[i, :sum(q)] = output.index[q]
                time[i, :sum(q)] = output.time[q]

            output.x = x
            output.y = y
            output.z = z
            output.vx = vx
            output.vy = vy
            output.vz = vz
            output.frac = frac
            output.index = index
            output.time = time
        return output