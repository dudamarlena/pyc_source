# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/source_distribution.py
# Compiled at: 2019-02-21 11:53:20
# Size of source mod 2**32: 12213 bytes
import os, os.path, numpy as np, pickle
import astropy.units as u
import astropy.constants as const
import mathMB, physicsMB

def gaussiandist(velocity, vprob, sigma):
    f_v = np.exp(-(velocity - vprob) ** 2 / 2.0 / sigma ** 2)
    f_v /= np.max(f_v)
    return f_v


def sputdist(velocity, U, alpha, beta, atom):
    matom = physicsMB.atomicmass(atom)
    v_b = np.sqrt(2 * U / matom)
    v_b = v_b.to(u.km / u.s)
    f_v = velocity ** (2 * beta + 1) / (velocity ** 2 + v_b ** 2) ** alpha
    f_v /= np.max(f_v)
    return f_v


def MaxwellianDist(velocity, temperature, atom):
    vth2 = 2 * temperature * const.k_B / physicsMB.atomicmass(atom)
    vth2 = vth2.to(u.km ** 2 / u.s ** 2)
    f_v = velocity ** 3 * np.exp(-velocity ** 2 / vth2)
    f_v /= np.max(f_v)
    return f_v


def xyz_from_lonlat(lon, lat, isplan, unit, exobase):
    if isplan:
        x0 = exobase * np.sin(lon) * np.cos(lat)
        y0 = -exobase * np.cos(lon) * np.cos(lat)
        z0 = exobase * np.sin(lat)
    else:
        x0 = -exobase * np.sin(lon) * np.cos(lat)
        y0 = -exobase * np.cos(lon) * np.cos(lat)
        z0 = exobase * np.sin(lat)
    X0 = np.array([x0, y0, z0]) * unit
    assert np.all(np.isfinite(X0)), 'Non-Finite values of X0'
    return X0


def surface_distribution(inputs, npack, unit):
    """
    Distribution packets on a sphere with radius r = SpatialDist.exobase

    Returns (x0, y0, z0, lon0, lat0)
    for satellites, assumes satellite is at phi=0

    Testing notes:
    1) Basic function with lon = [0,360], lat = [-90,90]
    2) Spatial map given
    3) Longitude, latitude range
    3) Longitude, latitude range, lon1 > lon0
    """
    SpatialDist = inputs.spatialdist
    if SpatialDist.use_map:
        mapfile = open(SpatialDist.mapfile, 'rb')
        sourcemap = pickle.load(mapfile)
        mapfile.close()
        lon, lat = mathMB.random_deviates_2d(sourcemap['map'], sourcemap['longitude'], np.sin(sourcemap['latitude']), npack)
        lat = np.arcsin(lat)
    else:
        lat0 = SpatialDist.latitude
        if lat0[0] == lat0[1]:
            lat = np.zeros(npack) + lat0[0]
        else:
            ll = (
             np.sin(lat0[0]), np.sin(lat0[1]))
            sinlat = ll[0] + (ll[1] - ll[0]) * np.random.rand(npack)
            lat = np.arcsin(sinlat)
        lon0 = SpatialDist.longitude
        if lon0[0] > lon0[1]:
            lon0 = [
             lon0[0], lon0[1] + 2 * np.pi * u.rad]
        lon = (lon0[0] + (lon0[1] - lon0[0]) * np.random.rand(npack)) % (2 * np.pi * u.rad)
    X0 = xyz_from_lonlat(lon, lat, inputs.geometry.planet.type == 'Planet', unit, SpatialDist.exobase)
    return (X0, lon, lat)


def surface_spot(inputs, npackets, unit):
    """Create a spot that drops off exponentially from (lon0, lat0)"""
    lon0, sigma = inputs.spatialdist.longitude
    lat0, _ = inputs.spatialdist.latitude
    spot0 = (
     np.sin(lon0) * np.cos(lat0),
     -np.cos(lon0) * np.cos(lat0),
     np.sin(lat0))
    longitude = np.linspace(0, 2 * np.pi, 361) * u.rad
    latitude = np.linspace(-np.pi / 2, np.pi / 2, 181) * u.rad
    ptsx = np.outer(np.sin(longitude), np.cos(latitude))
    ptsy = -np.outer(np.cos(longitude), np.cos(latitude))
    ptsz = -np.outer(np.ones_like(longitude), np.sin(latitude))
    cosphi = ptsx * spot0[0] + ptsy * spot0[1] + ptsz * spot0[2]
    cosphi[cosphi > 1] = 1
    cosphi[cosphi < -1] = -1
    phi = np.arccos(cosphi)
    sourcemap = np.exp(-phi / sigma)
    lon, lat = mathMB.random_deviates_2d(sourcemap, longitude, np.sin(latitude), npackets)
    lat = np.arcsin(lat)
    X0 = xyz_from_lonlat(lon, lat, inputs.geometry.planet.type == 'Planet', unit, inputs.spatialdist.exobase)
    return (
     X0, lon, lat)


