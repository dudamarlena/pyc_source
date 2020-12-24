# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/disk9/cfse/dettmann/code/airinnova/pytornado/src/lib/pytornado/aero/vlm.py
# Compiled at: 2019-09-25 04:24:27
# Size of source mod 2**32: 20439 bytes
"""
Functions for the discretisation of the aircraft geometry into panels.

Developed for AIRINNOVA AB, Stockholm, Sweden.
"""
import logging
from math import ceil
import numpy as np, scipy.linalg.lapack as lapack
from commonlibs.math.vectors import axis_rot_matrix
from commonlibs.math.interpolation import lin_interpol
from pytornado.objects.vlm_struct import VLMLattice
import pytornado.aero.c_vlm as c_vlm, pytornado.objects.objecttools as ot
from pytornado.objects.vlm_struct import BookKeepingEntry
from pytornado.objects.aircraft import get_abs_segment_point_coords
logger = logging.getLogger(__name__)
MIN_AUTOPANELS = 1

def set_autopanels(aircraft, settings):
    """
    Automatically set chord- and spanwise discretisation settings

    Args:
        :aircraft: (object) data structure for aircraft geometry
        :autopanels_c: (int) number of chordwise panels on the main wing
        :autopanels_s: (int) number of spanwise panels on the main wing
    """
    autopanels_c = settings.settings.get('vlm_autopanels_c', MIN_AUTOPANELS)
    autopanels_s = settings.settings.get('vlm_autopanels_s', MIN_AUTOPANELS)
    for this_segment, _ in ot.all_segments(aircraft):
        segment = this_segment[2]
        if segment.panels['num_c'] is None:
            segment.panels['num_c'] = autopanels_c
        if segment.panels['num_s'] is None:
            wing_span = segment.parent_wing.span
            segment_span = segment.geometry['span']
            segment.panels['num_s'] = ceil(segment_span / wing_span * autopanels_s)

    for this_control, this_wing in ot.all_controls(aircraft):
        control = this_control[2]
        if control.panels['num_c'] is None:
            control.panels['num_c'] = autopanels_c


def pre_panelling(aircraft):
    """
    Create subdivisions and subareas for all aircraft wings

    Note:
        * This routine divides the wing into subdivisions and subareas
          in order to generate a suitable mesh for wing with control surfaces.
        * In a first step "mandatory" subdivisions are made: The wing is divided
          into a minimum amount of subareas according to the leading and trailing
          edge control surfaces.
        * In a second step further spanwise subdivisions are added.

    Args:
        :aircraft: (obj) aircraft object
    """
    for this_control, this_wing in ot.all_controls(aircraft):
        control = this_control[2]
        wing = this_wing[2]
        segment_inner_name = control.segment_uid['inner']
        segment_outer_name = control.segment_uid['outer']
        eta_inner = control.rel_vertices['eta_inner']
        eta_outer = control.rel_vertices['eta_outer']
        xsi_inner = control.rel_vertices['xsi_inner']
        xsi_outer = control.rel_vertices['xsi_outer']
        xsi_h1 = control.rel_hinge_vertices['xsi_inner']
        xsi_h2 = control.rel_hinge_vertices['xsi_outer']
        if segment_inner_name == segment_outer_name:
            wing.segments[segment_inner_name].add_subdivision_for_control(eta_inner, eta_outer, control, xsi_inner, xsi_outer, xsi_h1, xsi_h2)
        else:
            list_of_segments = []
            inner_set = False
            outer_set = False
            xsi_avg = (xsi_inner + xsi_outer) / 2
            xsi_h_avg = (xsi_h1 + xsi_h2) / 2
            for segment_uid in wing.segments.keys():
                if segment_uid == segment_inner_name:
                    inner_set = True
                    list_of_segments.append([segment_uid, eta_inner, 1, xsi_inner, xsi_avg, xsi_h1, xsi_h_avg])
                    continue
                else:
                    if inner_set:
                        if not outer_set:
                            list_of_segments.append([segment_uid, 0, 1, xsi_avg, xsi_avg, xsi_h_avg, xsi_h_avg])
                            if segment_uid == segment_outer_name:
                                outer_set = True
                                list_of_segments[(-1)][2] = eta_outer
                                list_of_segments[(-1)][4] = xsi_outer
                                list_of_segments[(-1)][6] = xsi_h2
                                break

            if xsi_inner != xsi_outer or xsi_h1 != xsi_h2:
                control_len = [0]
                for row in list_of_segments:
                    segment_uid, eta_i, eta_o, xsi_i, xsi_o, xsi_hi, xsi_ho = row
                    segment = wing.segments[segment_uid]
                    segment_vertices = segment.vertices
                    a = get_abs_segment_point_coords(segment_vertices, eta_i, xsi_i)
                    b = get_abs_segment_point_coords(segment_vertices, eta_o, xsi_o)
                    ab = b - a
                    l = control_len[(-1)]
                    control_len.append(l + np.sqrt(np.dot(ab, ab)))

                l = control_len[(-1)]
                for i, row in enumerate(list_of_segments):
                    segment_uid, eta_i, eta_o, xsi_i, xsi_o, xsi_hi, xsi_ho = row
                    l_i = control_len[i]
                    l_o = control_len[(i + 1)]
                    xsi_i = lin_interpol((xsi_inner, xsi_outer), (0, l), l_i)
                    xsi_o = lin_interpol((xsi_inner, xsi_outer), (0, l), l_o)
                    xsi_hi = lin_interpol((xsi_h1, xsi_h2), (0, l), l_i)
                    xsi_ho = lin_interpol((xsi_h1, xsi_h2), (0, l), l_o)
                    list_of_segments[i] = [
                     segment_uid, eta_i, eta_o, xsi_i, xsi_o, xsi_hi, xsi_ho]

            for row in list_of_segments:
                segment_uid, eta_i, eta_o, xsi_i, xsi_o, xsi_h1, xsi_h2 = row
                wing.segments[segment_uid].add_subdivision_for_control(eta_i, eta_o, control, xsi_i, xsi_o, xsi_h1, xsi_h2)

    for this_segment, _ in ot.all_segments(aircraft):
        segment = this_segment[2]
        for eta in np.linspace(0, 1, segment.panels['num_s'] + 1):
            if not eta == 0:
                if eta == 1:
                    pass
                else:
                    segment.add_subdivision(eta, eta, ignore_inval_eta=True)


