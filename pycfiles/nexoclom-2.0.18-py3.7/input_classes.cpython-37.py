# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/input_classes.py
# Compiled at: 2019-04-04 13:27:11
# Size of source mod 2**32: 17478 bytes
"""Classes used by the Inputs class"""
import os, numpy as np
from astropy.time import Time
import astropy.units as u
from solarsystem import SSObject

class Geometry:

    def __init__(self, gparam):
        """Geometry object: object to model
           Fields:
               planet
               StartPoint
               objects
               starttime
               phi
               subsolarpt = (subsolarlong, subsolarlat)
               TAA"""
        if 'planet' in gparam:
            planet = gparam['planet'].title()
            self.planet = SSObject(planet)
        else:
            if not 0:
                raise AssertionError('Planet not defined.')
            else:
                objlist = [
                 self.planet.object]
                if self.planet.moons is not None:
                    objlist.extend([m.object for m in self.planet.moons])
                else:
                    self.startpoint = gparam['startpoint'].title() if 'startpoint' in gparam else self.planet.object
                    assert self.startpoint in objlist, 'Not a valid starting point'
                    if 'objects' in gparam:
                        inc = set((i.strip().title() for i in gparam['objects'].split(',')))
                    else:
                        inc = set((self.planet.object, self.startpoint))
                for i in inc:
                    assert i in objlist, 'Invalid object included: {}'.format(i)

                self.objects = set((SSObject(o) for o in inc))
                if 'time' in gparam:
                    try:
                        self.time = Time(gparam['time'].upper())
                    except:
                        assert 0, 'Time is not given in a valid format'

                    if not 0:
                        raise AssertionError('Need to figure out how to calculate orbital positions')
                else:
                    self.time = None
                if 'phi' in gparam:
                    phi = tuple((float(p) * u.rad for p in gparam['phi'].split(',')))
                    if not 0:
                        raise AssertionError('Need to figure out best way to do this')
                elif len(self.objects) == 1:
                    self.phi = [0.0 * u.rad]
                else:
                    assert 0, 'Need to give either an observation timeor orbital position.'
            subslong = float(gparam['subsolarlong']) * u.rad if 'subsolarlong' in gparam else 0.0 * u.rad
            subslat = float(gparam['subsolarlat']) * u.rad if 'subsolarlat' in gparam else 0.0 * u.rad
            self.subsolarpoint = (subslong, subslat)
            self.taa = float(gparam['taa']) if 'taa' in gparam else 0.0
            self.taa *= u.rad

    def __str__(self):
        print('geometry.planet = {}'.format(self.planet.object))
        print('geometry.StartPoint = {}'.format(self.startpoint))
        oo = [o.object for o in self.objects]
        obs = ', '.join(oo)
        print('geometry.objects = {}'.format(obs))
        if self.time is not None:
            print('geometry.starttime = {}'.format(self.time.iso))
        else:
            print('geometry.startime not specified')
        if len(self.phi) != 0:
            print('geometry.phi XXX')
        print(('geometry.subsolarpoint = ({}, {})'.format)(*self.subsolarpoint))
        print('geometry.TAA = {}'.format(self.taa))
        return ''


