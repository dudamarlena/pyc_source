# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/manager.py
# Compiled at: 2020-04-13 14:54:19
# Size of source mod 2**32: 43231 bytes
"""
Model Management and simulation objects.
"""
from __future__ import absolute_import
from __future__ import print_function
import pickle, time
from copy import deepcopy
from numpy import *
from collections import OrderedDict
from argparse import ArgumentParser
import six.moves.configparser, json, sqlite3, os, getpass
from tqdm import tqdm
import pandas as pd, pymysql.cursors, numpy as np
from Epigrass.simobj import graph, edge, siteobj
from Epigrass import spread
from Epigrass.data_io import *
from Epigrass import epigdal
from Epigrass import report
from Epigrass import __version__
import requests, hashlib, redis, six
from six.moves import range
from six.moves import zip
from six.moves import input
redisclient = redis.StrictRedis()

class simulate:
    __doc__ = '\n    This class takes care of setting up the model, simulating it, and storing the results\n    '

    def __init__(self, fname=None, host='localhost', port=3306, db='epigrass', user='epigrass', password='epigrass', backend='sqlite', silent=False):
        self.parallel = True
        self.host = host
        self.port = port
        self.usr = user
        self.db = db
        self.fname = fname
        self.backend = backend
        self.passw = password
        self.repname = None
        self.shapefile = None
        self.World = None
        self.shpout = True
        self.silent = silent
        self.dir = os.getcwd()
        sys.path.insert(0, self.dir)
        self.gui = 0
        self.now = time.asctime().replace(' ', '_').replace(':', '')
        self.modelName = os.path.split(self.fname)[(-1)].split('.')[0]
        self.config = self.loadModelScript(self.fname)
        self.evalConfig(self.config)
        if not self.outdir:
            self.outdir = outdir = 'outdata-' + self.modelName
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
        if self.shapefile:
            self.World = (epigdal.NewWorld)(*self.shapefile + [self.outdir])
        self.chkScript()
        self.encoding = 'utf-8'
        self.round = 0
        sitios = loadData((self.sites), sep=',', encoding=(self.encoding))
        ed = loadData((self.edges), sep=',', encoding=(self.encoding))
        l = self.instSites(sitios)
        e = self.instEdges(l, ed)
        self.g = self.instGraph(self.modelName, 1, l, e)

    def loadModelScript(self, fname):
        """
        Loads the model specification from the text file.
        Returns a dictionary with keys of the form
        <section>.<option> and the corresponding values.
        """
        config = {}
        config = config.copy()
        cp = six.moves.configparser.SafeConfigParser()
        cp.read(fname)
        for sec in cp.sections():
            name = sec.lower()
            for opt in cp.options(sec):
                config[name + '.' + opt.lower()] = cp.get(sec, opt).strip()

        return config

    def evalConfig(self, config):
        """
        Takes in the config dictionary and generates the global variables needed.
        """
        try:
            if config['the world.shapefile']:
                self.shapefile = eval(config['the world.shapefile'])
            else:
                self.shapefile = []
            self.sites = config['the world.sites']
            self.edges = config['the world.edges']
            if config['the world.encoding']:
                self.encoding = config['the world.encoding']
            self.modtype = config['epidemiological model.modtype']
            self.beta = config['model parameters.beta']
            self.alpha = config['model parameters.alpha']
            self.e = config['model parameters.e']
            self.r = config['model parameters.r']
            self.delta = config['model parameters.delta']
            self.B = config['model parameters.b']
            self.w = config['model parameters.w']
            self.p = config['model parameters.p']
            self.seed = eval(config['epidemic events.seed'])
            self.vaccinate = eval(config['epidemic events.vaccinate'])
            self.doTransp = eval(config['transportation model.dotransp'])
            self.stochTransp = eval(config['transportation model.stochastic'])
            self.speed = eval(config['transportation model.speed'])
            self.steps = eval(config['simulation and output.steps'])
            self.outdir = config['simulation and output.outdir']
            self.SQLout = eval(config['simulation and output.sqlout'])
            self.Rep = eval(config['simulation and output.report'])
            self.siteRep = eval(config['simulation and output.siterep'])
            self.replicas = eval(config['simulation and output.replicas'])
            self.randomize_seeds = eval(config['simulation and output.randseed'])
            self.Batch = eval(config['simulation and output.batch'])
        except KeyError as v:
            try:
                V = v.__str__().split('.')
                sys.exit("Please check the syntax of your '.epg' file.\nVariable %s, from section %s was not specified." % (
                 V[1], V[0]))
            finally:
                v = None
                del v

        if self.replicas:
            self.Rep = 0
            self.Batch = []
            self.round = 0
        self.inits = OrderedDict()
        self.parms = {}
        for k, v in config.items():
            try:
                k = k.decode('utf8')
            except AttributeError:
                pass

            if k.startswith('initial conditions'):
                self.inits[k.split('.')[(-1)]] = v
            elif k.startswith('model parameters'):
                self.parms[k.split('.')[(-1)]] = v
                continue

    def chkScript(self):
        """
        Checks the type of the variables on the script
        """
        self.Say('Checking syntax of model script... NOW')
        if not os.access(self.sites, os.F_OK):
            self.Say('Sites file %s does not exist, please check your script.' % self.sites)
            sys.exit()
        if not os.access(self.edges, os.F_OK):
            self.Say('Egdes file %s does not exist, please check your script.' % self.edges)
            sys.exit()
        if self.modtype not in ('SIS', 'SIS_s', 'SIR', 'SIR_s', 'SEIS', 'SEIS_s', 'SEIR',
                                'SEIR_s', 'SIpRpS', 'SIpRpS_s', 'SIpR,SIpR_s', 'Influenza',
                                'Custom'):
            self.Say('Model type %s is invalid, please check your script.' % self.modtype)
        self.Say('Script %s passed syntax check NOW.' % self.modelName)

    def deg2dec(self, coord):
        """
        converts lat/long to decimal
        """
        co = coord.split(':')
        if int(co[0]) < 0:
            result = float(co[0]) - float(co[1]) / 60 - float(co[2]) / 3600
        else:
            result = float(co[0]) + float(co[1]) / 60 + float(co[2]) / 3600
        return result

    def instSites(self, sitelist):
        """
        Instantiates and returns a list of siteobj instances, from a list of site specification
        as returned by data_io.loadData.
        Here the site specific events are passed to each site, and the site models are created.
        """
        header = sitelist.pop(0)
        ncols = len(header)
        objlist = []
        for site in sitelist:
            if len(site) != ncols:
                raise ValueError('This line in your sites file has a different number elements:\n%s' % str(site))
            elif ':' in str(site[0]):
                lat = self.deg2dec(str(site[0]))
                longit = self.deg2dec(str(site[1]))
            else:
                lat = site[0]
                longit = site[1]
            objlist.append(siteobj(site[2], site[3], (lat, longit), int(site[4]), tuple([float(i) for i in site[5:]])))

        for o in objlist:
            if self.stochTransp:
                o.stochtransp = 1
            else:
                o.stochtransp = 0
            N = o.totpop
            values = o.values
            inits = OrderedDict()
            parms = {}
            for k, v in self.inits.items():
                if isinstance(k, bytes):
                    k = k.decode('utf8')
                inits[k] = eval(v)
                inits[k.lower()] = eval(v)

            for k, v in self.parms.items():
                if isinstance(k, bytes):
                    k = k.decode('utf8')
                parms[k] = eval(v)

            if self.vaccinate:
                if self.vaccinate[0][0] == 'all':
                    o.vaccination = [
                     self.vaccinate[0][1], self.vaccinate[0][2]]
                else:
                    for i in self.vaccinate:
                        if int(o.geocode) == i[0]:
                            o.vaccination = [
                             i[1], float(i[2])]

            if self.seed:
                for j in self.seed:
                    if int(o.geocode) == j[0] or self.seed[0][0] == 'all':
                        inits[j[1].lower()] += j[2]
                        o.createModel((self.modtype), (self.modelName), v=values, bi=inits, bp=parms)
                    else:
                        o.createModel((self.modtype), (self.modelName), v=values, bi=inits, bp=parms)

            else:
                o.createModel((self.modtype), (self.modelName), v=values, bi=inits, bp=parms)

        return objlist

    def instEdges(self, sitelist, edgelist):
        """
        Instantiates and returns a list of edge objects,

        sitelist -- list of siteobj objects.

        edgelist -- list of edge specifications as returned by data_io.loadData.
        """
        header = edgelist.pop(0)
        objlist = []
        source = dest = None
        for edg in edgelist:
            if edg[5] == edg[6]:
                continue
            for site in sitelist:
                if site.geocode == edg[5]:
                    source = site
                else:
                    if site.geocode == edg[6]:
                        dest = site
                if source and dest:
                    break

            if not (source and dest):
                print(type(edg[5]), type(edg[6]))
                sys.exit(f"One of the vertices on edge {edg[0]}({edg[5]}) - {edg[1]}({edg[6]}) could not be found on the site list")
            objlist.append(edge(source, dest, edg[2], edg[3], float(edg[4])))
            source = dest = None

        return objlist

    def instGraph(self, name, digraph, siteobjlist, edgeobjlist):
        """
        Instantiates and returns a graph object from a list of edge objects.
        """
        g = graph(name, digraph)
        g.speed = self.speed
        for j in siteobjlist:
            g.addSite(j)

        for i in edgeobjlist:
            g.addEdge(i)

        return g

    def randomizeSeed--- This code section failed: ---

 L. 330         0  LOAD_FAST                'option'
                2  LOAD_CONST               1
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   176  'to 176'

 L. 331         8  LOAD_LISTCOMP            '<code_object <listcomp>>'
               10  LOAD_STR                 'simulate.randomizeSeed.<locals>.<listcomp>'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  LOAD_GLOBAL              six
               16  LOAD_METHOD              itervalues
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                g
               22  LOAD_ATTR                site_dict
               24  CALL_METHOD_1         1  '1 positional argument'
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'poplist'

 L. 332        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'poplist'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'lpl'

 L. 333        40  LOAD_GLOBAL              array
               42  LOAD_FAST                'poplist'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  LOAD_GLOBAL              sum
               48  LOAD_FAST                'poplist'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  BINARY_TRUE_DIVIDE
               54  STORE_FAST               'popprob'

 L. 334        56  LOAD_GLOBAL              floor
               58  LOAD_GLOBAL              np
               60  LOAD_ATTR                random
               62  LOAD_METHOD              uniform
               64  LOAD_CONST               0
               66  LOAD_FAST                'lpl'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                replicas
               72  CALL_METHOD_3         3  '3 positional arguments'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  STORE_FAST               'u'

 L. 335        78  BUILD_LIST_0          0 
               80  STORE_FAST               'sites'

 L. 336        82  LOAD_CONST               0
               84  STORE_FAST               'i'

 L. 337        86  LOAD_FAST                'self'
               88  LOAD_ATTR                g
               90  LOAD_ATTR                site_list
               92  STORE_FAST               'site_list'

 L. 338        94  SETUP_LOOP          192  'to 192'
             96_0  COME_FROM           138  '138'
               96  LOAD_FAST                'i'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                replicas
              102  COMPARE_OP               <
              104  POP_JUMP_IF_FALSE   172  'to 172'

 L. 339       106  LOAD_GLOBAL              np
              108  LOAD_ATTR                random
              110  LOAD_METHOD              uniform
              112  LOAD_CONST               0
              114  LOAD_CONST               1
              116  CALL_METHOD_2         2  '2 positional arguments'
              118  STORE_FAST               'p'

 L. 340       120  LOAD_FAST                'p'
              122  LOAD_FAST                'popprob'
              124  LOAD_GLOBAL              int
              126  LOAD_FAST                'u'
              128  LOAD_FAST                'i'
              130  BINARY_SUBSCR    
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  BINARY_SUBSCR    
              136  COMPARE_OP               <=
              138  POP_JUMP_IF_FALSE    96  'to 96'

 L. 341       140  LOAD_FAST                'sites'
              142  LOAD_METHOD              append
              144  LOAD_FAST                'site_list'
              146  LOAD_GLOBAL              int
              148  LOAD_FAST                'u'
              150  LOAD_FAST                'i'
              152  BINARY_SUBSCR    
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  BINARY_SUBSCR    
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          

 L. 342       162  LOAD_FAST                'i'
              164  LOAD_CONST               1
              166  INPLACE_ADD      
              168  STORE_FAST               'i'
              170  JUMP_BACK            96  'to 96'
            172_0  COME_FROM           104  '104'
              172  POP_BLOCK        
              174  JUMP_FORWARD        192  'to 192'
            176_0  COME_FROM             6  '6'

 L. 343       176  LOAD_FAST                'option'
              178  LOAD_CONST               2
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   192  'to 192'

 L. 344       184  LOAD_FAST                'self'
              186  LOAD_ATTR                g
              188  LOAD_ATTR                site_list
              190  STORE_FAST               'sites'
            192_0  COME_FROM           182  '182'
            192_1  COME_FROM           174  '174'
            192_2  COME_FROM_LOOP       94  '94'

 L. 345       192  LOAD_FAST                'sites'
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 192_2

    def setSeed(self, seed, n=1):
        """
        Resets the number of infected to zero in all nodes but seed,
        which get n infected cases.
        seed must be a siteobj object.
        """
        seedvar = self.seed[0][1].lower()
        self.Say('seedvar= %s' % seedvar)
        site_list = self.g.site_list
        self.seed = [(seed.geocode, seedvar, n)]
        for site in site_list:
            if site.geocode == seed.geocode or seed.geocode == 'all':
                site.bi[seedvar] = n
                self.Say('%s infected case(s) arrived at %s' % (n, seed.sitename))
            else:
                site.bi[seedvar] = 0

    def start(self):
        """
        Start the simulation
        """
        if '/' in self.modelName:
            self.modelName = os.path.split(self.modelName)[(-1)]
        else:
            time.sleep(10)
            self.Say('Simulation starting.')
            start = time.time()
            self.runGraph((self.g), (self.steps), transp=(self.doTransp))
            elapsed = time.time() - start
            self.Say('Simulation lasted %s seconds.' % elapsed)
            if self.SQLout:
                if self.backend == 'csv':
                    self.outToCsv(self.modelName)
                else:
                    self.outToDb(self.modelName)
        if self.shpout:
            self.outToShp()
        self.dumpData()
        spread.Spreadself.gself.outdirself.encoding

    def createDataFrame(self, site):
        """
        Saves the time series *site.ts* to outfile as specified on the
        model script.
        """
        ts = array([eval(st) for st in redisclient.lrangef"{site.geocode}:ts"0(-1)])
        data = array(ts, float)
        inc = site.incidence
        f = open(self.outdir + self.outfile, 'w')
        f.write('time,E,I,S,incidence\n')
        try:
            for t, i in enumerate(data):
                j = [str(k) for k in i]
                line = str(t) + ','.join(j) + str(inc[t]) + '\n'
                f.write(line)

        finally:
            f.close()

        return 'E,I,S\n'

    def outToShp(self):
        """
        Creates Data Layers in shapefile format
        """
        if not self.World:
            return
        varlist = [
         'prevalence', 'totalcases', 'arrivals', 'population']
        sitestats = [(site.geocode, float(site.totalcases) / site.totpop, site.totalcases, sum(site.thetahist), float(site.totpop)) for site in six.itervalues(self.g.site_dict)]
        simdf = pd.DataFrame(data=(array(sitestats)), columns=([self.World.geocfield] + varlist))
        self.World.map[self.World.geocfield] = self.World.map[self.World.geocfield].astype(int)
        self.World.map = pd.merge((self.World.map), simdf, on=(self.World.geocfield))
        self.Say('Saving results in the map Data.gpkg')
        self.World.map.to_file(os.path.join(self.outdir, 'Data.gpkg'))

    def out_to_kml(self, names):
        """
        Generates output to kml files
        """
        self.Say('Creating KML output files...')
        lr = self.World.datasource.GetLayer(0)
        k = epigdal.KmlGenerator()
        k.addNodes(lr, names)
        k.writeToFile(self.outdir)
        site_list = self.g.site_list
        site_dict = self.g.site_dict
        if len(site_dict) * len(list(site_dict.values())[0].ts) < 20000:
            for i, v in enumerate(list(site_dict.values())[0].vnames):
                ka = epigdal.AnimatedKML((os.path.join(self.outdir, 'Data.kml')), extrude=True)
                data = []
                for site in site_dict.values():
                    ts = [eval(st) for st in redisclient.lrangef"{site.geocode}:ts"0(-1)]
                    for t, p in enumerate(ts):
                        data.append((str(site.geocode), t, p[i]))

                ka.add_data(data)
                ka.save(v + '_animation')
                self.Say(v + '_animation')
                del ka

        else:
            self.Say('Simulation too large to export as kml.')
        self.Say('Done creating KML files!')

    def series_to_JSON(self):
        """
        Saves timeseries to JSON for uploading to epigrass web
        """
        self.Say('Saving series to JSON')
        series = {}
        for gc, s in six.iteritems(self.g.site_dict):
            length = max(map(len, s.ts))
            y = np.array([np.pad(xi, length, 'constant', constant_values=(np.NaN)) for xi in s.ts])
            ts = np.array(y)
            sdict = {}
            for i, vn in enumerate(s.vnames):
                sdict[vn] = ts[:, i].tolist()

            series[gc] = sdict

        with open('series.json', 'w') as (f):
            json.dump(series, f)

    def writeMetaCSV(self, table):
        """
        Writes a meta CSV table
        """
        if not self.outdir == os.getcwd():
            os.chdir(self.outdir)
        f = open(table + '_meta', 'w')
        cfgitems = list(self.config.items())
        h = ';'.join([k.strip().replace(' ', '_').replace('.', '$') for k, v in cfgitems])
        l = ';'.join([v.split('#')[0] for k, v in cfgitems])
        f.write(h + '\n')
        f.write(l + '\n')
        f.close()
        os.chdir(self.dir)

    def outToCsv(self, table):
        """
        Save simulation results in csv file.
        """
        if not self.outdir == os.getcwd():
            os.chdir(self.outdir)
        tablee = table + '_' + self.now + '_e.tab'
        table += '_' + self.now + '.tab'
        f = open(table, 'w')
        head = ['geocode', 'time', 'totpop', 'name',
         'lat', 'longit']
        headerwritten = False
        for site in self.g.site_dict.values():
            t = 0
            regb = [str(site.geocode), str(t), str(site.totpop),
             site.sitename.replace('"', '').encode('ascii', 'replace'),
             str(site.pos[0]), str(site.pos[1])]
            if site.values:
                for n, v in enumerate(site.values):
                    head.append('values%s' % n)
                    regb.append(str(v))

            ts = array([eval(st) for st in redisclient.lrangef"{site.geocode}:ts"0(-1)])
            head.extend(['incidence', 'arrivals'])
            for n, v in enumerate(site.vnames):
                head.append(str(v))

            for i in ts:
                reg = deepcopy(regb)
                reg.extend([str(site.incidence[t]), str(site.thetahist[t])])
                reg[1] = str(t)
                for n, v in enumerate(site.vnames):
                    reg.append(str(i[n]))

                if not headerwritten:
                    h = ','.join(head)
                    f.write(h + '\n')
                    headerwritten = True
                f.write(','.join(reg) + '\n')
                t += 1

        f.close()
        g = open(tablee, 'w')
        t = 0
        head = ['source_code', 'dest_code', 'time', 'ftheta', 'btheta']
        ehw = False
        for e in self.g.edge_list:
            for f, b in zip(e.ftheta, e.btheta):
                if not ehw:
                    g.write(','.join(head) + '\n')
                    ehw = True
                ereg = [
                 e.source.geocode, e.dest.geocode, t, f, b]
                ereg = [str(i) for i in ereg]
                g.write(','.join(ereg) + '\n')
                t += 1

        g.close()
        os.chdir(self.dir)

    def writeMetaTable(self, table):
        """
        Creates a Meta-Info Table on the database with the contents of the .epg file
        """
        try:
            table = table + '_meta'
            if self.backend.lower() == 'mysql':
                con = pymysql.connect(host=(self.host), port=(self.port), user=(self.usr),
                  passwd=(self.passw),
                  db=(self.db))
            else:
                if self.backend.lower() == 'sqlite':
                    if not self.outdir == os.getcwd():
                        os.chdir(self.outdir)
                    con = sqlite3.connect('Epigrass.sqlite')
                    os.chdir(self.dir)
            sqlstr1 = 'CREATE TABLE %s(' % table
            vars = []
            cfgitems = list(self.config.items())
            for k, v in cfgitems:
                vars.append(k.strip().replace(' ', '_').replace('.', '$'))

            sqlstr2 = ', '.join(['%s text' % i for i in vars])
            Cursor = con.cursor()
            Cursor.execute(sqlstr1 + sqlstr2 + ');')
            values = [v.split('#')[0] for k, v in cfgitems]
            str3 = ','.join(['"%s"' % i for i in values]) + ')'
            sqlstr3 = 'INSERT INTO %s VALUES(%s' % (table, str3)
            Cursor.execute(sqlstr3)
        finally:
            if con:
                con.commit()
                con.close()

    def outToDb(self, table):
        """
        Insert simulation results on a mysql or SQLite table
        :param table: Table name
        """
        if self.backend.lower() == 'mysql':
            self.Say('Saving data on MySQL...')
        else:
            if self.backend.lower() == 'sqlite':
                self.Say('Saving data on SQLite...')
        con = None
        try:
            table = table + '_' + self.now
            self.writeMetaTable(table)
            self.outtable = table
            if self.backend.lower() == 'mysql':
                con = pymysql.connect(host=(self.host), port=(self.port), user=(self.usr),
                  passwd=(self.passw),
                  db=(self.db))
            else:
                if self.backend.lower() == 'sqlite':
                    if not self.outdir == os.getcwd():
                        os.chdir(self.outdir)
                    con = sqlite3.connect('Epigrass.sqlite')
                    os.chdir(self.dir)
            nvar = len(list(self.g.site_dict.values())[0].vnames) + 4
            str1 = '`%s` FLOAT(9),' * nvar
            str1lite = '%s REAL,' * nvar
            varnames = ['lat', 'longit'] + list(list(self.g.site_dict.values())[0].vnames) + ['incidence'] + [
             'Arrivals']
            str1 = str1[:-1] % tuple(varnames)
            str1lite = str1lite[:len(str1lite) - 1] % tuple(varnames)
            Cursor = con.cursor()
            str2 = f"CREATE TABLE {table}(\n            `geocode` INT( 9 )  ,\n            `time` INT( 9 ) ,\n            `name` varchar(128) ,\n            "
            str2lite = 'CREATE TABLE %s(\n            geocode INTEGER  ,\n            time INTEGER ,\n            name TEXT ,\n            ' % table
            sql = str2 + str1 + ');'
            sqlite = str2lite + str1lite + ');'
            if self.backend.lower() == 'mysql':
                Cursor.execute(sql)
                str3 = (nvar + 3) * '%s,'
                str3 = str3[:-1] + ')'
            else:
                if self.backend.lower() == 'sqlite':
                    Cursor.execute(sqlite)
                    str3 = (nvar + 3) * '?,'
                    str3 = str3[:-1] + ')'
                sql2 = 'INSERT INTO %s' % table + ' VALUES(' + str3
                nvalues = []
                for site in self.g.site_dict.values():
                    geoc = site.geocode
                    lat = site.pos[0]
                    longit = site.pos[1]
                    name = site.sitename
                    ts = array([eval(st) for st in redisclient.lrangef"{geoc}:ts"0(-1)])
                    inc = site.incidence
                    thist = site.thetahist
                    t = 0
                    for incid, flow in zip(inc, thist):
                        tstep = str(t)
                        flow = float(thist[t])
                        nvalues.append(tuple([geoc, tstep, name] + [lat, longit] + list(ts[t]) + [incid] + [flow]))
                        t += 1

                Cursor.executemany(sql2, nvalues)
                con.commit()
            self.etable = etable = table + 'e'
            esql = 'CREATE TABLE %s(\n            `source_code` INT( 9 )  ,\n            `dest_code` INT( 9 )  ,\n            `time` INT( 9 ) ,\n            `ftheta` FLOAT(9) ,\n            `btheta` FLOAT(9) );' % etable
            esqlite = 'CREATE TABLE %s(\n            source_code INTEGER  ,\n            dest_code INTEGER  ,\n            time INTEGER ,\n            ftheta REAL ,\n            btheta REAL );' % etable
            if self.backend.lower() == 'mysql':
                Cursor.execute(esql)
                esql2 = 'INSERT INTO %s' % etable + ' VALUES(%s,%s,%s,%s,%s)'
            else:
                if self.backend.lower() == 'sqlite':
                    Cursor.execute(esqlite)
                    esql2 = 'INSERT INTO %s' % etable + ' VALUES(?,?,?,?,?)'
                values = []
                for gcs, e in six.iteritems(self.g.edge_dict):
                    s = gcs[0]
                    d = gcs[1]
                    t = 0
                    for f, b in zip(e.ftheta, e.btheta):
                        values.append((s, d, t, f, b))
                        t += 1

                Cursor.executemany(esql2, values)
        finally:
            if con:
                con.commit()
                con.close()

        matname = 'adj_' + self.modelName
        fname = os.path.join(self.outdir, matname)
        adjfile = open(fname, 'wb')
        pickle.dump(self.g.getConnMatrix(), adjfile)
        adjfile.close()

    def criaAdjMatrix(self):
        codeslist = [str(i.geocode) for i in six.itervalues(self.g.site_dict)]
        if not os.path.exists('adjmat.csv'):
            self.Say('Saving the adjacency  matrix...')
            am = self.g.getConnMatrix()
            amf = open('adjmat.csv', 'w')
            amf.write(','.join(codeslist) + '\n')
            for row in am:
                row = [str(i) for i in row]
                amf.write(','.join(row) + '\n')

            amf.close()
            self.Say('Done!')

    def dumpData(self):
        """
        Dumps data as csv (comma-separated-values)
        """
        self.Say('Starting simulation Analysis')
        curdir = os.getcwd()
        if not self.outdir == curdir:
            os.chdir(self.outdir)
        else:
            codeslist = list(self.g.site_dict.keys())
            self.criaAdjMatrix()
            self.Say('Saving Epidemic path...')
            if self.round:
                epp = codecs.open('epipath%s.csv' % str(self.round))'w'self.encoding
            else:
                epp = codecs.open'epipath.csv''w'self.encoding
            epp.write('time,site,infector\n')
            for i in self.g.epipath:
                site = self.g.site_dict[i[1]]
                infectors = i[(-1)]
                if len(infectors):
                    reverse_infectors = list(infectors.items())
                    reverse_infectors.sort(key=(lambda t: t[1]))
                    mli = reverse_infectors[(-1)][0].sitename
                else:
                    mli = 'NA'
                epp.write(str(i[0]) + ',' + site.sitename + ',' + mli + '\n')

            epp.close()
            self.Say('Done!')
            self.g.save_topology('network.gexf')
            self.Say('Saving Epidemiological results...')
            stats = [str(i) for i in self.g.getEpistats()]
            seed = [s for s in six.itervalues(self.g.site_dict) if not s.geocode == self.seed[0][0] if self.seed[0][0] == 'all'][0]
            stats.pop(1)
            if os.path.exists('epistats.csv'):
                stf = codecs.open'epistats.csv''a'self.encoding
            else:
                stf = codecs.open'epistats.csv''w'self.encoding
                stf.write('seed,name,size,infected_sites,spreadtime,median_survival,totvaccinated,totquarantined,seeddeg,seedpop\n')
            sdeg = str(seed.getDegree())
            spop = str(seed.totpop)
            sname = seed.sitename
            sstats = '%s,%s' % (sdeg, spop)
            stf.write(str(self.seed[0][0]) + ',' + sname + ',' + ','.join(stats) + ',' + sstats + '\n')
            stf.close()
            self.Say('Done saving!')
            self.Say('Saving site statistics...')
            if os.path.exists('sitestats.csv'):
                sitef = codecs.open'sitestats.csv''a'self.encoding
            else:
                sitef = codecs.open'sitestats.csv''w'self.encoding
        sitef.write('round,geocode,name,infection_time,degree,seed,seedname\n')
        for s in six.itervalues(self.g.site_dict):
            degree = str(s.getDegree())
            seedgc = str(self.seed[0][0])
            seedname = seed.sitename
            it = str(s.infected)
            if it == 'FALSE':
                it = 'NA'
            sitef.write(str(self.round) + ',' + str(s.geocode) + ',' + s.sitename + ',' + it + ',' + degree + ',' + seedgc + ',' + seedname + '\n')

        self.series_to_JSON()
        os.chdir(curdir)
        self.Say('Done saving data!')

    def saveModel(self, fname):
        """
        Save the fully specified graph.
        """
        f = open(fname, 'w')
        pickle.dump(self.g, f)
        f.close()

    def loadModel(self, fname):
        """
        Loads a pre-saved graph.
        """
        g = pickle.load(fname)
        return g

    def runGraph(self, graphobj, iterations=1, transp=0):
        """
        Starts the simulation on a graph.
        """
        g = graphobj
        g.maxstep = iterations
        sites = list(graphobj.site_dict.values())
        edges = list(graphobj.edge_dict.values())
        if transp:
            for n in tqdm((range(iterations)), desc='Simulation steps'):
                results = [i.runModel(self.parallel) for i in sites]
                if self.parallel:
                    [r.wait() for r in results]
                for j in edges:
                    j.migrate()

                if self.gui:
                    self.gui.stepLCD.display(g.simstep)
                    self.gui.app.processEvents()
                g.simstep += 1
                g.sites_done = 0

        else:
            for n in tqdm((range(iterations)), desc='Simulation steps'):
                for i in tqdm(sites, desc='Sites'):
                    i.runModel(self.parallel)

                if self.gui:
                    self.gui.stepLCD.display(g.simstep)
                    self.gui.app.processEvents()
                    self.gui.RT.mutex.lock()
                    self.gui.RT.emitself.gui.QtCore.SIGNAL('drawStep')g.simstepdict([(s.geocode, s.incidence[(-1)]) for s in sites])
                    self.gui.RT.mutex.unlock()
                g.simstep += 1

    def Say(self, string):
        """
        Exits outputs messages to the console or the gui accordingly
        """
        if self.gui:
            self.gui.textEdit1.insertPlainText(string + '\n')
        else:
            if self.silent:
                return
            print()
            string + '\n'


