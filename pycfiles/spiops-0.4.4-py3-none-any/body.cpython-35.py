# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/classes/body.py
# Compiled at: 2018-07-19 04:54:11
# Size of source mod 2**32: 11574 bytes
import spiceypy as cspice, numpy as np
from spiops.utils import utils

class Body(object):

    def __init__(self, body, time=object(), target=None):
        if isinstance(body, str):
            name = body
            id = cspice.bodn2c(body)
        else:
            id = body
            name = cspice.bodc2n(body)
        if target:
            self.target = target
        self.name = name
        self.id = id
        self.time = time
        self.previous_tw = []
        self.geometry_flag = False

    def __getattribute__(self, item):
        if item in ('altitude', 'distance', 'zaxis_target_angle', 'zaxis_earth_angle'):
            self._Body__Geometry()
            return object.__getattribute__(self, item)
        else:
            if item in ('sa_ang_p', 'sa_ang_n', 'sa_ang', 'saa_sa', 'saa_sc', 'hga_earth',
                        'hga_el_az'):
                self._Body__Structures()
                return object.__getattribute__(self, item)
            return object.__getattribute__(self, item)

    def __getattr__(self, item):
        if item in ('state_in_window', ):
            self._Body__StateInWindow()
            return object.__getattribute__(self, item)

    def State(self, target=False, reference_frame=False, current=False):
        if self.target and not target and not reference_frame:
            target = self.target.name
            reference_frame = self.target.frame
        if not self.target:
            if target is False:
                target = 'J2000'
            if reference_frame is False:
                reference_frame = 'J2000'
        self.trajectory_reference_frame = reference_frame
        if not current:
            current = self.time.current
        state, lt = cspice.spkezr(target, current, reference_frame, self.time.abcorr, self.name)
        return state

    def Orientation(self, frame='', target_frame='', current=False, format='msop quaternions'):
        if self.target and not target_frame:
            target_frame = self.target.frame
        if not self.target and not target_frame:
            target_frame = 'J2000'
        if not frame:
            frame = self.frame
        if not current:
            current = self.time.current
        else:
            current = current
        rot_mat = cspice.pxform(target_frame, frame, current)
        if format == 'spice quaternions':
            orientation = cspice.m2q(rot_mat)
        if format == 'msop quaternions':
            quaternions = cspice.m2q(rot_mat)
            orientation = [-quaternions[1],
             -quaternions[2],
             -quaternions[3],
             quaternions[0]]
        else:
            if format == 'euler angles':
                orientation = cspice.m2eul(rot_mat, 3, 2, 1)
            elif format == 'rotation matrix':
                orientation = rot_mat
        return orientation

    def __StateInWindow(self, target=False, reference_frame=False, start=False, finish=False):
        state_in_window = []
        for et in self.time.window:
            state_in_window.append(self.State(target, reference_frame, et))

        self.state_in_window = state_in_window

    def __Structures(self):
        if self.structures_flag is True and self.time.window.all() == self.previous_tw.all():
            return
        time = self.time
        import spiops
        sa_ang_p_list = []
        sa_ang_n_list = []
        saa_sa_list = []
        saa_sc_list = []
        hga_earth = []
        hga_angles = []
        for et in time.window:
            sa_ang_p = spiops.solar_array_angle('TGO_SA+Z', et)
            sa_ang_n = spiops.solar_array_angle('TGO_SA+Z', et)
            saa = spiops.solar_aspect_angles('TGO', et)
            sa_ang_p_list.append(sa_ang_p)
            sa_ang_n_list.append(sa_ang_n)
            saa_sa_list.append(saa[0])
            saa_sc_list.append(saa[1])
            hga_angles, hga_earth = spiops.hga_angles('MPO', et)

        self.sa_ang_p = sa_ang_p_list
        self.sa_ang_n = sa_ang_n_list
        self.sa_ang = [sa_ang_p_list, sa_ang_n_list]
        self.saa_sa = saa_sa_list
        self.saa_sc = saa_sc_list
        self.hga_earth = hga_earth
        self.hga_angles = hga_angles
        self.structures_flag = True
        self.previous_tw = self.time.window

    def __Geometry(self):
        distance = []
        altitude = []
        subpoint_xyz = []
        subpoint_pgc = []
        subpoint_pcc = []
        zaxis_target_angle = []
        tar = self.target
        time = self.time
        for et in time.window:
            ptarg, lt = cspice.spkpos(tar.name, et, tar.frame, time.abcorr, self.name)
            vout, vmag = cspice.unorm(ptarg)
            distance.append(vmag)
            spoint, trgepc, srfvec = cspice.subpnt(tar.method, tar.name, et, tar.frame, time.abcorr, self.name)
            subpoint_xyz.append(spoint)
            dist = cspice.vnorm(srfvec)
            altitude.append(dist)
            spglon, spglat, spgalt = cspice.recpgr(tar.name, spoint, tar.radii_equ, tar.flat)
            spglon *= cspice.dpr()
            spglat *= cspice.dpr()
            subpoint_pgc.append([spglon, spglat, spgalt])
            spcrad, spclon, spclat = cspice.reclat(spoint)
            spclon *= cspice.dpr()
            spclat *= cspice.dpr()
            subpoint_pcc.append([spcrad, spclon, spclat])
            obs_tar, ltime = cspice.spkpos(tar.name, et, 'J2000', time.abcorr, self.name)
            obs_zaxis = [0, 0, 1]
            try:
                matrix = cspice.pxform(self.frame, 'J2000', et)
                vecout = cspice.mxv(matrix, obs_zaxis)
                zax_target_angle = cspice.vsep(vecout, obs_tar)
                zax_target_angle *= cspice.dpr()
                zaxis_target_angle.append(zax_target_angle)
            except:
                zaxis_target_angle.append(0.0)

        self.distance = distance
        self.altitude = altitude
        self.subpoint_xyz = subpoint_xyz
        self.subpoint_pgc = subpoint_pgc
        self.subpoint_pcc = subpoint_pcc
        self.zaxis_target_angle = zaxis_target_angle
        self.geometry_flag = True
        self.previous_tw = self.time.window

    def Plot(self, yaxis='distance', date_format='TDB', external_data=[], notebook=False):
        self._Body__Geometry()
        self._Body__Structures()
        if yaxis == 'sa_ang':
            yaxis_name = [
             'sa_ang_p', 'sa_ang_n']
        else:
            if yaxis == 'saa_sc':
                yaxis_name = [
                 'saa_sc_x', 'saa_sc_y', 'saa_sc_z']
            else:
                if yaxis == 'saa_sa':
                    if self.name != 'MPO':
                        yaxis_name = [
                         'saa_sa_p', 'saa_sa_n']
                    else:
                        yaxis_name = [
                         'saa_sa']
                else:
                    if yaxis == 'hga_angles':
                        yaxis_name = [
                         'hga_el', 'hga_az']
                    else:
                        yaxis_name = yaxis
        utils.plot(self.time.window, self.__getattribute__(yaxis), notebook=notebook, external_data=external_data, yaxis_name=yaxis_name, mission=self.name, target=self.target.name, date_format=date_format)

    def Plot3D(self, data='trajectory', reference_frame=False):
        if not self.state_in_window:
            self._Body__StateInWindow(reference_frame=reference_frame)
        data = self.state_in_window
        utils.plot3d(data, self, self.target)