class StickingInfo:
    __doc__ = '\n    stickcoef\n    tsurf\n    stickfn\n    stick_mapfile\n    epsilon\n    n\n    tmin\n    emitfn\n    accom_mapfile\n    accom_factor\n    '

    def __init__--- This code section failed: ---

 L. 118         0  LOAD_STR                 'stickcoef'
                2  LOAD_FAST                'sparam'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_GLOBAL              float
               10  LOAD_FAST                'sparam'
               12  LOAD_STR                 'stickcoef'
               14  BINARY_SUBSCR    
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM             6  '6'

 L. 119        20  LOAD_CONST               1.0
             22_0  COME_FROM            18  '18'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               stickcoef

 L. 120        26  LOAD_FAST                'self'
               28  LOAD_ATTR                stickcoef
               30  LOAD_CONST               1.0
               32  COMPARE_OP               >
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 121        36  LOAD_CONST               1.0
               38  LOAD_FAST                'self'
               40  STORE_ATTR               stickcoef
             42_0  COME_FROM            34  '34'

 L. 124        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               tsurf

 L. 125        48  LOAD_STR                 'stickfn'
               50  LOAD_FAST                'sparam'
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_FAST                'sparam'
               58  LOAD_STR                 'stickfn'
               60  BINARY_SUBSCR    
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            54  '54'
               64  LOAD_CONST               None
             66_0  COME_FROM            62  '62'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               stickfn

 L. 126        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               stick_mapfile

 L. 127        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               epsilon

 L. 128        82  LOAD_CONST               None
               84  LOAD_FAST                'self'
               86  STORE_ATTR               n

 L. 129        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  STORE_ATTR               tmin

 L. 130        94  LOAD_STR                 'emitfn'
               96  LOAD_FAST                'sparam'
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   110  'to 110'
              102  LOAD_FAST                'sparam'
              104  LOAD_STR                 'emitfn'
              106  BINARY_SUBSCR    
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM           100  '100'
              110  LOAD_CONST               None
            112_0  COME_FROM           108  '108'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               emitfn

 L. 131       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               accom_mapfile

 L. 132       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               accom_factor

 L. 135       128  LOAD_FAST                'self'
              130  LOAD_ATTR                stickcoef
              132  LOAD_CONST               1
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   146  'to 146'

 L. 137       138  LOAD_STR                 'complete'
              140  LOAD_FAST                'self'
              142  STORE_ATTR               stickfn
              144  JUMP_FORWARD        370  'to 370'
            146_0  COME_FROM           136  '136'

 L. 138       146  LOAD_FAST                'self'
              148  LOAD_ATTR                stickcoef
              150  LOAD_CONST               0.0
              152  COMPARE_OP               >
              154  POP_JUMP_IF_FALSE   164  'to 164'

 L. 140       156  LOAD_STR                 'constant'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               stickfn
              162  JUMP_FORWARD        370  'to 370'
            164_0  COME_FROM           154  '154'

 L. 141       164  LOAD_FAST                'self'
              166  LOAD_ATTR                stickcoef
              168  LOAD_CONST               -1
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   196  'to 196'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                stickfn
              178  LOAD_STR                 'use_map'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   196  'to 196'

 L. 142       184  LOAD_FAST                'sparam'
              186  LOAD_STR                 'stick_mapfile'
              188  BINARY_SUBSCR    
              190  LOAD_FAST                'self'
              192  STORE_ATTR               stick_mapfile
              194  JUMP_FORWARD        370  'to 370'
            196_0  COME_FROM           182  '182'
            196_1  COME_FROM           172  '172'

 L. 143       196  LOAD_FAST                'self'
              198  LOAD_ATTR                stickcoef
              200  LOAD_CONST               -1
              202  COMPARE_OP               ==
          204_206  POP_JUMP_IF_FALSE   282  'to 282'
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                stickfn
              212  LOAD_STR                 'linear'
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   282  'to 282'

 L. 144       220  LOAD_GLOBAL              float
              222  LOAD_FAST                'sparam'
              224  LOAD_STR                 'epsilon'
              226  BINARY_SUBSCR    
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               epsilon

 L. 145       234  LOAD_STR                 'n'
              236  LOAD_FAST                'sparam'
              238  COMPARE_OP               in
              240  POP_JUMP_IF_FALSE   254  'to 254'
              242  LOAD_GLOBAL              float
              244  LOAD_FAST                'sparam'
              246  LOAD_STR                 'n'
              248  BINARY_SUBSCR    
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           240  '240'
              254  LOAD_CONST               1.0
            256_0  COME_FROM           252  '252'
              256  LOAD_FAST                'self'
              258  STORE_ATTR               n

 L. 146       260  LOAD_GLOBAL              float
              262  LOAD_FAST                'sparam'
              264  LOAD_STR                 'tmin'
              266  BINARY_SUBSCR    
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  LOAD_GLOBAL              u
              272  LOAD_ATTR                K
              274  BINARY_MULTIPLY  
              276  LOAD_FAST                'self'
              278  STORE_ATTR               tmin
              280  JUMP_FORWARD        370  'to 370'
            282_0  COME_FROM           216  '216'
            282_1  COME_FROM           204  '204'

 L. 147       282  LOAD_FAST                'self'
              284  LOAD_ATTR                stickcoef
              286  LOAD_CONST               -1
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   356  'to 356'
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                stickfn
              298  LOAD_STR                 'cossza'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   356  'to 356'

 L. 148       306  LOAD_STR                 'n'
              308  LOAD_FAST                'sparam'
              310  COMPARE_OP               in
          312_314  POP_JUMP_IF_FALSE   328  'to 328'
              316  LOAD_GLOBAL              float
              318  LOAD_FAST                'sparam'
              320  LOAD_STR                 'n'
              322  BINARY_SUBSCR    
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM           312  '312'
              328  LOAD_CONST               1.0
            330_0  COME_FROM           326  '326'
              330  LOAD_FAST                'self'
              332  STORE_ATTR               n

 L. 149       334  LOAD_GLOBAL              float
              336  LOAD_FAST                'sparam'
              338  LOAD_STR                 'tmin'
              340  BINARY_SUBSCR    
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  LOAD_GLOBAL              u
              346  LOAD_ATTR                K
              348  BINARY_MULTIPLY  
              350  LOAD_FAST                'self'
              352  STORE_ATTR               tmin
              354  JUMP_FORWARD        370  'to 370'
            356_0  COME_FROM           302  '302'
            356_1  COME_FROM           290  '290'

 L. 151       356  LOAD_CONST               0
          358_360  POP_JUMP_IF_TRUE    370  'to 370'
              362  LOAD_ASSERT              AssertionError
              364  LOAD_STR                 'sticking_info.stickfn not given or invalid.'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  RAISE_VARARGS_1       1  'exception instance'
            370_0  COME_FROM           358  '358'
            370_1  COME_FROM           354  '354'
            370_2  COME_FROM           280  '280'
            370_3  COME_FROM           194  '194'
            370_4  COME_FROM           162  '162'
            370_5  COME_FROM           144  '144'

 L. 154       370  LOAD_FAST                'self'
              372  LOAD_ATTR                emitfn
              374  LOAD_STR                 'use_map'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   394  'to 394'

 L. 155       382  LOAD_FAST                'sparam'
              384  LOAD_STR                 'accom_mapfile'
              386  BINARY_SUBSCR    
              388  LOAD_FAST                'self'
              390  STORE_ATTR               accom_mapfile
              392  JUMP_FORWARD        468  'to 468'
            394_0  COME_FROM           378  '378'

 L. 156       394  LOAD_FAST                'self'
              396  LOAD_ATTR                emitfn
              398  LOAD_STR                 'maxwellian'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   454  'to 454'

 L. 157       406  LOAD_GLOBAL              float
              408  LOAD_FAST                'sparam'
              410  LOAD_STR                 'accom_factor'
              412  BINARY_SUBSCR    
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  STORE_FAST               'ac'

 L. 158       418  LOAD_FAST                'ac'
              420  LOAD_CONST               0
              422  COMPARE_OP               <
          424_426  POP_JUMP_IF_FALSE   432  'to 432'

 L. 158       428  LOAD_CONST               0.0
              430  STORE_FAST               'ac'
            432_0  COME_FROM           424  '424'

 L. 159       432  LOAD_FAST                'ac'
              434  LOAD_CONST               1
              436  COMPARE_OP               >
          438_440  POP_JUMP_IF_FALSE   446  'to 446'

 L. 159       442  LOAD_CONST               1.0
              444  STORE_FAST               'ac'
            446_0  COME_FROM           438  '438'

 L. 160       446  LOAD_FAST                'ac'
              448  LOAD_FAST                'self'
              450  STORE_ATTR               accom_factor
              452  JUMP_FORWARD        468  'to 468'
            454_0  COME_FROM           402  '402'

 L. 161       454  LOAD_FAST                'self'
              456  LOAD_ATTR                emitfn
              458  LOAD_STR                 'elastic scattering'
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   468  'to 468'

 L. 162       466  JUMP_FORWARD        468  'to 468'
            468_0  COME_FROM           466  '466'
            468_1  COME_FROM           462  '462'
            468_2  COME_FROM           452  '452'
            468_3  COME_FROM           392  '392'