def idlversion(inputs, unit):
    from scipy.io import readsav
    path, _ = os.path.split(__file__)
    rfile = os.path.join(path, 'data', 'modeloutput_search_routines.sav')
    vfile = os.path.join(path, 'data', 'modeloutput_search_variables.sav')
    with open('make_file_list.pro', 'w') as (f):
        filelistfile = 'filelist.dat'
        f.write(f"\npro make_file_list\n\nrestore, '{vfile}'\ndefsysv, '!model', modelvar\nfilelist = modeloutput_search('{inputs.spatialdist.mapfile}')\nopenw, 1, '{filelistfile}'\nfor i=0,n_elements(filelist)-1 do printf, 1, filelist[i]\nclose, 1\n\nend")
    cmd = f"""/Applications/exelis/idl/bin/idl -e "restore, \'{rfile}\' & make_file_list" """
    os.system(cmd)
    x0 = None
    idloutputfiles = open('filelist.dat', 'r').readlines()
    print(f"{len(idloutputfiles)} IDL sav files found")
    for savfile in idloutputfiles:
        idl = readsav(savfile.strip())
        idlout = idl['output']
        index = sorted(list(set(idlout['index'][0])))
        x_ = [idlout['x0'][0][(idlout['index'][0] == i)][0] for i in index]
        y_ = [idlout['y0'][0][(idlout['index'][0] == i)][0] for i in index]
        z_ = [idlout['z0'][0][(idlout['index'][0] == i)][0] for i in index]
        vx_ = [idlout['vx0'][0][(idlout['index'][0] == i)][0] for i in index]
        vy_ = [idlout['vy0'][0][(idlout['index'][0] == i)][0] for i in index]
        vz_ = [idlout['vz0'][0][(idlout['index'][0] == i)][0] for i in index]
        f_ = np.ones_like(x_)
        if x0 is None:
            x0 = np.array(x_)
            y0 = np.array(y_)
            z0 = np.array(z_)
            vx0 = np.array(vx_)
            vy0 = np.array(vy_)
            vz0 = np.array(vz_)
            f = np.array(f_)
        else:
            x0 = np.append(x0, np.array(x_))
            y0 = np.append(y0, np.array(y_))
            z0 = np.append(z0, np.array(z_))
            vx0 = np.append(vx0, np.array(vx_))
            vy0 = np.append(vy0, np.array(vy_))
            vz0 = np.append(vz0, np.array(vz_))
            f = np.append(f, np.array(f_))

    X = [
     x0, y0, z0] * unit
    V = [vx0, vy0, vz0] * unit / u.s
    F = f
    return (
     X, V, F)


