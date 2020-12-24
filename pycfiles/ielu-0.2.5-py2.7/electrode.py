# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/electrode.py
# Compiled at: 2016-04-05 15:51:54
from __future__ import division
import numpy as np
from traits.api import HasTraits, List, Float, Tuple, Instance, Bool, Str, Int, Either, Property, Method, on_trait_change, Any, Enum, Button
from traitsui.api import View, Item, HGroup, Handler, CSVListEditor, VGroup, InstanceEditor, Group, OKCancelButtons, TableEditor, ObjectColumn, TextEditor, OKButton, CheckListEditor, Label, Action, ListStrEditor, MenuBar, Menu
from traitsui.message import error as error_dialog
from utils import ask_user_for_savefile
from functools import partial

class Electrode(HasTraits):
    ct_coords = Tuple
    surf_coords = Tuple
    iso_coords = Tuple
    snap_coords = Either(None, Instance(np.ndarray))
    pial_coords = Either(None, Instance(np.ndarray))
    special_name = Str
    is_interpolation = Bool(False)
    grid_name = Str('unsorted')
    grid_transition_to = Str('')
    hemi = Str
    vertno = Int(-1)
    plane_coords = Either(None, Tuple)
    geom_coords = List(Int)
    name = Str
    corner = List
    roi_list = List(Str)
    strrepr = Property

    def _get_strrepr(self):
        if self.special_name != '':
            return self.special_name
        return str(self)

    def __str__(self):
        return 'Elec: %s %s' % (self.grid_name, self.ct_coords)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        if other is None and self is not None:
            return 1
        else:
            if self is None and other is not None:
                return -1
            else:
                if self.name != '' and other.name != '':
                    return cmp(self.name, other.name)
                return cmp(str(self), str(other))

            return

    def astuple(self):
        return nparrayastuple(self.pial_coords)

    def asras(self):
        return self.surf_coords

    def asct(self):
        return self.ct_coords

    def asiso(self):
        return self.iso_coords


def nparrayastuple(nparray):
    nparray = np.array(nparray)
    return (nparray[0], nparray[1], nparray[2])