def storeSimulation(S, usr, passw, db='epigrass', host='localhost', port=3306):
    """
    store the Simulate object *s* in the epigrass database
    to allow distributed runs. Currently not working.
    """
    now = time.asctime().replace(' ', '_').replace(':', '')
    table = 'Model_' + S.modelName + now
    con = pymysql.connect(host=host, port=port, user=usr, passwd=passw, db=db)
    Cursor = con.cursor()
    sql = 'CREATE TABLE %s(\n        `simulation` BLOB);' % table
    Cursor.execute(sql)
    blob = pickle.dumps(S)
    sql2 = 'INSERT INTO %s' % table + ' VALUES(%s)'
    Cursor.execute(sql2, blob)
    con.close()


def onStraightRun(args):
    """
    Runs the model from the commandline
    """
    if args.backend == 'mysql':
        S = simulate(fname=(args.epg[0]), host=(args.dbhost), user=(args.dbuser), password=(args.dbpass), backend=(args.backend))
    else:
        S = simulate(fname=(args.epg[0]), backend=(args.backend))
    S.parallel = args.parallel
    if not S.replicas:
        S.start()
        spread.Spread(S.g)
        R = report.Report(S)
        R.Assemble(type=(S.Rep))
    else:
        repRuns(S)
    if S.Batch:
        S.Say('Simulation Started.')
        for i in S.Batch:
            os.chdir(S.dir)
            S.graph = None
            T = simulate(fname=i, host=(S.host), user=(S.usr), password=(S.passw), backend=(S.backend))
            print('starting model %s' % i)
            T.start()