Parse error at or near `COME_FROM' instruction at offset 468_2

    def __str__(self):
        print('sticking_info.stickcoef = {}'.format(self.stickcoef))
        if self.stickfn is not None:
            print('sticking_info.stickfn = {}'.format(self.stickfn))
        if self.tsurf is not None:
            print('sticking_info.tsurf = {}'.format(self.tsurf))
        if self.stick_mapfile is not None:
            print('sticking_info.stick_mapfile = {}'.format(self.stick_mapfile))
        if self.epsilon is not None:
            print('sticking_info.epsilon = {}'.format(self.epsilon))
        if self.n is not None:
            print('sticking_info.n = {}'.format(self.n))
        if self.tmin is not None:
            print('sticking_info.tmin = {}'.format(self.tmin))
        if self.emitfn is not None:
            print('sticking_info.emitfn = {}'.format(self.emitfn))
        if self.accom_mapfile is not None:
            print('sticking_info.accom_mapfile = {}'.format(self.accom_mapfile))
        if self.accom_factor is not None:
            print('sticking_info.accom_factor = {}'.format(self.accom_factor))
        return ''


class Forces:

    def __init__(self, fparam):
        """
        gravity
        radpres
        """
        self.gravity = bool(int(float(fparam['gravity']))) if 'gravity' in fparam else False
        self.radpres = bool(int(float(fparam['radpres']))) if 'radpres' in fparam else False

    def __str__(self):
        print('forces.gravity = {}'.format(self.gravity))
        print('forces.radpres = {}'.format(self.radpres))
        return ''


class SpatialDist:

    def __init__(self, sparam):
        """
        type
        exobase
        use_map
        mapfile
        lonrange
        latrange
        """
        self.type = sparam['type']
        self.exobase = 0.0
        self.use_map = False
        self.mapfile = None
        self.longitude = None
        self.latitude = None
        if self.type == 'surface':
            self.exobase = float(sparam['exobase']) if 'exobase' in sparam else 1.0
            self.use_map = bool(int(sparam['use_map'])) if 'use_map' in sparam else False
            if self.use_map:
                self.mapfile = sparam['mapfile']
            long0 = float(sparam['longitude0']) * u.rad if 'longitude0' in sparam else 0.0 * u.rad
            long1 = float(sparam['longitude1']) * u.rad if 'longitude1' in sparam else 2 * np.pi * u.rad
            lat0 = float(sparam['latitude0']) * u.rad if 'latitude0' in sparam else -np.pi / 2.0 * u.rad
            lat1 = float(sparam['latitude1']) * u.rad if 'latitude1' in sparam else np.pi / 2.0 * u.rad
            self.longitude = (long0, long1)
            self.latitude = (lat0, lat1)
        else:
            if self.type == 'surfacespot':
                self.exobase = float(sparam['exobase']) if 'exobase' in sparam else 1.0
                lon = float(sparam['longitude']) * u.rad if 'longitude' in sparam else 0.0 * u.rad
                lat = float(sparam['latitude']) * u.rad if 'latitude' in sparam else 0 * u.rad
                sigma = float(sparam['sigma']) * u.rad if 'sigma' in sparam else 25 * u.deg
                if sigma < 0 * u.deg:
                    sigma = 0 * u.deg
                else:
                    if sigma > 90 * u.deg:
                        sigma - 90 * u.deg
                    else:
                        self.longitude = (lon, sigma.to(u.rad))
                        self.latitude = (lat, sigma.to(u.rad))
            else:
                if self.type == 'idlversion':
                    if 'idlinputfile' in sparam:
                        self.mapfile = sparam['idlinputfile']
                    else:
                        assert 0, 'Must specify idlinputfile'
                else:
                    assert 0, f"{self.type} distribution not defined yet."

    def __str__(self):
        print('spatialdist.type = {}'.format(self.type))
        print('spatialdist.exobase = {}'.format(self.exobase))
        print('spatialdist.use_map = {}'.format(self.use_map))
        print('spatialdist.mapfile = {}'.format(self.mapfile))
        if self.longitude is None:
            print('spatialdist.longitude is None')
        else:
            print(('spatialdist.longitude = ({:0.2f}, {:0.2f})'.format)(*self.longitude))
        if self.latitude is None:
            print('spatialdist.latitude is None')
        else:
            print(('spatialdist.latitude = ({:0.2f}, {:0.2f})'.format)(*self.latitude))
        return ''


class SpeedDist:
    __doc__ = '\n    type\n    vprob\n    sigma\n    U\n    alpha\n    beta\n    temperature\n    delv\n    '

    def __init__(self, sparam):
        self.type = sparam['type']
        self.vprob = None
        self.sigma = None
        self.U = None
        self.alpha = None
        self.beta = None
        self.temperature = None
        self.delv = None
        if self.type == 'gaussian':
            self.vprob = float(sparam['vprob']) * u.km / u.s
            self.sigma = float(sparam['sigma']) * u.km / u.s
        else:
            if self.type == 'sputtering':
                self.U = float(sparam['u']) * u.eV
                self.alpha = float(sparam['alpha'])
                self.beta = float(sparam['beta'])
            else:
                if self.type == 'maxwellian':
                    self.temperature = float(sparam['temperature']) * u.K
                else:
                    if self.type == 'flat':
                        self.vprob = float(sparam['vprob']) * u.km / u.s
                        self.delv = float(sparam['delv']) * u.km / u.s
                    else:
                        assert 0, 'SpeedDist.type = {} not available'.format(sdist)

    def __str__(self):
        print('SpeedDist.type = {}'.format(self.type))
        if self.vprob is not None:
            print('SpeedDist.vprob = {}'.format(self.vprob))
        if self.sigma is not None:
            print('SpeedDist.sigma = {}'.format(self.sigma))
        if self.U is not None:
            print('SpeedDist.U = {}'.format(self.U))
        if self.alpha is not None:
            print('SpeedDist.alpha = {}'.format(self.alpha))
        if self.beta is not None:
            print('SpeedDist.beta = {}'.format(self.beta))
        if self.temperature is not None:
            print('SpeedDist.temperature = {}'.format(self.temperature))
        if self.delv is not None:
            print('SpeedDist.delv = {}'.format(self.delv))
        return ''


class AngularDist:
    __doc__ = '\n    type\n    azimuth\n    altitude\n    n\n    '

    def __init__--- This code section failed: ---

 L. 368         0  LOAD_STR                 'type'
                2  LOAD_FAST                'aparam'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    16  'to 16'
                8  LOAD_FAST                'aparam'
               10  LOAD_STR                 'type'
               12  BINARY_SUBSCR    
               14  JUMP_FORWARD         18  'to 18'
             16_0  COME_FROM             6  '6'
               16  LOAD_CONST               None
             18_0  COME_FROM            14  '14'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               type

 L. 369        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               azimuth

 L. 370        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               altitude

 L. 371        34  LOAD_CONST               None
               36  LOAD_FAST                'self'
               38  STORE_ATTR               n

 L. 373        40  LOAD_FAST                'self'
               42  LOAD_ATTR                type
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 374     50_52  JUMP_FORWARD        558  'to 558'
             54_0  COME_FROM            48  '48'

 L. 375        54  LOAD_FAST                'self'
               56  LOAD_ATTR                type
               58  LOAD_STR                 'radial'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    68  'to 68'

 L. 376     64_66  JUMP_FORWARD        558  'to 558'
             68_0  COME_FROM            62  '62'

 L. 377        68  LOAD_FAST                'self'
               70  LOAD_ATTR                type
               72  LOAD_STR                 'isotropic'
               74  COMPARE_OP               ==
            76_78  POP_JUMP_IF_FALSE   296  'to 296'

 L. 378        80  LOAD_STR                 'azimuth'
               82  LOAD_FAST                'aparam'
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE   142  'to 142'

 L. 379        88  LOAD_GLOBAL              tuple
               90  LOAD_GENEXPR             '<code_object <genexpr>>'
               92  LOAD_STR                 'AngularDist.__init__.<locals>.<genexpr>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 380        96  LOAD_FAST                'aparam'
               98  LOAD_STR                 'azimuth'
              100  BINARY_SUBSCR    
              102  LOAD_METHOD              split
              104  LOAD_STR                 ','
              106  CALL_METHOD_1         1  '1 positional argument'
              108  GET_ITER         
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               azimuth

 L. 381       118  LOAD_GLOBAL              len
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                azimuth
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  LOAD_CONST               2
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_TRUE    170  'to 170'
              132  LOAD_GLOBAL              AssertionError

 L. 382       134  LOAD_STR                 'AngularDist.azimuth must have two values.'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  RAISE_VARARGS_1       1  'exception instance'
              140  JUMP_FORWARD        170  'to 170'
            142_0  COME_FROM            86  '86'

 L. 384       142  LOAD_CONST               0
              144  LOAD_GLOBAL              u
              146  LOAD_ATTR                rad
              148  BINARY_MULTIPLY  
              150  LOAD_CONST               2
              152  LOAD_GLOBAL              np
              154  LOAD_ATTR                pi
              156  BINARY_MULTIPLY  
              158  LOAD_GLOBAL              u
              160  LOAD_ATTR                rad
              162  BINARY_MULTIPLY  
              164  BUILD_TUPLE_2         2 
              166  LOAD_FAST                'self'
              168  STORE_ATTR               azimuth
            170_0  COME_FROM           140  '140'
            170_1  COME_FROM           130  '130'

 L. 386       170  LOAD_STR                 'altitude'
              172  LOAD_FAST                'aparam'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   232  'to 232'

 L. 387       178  LOAD_GLOBAL              tuple
              180  LOAD_GENEXPR             '<code_object <genexpr>>'
              182  LOAD_STR                 'AngularDist.__init__.<locals>.<genexpr>'
              184  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 388       186  LOAD_FAST                'aparam'
              188  LOAD_STR                 'altitude'
              190  BINARY_SUBSCR    
              192  LOAD_METHOD              split
              194  LOAD_STR                 ','
              196  CALL_METHOD_1         1  '1 positional argument'
              198  GET_ITER         
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  LOAD_FAST                'self'
              206  STORE_ATTR               altitude

 L. 389       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                altitude
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  LOAD_CONST               2
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_TRUE    230  'to 230'
              222  LOAD_ASSERT              AssertionError

 L. 390       224  LOAD_STR                 'AngularDist.altitude must have two values.'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  RAISE_VARARGS_1       1  'exception instance'
            230_0  COME_FROM           220  '220'
              230  JUMP_FORWARD        558  'to 558'
            232_0  COME_FROM           176  '176'

 L. 392       232  LOAD_STR                 'surface'
              234  LOAD_FAST                'spatialdist'
              236  LOAD_ATTR                type
              238  COMPARE_OP               in
              240  POP_JUMP_IF_FALSE   252  'to 252'
              242  LOAD_CONST               0.0
              244  LOAD_GLOBAL              u
              246  LOAD_ATTR                rad
              248  BINARY_MULTIPLY  
              250  JUMP_FORWARD        268  'to 268'
            252_0  COME_FROM           240  '240'

 L. 393       252  LOAD_GLOBAL              np
              254  LOAD_ATTR                pi
              256  UNARY_NEGATIVE   
              258  LOAD_CONST               2.0
              260  BINARY_TRUE_DIVIDE
              262  LOAD_GLOBAL              u
              264  LOAD_ATTR                rad
              266  BINARY_MULTIPLY  
            268_0  COME_FROM           250  '250'
              268  STORE_FAST               'altmin'

 L. 394       270  LOAD_FAST                'altmin'
              272  LOAD_GLOBAL              np
              274  LOAD_ATTR                pi
              276  LOAD_CONST               2.0
              278  BINARY_TRUE_DIVIDE
              280  LOAD_GLOBAL              u
              282  LOAD_ATTR                rad
              284  BINARY_MULTIPLY  
              286  BUILD_TUPLE_2         2 
              288  LOAD_FAST                'self'
              290  STORE_ATTR               altitude
          292_294  JUMP_FORWARD        558  'to 558'
            296_0  COME_FROM            76  '76'

 L. 395       296  LOAD_FAST                'self'
              298  LOAD_ATTR                type
              300  LOAD_STR                 'costheta'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   558  'to 558'

 L. 396       308  LOAD_STR                 'azimuth'
              310  LOAD_FAST                'aparam'
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   374  'to 374'

 L. 397       318  LOAD_GLOBAL              tuple
              320  LOAD_GENEXPR             '<code_object <genexpr>>'
              322  LOAD_STR                 'AngularDist.__init__.<locals>.<genexpr>'
              324  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 398       326  LOAD_FAST                'aparam'
              328  LOAD_STR                 'azimuth'
              330  BINARY_SUBSCR    
              332  LOAD_METHOD              split
              334  LOAD_STR                 ','
              336  CALL_METHOD_1         1  '1 positional argument'
              338  GET_ITER         
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  LOAD_FAST                'self'
              346  STORE_ATTR               azimuth

 L. 399       348  LOAD_GLOBAL              len
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                azimuth
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  LOAD_CONST               2
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_TRUE    402  'to 402'
              364  LOAD_GLOBAL              AssertionError

 L. 400       366  LOAD_STR                 'AngularDist.azimuth must have two values.'
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  RAISE_VARARGS_1       1  'exception instance'
              372  JUMP_FORWARD        402  'to 402'
            374_0  COME_FROM           314  '314'

 L. 402       374  LOAD_CONST               0
              376  LOAD_GLOBAL              u
              378  LOAD_ATTR                rad
              380  BINARY_MULTIPLY  
              382  LOAD_CONST               2
              384  LOAD_GLOBAL              np
              386  LOAD_ATTR                pi
              388  BINARY_MULTIPLY  
              390  LOAD_GLOBAL              u
              392  LOAD_ATTR                rad
              394  BINARY_MULTIPLY  
              396  BUILD_TUPLE_2         2 
              398  LOAD_FAST                'self'
              400  STORE_ATTR               azimuth
            402_0  COME_FROM           372  '372'
            402_1  COME_FROM           360  '360'

 L. 404       402  LOAD_STR                 'altitude'
              404  LOAD_FAST                'aparam'
              406  COMPARE_OP               in
          408_410  POP_JUMP_IF_FALSE   468  'to 468'

 L. 405       412  LOAD_GLOBAL              tuple
              414  LOAD_GENEXPR             '<code_object <genexpr>>'
              416  LOAD_STR                 'AngularDist.__init__.<locals>.<genexpr>'
              418  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 406       420  LOAD_FAST                'aparam'
              422  LOAD_STR                 'altitude'
              424  BINARY_SUBSCR    
              426  LOAD_METHOD              split
              428  LOAD_STR                 ','
              430  CALL_METHOD_1         1  '1 positional argument'
              432  GET_ITER         
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  CALL_FUNCTION_1       1  '1 positional argument'
              438  LOAD_FAST                'self'
              440  STORE_ATTR               altitude

 L. 407       442  LOAD_GLOBAL              len
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                altitude
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  LOAD_CONST               2
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_TRUE    530  'to 530'
              458  LOAD_GLOBAL              AssertionError

 L. 408       460  LOAD_STR                 'AngularDist.altitude must have two values.'
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  RAISE_VARARGS_1       1  'exception instance'
              466  JUMP_FORWARD        530  'to 530'
            468_0  COME_FROM           408  '408'

 L. 410       468  LOAD_STR                 'surface'
              470  LOAD_FAST                'spatialdist'
              472  LOAD_ATTR                type
              474  COMPARE_OP               in
          476_478  POP_JUMP_IF_FALSE   490  'to 490'
              480  LOAD_CONST               0.0
              482  LOAD_GLOBAL              u
              484  LOAD_ATTR                rad
              486  BINARY_MULTIPLY  
              488  JUMP_FORWARD        506  'to 506'
            490_0  COME_FROM           476  '476'

 L. 411       490  LOAD_GLOBAL              np
              492  LOAD_ATTR                pi
            494_0  COME_FROM           230  '230'
              494  UNARY_NEGATIVE   
              496  LOAD_CONST               2.0
              498  BINARY_TRUE_DIVIDE
              500  LOAD_GLOBAL              u
              502  LOAD_ATTR                rad
              504  BINARY_MULTIPLY  
            506_0  COME_FROM           488  '488'
              506  STORE_FAST               'altmin'

 L. 412       508  LOAD_FAST                'altmin'
              510  LOAD_GLOBAL              np
              512  LOAD_ATTR                pi
              514  LOAD_CONST               2.0
              516  BINARY_TRUE_DIVIDE
              518  LOAD_GLOBAL              u
              520  LOAD_ATTR                rad
              522  BINARY_MULTIPLY  
              524  BUILD_TUPLE_2         2 
              526  LOAD_FAST                'self'
              528  STORE_ATTR               altitude
            530_0  COME_FROM           466  '466'
            530_1  COME_FROM           454  '454'

 L. 414       530  LOAD_STR                 'n'
              532  LOAD_FAST                'aparam'
              534  COMPARE_OP               in
          536_538  POP_JUMP_IF_FALSE   552  'to 552'
              540  LOAD_GLOBAL              float
              542  LOAD_FAST                'aparam'
              544  LOAD_STR                 'n'
              546  BINARY_SUBSCR    
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  JUMP_FORWARD        554  'to 554'
            552_0  COME_FROM           536  '536'
              552  LOAD_CONST               1.0
            554_0  COME_FROM           550  '550'
              554  LOAD_FAST                'self'
              556  STORE_ATTR               n
            558_0  COME_FROM           304  '304'
            558_1  COME_FROM           292  '292'
            558_2  COME_FROM            64  '64'
            558_3  COME_FROM            50  '50'

Parse error at or near `COME_FROM' instruction at offset 506_0

    def __str__(self):
        print('AngularDist.type = {}'.format(self.type))
        if self.altitude is not None:
            print(('AngularDist.altitude = ({:0.2f}, {:0.2f})'.format)(*self.altitude))
        if self.azimuth is not None:
            print(('AngularDist.azimuth = ({:0.2f}, {:0.2f})'.format)(*self.azimuth))
        if self.n is not None:
            print('AngularDist.n = {}'.format(self.n))
        return ''