class ElectrodeWindow(Handler):
    model = Any
    cur_grid = Str
    electrodes = List(Instance(Electrode))
    cur_sel = Instance(Electrode)
    selection_callback = Method
    selected_ixes = Any
    swap_action = Action(name='Swap two electrodes', action='do_swap')
    add_blank_action = Action(name='Add blank electrode', action='do_add_blank')
    previous_sel = Instance(Electrode)
    previous_color = Int
    distinct_prev_sel = Instance(Electrode)
    save_montage_action = Action(name='Save montage file', action='do_montage')
    save_csv_action = Action(name='Save CSV file', action='do_csv')
    interpolate_action = Action(name='Linear interpolation', action='do_linear_interpolation')
    naming_convention = Enum('line', 'grid_serial', 'grid_concatenate')
    grid_type = Enum('depth', 'subdural')
    label_auto_action = Action(name='Automatic labeling', action='do_label_automatically')
    label_manually_action = Action(name='Label with current geometry', action='do_label_manually')
    rotate_grid_left_action = Action(name='Rotate left 90 deg', action='do_rotate_left')
    rotate_grid_right_action = Action(name='Rotate right 90 deg', action='do_rotate_right')
    rotate_grid_180_action = Action(name='Rotate 180 deg', action='do_rotate_180')
    reflect_grid_action = Action(name='Reflect', action='do_reflect')
    name_stem = Str
    c1, c2, c3 = 3 * (Instance(Electrode),)
    parcellation = Str
    error_radius = Float(4)
    find_rois_action = Action(name='Estimate single ROI contacts', action='do_rois')
    find_all_rois_action = Action(name='Estimate all ROI contacts', action='do_all_rois')
    manual_reposition_action = Action(name='Manually modify electrode position', action='do_manual_reposition')
    img_dpi = Float(125.0)
    img_size = List(Float)
    save_coronal_slice_action = Action(name='Save coronal slice', action='do_coronal_slice')
    labeling_delta = Float(0.25)
    labeling_epsilon = Int(25)
    labeling_rho = Int(40)
    include_underscore = Bool(True)

    def _img_size_default(self):
        return [
         450.0, 450.0]

    def electrode_factory(self):
        return Electrode(special_name='Electrode for linear interpolation', grid_name=self.cur_grid, is_interpolation=True)

    def dynamic_view(self):
        return View(Item('electrodes', editor=TableEditor(columns=[
         ObjectColumn(label='electrode', editor=TextEditor(), style='readonly', editable=False, name='strrepr'),
         ObjectColumn(label='corner', editor=CheckListEditor(values=[
          '', 'corner 1', 'corner 2',
          'corner 3']), style='simple', name='corner'),
         ObjectColumn(label='geometry', editor=CSVListEditor(), name='geom_coords'),
         ObjectColumn(label='channel name', editor=TextEditor(), name='name'),
         ObjectColumn(label='ROIs', editor=ListStrEditor(), editable=False, name='roi_list')], selected='cur_sel', deletable=True, row_factory=self.electrode_factory), show_label=False, height=350, width=700), HGroup(VGroup(Label('Automatic labeling parameters'), HGroup(Item('name_stem'), Item('naming_convention'), Item('include_underscore'), Item('grid_type')), HGroup(Item('labeling_delta'), Item('labeling_rho'), Item('labeling_epsilon')))), resizable=True, kind='panel', title='modify electrodes', buttons=[
         self.label_auto_action, self.swap_action, OKButton], menubar=MenuBar(Menu(self.label_auto_action, self.label_manually_action, self.rotate_grid_left_action, self.rotate_grid_right_action, self.rotate_grid_180_action, self.reflect_grid_action, name='Labeling'), Menu(self.add_blank_action, self.interpolate_action, self.find_rois_action, self.find_all_rois_action, self.manual_reposition_action, name='Operations'), Menu(self.save_montage_action, self.save_csv_action, self.save_coronal_slice_action, name='Save Output')))

    def edit_traits(self):
        super(ElectrodeWindow, self).edit_traits(view=self.dynamic_view())

    @on_trait_change('cur_sel')
    def selection_callback(self):
        if self.cur_sel is None:
            return
        else:
            if self.previous_sel is not None:
                self.model._new_glyph_color = self.previous_color
                self.model._single_glyph_to_recolor = self.previous_sel.asiso()
                self.model._update_single_glyph_event = True
            if self.cur_sel.special_name == 'Electrode for linear interpolation':
                self.previous_sel = None
                self.distinct_prev_sel = None
                return
            if self.distinct_prev_sel != self.previous_sel:
                self.distinct_prev_sel = self.previous_sel
            self.previous_sel = self.cur_sel
            self.previous_color = self.model._colors.keys().index(self.cur_grid)
            selection_color = self.model._colors.keys().index('selection')
            self.model._new_glyph_color = selection_color
            self.model._single_glyph_to_recolor = self.cur_sel.asiso()
            self.model._update_single_glyph_event = True
            return

    def closed(self, is_ok, info):
        self.cur_sel = None
        del self.model.ews[self.cur_grid]
        if self.previous_sel is not None:
            self.model._new_glyph_color = self.previous_color
            self.model._single_glyph_to_recolor = self.previous_sel.asiso()
            self.model._update_single_glyph_event = True
        return

    @on_trait_change('grid_type')
    def change_grid_type(self):
        self.model._grid_types[self.cur_grid] = self.grid_type

    def do_add_blank(self, info):
        e = self.electrode_factory()
        e.grid_name = self.cur_grid
        self.electrodes.append(e)

    def do_swap(self, info):
        if self.distinct_prev_sel == self.cur_sel:
            return
        else:
            if None in (self.distinct_prev_sel, self.cur_sel):
                return
            e1 = self.cur_sel
            e2 = self.distinct_prev_sel
            geom_swap = e1.geom_coords
            name_swap = e1.name
            e1.geom_coords = e2.geom_coords
            e1.name = e2.name
            e2.geom_coords = geom_swap
            e2.name = name_swap
            return

    def do_label_automatically(self, info):
        cur_geom = self.model._grid_geom[self.cur_grid]
        if cur_geom == 'user-defined' and self.naming_convention != 'line':
            from color_utils import mayavi2traits_color
            from name_holder import GeometryNameHolder, GeomGetterWindow
            nameholder = GeometryNameHolder(geometry=cur_geom, color=mayavi2traits_color(self.model._colors[self.cur_grid]))
            geomgetterwindow = GeomGetterWindow(holder=nameholder)
            if geomgetterwindow.edit_traits().result:
                cur_geom = geomgetterwindow.geometry
            else:
                error_dialog('User did not specify any geometry')
                return
        import pipeline as pipe
        if self.naming_convention == 'line':
            pipe.fit_grid_to_line(self.electrodes, delta=self.labeling_delta, rho_loose=self.labeling_rho + 10, epsilon=self.labeling_epsilon)
        else:
            pipe.fit_grid_by_fixed_points(self.electrodes, cur_geom, delta=self.labeling_delta, rho=self.labeling_rho, rho_strict=self.labeling_rho - 10, rho_loose=self.labeling_rho + 15, epsilon=self.labeling_epsilon, mindist=0, maxdist=36)
        self.naming_following_labeling(cur_geom=cur_geom)

    def do_labeling_manually(self):
        cur_geom = self.model._grid_geom[self.cur_grid]
        self.naming_following_labeling(cur_geom=cur_geom)

    def naming_following_labeling(self, cur_geom=None):
        for elec in self.electrodes:
            x, y = elec.geom_coords
            if self.naming_convention == 'grid_serial':
                index = x * np.min(cur_geom) + y + 1
            elif self.naming_convention == 'grid_concatenate':
                index = ('{0}{1}').format(x + 1, y + 1)
            elif self.naming_convention == 'line':
                index = y + 1
            elec.name = ('{0}{1}{2}').format(self.name_stem, '_' if self.include_underscore else '', index)

    def do_linear_interpolation(self, info):
        if self.cur_sel is None:
            return
        else:
            if self.cur_sel.special_name == '':
                return
            if len(self.cur_sel.geom_coords) == 0:
                error_dialog('Specify geom_coords before linear interpolation')
                return
            x, y = self.cur_sel.geom_coords
            x_low = self._find_closest_neighbor(self.cur_sel, 'x', '-')
            x_hi = self._find_closest_neighbor(self.cur_sel, 'x', '+')
            y_low = self._find_closest_neighbor(self.cur_sel, 'y', '-')
            y_hi = self._find_closest_neighbor(self.cur_sel, 'y', '+')
            loc = None
            if x_low is not None and x_hi is not None:
                xl = x_low.geom_coords[0]
                xh = x_hi.geom_coords[0]
                ratio = (x - xl) / (xh - xl)
                loc = np.array(x_low.iso_coords) + (np.array(x_hi.iso_coords) - np.array(x_low.iso_coords)) * ratio
            elif y_low is not None and y_hi is not None:
                yl = y_low.geom_coords[1]
                yh = y_hi.geom_coords[1]
                ratio = (y - yl) / (yh - yl)
                loc = np.array(y_low.iso_coords) + (np.array(y_hi.iso_coords) - np.array(y_low.iso_coords)) * ratio
            if x_low is not None and loc is None:
                x_lower = self._find_closest_neighbor(x_low, 'x', '-')
                xl = x_low.geom_coords[0]
                xll = x_lower.geom_coords[0]
                if xl == xll + 1:
                    loc = 2 * np.array(x_low.iso_coords) - np.array(x_lower.iso_coords)
            if x_hi is not None and loc is None:
                x_higher = self._find_closest_neighbor(x_hi, 'x', '+')
                xh = x_hi.geom_coords[0]
                xhh = x_higher.geom_coords[0]
                if xh == xhh - 1:
                    loc = 2 * np.array(x_hi.iso_coords) - np.array(x_higher.iso_coords)
            if y_low is not None and loc is None:
                y_lower = self._find_closest_neighbor(y_low, 'y', '-')
                yl = y_low.geom_coords[1]
                yll = y_lower.geom_coords[1]
                if yl == yll + 1:
                    loc = 2 * np.array(y_low.iso_coords) - np.array(y_lower.iso_coords)
            if y_hi is not None and loc is None:
                y_higher = self._find_closest_neighbor(y_hi, 'y', '+')
                yh = y_hi.geom_coords[1]
                yhh = y_higher.geom_coords[1]
                if yh == yhh - 1:
                    loc = 2 * np.array(y_hi.iso_coords) - np.array(y_higher.iso_coords)
            if loc is not None:
                self.cur_sel.iso_coords = tuple(loc)
                self.cur_sel.special_name = 'Linearly interpolated electrode'
            else:
                error_dialog('No line for simple linear interpolation\nBetter algorithm needed')
            import pipeline as pipe
            pipe.linearly_transform_electrodes_to_isotropic_coordinate_space([
             self.cur_sel], self.model.ct_scan, isotropization_strategy=self.model.isotropize, isotropization_direction_off='copy_to_ct', isotropization_direction_on='deisotropize', iso_vector_override=self.model.isotropization_override)
            aff = self.model.acquire_affine()
            pipe.translate_electrodes_to_surface_space([self.cur_sel], aff, subjects_dir=self.model.subjects_dir, subject=self.model.subject)
            self.model.add_electrode_to_grid(self.cur_sel, self.cur_grid)
            return

    def _find_closest_neighbor(self, cur_elec, axis, direction):
        x, y = cur_elec.geom_coords
        if direction == '+':
            new_ix = np.inf
        else:
            new_ix = -np.inf
        new_e = None
        for e in self.electrodes:
            if len(e.geom_coords) == 0:
                continue
            ex, ey = e.geom_coords
            if axis == 'x' and direction == '+':
                if ex < new_ix and ex > x and ey == y:
                    new_e = e
                    new_ix = ex
            if axis == 'x' and direction == '-':
                if ex > new_ix and ex < x and ey == y:
                    new_e = e
                    new_ix = ex
            if axis == 'y' and direction == '+':
                if ey < new_ix and ey > y and ex == x:
                    new_e = e
                    new_ix = ey
            if axis == 'y' and direction == '-':
                if ey > new_ix and ey < y and ex == x:
                    new_e = e
                    new_ix = ey

        return new_e

    def do_rotate_left(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        geom_x, geom_y = (-1, -1)
        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            if curx > geom_x:
                geom_x = curx
            if cury > geom_y:
                geom_y = cury

        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            newx = cury
            newy = geom_x - curx
            elec.geom_coords = [newx, newy]

    def do_rotate_right(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        geom_x, geom_y = (-1, -1)
        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            if curx > geom_x:
                geom_x = curx
            if cury > geom_y:
                geom_y = cury

        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            newx = geom_y - cury
            newy = curx
            elec.geom_coords = [newx, newy]

    def do_rotate_180(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        geom_x, geom_y = (-1, -1)
        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            if curx > geom_x:
                geom_x = curx
            if cury > geom_y:
                geom_y = cury

        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            newx = geom_x - curx
            newy = geom_y - cury
            elec.geom_coords = [newx, newy]

    def do_reflect(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        for elec in electrodes:
            if len(elec.geom_coords) == 0:
                continue
            curx, cury = elec.geom_coords
            newx = cury
            newy = curx
            elec.geom_coords = [newx, newy]

    def do_montage(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        if electrodes is None:
            return
        else:
            from electrode_group import save_coordinates
            save_coordinates(electrodes, self.model._grid_types, snapping_completed=self.model._snapping_completed, file_type='montage')
            return

    def do_csv(self, info):
        electrodes = self.model.get_electrodes_from_grid(target=self.cur_grid, electrodes=self.electrodes)
        if electrodes is None:
            return
        else:
            from electrode_group import save_coordinates
            save_coordinates(electrodes, self.model._grid_types, snapping_completed=self.model._snapping_completed, file_type='csv')
            return

    def do_rois(self, info):
        from electrode_group import get_nearby_rois_elec
        get_nearby_rois_elec(self.cur_sel, parcellation=self.model.roi_parcellation, error_radius=self.model.roi_error_radius, subjects_dir=self.model.subjects_dir, subject=self.model.subject)

    def do_all_rois(self, info):
        from electrode_group import get_nearby_rois_grid
        get_nearby_rois_grid(self.electrodes, parcellation=self.model.roi_parcellation, error_radius=self.model.roi_error_radius, subjects_dir=self.model.subjects_dir, subject=self.model.subject)

    def do_coronal_slice(self, info):
        savefile = ask_user_for_savefile('save png file with slice image')
        from electrode_group import coronal_slice_grid
        coronal_slice_grid(self.electrodes, savefile=savefile, subjects_dir=self.model.subjects_dir, subject=self.model.subject, dpi=self.model.coronal_dpi, size=tuple(self.model.coronal_size), title=self.name_stem)

    def do_manual_reposition(self, info):
        if self.cur_sel is None:
            return
        else:
            pd = self.model.construct_panel2d()
            x, y, z = self.cur_sel.asct()
            pd.move_cursor(x, y, z)
            pd.drop_pin(x, y, z, color='cyan', name='electrode', image_name='ct')
            rx, ry, rz = self.cur_sel.asras()
            pd.drop_pin(rx, ry, rz, color='cyan', name='electrode', image_name='t1', ras_coords=True)
            pd.edit_traits(kind='livemodal')
            return

    @on_trait_change('model:panel2d:move_electrode_internally_event')
    def _internally_effect_electrode_reposition(self):
        if self.cur_sel is None:
            error_dialog('No electrode specified to move')
            return
        else:
            pd = self.model.panel2d
            image_name = pd.currently_showing.name
            px, py, pz, _ = pd.pins[image_name][pd.current_pin]
            if image_name == 't1':
                px, py, pz = pd.map_cursor((px, py, pz), pd.images['t1'][2])
            self.model.move_electrode(self.cur_sel, (px, py, pz), in_ras=image_name == 't1')
            return

    @on_trait_change('model:panel2d:move_electrode_postprocessing_event')
    def _postprocessing_effect_electrode_reposition(self):
        if self.cur_sel is None:
            error_dialog('No electrode specified to move')
            return
        else:
            pd = self.model.panel2d
            image_name = pd.currently_showing.name
            px, py, pz, _ = pd.pins[image_name][pd.current_pin]
            if image_name == 't1':
                px, py, pz = pd.map_cursor((px, py, pz), pd.images['t1'][2])
            self.model.move_electrode(self.cur_sel, (px, py, pz), in_ras=image_name == 't1', as_postprocessing=True)
            return