def gen_lattice(aircraft, state, settings, make_new_subareas=True):
    """
    Generate aircraft lattice

    Perform count of number of wings, segments, controls, panels and strips.
    Pre-allocate memory for lattice data, which is directly operated on in C.

    The function `py2c_lattice` is called which generates the VLM lattice.
    The following lattice data (for all panel) is generated:

        * :lattice.p: panel corner points
        * :lattice.v: panel vortex filament endpoints
        * :lattice.c: panel collocation point
        * :lattice.n: panel normal vector
        * :lattice.a: panel surface area

    When `py2c_lattice` is called it takes the following input arguments:

        * :lattice: pre-allocated memory for the struct described above
        * :array_segments: segment corner points (N*4*3)
        * :array_airfoils: file names for airfoils at inner and outer segment (N*2)
        * :array_symmetry: segment symmetry information (N)
        * :array_panels: number of chordwise and spanwise panels for each segment (N*2)

    Display lattice metrics in console and log file.

    Args:
        :aircraft: (object) data structure for aircraft geometry
        :state: (object) data structure for flight state
        :settings: (object) data structure for execution settings
        :make_new_subareas: Flag

    Returns:
        :lattice: (object) data structure for VLM lattice
    """
    if make_new_subareas:
        pre_panelling(aircraft)
    lattice = VLMLattice()
    lattice.clean_bookkeeping()
    logger.info('Getting lattice information ... ')
    num_subareas = 0
    num_r = 0
    num_p = 0
    for this_subarea, _, this_segment, this_wing in ot.all_subareas(aircraft):
        wing = this_wing[2]
        segment = this_segment[2]
        subarea = this_subarea[2]
        num_subareas += 1
        pan_idx1 = num_p
        num_chordwise_panels = subarea.parent_control.panels['num_c'] if subarea.parent_control is not None else segment.panels['num_c']
        if subarea.type == 'segment':
            num_chordwise_panels = ceil(subarea.rel_length * num_chordwise_panels)
        num_r += num_chordwise_panels
        num_p += num_chordwise_panels
        lattice.update_bookkeeping(BookKeepingEntry(subarea, (range(pan_idx1, num_p)), num_chordwise_panels, mirror=False))
        if wing.symmetry:
            num_subareas += 1
            pan_idx1 = num_p
            num_r += num_chordwise_panels
            num_p += num_chordwise_panels
            lattice.update_bookkeeping(BookKeepingEntry(subarea, (range(pan_idx1, num_p)), num_chordwise_panels, mirror=True))

    num_wings = int(ot.count_all_wings(aircraft))
    num_controls = int(ot.count_all_controls(aircraft))
    num_subareas = int(num_subareas)
    num_r = int(num_r)
    num_p = int(num_p)
    lattice.info['num_wings'] = num_wings
    lattice.info['num_segments'] = num_subareas
    lattice.info['num_controls'] = num_controls
    lattice.info['num_strips'] = num_r
    lattice.info['num_panels'] = num_p
    logger.info('Pre-allocating lattice memory...')
    array_subareas = np.zeros((num_subareas, 4, 3), dtype=float, order='C')
    array_symmetry = np.zeros(num_subareas, dtype=int, order='C')
    array_panels = np.ones((num_subareas, 2), dtype=int, order='C')
    i = 0
    for entry in lattice.panel_bookkeeping:
        subarea = entry.subarea
        pan_idx = entry.pan_idx
        mirror = entry.mirror
        vertices = subarea.abs_vertices(mirror)
        array_subareas[i, 0, :] = vertices['a']
        array_subareas[i, 1, :] = vertices['b']
        array_subareas[i, 2, :] = vertices['c']
        array_subareas[i, 3, :] = vertices['d']
        array_panels[(i, 1)] = entry.num_chordwise_panels
        i += 1

    array_symmetry = np.zeros(num_p, dtype=int, order='C')
    lattice.p = np.zeros((num_p, 4, 3), dtype=float, order='C')
    lattice.v = np.zeros((num_p, 4, 3), dtype=float, order='C')
    lattice.c = np.zeros((num_p, 3), dtype=float, order='C')
    lattice.bound_leg_midpoints = np.zeros((num_p, 3), dtype=float, order='C')
    lattice.n = np.zeros((num_p, 3), dtype=float, order='C')
    lattice.a = np.zeros(num_p, dtype=float, order='C')
    lattice.epsilon = settings.settings['_epsilon']
    logger.info('Generating lattice...')
    c_vlm.py2c_lattice(lattice, state, array_subareas, array_symmetry, array_panels)
    logger.info(f"--> Number of panels: {lattice.info['num_panels']}")
    logger.info(f"--> Min panel area = {lattice.info['area_min']:.3e}")
    logger.info(f"--> Max panel area = {lattice.info['area_max']:.3e}")
    logger.info(f"--> Avg panel area = {lattice.info['area_avg']:.3e}")
    logger.info(f"--> Min panel aspect ratio = {lattice.info['aspect_min']:.3e}")
    logger.info(f"--> Max panel aspect ratio = {lattice.info['aspect_max']:.3e}")
    logger.info(f"--> Avg panel aspect ratio = {lattice.info['aspect_avg']:.3e}")
    if settings.settings['_do_normal_rotations']:
        for entry in lattice.panel_bookkeeping:
            subarea = entry.subarea
            pan_idx = entry.pan_idx
            mirror = entry.mirror
            if subarea.parent_control is not None:
                hinge_axis = subarea.abs_hinge_axis(mirror)
                if mirror:
                    deflection = subarea.parent_control.deflection_mirror
                else:
                    deflection = subarea.parent_control.deflection
                if deflection:
                    deflection = np.deg2rad(deflection)
                    R = axis_rot_matrix(hinge_axis, deflection)
                    for i in pan_idx:
                        lattice.n[i, :] = R @ lattice.n[i, :]

            eta_a = subarea.parent_subdivision.rel_vertices['eta_a']
            eta_b = subarea.parent_subdivision.rel_vertices['eta_b']
            eta_m = (eta_a + eta_b) / 2
            airfoil = subarea.parent_segment.segment_airfoil.at_eta(eta_m)
            num_panels = len([i for i in pan_idx])
            collocation_xsi = subarea.get_xsi_for_collocation_points(num_panels)
            for pan_of_subarea, i in enumerate(pan_idx):
                rot_axis = subarea.abs_camber_line_rot_axis(mirror)
                xsi = collocation_xsi[pan_of_subarea]
                angle = np.deg2rad(airfoil.camber_line_angle(xsi))
                if angle:
                    R = axis_rot_matrix(rot_axis, angle)
                    lattice.n[i, :] = R @ lattice.n[i, :]

    return lattice