class Target(Body):

    def __init__(self, body, time=object(), target=False, frame='', method='INTERCEPT/ELLIPSOID'):
        """

        :param body:
        :type body:
        :param time:
        :type time:
        :param target: It no target is provided the default is 'SUN'
        :type target:
        :param frame:
        :type frame:
        :param method:
        :type method:
        """
        if not target:
            target = Target('SUN', time=time, target=object())
        super(Target, self).__init__(body, time=time, target=target)
        if not frame:
            self.frame = 'IAU_{}'.format(self.name)
        else:
            self.frame = frame
        self.method = method
        self._Target__getRadii()

    def __getRadii(self):
        try:
            self.radii = cspice.bodvar(self.id, 'RADII', 3)
        except:
            print('Ephemeris object has no radii')
            return

        self.radii_equ = self.radii[0]
        self.radii_pol = self.radii[2]
        self.flat = (self.radii_equ - self.radii_pol) / self.radii_equ


class Observer(Body):

    def __init__(self, body, time=object(), target=False, frame=''):
        super(Observer, self).__init__(body, time=time, target=target)
        if not frame:
            self.frame = '{}_SPACECRAFT'.format(self.name)
            if cspice.namfrm(self.frame) == 0:
                self.frame = self.name
            if cspice.namfrm(self.frame) == 0:
                self.frame = '{}_LANDER'.format(self.name)
                print('The frame name has not been able to be built; please introduce it manually')
        else:
            self.frame = frame