class Options:
    __doc__ = '\n    endtime\n    resolution\n    at_once\n    atom\n    lifetime\n    fullsystem\n    outeredge\n    motion\n    streamlines\n    nsteps\n    '

    def __init__(self, oparam, planet):
        self.endtime = float(oparam['endtime']) * u.s
        self.at_once = bool(int(oparam['at_once'])) if 'at_once' in oparam else False
        self.atom = oparam['atom'].title()
        self.motion = bool(int(oparam['motion'])) if 'motion' in oparam else True
        self.lifetime = float(oparam['lifetime']) * u.s if 'lifetime' in oparam else 0.0 * u.s
        if 'fullsystem' in oparam:
            self.fullsystem = bool(int(oparam['fullsystem']))
        else:
            self.fullsystem = False if planet == 'Mercury' else True
        if not self.fullsystem:
            self.outeredge = float(oparam['outeredge']) if 'outeredge' in oparam else 20.0
        else:
            self.outeredge = None
        self.streamlines = bool(int(oparam['streamlines'])) if 'streamlines' in oparam else False
        if self.streamlines:
            self.nsteps = int(oparam['nsteps']) if 'nsteps' in oparam else 1000
            self.resolution = None
        else:
            self.nsteps = None
            self.resolution = float(oparam['resolution']) if 'resolution' in oparam else 0.001

    def __str__(self):
        print('options.endtime = {}'.format(self.endtime))
        print('options.resolution = {}'.format(self.resolution))
        print('options.at_once = {}'.format(self.at_once))
        print('options.atom = {}'.format(self.atom))
        print('options.motion = {}'.format(self.motion))
        print('options.lifetime = {}'.format(self.lifetime))
        print('options.fullsystem = {}'.format(self.fullsystem))
        if self.outeredge is not None:
            print('options.outeredge = {}'.format(self.outeredge))
        print('options.streamlines = {}'.format(self.streamlines))
        if self.nsteps is not None:
            print('options.nsteps = {}'.format(self.nsteps))
        return ''