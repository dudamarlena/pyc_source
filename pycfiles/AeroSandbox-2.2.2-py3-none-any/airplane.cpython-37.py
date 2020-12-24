# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\geometry\airplane.py
# Compiled at: 2020-04-29 17:24:11
# Size of source mod 2**32: 22022 bytes
from aerosandbox.geometry.common import *

class Airplane(AeroSandboxObject):
    """Airplane"""

    def __init__(self, name='Untitled', x_ref=0, y_ref=0, z_ref=0, mass_props=None, wings=[], fuselages=[], s_ref=None, c_ref=None, b_ref=None):
        self.name = name
        self.xyz_ref = cas.vertcat(x_ref, y_ref, z_ref)
        self.wings = wings
        self.fuselages = fuselages
        if len(self.wings) > 0:
            self.set_ref_dims_from_wing(main_wing_index=0)
        if s_ref is not None:
            self.s_ref = s_ref
        if c_ref is not None:
            self.c_ref = c_ref
        if b_ref is not None:
            self.b_ref = b_ref
        assert self.name is not None
        assert self.xyz_ref is not None
        assert self.s_ref is not None
        assert self.c_ref is not None
        assert self.b_ref is not None

    def __repr__(self):
        return 'Airplane %s (%i wings, %i fuselages)' % (
         self.name,
         len(self.wings),
         len(self.fuselages))

    def set_ref_dims_from_wing(self, main_wing_index=0):
        main_wing = self.wings[main_wing_index]
        self.s_ref = main_wing.area()
        self.b_ref = main_wing.span()
        self.c_ref = main_wing.mean_geometric_chord()

    def set_paneling_everywhere(self, n_chordwise_panels, n_spanwise_panels):
        for wing in self.wings:
            wing.chordwise_panels = n_chordwise_panels
            for xsec in wing.xsecs:
                xsec.spanwise_panels = n_spanwise_panels

    def set_spanwise_paneling_everywhere(self, n_spanwise_panels):
        for wing in self.wings:
            for xsec in wing.xsecs:
                xsec.spanwise_panels = n_spanwise_panels

    def draw(self, show=True, colorscale='mint', colorbar_title='Component ID', draw_quarter_chord=True):
        """
        Draws the airplane using a Plotly interface.
        :param show: Do you want to show the figure? [boolean]
        :param colorscale: Which colorscale do you want to use? ("viridis", "plasma", mint", etc.)
        :param draw_quarter_chord: Do you want to draw the quarter-chord? [boolean]
        :return: A plotly figure object [go.Figure]
        """
        fig = Figure3D()
        for wing_id in range(len(self.wings)):
            wing = self.wings[wing_id]
            for xsec_id in range(len(wing.xsecs) - 1):
                xsec_1 = wing.xsecs[xsec_id]
                xsec_2 = wing.xsecs[(xsec_id + 1)]
                le_start = xsec_1.xyz_le + wing.xyz_le
                te_start = xsec_1.xyz_te() + wing.xyz_le
                le_end = xsec_2.xyz_le + wing.xyz_le
                te_end = xsec_2.xyz_te() + wing.xyz_le
                fig.add_quad(points=[
                 le_start,
                 le_end,
                 te_end,
                 te_start],
                  intensity=wing_id,
                  mirror=(wing.symmetric))
                if draw_quarter_chord:
                    fig.add_line(points=[
                     0.75 * le_start + 0.25 * te_start,
                     0.75 * le_end + 0.25 * te_end],
                      mirror=(wing.symmetric))

        for fuse_id in range(len(self.fuselages)):
            fuse = self.fuselages[fuse_id]
            for xsec_id in range(len(fuse.xsecs) - 1):
                xsec_1 = fuse.xsecs[xsec_id]
                xsec_2 = fuse.xsecs[(xsec_id + 1)]
                r1 = xsec_1.radius
                r2 = xsec_2.radius
                points_1 = np.zeros((fuse.circumferential_panels, 3))
                points_2 = np.zeros((fuse.circumferential_panels, 3))
                for point_index in range(fuse.circumferential_panels):
                    rot = angle_axis_rotation_matrix(2 * cas.pi * point_index / fuse.circumferential_panels, [
                     1, 0, 0], True).toarray()
                    points_1[point_index, :] = rot @ np.array([0, 0, r1])
                    points_2[point_index, :] = rot @ np.array([0, 0, r2])

                points_1 = points_1 + np.array(fuse.xyz_le).reshape(-1) + np.array(xsec_1.xyz_c).reshape(-1)
                points_2 = points_2 + np.array(fuse.xyz_le).reshape(-1) + np.array(xsec_2.xyz_c).reshape(-1)
                for point_index in range(fuse.circumferential_panels):
                    fig.add_quad(points=[
                     points_1[point_index % fuse.circumferential_panels, :],
                     points_1[(point_index + 1) % fuse.circumferential_panels, :],
                     points_2[(point_index + 1) % fuse.circumferential_panels, :],
                     points_2[point_index % fuse.circumferential_panels, :]],
                      intensity=fuse_id,
                      mirror=(fuse.symmetric))

        return fig.draw(show=show,
          colorscale=colorscale,
          colorbar_title=colorbar_title)

    def is_symmetric(self):
        """
        Returns a boolean describing whether the airplane is geometrically entirely symmetric across the XZ-plane.
        :return: [boolean]
        """
        for wing in self.wings:
            for xsec in wing.xsecs:
                if not xsec.control_surface_type == 'symmetric':
                    if not xsec.control_surface_deflection == 0:
                        return False
                    else:
                        if not (wing.symmetric or xsec.xyz_le[1] == 0):
                            return False
                        if not xsec.twist == 0:
                            return xsec.twist_axis[0] == 0 and xsec.twist_axis[2] == 0 or 
                        return xsec.airfoil.CL_function(0, 1000000.0, 0, 0) == 0 or False
                    return xsec.airfoil.Cm_function(0, 1000000.0, 0, 0) == 0 or False

        return True

    def write_aswing(self, filepath=None):
        """
        Contributed by Brent Avery, Edited by Peter Sharpe. Work in progress.
        Writes a geometry file compatible with Mark Drela's ASWing.
        :param filepath: Filepath to write to. Should include ".asw" extension [string]
        :return: None
        """
        if filepath is None:
            filepath = '%s.asw' % self.name
        with open(filepath, 'w+') as (f):
            f.write('\n'.join(['#============',
             'Name',
             self.name,
             'End']))
            f.write('\n'.join(['', '#============',
             'Units',
             'L 0.3048 m',
             'T 1.0  s',
             'F 4.450 N',
             'End']))
            f.write('\n'.join(['', '#============',
             'Constant',
             '#  g     rho_0     a_0',
             '   '.join([str(9.81), str(1.205), str(343.3)]),
             'End']))
            f.write('\n'.join(['', '#============',
             'Reference',
             '#   Sref    Cref    Bref',
             '   '.join([str(self.s_ref), str(self.c_ref), str(self.b_ref)]),
             'End']))
            f.write('\n'.join(['', '#============',
             'Ground',
             '#  Nbeam  t',
             '    '.join([' ', str(1), str(0)]),
             'End']))
            f.write('\n'.join(['', '#============',
             'Joint',
             '#   Nbeam1   Nbeam2    t1     t2']))
            for onewing in range(1, len(self.wings)):
                wing = self.wings[onewing]
                if wing.name == 'Horizontal Stabilizer':
                    xsecs = []
                    for xsec in wing.xsecs:
                        xsecs.append(xsec)

                    t = xsecs[0].y_le + wing.xyz_le[1]
                    coords = '       '.join(['    1', str(onewing + 1), str(t), '0'])
                    f.write('\n'.join(['', coords]))
                if wing.name == 'Vertical Stabilizer':
                    wing2 = self.wings[np.ceil(onewing / 2)]
                    wing3 = self.wings[0]
                    xsecs = []
                    for xsec in wing.xsecs:
                        xsecs.append(xsec)

                    xsecs2 = []
                    for xsec2 in wing2.xsecs:
                        xsecs2.append(xsec2)

                    xsecs3 = []
                    for xsec3 in wing3.xsecs:
                        xsecs3.append(xsec3)

                    t = xsecs2[0].y_le + wing.xyz_le[1]
                    t2 = 1 + (xsecs2[0].z_le + wing2.xyz_le[2]) - (xsecs[0].z_le + wing.xyz_le[2])
                    coords = '       '.join(['    1', str(onewing + 1), str(t), str(t2)])
                    f.write('\n'.join(['', coords]))

            for fuse in range(len(self.fuselages)):
                onefuse = self.fuselages[fuse]
                wing = self.wings[0]
                xsecs = []
                xsecs.append(onefuse.xsecs[0])
                xsecs.append(onefuse.xsecs[(-1)])
                xsecs2 = []
                for xsec2 in wing.xsecs:
                    xsecs2.append(xsec2)

                t = xsecs[0].y_c + onefuse.xyz_le[1]
                t2 = (wing.xyz_le[0] + xsecs2[0].x_le + (wing.xyz_le[0] + xsecs2[(-1)].x_le)) / 2
                coords = '      '.join(['    1', str(onewing + fuse + 2), str(t), str(t2)])
                f.write('\n'.join(['', coords]))

            corr_stab = {}
            for fuse in range(len(self.fuselages)):
                corr_stab.update({fuse + len(self.wings) + 1: [fuse + 1, fuse + 1 + np.floor(len(self.wings) / 2)]})

            for fuse in range(len(self.fuselages)):
                onefuse = self.fuselages[fuse]
                xsecs = []
                xsecs.append(onefuse.xsecs[0])
                xsecs.append(onefuse.xsecs[(-1)])
                horiz = self.wings[corr_stab[(fuse + len(self.wings) + 1)][0]]
                xsecs2 = []
                for xsec2 in horiz.xsecs:
                    xsecs2.append(xsec2)

                vert = self.wings[corr_stab[(fuse + len(self.wings) + 1)][1]]
                xsecs3 = []
                for xsec3 in vert.xsecs:
                    xsecs3.append(xsec3)

                t = xsecs2[0].x_le + horiz.xyz_le[0]
                t2 = 0
                t3 = xsecs3[0].x_le + vert.xyz_le[0]
                t4 = 1 + (xsecs2[0].z_le + horiz.xyz_le[2]) - (xsecs3[0].z_le + vert.xyz_le[2])
                coords = '     '.join([
                 '', str(fuse + len(self.wings) + 1), str(corr_stab[(fuse + len(self.wings) + 1)][0] + 1), str(t),
                 str(t2)])
                coords2 = '     '.join([
                 '', str(fuse + len(self.wings) + 1), str(corr_stab[(fuse + len(self.wings) + 1)][1] + 1), str(t3),
                 str(t4)])
                f.write('\n'.join(['', coords, coords2]))

            f.write('\n'.join(['', 'End']))
            for onewing in range(len(self.wings)):
                wing = self.wings[onewing]
                if wing.name == 'Main Wing':
                    xsecs = []
                    for xsec in wing.xsecs:
                        xsecs.append(xsec)

                    chordalfa = []
                    coords = []
                    max_le = {abs(xsecs[(-1)].x_le - xsecs[0].x_le): 'sec.x_le', 
                     abs(xsecs[(-1)].y_le - xsecs[0].y_le): 'sec.y_le', 
                     abs(xsecs[(-1)].z_le - xsecs[0].z_le): 'sec.z_le'}
                    for sec in xsecs:
                        if max_le.get(max(max_le)) == 'sec.x_le':
                            t = sec.x_le
                        elif max_le.get(max(max_le)) == 'sec.y_le':
                            t = sec.y_le
                        elif max_le.get(max(max_le)) == 'sec.z_le':
                            t = sec.z_le
                        chordalfa.append('    '.join([str(t), str(sec.chord), str(sec.twist)]))
                        coords.append('    '.join([str(t), str(sec.x_le + wing.xyz_le[0]), str(sec.y_le + wing.xyz_le[1]),
                         str(sec.z_le + wing.xyz_le[2])]))

                    f.write('\n'.join(['', '#============',
                     ' '.join(['Beam', str(onewing + 1)]),
                     wing.name,
                     't    chord    twist',
                     '\n'.join(chordalfa),
                     '#',
                     't    x    y    z',
                     '\n'.join(coords),
                     'End']))
                elif wing.name == 'Horizontal Stabilizer':
                    xsecs = []
                    for xsec in wing.xsecs:
                        xsecs.append(xsec)

                    chordalfa = []
                    coords = []
                    max_le = {abs(xsecs[(-1)].x_le - xsecs[0].x_le): 'sec.x_le', 
                     abs(xsecs[(-1)].y_le - xsecs[0].y_le): 'sec.y_le', 
                     abs(xsecs[(-1)].z_le - xsecs[0].z_le): 'sec.z_le'}
                    for sec in xsecs:
                        if max_le.get(max(max_le)) == 'sec.x_le':
                            t = sec.x_le
                        elif max_le.get(max(max_le)) == 'sec.y_le':
                            t = sec.y_le
                        elif max_le.get(max(max_le)) == 'sec.z_le':
                            t = sec.z_le
                        chordalfa.append('    '.join([str(t), str(sec.chord), str(sec.twist), str(0.07)]))
                        coords.append('    '.join([str(t), str(sec.x_le + wing.xyz_le[0]), str(sec.y_le + wing.xyz_le[1]),
                         str(sec.z_le + wing.xyz_le[2])]))

                    f.write('\n'.join(['', '#============',
                     ' '.join(['Beam', str(onewing + 1)]),
                     wing.name,
                     't    chord    twist dCLdF1',
                     '\n'.join(chordalfa),
                     '#',
                     't    x    y    z',
                     '\n'.join(coords),
                     'End']))
                elif wing.name == 'Vertical Stabilizer':
                    xsecs = []
                    for xsec in wing.xsecs:
                        xsecs.append(xsec)

                    chordalfa = []
                    coords = []
                    max_le = {abs(xsecs[(-1)].x_le - xsecs[0].x_le): 'sec.x_le', 
                     abs(xsecs[(-1)].y_le - xsecs[0].y_le): 'sec.y_le', 
                     abs(xsecs[(-1)].z_le - xsecs[0].z_le): 'sec.z_le'}
                    for sec in xsecs:
                        if max_le.get(max(max_le)) == 'sec.x_le':
                            t = sec.x_le + 1
                        elif max_le.get(max(max_le)) == 'sec.y_le':
                            t = sec.y_le + 1
                        elif max_le.get(max(max_le)) == 'sec.z_le':
                            t = sec.z_le + 1
                        chordalfa.append('    '.join([str(t), str(sec.chord), str(sec.twist)]))
                        coords.append('    '.join([str(t), str(sec.x_le + wing.xyz_le[0]), str(sec.y_le + wing.xyz_le[1]),
                         str(sec.z_le + wing.xyz_le[2])]))

                    f.write('\n'.join(['', '#============',
                     ' '.join(['Beam', str(onewing + 1)]),
                     wing.name,
                     '  t    chord    twist',
                     '\n'.join(chordalfa),
                     '#',
                     't    x    y    z',
                     '\n'.join(coords),
                     'End']))

            for fuse in range(len(self.fuselages)):
                onefuse = self.fuselages[fuse]
                xsecs = []
                xsecs.append(onefuse.xsecs[0])
                xsecs.append(onefuse.xsecs[(-1)])
                coords = []
                max_c = {abs(xsecs[1].x_c - xsecs[0].x_c): 'sec.x_c', 
                 abs(xsecs[1].y_c - xsecs[0].y_c): 'sec.y_c', 
                 abs(xsecs[1].z_c - xsecs[0].z_c): 'sec.z_c'}
                for sec in xsecs:
                    if max_c.get(max(max_c)) == 'sec.x_c':
                        t = sec.x_c
                    elif max_c.get(max(max_c)) == 'sec.y_c':
                        t = sec.y_c
                    elif max_c.get(max(max_c)) == 'sec.z_c':
                        t = sec.z_c
                    coords.append('    '.join([str(t), str(sec.x_c + onefuse.xyz_le[0]), str(sec.y_c + onefuse.xyz_le[1]),
                     str(sec.z_c + onefuse.xyz_le[2])]))

                f.write('\n'.join(['', '#============',
                 '  '.join(['Beam', str(onewing + fuse + 2)]),
                 onefuse.name,
                 't    x    y    z',
                 '\n'.join(coords),
                 'End']))