# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/distance.py
# Compiled at: 2020-04-24 23:10:50
# Size of source mod 2**32: 1323 bytes
"""
Module that contains functions and classes related with attributes
"""
from __future__ import print_function, division, absolute_import

def get_closest_distance_info(source=None, targets=None, mode='close', res_mode='point', source_pivot='rp', target_pivot='rp'):
    """
    Returns the closest return based on a source and target and given modes
    :param source: str, base object to measure from
    :param targets: list<stt>, list of object types
    :param mode: str, what mode we are checking dat from (close or far)
    :param res_mode: str
        - object: return the [closest] target
        - point: retur the [closest] point
        - component: resturn the [closest] base component
        - pointOnSurface: [closest] point on the target shape(s)
        - pointOnSurfaceLoc: [closest] point on target shape(s) loc'd
        - shape: gets closest point on every shape, returns closest
    :param source_pivot: str
    :param target_pivot:str
    :return: tuple(res, distance)
    """
    fn_name = 'get_closest_distance_info'

    def get_from_targets(source_pos, targets, target_pivot, res_mode, mode):
        pass

    dist_modes_dict = {'close':[
      'closest', 'c', 'near'], 
     'far':['furthest', 'long']}
    source = None