def speed_distribution--- This code section failed: ---

 L. 208         0  LOAD_FAST                'inputs'
                2  LOAD_ATTR                speeddist
                4  STORE_FAST               'SpeedDist'

 L. 210         6  LOAD_FAST                'inputs'
                8  LOAD_ATTR                spatialdist
               10  LOAD_ATTR                type
               12  LOAD_STR                 'idlversion'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 211        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 215        22  LOAD_FAST                'SpeedDist'
               24  LOAD_ATTR                type
               26  LOAD_METHOD              lower
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  LOAD_STR                 'gaussian'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE   114  'to 114'

 L. 216        36  LOAD_FAST                'SpeedDist'
               38  LOAD_ATTR                sigma
               40  LOAD_CONST               0.0
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    76  'to 76'

 L. 217        46  LOAD_GLOBAL              np
               48  LOAD_METHOD              zeros
               50  LOAD_FAST                'npackets'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  LOAD_GLOBAL              u
               56  LOAD_ATTR                km
               58  BINARY_MULTIPLY  
               60  LOAD_GLOBAL              u
               62  LOAD_ATTR                s
               64  BINARY_TRUE_DIVIDE
               66  LOAD_FAST                'SpeedDist'
               68  LOAD_ATTR                vprob
               70  BINARY_ADD       
               72  STORE_FAST               'v0'
               74  JUMP_FORWARD        436  'to 436'
             76_0  COME_FROM            44  '44'

 L. 219        76  LOAD_GLOBAL              mathMB
               78  LOAD_METHOD              random_gaussian
               80  LOAD_FAST                'SpeedDist'
               82  LOAD_ATTR                vprob
               84  LOAD_ATTR                value

 L. 220        86  LOAD_FAST                'SpeedDist'
               88  LOAD_ATTR                sigma
               90  LOAD_ATTR                value

 L. 221        92  LOAD_FAST                'npackets'
               94  CALL_METHOD_3         3  '3 positional arguments'
               96  STORE_FAST               'v0'

 L. 222        98  LOAD_FAST                'v0'
              100  LOAD_FAST                'SpeedDist'
              102  LOAD_ATTR                vprob
              104  LOAD_ATTR                unit
              106  INPLACE_MULTIPLY 
              108  STORE_FAST               'v0'
          110_112  JUMP_FORWARD        436  'to 436'
            114_0  COME_FROM            34  '34'

 L. 223       114  LOAD_FAST                'SpeedDist'
              116  LOAD_ATTR                type
              118  LOAD_STR                 'sputtering'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   202  'to 202'

 L. 224       124  LOAD_GLOBAL              np
              126  LOAD_METHOD              linspace
              128  LOAD_CONST               0.1
              130  LOAD_CONST               50
              132  LOAD_CONST               5000
              134  CALL_METHOD_3         3  '3 positional arguments'
              136  LOAD_GLOBAL              u
              138  LOAD_ATTR                km
              140  BINARY_MULTIPLY  
              142  LOAD_GLOBAL              u
              144  LOAD_ATTR                s
              146  BINARY_TRUE_DIVIDE
              148  STORE_FAST               'velocity'

 L. 225       150  LOAD_GLOBAL              sputdist
              152  LOAD_FAST                'velocity'
              154  LOAD_FAST                'SpeedDist'
              156  LOAD_ATTR                U
              158  LOAD_FAST                'SpeedDist'
              160  LOAD_ATTR                alpha

 L. 226       162  LOAD_FAST                'SpeedDist'
              164  LOAD_ATTR                beta
              166  LOAD_FAST                'inputs'
              168  LOAD_ATTR                options
              170  LOAD_ATTR                atom
              172  CALL_FUNCTION_5       5  '5 positional arguments'
              174  STORE_FAST               'f_v'

 L. 228       176  LOAD_GLOBAL              mathMB
              178  LOAD_METHOD              random_deviates_1d
              180  LOAD_FAST                'velocity'
              182  LOAD_ATTR                value
              184  LOAD_FAST                'f_v'
              186  LOAD_ATTR                value
              188  LOAD_FAST                'npackets'
              190  CALL_METHOD_3         3  '3 positional arguments'

 L. 229       192  LOAD_FAST                'velocity'
              194  LOAD_ATTR                unit
              196  BINARY_MULTIPLY  
              198  STORE_FAST               'v0'
              200  JUMP_FORWARD        436  'to 436'
            202_0  COME_FROM           122  '122'

 L. 230       202  LOAD_FAST                'SpeedDist'
              204  LOAD_ATTR                type
              206  LOAD_STR                 'maxwellian'
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   374  'to 374'

 L. 231       214  LOAD_FAST                'SpeedDist'
              216  LOAD_ATTR                temperature
              218  LOAD_CONST               0
              220  COMPARE_OP               !=
          222_224  POP_JUMP_IF_FALSE   358  'to 358'

 L. 233       226  LOAD_GLOBAL              physicsMB
              228  LOAD_METHOD              atomicmass
              230  LOAD_FAST                'inputs'
              232  LOAD_ATTR                options
              234  LOAD_ATTR                atom
              236  CALL_METHOD_1         1  '1 positional argument'
              238  STORE_FAST               'amass'

 L. 234       240  LOAD_GLOBAL              np
              242  LOAD_METHOD              sqrt
              244  LOAD_CONST               2
              246  LOAD_FAST                'SpeedDist'
              248  LOAD_ATTR                temperature
              250  BINARY_MULTIPLY  
              252  LOAD_GLOBAL              const
              254  LOAD_ATTR                k_B
              256  BINARY_MULTIPLY  
              258  LOAD_FAST                'amass'
              260  BINARY_TRUE_DIVIDE
              262  CALL_METHOD_1         1  '1 positional argument'
              264  STORE_FAST               'v_th'

 L. 235       266  LOAD_FAST                'v_th'
              268  LOAD_METHOD              to
              270  LOAD_GLOBAL              u
              272  LOAD_ATTR                km
              274  LOAD_GLOBAL              u
              276  LOAD_ATTR                s
              278  BINARY_TRUE_DIVIDE
              280  CALL_METHOD_1         1  '1 positional argument'
              282  STORE_FAST               'v_th'

 L. 236       284  LOAD_GLOBAL              np
              286  LOAD_METHOD              linspace
              288  LOAD_CONST               0.1
              290  LOAD_GLOBAL              u
              292  LOAD_ATTR                km
              294  BINARY_MULTIPLY  
              296  LOAD_GLOBAL              u
              298  LOAD_ATTR                s
              300  BINARY_TRUE_DIVIDE
              302  LOAD_FAST                'v_th'
              304  LOAD_CONST               5
              306  BINARY_MULTIPLY  
              308  LOAD_CONST               5000
              310  CALL_METHOD_3         3  '3 positional arguments'
              312  STORE_FAST               'velocity'

 L. 237       314  LOAD_GLOBAL              MaxwellianDist
              316  LOAD_FAST                'velocity'
              318  LOAD_FAST                'SpeedDist'
              320  LOAD_ATTR                temperature

 L. 238       322  LOAD_FAST                'inputs'
              324  LOAD_ATTR                options
              326  LOAD_ATTR                atom
              328  CALL_FUNCTION_3       3  '3 positional arguments'
              330  STORE_FAST               'f_v'

 L. 239       332  LOAD_GLOBAL              mathMB
              334  LOAD_METHOD              random_deviates_1d
              336  LOAD_FAST                'velocity'
              338  LOAD_ATTR                value
              340  LOAD_FAST                'f_v'
              342  LOAD_ATTR                value
              344  LOAD_FAST                'npackets'
              346  CALL_METHOD_3         3  '3 positional arguments'

 L. 240       348  LOAD_FAST                'velocity'
              350  LOAD_ATTR                unit
              352  BINARY_MULTIPLY  
              354  STORE_FAST               'v0'
              356  JUMP_FORWARD        372  'to 372'
            358_0  COME_FROM           222  '222'

 L. 244       358  LOAD_CONST               0
          360_362  POP_JUMP_IF_TRUE    436  'to 436'
              364  LOAD_ASSERT              AssertionError
              366  LOAD_STR                 'Not implemented yet'
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  RAISE_VARARGS_1       1  'exception instance'
            372_0  COME_FROM           356  '356'
              372  JUMP_FORWARD        436  'to 436'
            374_0  COME_FROM           210  '210'

 L. 245       374  LOAD_FAST                'SpeedDist'
              376  LOAD_ATTR                type
              378  LOAD_STR                 'flat'
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   422  'to 422'

 L. 247       386  LOAD_GLOBAL              np
              388  LOAD_ATTR                random
              390  LOAD_METHOD              rand
              392  LOAD_FAST                'npackets'
              394  CALL_METHOD_1         1  '1 positional argument'
              396  LOAD_CONST               2
            398_0  COME_FROM            74  '74'
              398  BINARY_MULTIPLY  
              400  LOAD_FAST                'SpeedDist'
              402  LOAD_ATTR                delv
              404  BINARY_MULTIPLY  
              406  LOAD_FAST                'SpeedDist'
              408  LOAD_ATTR                vprob
              410  BINARY_ADD       
              412  LOAD_FAST                'SpeedDist'
              414  LOAD_ATTR                delv
              416  BINARY_SUBTRACT  
              418  STORE_FAST               'v0'
              420  JUMP_FORWARD        436  'to 436'
            422_0  COME_FROM           382  '382'

 L. 250       422  LOAD_CONST               0
          424_426  POP_JUMP_IF_TRUE    436  'to 436'
              428  LOAD_ASSERT              AssertionError
              430  LOAD_STR                 'Distribtuion does not exist'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  RAISE_VARARGS_1       1  'exception instance'
            436_0  COME_FROM           424  '424'
            436_1  COME_FROM           420  '420'
            436_2  COME_FROM           372  '372'
            436_3  COME_FROM           360  '360'
            436_4  COME_FROM           200  '200'
            436_5  COME_FROM           110  '110'

 L. 252       436  LOAD_GLOBAL              np
              438  LOAD_METHOD              all
              440  LOAD_GLOBAL              np
              442  LOAD_METHOD              isfinite
              444  LOAD_FAST                'v0'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  CALL_METHOD_1         1  '1 positional argument'
          450_452  POP_JUMP_IF_TRUE    462  'to 462'
              454  LOAD_ASSERT              AssertionError
              456  LOAD_STR                 'Infinite values for v0'
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  RAISE_VARARGS_1       1  'exception instance'
            462_0  COME_FROM           450  '450'

 L. 254       462  LOAD_FAST                'v0'
              464  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 398_0