def repRuns(S):
    """
    Do repeated runs
    """
    randseed = S.randomize_seeds
    fname = S.fname
    host = S.host
    user = S.usr
    password = S.passw
    backend = S.backend
    nseeds = S.seed[0][2]
    print('Replication type: ', randseed)
    if randseed:
        seeds = S.randomizeSeed(randseed)
    reps = S.replicas
    for i in range(reps):
        print('Starting replicate number %s' % i)
        S = simulate(fname=fname, host=host, user=user, password=password, backend=backend)
        if randseed:
            S.setSeed(seeds[i], nseeds)
        S.round = i
        S.shpout = False
        S.start()
        del S


def upload_model(args):
    """
    Uploads Model specification, auxiliary files and
    :return:
    """
    username = input('Enter your epigrass Web User id:')
    passwd = getpass('Enter your Epigrass Web password:')
    S = simulate(fname=(args.epg[0]), backend=(args.backend))
    app_url = 'http://app.epigrass.net/simulations/view/new/'
    r = requests.get(app_url, auth=(username, passwd))
    fields = {'epg': (S.modelName, open(S.fname, 'rb'), 'text/plain')}
    if os.path.exists(os.path.join(S.outdir, 'data.json')):
        fields['map'] = (
         'data.json', open(os.path.join(S.outdir, 'data.json'), 'rb'), 'text/plain')
    else:
        if os.path.exists(os.path.join(S.outdir, 'series.json')):
            fields['series'] = (
             'series.json', open(os.path.join(S.outdir, 'series.json'), 'rb'), 'text/plain')
        if os.path.exists(os.path.join(S.outdir, 'network.json')):
            fields['network'] = (
             'network.json', open(os.path.join(S.outdir, 'network.json'), 'rb'), 'text/plain')
        if os.path.exists(os.path.join(S.outdir, 'spread.json')):
            fields['spread'] = (
             'spread.json', open(os.path.join(S.outdir, 'spread.json'), 'rb'), 'text/plain')
        hdrs = {'Content-Type':fields.content_type,  'content-encoding':'gzip', 
         'transfer-encoding':'chunked'}
        r = requests.post(app_url, files=fields, headers=hdrs)
        if r.status_code == requests.codes.ok:
            print('Model has been uploaded sucessfully!')
        else:
            print('Model Upload failed.')


