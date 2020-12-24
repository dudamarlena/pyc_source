# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/data/curve.py
# Compiled at: 2020-04-11 22:28:15
# Size of source mod 2**32: 13267 bytes
"""
This module include data class for curves
"""
from __future__ import print_function, division, absolute_import
import tpDcc as tp, tpDcc.dccs.maya as maya
from tpDcc.core import data
from tpDcc.dccs.maya.core import exceptions, curve as curve_utils

class CurveData(data.Data, object):

    def __init__(self, curve=''):
        super(CurveData, self).__init__()
        self._curve = curve
        self.world_space = False
        if self._curve:
            self.build_data()

    def build_data(self):
        """
        Data is build from the given scene objects
        """
        if not self._curve:
            tp.logger.exception('No Curves Given')
        if type(self._curve) not in [list, tuple]:
            self._curve = [
             self._curve]
        shapes = maya.cmds.listRelatives((self._curve), shapes=True, pa=True) or []
        curves = maya.cmds.ls(shapes, type='nurbsCurve')
        curves += maya.cmds.ls(curves, type='nurbsCurve') or []
        if not curves:
            return
        else:
            self.reset()
            for crv in curves:
                cv_array = list()
                world_cv_array = list()
                knot_settings = list()
                knot_settings_world = list()
                curve_fn = curve_utils.get_curve_fn(curve=crv)
                if tp.is_new_api():
                    point_array = curve_fn.cvPositions(maya.OpenMaya.MSpace.kObject)
                    world_point_array = curve_fn.cvPositions(maya.OpenMaya.MSpace.kWorld)
                else:
                    point_array = maya.OpenMaya.MPointArray()
                    world_point_array = maya.OpenMaya.MPointArray()
                    curve_fn.getCVs(point_array, maya.OpenMaya.MSpace.kObject)
                    curve_fn.getCVs(world_point_array, maya.OpenMaya.MSpace.kWorld)
                point_array_length = point_array.length() if hasattr(point_array, 'length') else len(point_array)
                for i in range(point_array_length):
                    cv_array.append([point_array[i].x, point_array[i].y, point_array[i].z])
                    world_cv_array.append([world_point_array[i].x, world_point_array[i].y, world_point_array[i].z])

                self._data[crv] = [
                 cv_array, world_cv_array]

            return curves

    def rebuild(self, controls=[]):
        """
        Rebuild curve from already build data
        :param controls: list<str>, list of controls curve shapes to rebuild
        """
        data_keys = self._data.keys()
        if not data_keys:
            return
        else:
            if not controls:
                controls = data_keys
            if type(controls) not in [list, tuple]:
                controls = [
                 controls]
            for ctrl in controls:
                if not maya.cmds.objExists(ctrl):
                    tp.logger.warning('CurveData: Curve Shape "{}" does not exists!'.format(ctrl))
                elif not data_keys.count(ctrl):
                    tp.logger.warning('CurveData: No Data for Curve Shape "{}"'.format(ctrl))
                else:
                    point_array = maya.OpenMaya.MPointArray()
                    if self.world_space:
                        crv = self._data[ctrl][1]
                    else:
                        crv = self._data[ctrl][0]
                    for cv in crv:
                        point_array.append(maya.OpenMaya.MPoint(cv[0], cv[1], cv[2], 1.0))

                    curve_fn = curve_utils.get_curve_fn(curve=ctrl)
                    if self.world_space:
                        curve_fn.setCVs(point_array, maya.OpenMaya.MSpace.kWorld)
                    else:
                        curve_fn.setCVs(point_array, maya.OpenMaya.MSpace.kObject)
                    curve_fn.updateCurve()

            return controls