def calc_downwash(lattice, vlmdata):
    """
    Generate downwash factors for aircraft lattice.

    Pre-allocate memory for the (num_p x num_p) downwash factor matrix.
    The downwash calculations are performed in C, directly into this matrix.

    Display matrix condition number in console and log file.

    Args:
        :lattice: (object) data structure for VLM lattice
        :vlmdata: (object) data structure for VLM input and output
    """
    logger.info('Pre-allocating downwash matrix in memory...')
    num_p = lattice.info['num_panels']
    vlmdata.matrix_downwash = np.zeros((num_p, num_p), dtype=float, order='C')
    logger.info('Computing downwash factors...')
    c_vlm.py2c_downwash(lattice, vlmdata.matrix_downwash)
    logger.info(f"--> Condition number = {np.linalg.cond(vlmdata.matrix_downwash):.3e}")


def calc_boundary(lattice, state, vlmdata):
    """
    Generate boundary conditions (RHS term) for VLM.

    Pre-allocate memory for the (num_p x 1) right-hand-side array.
    The right-hand side terms are computed in C, directly into this memory.

    Args:
        :lattice: (object) data structure for VLM lattice
        :state: (object) data structure for flight state
        :vlmdata: (object) data structure for VLM input and output
    """
    logger.info('Pre-allocating rhs array in memory...')
    num_p = lattice.info['num_panels']
    vlmdata.array_rhs = np.zeros(num_p, dtype=float, order='C')
    logger.info('Computing right-hand side term...')
    c_vlm.py2c_boundary(lattice, state, vlmdata.array_rhs)
    vlmdata.array_rhs = np.array(vlmdata.array_rhs)