def main():
    usage = 'usage: epirunner [options] your_model.epg'
    parser = ArgumentParser(usage=usage, description='Run epigrass models from the console', prog=('epirunner ' + __version__.version))
    parser.add_argument('-b', '--backend', dest='backend', help='Define which datastorage backend to use',
      metavar='<mysql|sqlite|csv>',
      default='sqlite')
    parser.add_argument('-u', '--dbusername', dest='dbuser',
      help='MySQL user name')
    parser.add_argument('-p', '--password', dest='dbpass',
      help='MySQL password for user')
    parser.add_argument('-H', '--dbhost', dest='dbhost',
      default='localhost',
      help='MySQL hostname or IP address')
    parser.add_argument('--upload', help='Upload your models and latest simulation to Epigrass Web')
    parser.add_argument('-P', '--parallel', action='store_true', default=False, dest='parallel',
      help='use multiprocessing to run the simulation')
    parser.add_argument('epg', metavar='EPG', nargs=1, help='Epigrass model definition file (.epg).')
    args = parser.parse_args()
    if args.backend == 'mysql':
        args.dbuser and args.dbpass or parser.error('You must specify a user and password when using MySQL.')
    else:
        if args.backend not in ('mysql', 'sqlite', 'csv'):
            parser.error('"%s" is an invalid backend type.' % args.backend)
        print('==> ', args.epg)
        if args.upload:
            upload_model(args)
        else:
            onStraightRun(args)


if __name__ == '__main__':
    main()