# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/spiops.py
# Compiled at: 2017-07-31 20:38:34
import math, spiceypy as cspice
from spiceypy.utils.support_types import *
from .utils import time

def fov_illum(mk, sensor, time=None, angle='DEGREES', report=False):
    """
    Determine the Illumination of a given FoV (for light scattering computatons
    for example). Mainly uses the following SPICE APIs:

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html

    :param mk: Meta-kernel to load the computation scenario
    :type mk: str
    :param sensor: Sensor id code or name
    :type sensor: Union[str, int]
    :param time: Time to compute the quantity
    :type time: Union[str, float]
    :param angle: Angular unit it can be 'DEGREES' or 'RADIANS'
    :type angle: str
    :param report: If True prints the resulting illumination angle on the screen
    :type report: bool
    :return: Angle in between a sensor's boresight and the sun-sc direction
    :rtype: float
    """
    cspice.furnsh(mk)
    angle = angle.upper()
    room = 99
    shapelen = 1000
    framelen = 1000
    if time:
        time = cspice.utc2et(time)
    else:
        time = cspice.utc2et('2016-08-10T00:00:00')
    if angle != 'DEGREES' and angle != 'RADIANS':
        print 'angle should be either degrees or radians'
    if isinstance(sensor, str):
        instid = cspice.bodn2c(sensor)
    else:
        instid = sensor
    shape, frame, bsight, n, bounds = cspice.getfov(instid, room, shapelen, framelen)
    rotation = cspice.pxform(frame, 'J2000', time)
    bsight = cspice.mxv(rotation, bsight)
    sc_id = int(str(instid)[:-3])
    ptarg, lt = cspice.spkezp(10, time, 'J2000', 'LT+S', sc_id)
    fov_illumination = cspice.vsep(bsight, ptarg)
    cspice.kclear()
    if angle == 'DEGREES':
        return math.degrees(fov_illumination)
    else:
        return fov_illumination


def cov_spk_obj(mk, object, time_format='TDB', global_boundary=False, report=False, unload=False):
    cspice.furnsh(mk)
    boundaries_list = []
    et_boundaries_list = []
    object_id = cspice.bodn2c(object)
    maxwin = 2000
    spk_count = cspice.ktotal('SPK') - 1
    while spk_count >= 0:
        spk_kernel = cspice.kdata(spk_count, 'SPK', 155, 155, 155)
        spk_ids = cspice.spkobj(spk_kernel[0])
        for id in spk_ids:
            if id == object_id:
                object_cov = SPICEDOUBLE_CELL(maxwin)
                cspice.spkcov(spk_kernel[0], object_id, object_cov)
                boundaries = time.cov_int(object_cov=object_cov, object_id=object_id, kernel=spk_kernel[0], global_boundary=global_boundary, time_format=time_format, report=report)
                boundaries_list.append(boundaries)
                if global_boundary:
                    et_boundaries_list.append(cov_int(object_cov=object_cov, object_id=object_id, kernel=spk_kernel[0], global_boundary=True, time_format='TDB', report=False))

        spk_count -= 1

    if global_boundary:
        start_time = min(et_boundaries_list)[0]
        finish_time = max(et_boundaries_list)[1]
        boundaries_list = time.et2cal([start_time, finish_time], format=time_format)
        if report:
            print ('Global Coverage for {} [{}]: {} - {}').format(str(cspice.bodc2n(object_id)), time_format, boundaries_list[0], boundaries_list[1])
    if unload:
        cspice.unload(mk)
    return boundaries_list


def cov_spk_ker(spk, support_ker, object='ALL', time_format='TDB', report=False, unload=False):
    cspice.furnsh(spk)
    maxwin = 2000
    cspice.furnsh(support_ker)
    boundaries_list = []
    boundaries = []
    spk_ids = cspice.spkobj(spk)
    if object == 'ALL':
        object_id = spk_ids
    else:
        object_id = cspice.bodn2c(object)
    for id in spk_ids:
        if id == object_id:
            object_cov = SPICEDOUBLE_CELL(maxwin)
            cspice.spkcov(spk, object_id, object_cov)
            boundaries = time.cov_int(object_cov=object_cov, object_id=object_id, kernel=spk, time_format=time_format, report=report)
        boundaries_list += boundaries
        if unload:
            cspice.unload(spk)

    return boundaries_list


def cov_ck_obj(mk, object, time_format='UTC', global_boundary=False, report=False, unload=False):
    cspice.furnsh(mk)
    boundaries_list = []
    et_boundaries_list = []
    object_id = cspice.namfrm(object)
    MAXIV = 2000
    ck_count = cspice.ktotal('CK') - 1
    WINSIZ = 2 * MAXIV
    MAXOBJ = 10000
    while ck_count >= 0:
        ck_ids = cspice.support_types.SPICEINT_CELL(MAXOBJ)
        ck_kernel = cspice.kdata(ck_count, 'CK', 155, 155, 155)
        ck_ids = cspice.ckobj(ck=ck_kernel[0], outCell=ck_ids)
        for id in ck_ids:
            if id == object_id:
                object_cov = cspice.support_types.SPICEDOUBLE_CELL(WINSIZ)
                object_cov = cspice.ckcov(ck=ck_kernel[0], idcode=object_id, needav=False, level='SEGMENT', tol=0.0, timsys='TDB', cover=object_cov)
                boundaries = time.cov_int(object_cov=object_cov, object_id=object_id, kernel=ck_kernel[0], global_boundary=global_boundary, time_format=time_format, report=report)
                boundaries_list.append(boundaries)
                if global_boundary:
                    et_boundaries_list.append(time.cov_int(object_cov=object_cov, object_id=object_id, kernel=ck_kernel[0], global_boundary=True, time_format='TDB', report=False))

        ck_count -= 1

    if global_boundary:
        start_time = min(et_boundaries_list)[0]
        finish_time = max(et_boundaries_list)[1]
        boundaries_list = time.et2cal([start_time, finish_time], format=time_format)
        if report:
            try:
                body_name = cspice.bodc2n(object_id)
            except:
                body_name = cspice.frmnam(object_id, 60)

            print ('Global Coverage for {} [{}]: {} - {}').format(body_name, time_format, boundaries_list[0], boundaries_list[1])
    if unload:
        cspice.unload(mk)
    return boundaries_list


def cov_ck_ker(ck, support_ker, object='ALL', time_format='UTC', report=False, unload=False):
    cspice.furnsh(ck)
    if isinstance(support_ker, str):
        support_ker = [
         support_ker]
    for ker in support_ker:
        cspice.furnsh(ker)

    boundaries_list = []
    boundaries = []
    object_id = cspice.namfrm(object)
    MAXIV = 2000
    WINSIZ = 2 * MAXIV
    MAXOBJ = 10000
    if object == 'ALL':
        ck_ids = cspice.support_types.SPICEINT_CELL(MAXOBJ)
        ck_ids = cspice.ckobj(ck, outCell=ck_ids)
    else:
        ck_ids = [
         cspice.namfrm(object)]
    for id in ck_ids:
        if id == object_id:
            object_cov = cspice.support_types.SPICEDOUBLE_CELL(WINSIZ)
            (cspice.scard, 0, object_cov)
            object_cov = cspice.ckcov(ck=ck, idcode=object_id, needav=False, level='SEGMENT', tol=0.0, timsys='TDB', cover=object_cov)
            boundaries = time.cov_int(object_cov=object_cov, object_id=object_id, kernel=ck, time_format=time_format, report=report)

    if boundaries != []:
        boundaries_list += boundaries
    if unload:
        cspice.unload(ck)
    return boundaries_list