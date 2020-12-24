# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/Input.py
# Compiled at: 2019-02-20 14:44:49
# Size of source mod 2**32: 14435 bytes
import os, os.path, numpy as np, psycopg2
from astropy.io import ascii
import astropy.units as u
from .produce_image import ModelImage
from .modeldriver import modeldriver
from .configure_model import configfile
from .input_classes import Geometry, StickingInfo, Forces, SpatialDist, SpeedDist, AngularDist, Options

class Input:

    def __init__(self, infile, verbose=False):
        self.database, self.savepath, self.datapath = configfile()
        self.inputfile = infile
        if os.path.isfile(infile):
            data = ascii.read(infile, delimiter='=', comment=';', data_start=0,
              names=['Param', 'Value'])
        else:
            assert 0, 'Input file {} does not exist.'.format(infile)
        section = [d.split('.')[0].casefold() for d in data['Param']]
        param = [d.split('.')[1].casefold() for d in data['Param']]
        values = [v.split(';')[0].strip().casefold() if ';' in v else v.casefold() for v in data['Value']]
        gparam = {b:c for a, b, c in zip(section, param, values) if a == 'geometry' if a == 'geometry'}
        self.geometry = Geometry(gparam)
        sparam = {b:c for a, b, c in zip(section, param, values) if a == 'sticking_info' if a == 'sticking_info'}
        self.sticking_info = StickingInfo(sparam)
        fparam = {b:c for a, b, c in zip(section, param, values) if a == 'forces' if a == 'forces'}
        self.forces = Forces(fparam)
        sparam = {b:c for a, b, c in zip(section, param, values) if a == 'spatialdist' if a == 'spatialdist'}
        self.spatialdist = SpatialDist(sparam)
        sparam = {b:c for a, b, c in zip(section, param, values) if a == 'speeddist' if a == 'speeddist'}
        self.speeddist = SpeedDist(sparam)
        aparam = {b:c for a, b, c in zip(section, param, values) if a == 'angulardist' if a == 'angulardist'}
        self.angulardist = AngularDist(aparam, self.spatialdist)
        oparam = {b:c for a, b, c in zip(section, param, values) if a == 'options' if a == 'options'}
        self.options = Options(oparam, self.geometry.planet)

    def __str__(self):
        print(self.geometry)
        print(self.sticking_info)
        print(self.forces)
        print(self.spatialdist)
        print(self.speeddist)
        print(self.angulardist)
        print(self.options)
        return ''

    def findpackets(self):
        """
        Search the database for identical inputs
        """
        con = psycopg2.connect(host='localhost', database=(self.database))
        cur = con.cursor()
        dtor = np.pi / 180.0

        def isNone(x):
            try:
                q = x.value
            except:
                q = x

            if type(q) == str:
                if q is None:
                    return 'is NULL'
                return f"= '{q}'"
            if q is None:
                return 'is NULL'
            return f"= {q}"

        def inRange(field, x, delta):
            return f"ABS({field} - {x}) <= {delta / 2}"

        geometry = self.geometry
        objs = [obj.object for obj in geometry.objects]
        objs.sort()
        objs2 = ','.join(objs)
        phi = [p.value for p in geometry.phi]
        if not phi[0] == 0.0:
            raise AssertionError('There is a problem with phi')
        else:
            dtaa = (5.0 * u.deg).to(u.rad)
            taa = [geometry.taa - dtaa / 2.0, geometry.taa + dtaa / 2.0]
            taa = [taa[0].value, taa[1].value]
            if taa[0] < 0.0:
                taabit = '(taa>={} or taa<{})'.format(2 * np.pi + taa[0], taa[1])
            else:
                if taa[1] > 2 * np.pi:
                    taabit = '(taa>={} or taa<{})'.format(taa[0], taa[1] % (2 * np.pi))
                else:
                    taabit = inRange('taa', geometry.taa.value, dtaa.value)
            ptxt = [inRange('phi[{}]'.format(i + 1), p, 5.0 * dtor) for i, p in enumerate(phi)]
            ptxt2 = ' and '.join(ptxt)
            query = "SELECT geo_idnum FROM geometry\n                   WHERE planet='{}' and\n                         StartPoint='{}' and\n                         objects=ARRAY['{}']::SSObject[] and\n                         {} and\n                         {} and\n                         {} and\n                         {}".format(geometry.planet.object, geometry.startpoint, objs2, ptxt2, inRange('subsolarpt[0]', geometry.subsolarpoint[0].value, 5 * dtor), inRange('subsolarpt[1]', geometry.subsolarpoint[1].value, 5 * dtor), taabit)
            cur.execute(query)
            if cur.rowcount == 0:
                return ([], 0, 0)
            else:
                result = cur.fetchall()
                georesult = [r[0] for r in result]
                sticking_info = self.sticking_info
                geostr = [str(i) for i in georesult]
                geostr = '(' + ', '.join(geostr) + ')'
                if sticking_info.stickcoef == 1:
                    query = 'SELECT st_idnum FROM sticking_info\n                       WHERE stickcoef=1 and\n                             st_idnum in {}'.format(geostr)
                else:
                    query = 'SELECT st_idnum FROM sticking_info\n                       WHERE stickcoef={} and\n                             tsurf {} and\n                             stickfn {} and\n                             stick_mapfile {} and\n                             epsilon {} and\n                             n {} and\n                             tmin {} and\n                             emitfn {} and\n                             accom_mapfile {} and\n                             st_idnum in {}'.format(sticking_info.stickcoef, isNone(sticking_info.tsurf), isNone(sticking_info.stickfn), isNone(sticking_info.stick_mapfile), isNone(sticking_info.epsilon), isNone(sticking_info.n), isNone(sticking_info.tmin), isNone(sticking_info.emitfn), isNone(sticking_info.accom_mapfile), geostr)
            cur.execute(query)
            if cur.rowcount == 0:
                return ([], 0, 0)
            result = cur.fetchall()
            stickresult = [s[0] for s in result]
            stickstr = [str(i) for i in stickresult]
            stickstr = '(' + ', '.join(stickstr) + ')'
            forces = self.forces
            query = 'SELECT f_idnum FROM forces\n                   WHERE gravity=%s and\n                         radpres=%s and\n                         f_idnum in {}'.format(stickstr)
            cur.execute(query, (
             forces.gravity, forces.radpres))
            result = cur.fetchall()
            if cur.rowcount == 0:
                return ([], 0, 0)
                forceresult = [s[0] for s in result]
                spatialdist = self.spatialdist
                forcestr = [str(i) for i in forceresult]
                forcestr = '(' + ', '.join(forcestr) + ')'
                if spatialdist.longitude is None:
                    long0 = 'longitude[1] = 0.'
                    long1 = 'longitude[2] = 0.'
                else:
                    long0 = inRange('longitude[1]', spatialdist.longitude[0].value, 5 * dtor)
                    long1 = inRange('longitude[2]', spatialdist.longitude[1].value, 5 * dtor)
                if spatialdist.latitude is None:
                    lat0 = 'latitude[1] = 0.'
                    lat1 = 'latitude[2] = 0.'
                else:
                    lat0 = inRange('latitude[1]', spatialdist.latitude[0].value, 5 * dtor)
                    lat1 = inRange('latitude[2]', spatialdist.latitude[1].value, 5 * dtor)
                query = "SELECT spat_idnum FROM spatialdist\n                   WHERE type = '{}' and\n                         {} and\n                         use_map {} and\n                         mapfile {} and\n                         {} and\n                         {} and\n                         {} and\n                         {} and\n                         spat_idnum in {}".format(spatialdist.type, inRange('exobase', spatialdist.exobase, 0.05), isNone(spatialdist.use_map), isNone(spatialdist.mapfile), long0, long1, lat0, lat1, forcestr)
                cur.execute(query)
                if cur.rowcount == 0:
                    return ([], 0, 0)
                else:
                    result = cur.fetchall()
                    spatresult = [s[0] for s in result]
                    speeddist = self.speeddist
                    spatstr = [str(i) for i in spatresult]
                    spatstr = '(' + ', '.join(spatstr) + ')'
                    if speeddist.vprob is None:
                        vstr = 'vprob is NULL'
                    else:
                        vstr = inRange('vprob', speeddist.vprob.value, speeddist.vprob.value * 0.05)
                if speeddist.temperature is None:
                    Tstr = 'temperature is NULL'
            else:
                Tstr = inRange('temperature', speeddist.temperature.value, speeddist.temperature.value * 0.05)
        query = "SELECT spd_idnum FROM speeddist\n                   WHERE type = '{}' and\n                         {} and\n                         sigma {} and\n                         U {} and\n                         alpha {} and\n                         beta {} and\n                         {} and\n                         delv {} and\n                         spd_idnum in {}".format(speeddist.type, vstr, isNone(speeddist.sigma), isNone(speeddist.U), isNone(speeddist.alpha), isNone(speeddist.beta), Tstr, isNone(speeddist.delv), spatstr)
        cur.execute(query)
        if cur.rowcount == 0:
            return ([], 0, 0)
        result = cur.fetchall()
        speedresult = [s[0] for s in result]
        angdist = self.angulardist
        spdstr = [str(i) for i in speedresult]
        spdstr = '(' + ', '.join(spdstr) + ')'
        if angdist.azimuth is None:
            az0 = 'azimuth[1] is NULL'
            az1 = 'azimuth[2] is NULL'
        else:
            az0 = inRange('azimuth[1]', angdist.azimuth[0].value, 5 * dtor)
            az1 = inRange('azimuth[2]', angdist.azimuth[1].value, 5 * dtor)
        if angdist.altitude is None:
            alt0 = 'altitude[1] is NULL'
            alt1 = 'altitude[2] is NULL'
        else:
            alt0 = inRange('altitude[1]', angdist.altitude[0].value, 5 * dtor)
            alt1 = inRange('altitude[2]', angdist.altitude[1].value, 5 * dtor)
        n = isNone(angdist.n)
        query = "SELECT ang_idnum from angulardist\n                   WHERE type = '{}' and\n                         {} and {} and\n                         {} and {} and\n                         n {} and\n                         ang_idnum in {}".format(angdist.type, az0, az1, alt0, alt1, n, spdstr)
        cur.execute(query)
        if cur.rowcount == 0:
            return ([], 0, 0)
        result = cur.fetchall()
        angresult = [a[0] for a in result]
        options = self.options
        angstr = [str(i) for i in angresult]
        angstr = '(' + ', '.join(angstr) + ')'
        endtime = inRange('endtime', options.endtime.value, options.endtime.value * 0.05)
        outeredge = isNone(options.outeredge)
        nsteps = isNone(options.nsteps)
        res = isNone(options.resolution)
        query = "SELECT opt_idnum from options\n                   WHERE {} and\n                         resolution {} and\n                         at_once = {} and\n                         atom = '{}' and\n                         lifetime = {} and\n                         fullsystem = {} and\n                         outeredge {} and\n                         motion = {} and\n                         streamlines = {} and\n                         nsteps {} and\n                         opt_idnum in {}".format(endtime, res, options.at_once, options.atom, options.lifetime.value, options.fullsystem, outeredge, options.motion, options.streamlines, nsteps, angstr)
        cur.execute(query)
        if cur.rowcount == 0:
            return ([], 0, 0)
        result = cur.fetchall()
        finalresult = [str(a[0]) for a in result]
        finalresult = '(' + ', '.join(finalresult) + ')'
        query = 'SELECT filename, npackets, totalsource FROM outputfile\n                   WHERE idnum in {}'.format(finalresult)
        cur.execute(query)
        result = cur.fetchall()
        filenames = [r[0] for r in result]
        npackets = sum((r[1] for r in result))
        totalsource = sum((r[2] for r in result))
        return (
         filenames, npackets, totalsource)

    def run(self, npackets, overwrite=False, compress=True):
        modeldriver(self, npackets, overwrite, compress)

    def produce_image(self, format_, filenames=None):
        return ModelImage(self, format_, filenames=filenames)