class NurbsCurveData(CurveData, object):

    def __init__(self, curve=''):
        super(NurbsCurveData, self).__init__()
        self._curve = curve
        self.world_space = False
        self._data['name'] = ''
        self._data['cv'] = list()
        self._data['editPt'] = list()
        self._data['knots'] = list()
        self._data['degree'] = 0
        self._data['form'] = 0
        self._data['2d'] = False
        self._data['rational'] = True
        if self._curve:
            self.build_data()

    def build_data(self):
        """
        Data is build from the given scene objects
        """
        if not self._curve:
            tp.logger.exception('No Curve Given')
        else:
            if not curve_utils.is_curve(curve=(self._curve)):
                raise exceptions.NURBSCurveException(curve=(self._curve))
            space = maya.OpenMaya.MSpace.kWorld
            if self.world_space:
                space = maya.OpenMaya.MSpace.kWorld
            timer = maya.cmds.timerX()
            curve_fn = curve_utils.get_curve_fn(curve=(self._curve))
            self._data['name'] = self._curve
            if tp.is_new_api():
                knot_array = curve_fn.knots()
                cv_array = curve_fn.cvs(space)
                cv_length = len(cv_array)
                self._data['degree'] = curve_fn.degree
                self._data['form'] = int(curve_fn.form)
            else:
                knot_array = maya.OpenMaya.MDoubleArray()
                cv_array = maya.OpenMaya.MPointArray()
                curve_fn.getKnots(knot_array)
                curve_fn.getCVs(cv_array, space)
            cv_length = cv_array.length()
            self._data['degree'] = int(curve_fn.degree())
            self._data['form'] = int(curve_fn.form())
        self._data['knots'] = list(knot_array)
        self._data['cvs'] = [(cv_array[i].x, cv_array[i].y, cv_array[i].z) for i in range(cv_length)]
        for u in self._data['knots']:
            if tp.is_new_api():
                edit_pt = curve_fn.getPointAtParam(u, space)
            else:
                edit_pt = maya.OpenMaya.MPoint()
            try:
                curve_fn.getPointAtParam(u, edit_pt, space)
            except Exception:
                continue

            self._data['editPt'].append((edit_pt.x, edit_pt.y, edit_pt.z))

        build_time = maya.cmds.timerX(st=timer)
        tp.logger.debug('NurbsCurveData: Data build time for curve "{}" : {}'.format(self._data['name'], str(build_time)))
        return self._data['name']

    def rebuild(self):
        timer = maya.cmds.timerX()
        num_cvs = len(self._data['cvs'])
        num_knots = len(self._data['knots'])
        if tp.is_new_api():
            cv_array = maya.OpenMaya.MPointArray(num_cvs, maya.OpenMaya.MPoint.kOrigin)
            knots = maya.OpenMaya.MDoubleArray(num_knots, 0)
            for i in range(num_cvs):
                cv_array[i] = maya.OpenMaya.MPoint(self._data['cvs'][i][0], self._data['cvs'][i][1], self._data['cvs'][i][2], 1.0)

            for i in range(num_knots):
                knots[i] = self._data[knots][i]

        else:
            cv_array = maya.OpenMaya.MPointArray(num_cvs, maya.OpenMaya.MPoint.origin)
            knots = maya.OpenMaya.MDoubleArray(num_knots, 0)
            for i in range(num_cvs):
                cv_array.set(maya.OpenMaya.MPoint(self._data['cvs'][i][0], self._data['cvs'][i][1], self._data['cvs'][i][2], 1.0), i)

            for i in range(num_knots):
                knots.set(self._data['knots'][i], i)

        curve_fn = maya.OpenMaya.MFnNurbsCurve()
        curve_data = maya.OpenMaya.MFnNurbsCurveData().create()
        curve_obj = curve_fn.create(cv_array, knots, self._data['degree'], self._data['form'], self._data['2d'], self._data['rational'], curve_data)
        curve_obj_handle = maya.OpenMaya.MObjectHandle(curve_obj)
        build_time = maya.cmds.timerX(st=timer)
        tp.logger.debug('NurbsCurveData: Data rebuild time for curve "{}" : {}'.format(self._data['name'], str(build_time)))
        return curve_obj_handle

    def rebuild_curve(self):
        timer = maya.cmds.timerX()
        num_cvs = len(self._data['cvs'])
        num_knots = len(self._data['knots'])
        if tp.is_new_api():
            cv_array = maya.OpenMaya.MPointArray(num_cvs, maya.OpenMaya.MPoint.kOrigin)
            knots = maya.OpenMaya.MDoubleArray(num_knots, 0)
            for i in range(num_cvs):
                cv_array[i] = maya.OpenMaya.MPoint(self._data['cvs'][i][0], self._data['cvs'][i][1], self._data['cvs'][i][2], 1.0)

            for i in range(num_knots):
                knots[i] = self._data[knots][i]

        else:
            cv_array = maya.OpenMaya.MPointArray(num_cvs, maya.OpenMaya.MPoint.origin)
            knots = maya.OpenMaya.MDoubleArray(num_knots, 0)
            for i in range(num_cvs):
                cv_array.set(maya.OpenMaya.MPoint(self._data['cvs'][i][0], self._data['cvs'][i][1], self._data['cvs'][i][2], 1.0), i)

            for i in range(num_knots):
                knots.set(self._data['knots'][i], i)

        curve_fn = maya.OpenMaya.MFnNurbsCurve()
        curve_data = maya.OpenMaya.MObject()
        curve_obj = curve_fn.create(cv_array, knots, self._data['degree'], self._data['form'], self._data['2d'], self._data['rational'], curve_data)
        crv = maya.OpenMaya.MFnDependencyNode(curve_obj).setName(self._data['name'])
        build_time = maya.cmds.timerX(st=timer)
        tp.logger.debug('NurbsCurveData: Curve rebuild time for curve "{}" : {}'.format(self._data['name'], str(build_time)))