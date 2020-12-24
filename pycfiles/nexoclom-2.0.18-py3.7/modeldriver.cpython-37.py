# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/modeldriver.py
# Compiled at: 2019-04-02 14:09:10
# Size of source mod 2**32: 5594 bytes
import os, numpy as np
from astropy.time import Time
import astropy.units as u
from .Output import Output

def delete_files(filelist, database):
    """ Delete output files and remove them from the database """
    import psycopg2
    with psycopg2.connect(host='localhost', database=database) as (con):
        con.autocommit = True
        cur = con.cursor()
        for f in filelist:
            print(f)
            if os.path.exists(f):
                os.remove(f)
            cur.execute('SELECT idnum FROM outputfile\n                           WHERE filename = %s', (f,))
            idnum = cur.fetchone()[0]
            cur.execute('DELETE FROM outputfile\n                           WHERE idnum = %s', (idnum,))
            cur.execute('DELETE FROM geometry\n                           WHERE geo_idnum = %s', (idnum,))
            cur.execute('DELETE FROM sticking_info\n                           WHERE st_idnum = %s', (idnum,))
            cur.execute('DELETE FROM forces\n                           WHERE f_idnum = %s', (idnum,))
            cur.execute('DELETE FROM spatialdist\n                           WHERE spat_idnum = %s', (idnum,))
            cur.execute('DELETE FROM speeddist\n                           WHERE spd_idnum = %s', (idnum,))
            cur.execute('DELETE FROM angulardist\n                           WHERE ang_idnum = %s', (idnum,))
            cur.execute('DELETE FROM options\n                       WHERE opt_idnum = %s', (idnum,))
            print(f"Removed {idnum}: {os.path.basename(f)} from database")
            cur.execute('SELECT idnum, filename FROM modelimages\n                           WHERE out_idnum = %s', (idnum,))
            for mid, mfile in cur.fetchall():
                cur.execute('DELETE from modelimages\n                               WHERE idnum = %s', (mid,))
                if os.path.exists(mfile):
                    os.remove(mfile)

            cur.execute('SELECT idnum, filename FROM uvvsmodels\n                           WHERE out_idnum = %s', (idnum,))
            for mid, mfile in cur.fetchall():
                cur.execute('DELETE from uvvsmodels\n                               WHERE idnum = %s', (mid,))
                if os.path.exists(mfile):
                    os.remove(mfile)


def modeldriver(inputs, npackets, overwrite=False, compress=True):
    """
    Starting point for running the model
    INPUTS:
        inputs: Input object
        npackets: Total number of packets to run for this simulation
        overwrite: If True, delete existing files for this set of inputs
    """
    t0_ = Time.now()
    print(f"Starting at {t0_}")
    assert len(inputs.geometry.planet) == 1, 'Gravity and impact check not working for planets with moons.'
    outputfiles, totalpackets, _ = inputs.findpackets()
    print(f"Found {len(outputfiles)} files with {totalpackets} packets")
    if inputs.spatialdist.type == 'idlversion':
        overwrite = True
    else:
        if overwrite and totalpackets > 0:
            delete_files(outputfiles, inputs.database)
            totalpackets = 0
        else:
            npackets = int(npackets)
            ntodo = npackets - totalpackets
            packs_per_it = 100000 if inputs.options.streamlines else int(1000000.0)
            packs_per_it = min(ntodo, packs_per_it)
            if ntodo > 0:
                if inputs.options.streamlines:
                    if inputs.options.at_once is False:
                        raise RuntimeError
                nits = int(np.ceil(ntodo / packs_per_it))
                print('Running Model')
                print(f"Will compute {nits} iterations of {packs_per_it} packets.")
                for _ in range(nits):
                    tit0_ = Time.now()
                    print(f"** Starting iteration #{_ + 1} of {nits} **")
                    output = Output(inputs, packs_per_it, compress=compress)
                    if inputs.options.streamlines:
                        output.stream_driver()
                    else:
                        output.driver()
                    output.save()
                    del output
                    tit1_ = Time.now()
                    print(f"** Completed iteration #{_ + 1} in {(tit1_ - tit0_).sec} seconds.")

            else:
                t2_ = Time.now()
                dt_ = (t2_ - t0_).sec
                if dt_ < 60:
                    dt_ = f"{dt_} sec"
                else:
                    if dt_ < 3600:
                        dt_ = f"{dt_ / 60} min"
                    else:
                        dt_ = f"{dt_ / 3600} hr"
                print(f"Model run completed in {dt_}")


def load_idl_startpoints(output):
    from scipy.io import readsav
    idl = readsav('output0.sav')
    idlout = idl['output']
    output.x0 = idlout['x0'][0] * output.unit
    output.y0 = idlout['y0'][0] * output.unit
    output.z0 = idlout['z0'][0] * output.unit
    output.vx0 = idlout['vx0'][0] * output.unit / u.s
    output.vy0 = idlout['vy0'][0] * output.unit / u.s
    output.vz0 = idlout['vz0'][0] * output.unit / u.s
    output.x = idlout['x0'][0] * output.unit
    output.y = idlout['y0'][0] * output.unit
    output.z = idlout['z0'][0] * output.unit
    output.vx = idlout['vx0'][0] * output.unit / u.s
    output.vy = idlout['vy0'][0] * output.unit / u.s
    output.vz = idlout['vz0'][0] * output.unit / u.s