def solver(vlmdata):
    """
    Solve linear system for vortex strengths

    Args:
        :vlmdata: (object) data structure for VLM input and output
    """
    logger.info('Solving linear system...')
    vlmdata.matrix_lu, vlmdata.array_pivots, vlmdata.panelwise['gamma'], _ = lapack.dgesv(vlmdata.matrix_downwash, vlmdata.array_rhs)


def calc_results(lattice, state, vlmdata):
    """
    Calculate inwash at collocation points

    Args:
        :lattice: (object) data structure for VLM lattice
        :state: (object) data structure for flight state
        :vlmdata: (object) data structure for VLM input and output
    """
    logger.info('Pre-allocating vortex-lattice method results...')
    num_p = lattice.info['num_panels']
    for key in ('vx', 'vy', 'vz', 'vmag', 'fx', 'fy', 'fz', 'fmag', 'cp'):
        vlmdata.panelwise[key] = np.zeros(num_p, dtype=float, order='C')

    logger.info('Computing results...')
    c_vlm.py2c_results(lattice, state, vlmdata)
    logger.info(f"--> Fx = {vlmdata.forces['x']:10.3e}")
    logger.info(f"--> Fy = {vlmdata.forces['y']:10.3e}")
    logger.info(f"--> Fz = {vlmdata.forces['z']:10.3e}")
    logger.info(f"--> FD = {vlmdata.forces['D']:10.3e}")
    logger.info(f"--> FC = {vlmdata.forces['C']:10.3e}")
    logger.info(f"--> FL = {vlmdata.forces['L']:10.3e}")
    logger.info(f"--> Mx = {vlmdata.forces['l']:10.3e}")
    logger.info(f"--> My = {vlmdata.forces['m']:10.3e}")
    logger.info(f"--> Mz = {vlmdata.forces['n']:10.3e}")
    logger.info(f"--> Cx = {vlmdata.coeffs['x']:7.4f}")
    logger.info(f"--> Cy = {vlmdata.coeffs['y']:7.4f}")
    logger.info(f"--> Cz = {vlmdata.coeffs['z']:7.4f}")
    logger.info(f"--> CD = {vlmdata.coeffs['D']:7.4f}")
    logger.info(f"--> CC = {vlmdata.coeffs['C']:7.4f}")
    logger.info(f"--> CL = {vlmdata.coeffs['L']:7.4f}")
    logger.info(f"--> Cl = {vlmdata.coeffs['l']:7.4f}")
    logger.info(f"--> Cm = {vlmdata.coeffs['m']:7.4f}")
    logger.info(f"--> Cn = {vlmdata.coeffs['n']:7.4f}")