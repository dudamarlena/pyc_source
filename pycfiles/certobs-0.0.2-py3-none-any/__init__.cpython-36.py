# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dmoral/.config/spyder-py3/certobs/certobs/__init__.py
# Compiled at: 2019-09-16 10:35:27
# Size of source mod 2**32: 34899 bytes


def pointingscan():
    import numpy as np
    from datetime import datetime
    import astropy.units as u
    from astropy.time import Time, TimeDelta, TimezoneInfo
    from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle, ITRS
    from astropy.coordinates import get_body, get_moon, solar_system_ephemeris
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')
    VIL1 = EarthLocation(lat=(Angle('40d26m33.233s')), lon=(Angle('-3d57m5.70s')), height=(655.15 * u.m))
    VIL2 = EarthLocation(lat=(Angle('40d26m44.2s')), lon=(Angle('-3d57m9.4s')), height=(664.8 * u.m))
    utc_plus_two_hours = TimezoneInfo(utc_offset=(2 * u.hour))
    f = open('certobs/CERT-Cat.dat', mode='r', encoding='iso-8859-1')
    wid = (10, 21, 17, 9)
    cat = np.genfromtxt(f, usecols=(0, 1, 2, 3), skip_header=3, skip_footer=12, dtype=(
     'U7', 'U18', float, float),
      delimiter=wid)
    cata = []
    for i in cat:
        cata.append(i)

    nowtime = Time((datetime.utcnow()), scale='utc')
    mode = input('Select the operation mode for the observation: transit/tracking/scanning/tipping-curve:\n')
    if mode == 'tracking' or mode == 'Tracking' or mode == 'TRACKING':
        otime = [input('Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n')]
        obs_time = Time(otime, format='iso', scale='utc')
        with solar_system_ephemeris.set('builtin'):
            sun = get_body('sun', obs_time, VIL2)
            moon = get_body('moon', obs_time, VIL2)
            mercury = get_body('mercury', obs_time, VIL2)
            venus = get_body('venus', obs_time, VIL2)
            mars = get_body('mars', obs_time, VIL2)
            jupiter = get_body('jupiter', obs_time, VIL2)
            saturn = get_body('saturn', obs_time, VIL2)
            uranus = get_body('uranus', obs_time, VIL2)
            neptune = get_body('neptune', obs_time, VIL2)
        solar = [
         moon, mercury, venus, mars, jupiter, saturn, uranus, neptune]
        ss = ['moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        source = input('Enter the name of the radio-source. Press ENTER if the source is neither in the catalogue nor a planet:\n')
        name = []
        ra = []
        dec = []
        for i, item in enumerate(ss):
            if source == item:
                name = ss[i]
                ra = solar[i].ra.degree[0]
                dec = solar[i].dec.degree[0]
            else:
                for a, atem in enumerate(cata):
                    if source == atem[0]:
                        name = cata[a][1]
                        ra = cata[a][2]
                        dec = cata[a][3]

        if name == []:
            name = 'unknown source'
            ra = float(input('Enter manually the desired right ascension: '))
            dec = float(input('Enter manually the desired declination: '))
        ra_sun = sun.ra.degree[0]
        dec_sun = sun.dec.degree[0]
        suncoords = SkyCoord(Angle(ra_sun, unit=(u.deg)), Angle(dec_sun, unit=(u.deg)), frame='icrs')
        ra_dif = abs(ra_sun - ra)
        dec_dif = abs(dec_sun - dec)
        if ra_dif < 1.5:
            if dec_dif < 1.5:
                print('WARNING: YOU FLEW TOO CLOSE TO THE SUN!!!!!!!!!!!!!!!!!!!!')
        obj = SkyCoord(Angle(ra, unit=(u.deg)), Angle(dec, unit=(u.deg)), frame='icrs')
        obj_itrs = obj.transform_to(ITRS(obstime=obs_time))
        local_ha = VIL2.lon - obj_itrs.spherical.lon
        local_ha.wrap_at((24 * u.hourangle), inplace=True)
        local_dec = obj_itrs.spherical.lat
        print('Local apparent HA, Dec={} {}'.format(local_ha.to_string(unit=(u.hourangle), sep=':'), local_dec.to_string(unit=(u.deg), sep=':', alwayssign=True)))
        duration = float(input('Enter the duration of the observation, in minutes: '))
        dt = float(input('Enter the time interval between two consecutive pointings (in seconds): '))
        pointings = duration * 60 / dt
        dt2 = TimeDelta(dt, format='sec')
        suc = np.linspace(0.0, pointings, pointings + 1)
        t = obs_time[0] + dt2 * suc
        pre = TimeDelta(300, format='sec')
        t0 = obs_time[0] - pre
        tf = obs_time[0] + pre
        completecoords = []
        time = []
        alti = []
        azi = []
        for i in suc.astype(int):
            new = obj.transform_to(AltAz(obstime=(t[i]), location=VIL2))
            alt_i = new.alt.degree
            az_i = new.az.degree
            alti.append(alt_i)
            azi.append(az_i)
            time.append(t[i].isot)
            cco = (time[i], alti[i], azi[i])
            completecoords.append(cco)

        for i in suc.astype(int):
            if completecoords[i][1] < 10:
                completecoords[i] = np.ma.masked
                print('Object non visible at the ' + str(i) + 'position of the observation')

        r = []
        elev = []
        n0 = 1.00031
        for i in suc.astype(int):
            p = np.deg2rad(alti[i] + 4.7 / (2.24 + alti[i]))
            r.append((n0 - 1) * 1 / np.tan(p))
            elev.append(alti[i] + r[i])

        t.format = 'isot'
        t0 = t0.isot
        tf = tf.isot
        tt = []
        for i in time:
            tt.append([i])

        elev = np.around(elev, decimals=4)
        azi = np.around(azi, decimals=4)
        final = np.column_stack((time, azi, elev))
        r0 = np.column_stack((t0, azi[0], elev[0]))
        rf = np.column_stack((tf, azi[(-1)], elev[(-1)]))
        final = np.vstack((r0, final, rf))
        final = np.hstack((final, np.zeros((final.shape[0], 10))))
        header = '<FILE>\n<HEADER>\nGENERATION DATE       : ' + str(nowtime) + '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : ' + str(source) + '\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : ' + str(obs_time[0]) + '\nANALYSIS PERIOD-END   : ' + str(obs_time[(-1)]) + '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n' + str(obs_time[0]) + '  ' + str(obs_time[(-1)]) + '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
        obs_time.out_subfmt = 'date'
        np.savetxt(('track-' + str(name) + str(obs_time[0]) + '.txt'), final, fmt='%s', delimiter=' ', header=header, footer='</PASS>\n</FILE>', comments='')
        obs_time.out_subfmt = 'date_hms'
    else:
        if mode == 'transit' or mode == 'Transit' or mode == 'TRANSIT':
            otime = [input('Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n')]
            obs_time = Time(otime, format='iso', scale='utc')
            with solar_system_ephemeris.set('builtin'):
                moon = get_body('moon', obs_time, VIL2)
                mercury = get_body('mercury', obs_time, VIL2)
                venus = get_body('venus', obs_time, VIL2)
                mars = get_body('mars', obs_time, VIL2)
                jupiter = get_body('jupiter', obs_time, VIL2)
                saturn = get_body('saturn', obs_time, VIL2)
                uranus = get_body('uranus', obs_time, VIL2)
                neptune = get_body('neptune', obs_time, VIL2)
            solar = [
             moon, mercury, venus, mars, jupiter, saturn, uranus, neptune]
            ss = ['moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
            source = input('Enter the name of the radio-source. Press ENTER if the source is neither in the catalogue nor a planet:\n')
            name = []
            ra = []
            dec = []
            for i, item in enumerate(ss):
                if source == item:
                    name = ss[i]
                    ra = solar[i].ra.degree[0]
                    dec = solar[i].dec.degree[0]
                else:
                    for a, atem in enumerate(cata):
                        if source == atem[0]:
                            name = cata[a][1]
                            ra = cata[a][2]
                            dec = cata[a][3]

            if name == []:
                name = 'unknown source'
                ra = float(input('Enter manually the desired right ascension: '))
                dec = float(input('Enter manually the desired declination: '))
            obj = SkyCoord(Angle(ra, unit=(u.deg)), Angle(dec, unit=(u.deg)), frame='icrs')
            obj_itrs = obj.transform_to(ITRS(obstime=obs_time))
            local_ha = VIL2.lon - obj_itrs.spherical.lon
            local_ha.wrap_at((24 * u.hourangle), inplace=True)
            local_dec = obj_itrs.spherical.lat
            print('Local apparent HA, Dec={} {}'.format(local_ha.to_string(unit=(u.hourangle), sep=':'), local_dec.to_string(unit=(u.deg), sep=':', alwayssign=True)))
            duration = float(input('Enter the duration of the transit, in minutes: '))
            t = obs_time[0]
            pre = TimeDelta(300, format='sec')
            dur = TimeDelta((duration * 60), format='sec')
            t0 = t - pre
            obs_time_end = t + dur
            tf = t + dur + pre
            completecoords = []
            time = []
            new = obj.transform_to(AltAz(obstime=t, location=VIL2))
            alti = new.alt.degree
            azi = new.az.degree
            completecoords = (t.isot, azi, alti)
            if alti < 10:
                completecoords = np.ma.masked
                print('Too low pointing')
            r = []
            elev = []
            n0 = 1.00031
            p = np.deg2rad(alti + 4.7 / (2.24 + alti))
            r = (n0 - 1) * 1 / np.tan(p)
            elev = [alti + r]
            max_elev = 85
            if max(elev) > max_elev:
                print('DANGER: TOO HIGH ELEVATION. THERE MIGHT BE TRACKING ISSUES')
            t.format = 'isot'
            t0 = t0.isot
            tf = tf.isot
            tt = []
            for i in time:
                tt.append([i])

            elev = np.around(elev, decimals=4)
            azi = np.around(azi, decimals=4)
            r0 = np.column_stack((t0, azi, elev))
            rf = np.column_stack((tf, azi, elev))
            final = np.vstack((r0, rf))
            final = np.hstack((final, np.zeros((final.shape[0], 10))))
            header = '<FILE>\n<HEADER>\nGENERATION DATE       : ' + str(nowtime) + '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : ' + str(source) + '\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : ' + str(obs_time[0]) + '\nANALYSIS PERIOD-END   : ' + str(obs_time_end) + '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n' + str(obs_time[0]) + '  ' + str(obs_time_end) + '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
            obs_time.out_subfmt = 'date'
            np.savetxt(('transit-' + str(name) + str(obs_time[0]) + '.txt'), final, fmt='%s', delimiter=' ', header=header, footer='</PASS>\n</FILE>', comments='')
            obs_time.out_subfmt = 'date_hms'
        else:
            if mode == 'tipping curve' or mode == 'tipping' or mode == 'tip' or mode == 'TIPPING' or mode == 'TIP' or mode == 'Tipping':
                otime = [input('Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n')]
                obs_time = Time(otime, format='iso', scale='utc')
                dt = 2
                dt2 = TimeDelta(dt, format='sec')
                pre = TimeDelta(300, format='sec')
                t0 = obs_time[0] - pre
                suc = np.linspace(0, 90, 91)
                t = list()
                t.append(obs_time[0])
                for i, tex in enumerate(suc):
                    if i > 0:
                        t.append(t[(i - 1)] + dt2)

                azimuth = float(input('Enter the azimuth for the tipping curve: '))
                elev = []
                azi = []
                for i, tex in enumerate(suc):
                    elev.append(tex)
                    azi.append(azimuth)

                completecoords = []
                for i, tex in enumerate(suc):
                    cco = (
                     t[i].isot, elev[i], azi[i])
                    completecoords.append(cco)

                for i, tex in enumerate(t):
                    t[i].format = 'isot'

                t0 = t0.isot
                duration = t[(-1)] - t[0]
                final = []
                final = np.column_stack((t, azi, elev))
                r0 = (t0, azi[0], elev[0])
                final = np.vstack((r0, final))
                final = np.hstack((final, np.zeros((final.shape[0], 10))))
                header = '<FILE>\n<HEADER>\nGENERATION DATE       : ' + str(nowtime) + '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : TIPPING CURVE\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : ' + str(obs_time[0]) + '\nANALYSIS PERIOD-END   : ' + str(obs_time[(-1)]) + '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n' + str(obs_time[0]) + '  ' + str(obs_time[(-1)]) + '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
                obs_time.out_subfmt = 'date'
                np.savetxt(('tip-' + str(nowtime) + '.txt'), final, fmt='%s', delimiter=' ', header=header, footer='</PASS>\n</FILE>', comments='')
                obs_time.out_subfmt = 'date_hms'
            else:
                if mode == 'scanning' or mode == 'Scanning' or mode == 'SCANNING' or mode == 'SCAN' or mode == 'scan':
                    otime = [input('Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n')]
                    obs_time = Time(otime, format='iso', scale='utc')
                    with solar_system_ephemeris.set('builtin'):
                        sun = get_body('sun', obs_time, VIL2)
                        moon = get_body('moon', obs_time, VIL2)
                        mercury = get_body('mercury', obs_time, VIL2)
                        venus = get_body('venus', obs_time, VIL2)
                        mars = get_body('mars', obs_time, VIL2)
                        jupiter = get_body('jupiter', obs_time, VIL2)
                        saturn = get_body('saturn', obs_time, VIL2)
                        uranus = get_body('uranus', obs_time, VIL2)
                        neptune = get_body('neptune', obs_time, VIL2)
                    ra1 = float(input('Enter manually the right ascension for the first observing point: '))
                    dec1 = float(input('Enter manually the declination for the first observing point: '))
                    ra2 = float(input('Enter manually the right ascension for the last observing point: '))
                    dec2 = float(input('Enter manually the declination for the last observing point: '))
                    dra = 0.308
                    ddec = 0.308
                    if ra1 >= ra2:
                        ra1 = ra1 + dra
                        ra2 = ra2 - dra
                    else:
                        ra1 = ra1 - dra
                        ra2 = ra2 + dra
                    if dec1 >= dec2:
                        dec1 = dec1 + ddec
                        dec2 = dec2 - ddec
                    else:
                        dec1 = dec1 - ddec
                        dec2 = dec2 + ddec
                    deltara = abs(ra2 - ra1)
                    nra = int(np.around((deltara / dra + 1), decimals=0))
                    deltadec = abs(dec2 - dec1)
                    ndec = int(np.around((deltadec / ddec + 1), decimals=0))
                    ra_sun = sun.ra.degree[0]
                    dec_sun = sun.dec.degree[0]
                    suncoords = SkyCoord(Angle(ra_sun, unit=(u.deg)), Angle(dec_sun, unit=(u.deg)), frame='icrs')
                    ra_dif = abs(ra_sun - ra1)
                    dec_dif = abs(dec_sun - dec1)
                    if ra_dif < 1.5:
                        if dec_dif < 1.5:
                            print('WARNING: YOU FLEW TOO CLOSE TO THE SUN!!!!!!!!!!!!!!!!!!!!')
                    nnra = np.linspace(0, nra - 1, nra)
                    nndec = np.linspace(0, ndec - 1, ndec)
                    ra = []
                    dec = []
                    for i in nnra:
                        ra.append(ra1 + dra * i)

                    for i in nndec:
                        dec.append(dec1 + ddec * i)

                    decr = dec[::-1]
                    ccc = np.zeros((nra, ndec), dtype=object)
                    for i in nnra.astype(int):
                        for j in nndec.astype(int):
                            if i % 2 == 0:
                                ccc[i][j] = SkyCoord(Angle((ra[i]), unit=(u.deg)), Angle((dec[j]), unit=(u.deg)), frame='icrs')
                            else:
                                ccc[i][j] = SkyCoord(Angle((ra[i]), unit=(u.deg)), Angle((decr[j]), unit=(u.deg)), frame='icrs')

                    dt = 2
                    dt2 = TimeDelta(dt, format='sec')
                    pointings = nra * ndec
                    pre = TimeDelta(300, format='sec')
                    t0 = obs_time[0] - pre
                    suc = np.linspace(0.0, pointings, pointings + 1)
                    t = list()
                    t.append(t0)
                    t.append(obs_time[0])
                    dt3 = np.sqrt((deltara / 3) ** 2 + (deltadec / 3) ** 2)
                    dt3 = TimeDelta(dt3, format='sec')
                    for i, tex in enumerate(suc):
                        if i > 1:
                            if (i - 1) % nra != 0:
                                t.append(t[(i - 1)] + dt2)
                            else:
                                t.append(t[(i - 1)] + dt3)

                    completecoords = []
                    time = []
                    ccc_f = ccc.flatten()
                    ccc_n = np.zeros((np.shape(ccc_f)), dtype=object)
                    for i, tex in enumerate(ccc_f):
                        ccc_n[i] = ccc_f[i].transform_to(AltAz(obstime=(t[i]), location=VIL2))
                        cco = (
                         t[i].isot, ccc_n[i].alt.degree, ccc_n[i].az.degree)
                        ccl = list(cco)
                        completecoords.append(ccl)

                    completecoords[0][1] = completecoords[1][1]
                    completecoords[0][2] = completecoords[1][2]
                    figure, (ax, ay) = plt.subplots(2, 1, figsize=(18, 18))
                    if pointings > 500:
                        for i, tex in enumerate(ccc_f):
                            if i % 100 == 0:
                                ax.annotate(i, (ccc_f[i].ra.deg, ccc_f[i].dec.deg))
                                ax.set_xlabel('Right Ascension (deg)')
                                ax.set_ylabel('Declination (deg)')
                                ax.scatter((ccc_f[i].ra.deg), (ccc_f[i].dec.deg), s=12000, alpha=0.35)
                                ay.annotate(i, (ccc_n[i].az.deg, ccc_n[i].alt.deg))
                                ay.set_xlabel('Azimuth (deg)')
                                ay.set_ylabel('Elevation (deg)')
                                ay.scatter((ccc_n[i].az.deg), (ccc_n[i].alt.deg), s=12000, alpha=0.35)

                    else:
                        for i, tex in enumerate(ccc_f):
                            ax.annotate(i, (ccc_f[i].ra.deg, ccc_f[i].dec.deg))
                            ax.set_xlabel('Right Ascension (deg)')
                            ax.set_ylabel('Declination (deg)')
                            ax.scatter((ccc_f[i].ra.deg), (ccc_f[i].dec.deg), s=12000, alpha=0.35)
                            ay.annotate(i, (ccc_n[i].az.deg, ccc_n[i].alt.deg))
                            ay.set_xlabel('Azimuth (deg)')
                            ay.set_ylabel('Elevation (deg)')
                            ay.scatter((ccc_n[i].az.deg), (ccc_n[i].alt.deg), s=12000, alpha=0.35)

                    for i, tex in enumerate(ccc_f):
                        if completecoords[i][1] < 10:
                            completecoords[i] = np.ma.masked
                            print('Too low scanning position')

                    r = []
                    elev = []
                    azi = []
                    n0 = 1.00031
                    for i, tex in enumerate(ccc_f):
                        p = np.deg2rad(ccc_n[i].alt.deg + 4.7 / (2.24 + ccc_n[i].alt.deg))
                        r.append((n0 - 1) * 1 / np.tan(p))
                        elev.append(ccc_n[i].alt.deg + r[i])
                        azi.append(ccc_n[i].az.deg)

                    azi.insert(0, azi[0])
                    elev.insert(0, elev[0])
                    for i, tex in enumerate(t):
                        t[i].format = 'isot'

                    duration = t[(-1)] - t[0]
                    elev = np.around(elev, decimals=4)
                    azi = np.around(azi, decimals=4)
                    final = np.column_stack((t, azi, elev))
                    final = np.hstack((final, np.zeros((final.shape[0], 10))))
                    header = '<FILE>\n<HEADER>\nGENERATION DATE       : ' + str(nowtime) + '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : SCANNING\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : ' + str(obs_time[0]) + '\nANALYSIS PERIOD-END   : ' + str(obs_time[(-1)]) + '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n' + str(obs_time[0]) + '  ' + str(obs_time[(-1)]) + '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
                    obs_time.out_subfmt = 'date'
                    np.savetxt(('scan-' + str(nowtime) + '.txt'), final, fmt='%s', delimiter=' ', header=header, footer='</PASS>\n</FILE>', comments='')
                    inter = '\n<PASS>\n' + str(nowtime) + '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
                    obs_time.out_subfmt = 'date_hms'
                else:
                    raise ValueError('Invalid observing mode')