def angular_distribution(inputs, X0, vv):
    if inputs.spatialdist.type == 'idlversion':
        return
    npackets = len(vv)
    AngularDist = inputs.angulardist
    if AngularDist.type == 'none':
        pass
    elif AngularDist.type == 'radial':
        alt = np.zeros(npackets) + np.pi / 2.0
        az = np.zeros(npackets)
    else:
        if AngularDist.type == 'isotropic':
            alt0 = AngularDist.altitude
            aa = (np.sin(alt0[0]), np.sin(alt0[1]))
            sinalt = np.random.rand(npackets) * (aa[1] - aa[0]) + aa[0]
            alt = np.arcsin(sinalt)
            az0, az1 = AngularDist.azimuth
            m = (az0, az1) if az0 < az1 else (az1, az0 + 2 * np.pi)
            az = (m[0] + (m[1] - m[0]) * np.random.rand(npackets)) % (2 * np.pi * u.rad)
        else:
            if AngularDist.type == 'costheta':
                alt0 = AngularDist.altitude
                aa = (np.sin(alt0[0]), np.sin(alt0[1]))
                sinalt = np.random.rand(npackets) * (aa[1] - aa[0]) + aa[0]
                alt = np.arcsin(sinalt)
                az0, az1 = AngularDist.azimuth
                m = (az0, az1) if az0 < az1 else (az1, az0 + 2 * np.pi)
                az = (m[0] + (m[1] - m[0]) * np.random.rand(npackets)) % (2 * np.pi * u.rad)
            else:
                assert 0, 'Angular Distribution not defined.'
                v_rad = np.sin(alt)
                v_tan0 = np.cos(alt) * np.cos(az)
                v_tan1 = np.cos(alt) * np.sin(az)
                rr = np.sqrt(X0[0, :] ** 2 + X0[1, :] ** 2 + X0[2, :] ** 2)
                x0, y0, z0 = X0[0, :] / rr, X0[1, :] / rr, X0[2, :] / rr
                rad = np.array([x0, y0, z0])
                east = np.array([y0, -x0, np.zeros_like(z0)])
                north = np.array([-z0 * x0, -z0 * y0, x0 ** 2 + y0 ** 2])
                east /= np.linalg.norm(east, axis=0)
                north /= np.linalg.norm(north, axis=0)
                v0 = v_tan0 * north + v_tan1 * east + v_rad * rad
                vx0 = v0[0, :] * vv
                vy0 = v0[1, :] * vv
                vz0 = v0[2, :] * vv
                V0 = np.array([vx0, vy0, vz0])
                return V0


if __name__ == '__main__':
    velocity = np.linspace(0.1, 50, 5000) * u.km / u.s
    f_v = gaussiandist(velocity, 2 * u.km / u.s, 0.5 * u.km / u.s)
    plt.plot(velocity, f_v)
    plt.minorticks_on()
    plt.ylim((1e-10, 10))
    plt.xlim((0, 20))
    plt.yscale('log')
    plt.xlabel('Velocity (km s$^{-1}$)')
    plt.ylabel('Relative f$_v$')
    plt.title('Speed Distribution Function')
    plt.show()