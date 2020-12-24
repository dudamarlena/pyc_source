# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/configure_model.py
# Compiled at: 2019-04-02 13:35:30
# Size of source mod 2**32: 9478 bytes
import os, os.path, psycopg2

def configfile(setconfig=False):
    """Configure external resources used in the model

    Paths are saved in $HOME/.nexoclom
    * savepath = path where output files are saved
    * database = name of the postgresql database to use
    """
    configfile = os.path.join(os.environ['HOME'], '.nexoclom')
    config = {}
    if os.path.isfile(configfile):
        for line in open(configfile, 'r').readlines():
            if '=' in line:
                key, value = line.split('=')
                config[key.strip()] = value.strip()

    else:
        setconfig = True
    if setconfig:
        if 'savepath' in config:
            oldfile = config['savepath']
            savepath_ = input(f"Path to save files [{oldfile}]: ")
            savepath = oldfile if savepath_ == '' else savepath_
        else:
            savepath = input('Path to save model output: ')
        if 'datapath' in config:
            oldfile = config['datapath']
            datapath_ = input(f"Path to data files [{oldfile}]: ")
            datapath = oldfile if datapath_ == '' else datapath_
        else:
            datapath = input('Path to data files: ')
        if 'database' in config:
            olddb = config['database']
        else:
            olddb = 'thesolarsystem'
        database_ = input(f"Database name [{olddb}]: ")
        database = olddb if database_ == '' else database_
        with psycopg2.connect(host='localhost', database='postgres') as (con):
            con.autocommit = True
            cur = con.cursor()
            try:
                cur.execute(f"CREATE database {database}")
            except:
                pass

        if not os.path.isdir(savepath):
            try:
                os.makedir(savepath)
            except:
                assert 0, f"Could not create directory {savepath}"

        if not os.path.isdir(datapath):
            try:
                os.makedir(datapath)
            except:
                assert 0, f"Could not create directory {datapath}"

        try:
            cfile = open(configfile, 'w')
        except:
            assert 0, f"Could not open {configfile}"

        cfile.write(f"savepath = {savepath}\n")
        cfile.write(f"datapath = {datapath}\n")
        cfile.write(f"database = {database}\n")
        cfile.close()
    else:
        savepath = config['savepath']
        datapath = config['datapath']
        database = config['database']
    return (database, savepath, datapath)


def set_up_output_tables(con):
    cur = con.cursor()
    tables = [
     'outputfile', 'geometry', 'sticking_info', 'forces',
     'spatialdist', 'speeddist', 'angulardist', 'options',
     'modelimages', 'uvvsmodels']
    for tab in tables:
        try:
            cur.execute(f"DROP table {tab}")
        except:
            con.rollback()

    try:
        cur.execute("CREATE TYPE SSObject\n                       as ENUM (\n                            'Milky Way',\n                            'Sun',\n                            'Mercury',\n                            'Venus',\n                            'Earth',\n                            'Mars',\n                            'Jupiter',\n                            'Saturn',\n                            'Uranus',\n                            'Neptune',\n                            'Ceres',\n                            'Pluto',\n                            'Moon',\n                            'Phobos',\n                            'Deimos',\n                            'Io',\n                            'Europa',\n                            'Ganymede',\n                            'Callisto',\n                            'Mimas',\n                            'Enceladus',\n                            'Tethys',\n                            'Dione',\n                            'Rhea',\n                            'Titan',\n                            'Hyperion',\n                            'Iapetus',\n                            'Phoebe',\n                            'Charon',\n                            'Nix',\n                            'Hydra')")
    except:
        pass

    cur.execute('CREATE TABLE outputfile (\n                       idnum SERIAL PRIMARY KEY,\n                       filename text UNIQUE,\n                       npackets bigint,\n                       totalsource float,\n                       creationtime timestamp NOT NULL)')
    print('Created outputfile table')
    cur.execute('CREATE TABLE geometry (\n                       geo_idnum bigint PRIMARY KEY,\n                       planet SSObject,\n                       StartPoint SSObject,\n                       objects SSObject ARRAY,\n                       starttime timestamp,\n                       phi real ARRAY,\n                       subsolarpt point,\n                       TAA float)')
    print('Created geometry table')
    cur.execute('CREATE TABLE sticking_info (\n                       st_idnum bigint PRIMARY KEY,\n                       stickcoef float,\n                       tsurf float,\n                       stickfn text,\n                       stick_mapfile text,\n                       epsilon float,\n                       n float,\n                       tmin float,\n                       emitfn text,\n                       accom_mapfile text,\n                       accom_factor float)')
    print('Created sticking_info table')
    cur.execute('CREATE TABLE forces (\n                       f_idnum bigint PRIMARY KEY,\n                       gravity boolean,\n                       radpres boolean)')
    print('Created forces table')
    cur.execute('CREATE TABLE spatialdist (\n                       spat_idnum bigint PRIMARY KEY,\n                       type text,\n                       exobase float,\n                       use_map boolean,\n                       mapfile text,\n                       longitude float[2],\n                       latitude float[2])')
    print('Created spatialdist table')
    cur.execute('CREATE TABLE speeddist (\n                       spd_idnum bigint PRIMARY KEY,\n                       type text,\n                       vprob float,\n                       sigma float,\n                       U float,\n                       alpha float,\n                       beta float,\n                       temperature float,\n                       delv float)')
    print('Created speeddist table')
    cur.execute('CREATE TABLE angulardist (\n                       ang_idnum bigint PRIMARY KEY,\n                       type text,\n                       azimuth float[2],\n                       altitude float[2],\n                       n float)')
    print('Created angulardist table')
    cur.execute('CREATE TABLE options (\n                       opt_idnum bigint PRIMARY KEY,\n                       endtime float,\n                       resolution float,\n                       at_once boolean,\n                       atom text,\n                       lifetime float,\n                       fullsystem boolean,\n                       outeredge float,\n                       motion boolean,\n                       streamlines boolean,\n                       nsteps int)')
    print('Created options table')
    cur.execute('CREATE TABLE modelimages (\n                       idnum SERIAL PRIMARY KEY,\n                       out_idnum bigint,\n                       quantity text,\n                       origin text,\n                       dims float[2],\n                       center float[2],\n                       width float[2],\n                       subobslongitude float,\n                       subobslatitude float,\n                       mechanism text,\n                       wavelength text,\n                       filename text)')
    print('Created modelimages table')
    cur.execute('CREATE TABLE uvvsmodels (\n                       idnum SERIAL PRIMARY KEY,\n                       out_idnum bigint,\n                       quantity text,\n                       orbit int,\n                       dphi float,\n                       mechanism text,\n                       wavelength text,\n                       filename text)')
    print('Created uvvsmodels table')


if __name__ == '__main__':
    cfgfile = input('Reset the model configuration file? (y/n) ')
    setcfg = True if cfgfile.lower() in ('y', 'yes') else False
    database, savepath, datapath = configfile(setconfig=setcfg)
    print(database, savepath, datapath)
    cfgdb = input('Reset the modeloutputs database? (y/n) ')
    if cfgdb.lower() in ('y', 'yes'):
        with psycopg2.connect(host='localhost', database=database) as (con):
            con.autocommit = True
            set_up_output_tables(con)