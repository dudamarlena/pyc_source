# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/simplegui.py
# Compiled at: 2011-04-23 08:43:29
import math
from astral import Astral
import geo, geocaching, gobject, gtk, logging
logger = logging.getLogger('simplegui')
try:
    import gtk.glade, extListview
except ImportError:
    logger.info("Please install glade if you're NOT on the maemo platform.")

import pango
from os import path, extsep
import re
from cachedownloader import HTMLManipulations
from gtkmap import *
from gui import Gui

class SimpleGui(Gui):
    USES = [
     'gpsprovider']
    XMLFILE = 'freerunner.glade'
    REDRAW_DISTANCE_TRACKING = 50
    REDRAW_DISTANCE_MINOR = 4
    DISTANCE_DISABLE_ARROW = 5
    MAX_NUM_RESULTS = 50
    ARROW_OFFSET = 1.0 / 3.0
    ARROW_SHAPE = [(0, -2 + ARROW_OFFSET), (1, +1 + ARROW_OFFSET), (0, 0 + ARROW_OFFSET), (-1, 1 + ARROW_OFFSET)]
    COLOR_ARROW_DEFAULT = gtk.gdk.color_parse('green')
    COLOR_ARROW_NEAR = gtk.gdk.color_parse('orange')
    COLOR_ARROW_ATTARGET = gtk.gdk.color_parse('red')
    COLOR_ARROW_DISABLED = gtk.gdk.color_parse('red')
    COLOR_ARROW_CIRCLE = gtk.gdk.color_parse('darkgray')
    COLOR_ARROW_OUTER_LINE = gtk.gdk.color_parse('black')
    COLOR_ARROW_CROSS = gtk.gdk.color_parse('darkslategray')
    COLOR_ARROW_ERROR = gtk.gdk.color_parse('gold')
    COLOR_NORTH_INDICATOR = gtk.gdk.color_parse('gold')
    COLOR_SUN_INDICATOR = gtk.gdk.color_parse('yellow')
    COLOR_SUN_INDICATOR_TEXT = gtk.gdk.color_parse('black')
    ARROW_LINE_WIDTH = 3
    NORTH_INDICATOR_SIZE = 30
    FONT_NORTH_INDICATOR = pango.FontDescription('Sans 9')
    FONT_SUN_INDICATOR = pango.FontDescription('Sans 8')
    COLOR_QUALITY_OUTER = gtk.gdk.color_parse('black')
    COLOR_QUALITY_INNER = gtk.gdk.color_parse('green')
    SETTINGS_CHECKBOXES = [
     'download_visible',
     'download_notfound',
     'download_new',
     'download_nothing',
     'download_resize',
     'options_show_name',
     'download_noimages',
     'options_hide_found',
     'options_map_double_size']
    SETTINGS_INPUTS = [
     'download_output_dir',
     'download_resize_pixel',
     'options_username',
     'options_password',
     'download_map_path']

    def __init__(self, core, dataroot):
        global xml
        gtk.gdk.threads_init()
        self._prepare_images(dataroot)
        self.core = core
        self.core.connect('map-marks-changed', self._on_map_changed)
        self.core.connect('cache-changed', self._on_cache_changed)
        self.core.connect('target-changed', self._on_target_changed)
        self.core.connect('good-fix', self._on_good_fix)
        self.core.connect('no-fix', self._on_no_fix)
        self.core.connect('settings-changed', self._on_settings_changed)
        self.core.connect('save-settings', self._on_save_settings)
        self.core.connect('error', lambda caller, message: self.show_error(message))
        self.core.connect('progress', lambda caller, fraction, text: self.set_progress(fraction, text))
        self.core.connect('hide-progress', lambda caller: self.hide_progress())
        self.core.connect('fieldnotes-changed', self._on_fieldnotes_changed)
        self.settings = {}
        Map.set_config(self.core.settings['map_providers'], self.core.settings['download_map_path'], self.noimage_cantload, self.noimage_loading)
        self.format = geo.Coordinate.FORMAT_DM
        self.current_cache = None
        self.gps_data = None
        self.gps_has_fix = False
        self.gps_last_good_fix = None
        self.gps_last_screen_position = (0, 0)
        self.block_changes = False
        self.image_zoomed = False
        self.image_no = 0
        self.images = []
        self.north_indicator_layout = None
        self.drawing_area_configured = self.drawing_area_arrow_configured = False
        self.notes_changed = False
        self.fieldnotes_changed = False
        self.astral = Astral()
        xml = gtk.glade.XML(path.join(dataroot, self.XMLFILE))
        self.load_ui()
        return

    def _get_geocaches_callback(self, visible_area, maxresults):
        return self.core.pointprovider.get_points_filter(visible_area, False if self.settings['options_hide_found'] else None, maxresults)

    def _prepare_images(self, dataroot):
        p = '%s%s%%s' % (path.join(dataroot, '%s'), extsep)
        self.noimage_cantload = p % ('noimage-cantload', 'png')
        self.noimage_loading = p % ('noimage-loading', 'png')

    def _on_cache_changed(self, something, cache):
        if self.current_cache != None and cache.name == self.current_cache.name:
            self.show_cache(cache)
        return False

    def set_current_cache(self, cache):
        pass

    def _on_map_changed(self, something):
        self.map.redraw_layers()
        return False

    def load_ui(self):
        self.window = xml.get_widget('window1')
        xml.signal_autoconnect(self)
        self.drawing_area = xml.get_widget('drawingarea')
        self.drawing_area_arrow = xml.get_widget('drawingarea_arrow')
        self.filtermsg = xml.get_widget('label_filtermsg')
        self.scrolledwindow_image = xml.get_widget('scrolledwindow_image')
        self.image_cache = xml.get_widget('image_cache')
        self.image_cache_caption = xml.get_widget('label_cache_image_caption')
        self.notebook_cache = xml.get_widget('notebook_cache')
        self.notebook_all = xml.get_widget('notebook_all')
        self.notebook_search = xml.get_widget('notebook_search')
        self.progressbar = xml.get_widget('progress_download')
        self.button_download_details = xml.get_widget('button_download_details')
        self.button_track = xml.get_widget('togglebutton_track')
        self.check_result_marked = xml.get_widget('check_result_marked')
        self.label_fieldnotes = xml.get_widget('label_fieldnotes')
        self.button_upload_fieldnotes = xml.get_widget('button_upload_fieldnotes')
        self.button_check_updates = xml.get_widget('button_check_updates')
        self.label_bearing = xml.get_widget('label_bearing')
        self.label_dist = xml.get_widget('label_dist')
        self.label_altitude = xml.get_widget('label_altitude')
        self.label_latlon = xml.get_widget('label_latlon')
        self.label_target = xml.get_widget('label_target')
        self.label_quality = xml.get_widget('label_quality')
        self.input_export_path = xml.get_widget('input_export_path')
        self.drawing_area_arrow.connect('expose_event', self._expose_event_arrow)
        self.drawing_area_arrow.connect('configure_event', self._configure_event_arrow)
        self.drawing_area_arrow.set_events(gtk.gdk.EXPOSURE_MASK)
        self._configure_map()
        xml.get_widget('tableMap').attach(self.map, 0, 4, 1, 2)
        self.cache_elements = {'name_downloaded': xml.get_widget('link_cache_name'), 
           'name_not_downloaded': xml.get_widget('button_cache_name'), 
           'title': xml.get_widget('label_cache_title'), 
           'type': xml.get_widget('label_cache_type'), 
           'size': xml.get_widget('label_cache_size'), 
           'terrain': xml.get_widget('label_cache_terrain'), 
           'difficulty': xml.get_widget('label_cache_difficulty'), 
           'desc': xml.get_widget('textview_cache_desc').get_buffer(), 
           'notes': xml.get_widget('textview_cache_notes').get_buffer(), 
           'fieldnotes': xml.get_widget('textview_cache_fieldnotes').get_buffer(), 
           'hints': xml.get_widget('label_cache_hints').get_buffer(), 
           'coords': xml.get_widget('label_cache_coords'), 
           'log_found': xml.get_widget('radiobutton_cache_log_found'), 
           'log_notfound': xml.get_widget('radiobutton_cache_log_notfound'), 
           'log_note': xml.get_widget('radiobutton_cache_log_note'), 
           'log_no': xml.get_widget('radiobutton_cache_log_no'), 
           'log_date': xml.get_widget('label_cache_log_date'), 
           'marked': xml.get_widget('check_cache_marked')}
        self.search_elements = {'type': {geocaching.GeocacheCoordinate.TYPE_REGULAR: xml.get_widget('check_search_type_traditional'), 
                    geocaching.GeocacheCoordinate.TYPE_MULTI: xml.get_widget('check_search_type_multi'), 
                    geocaching.GeocacheCoordinate.TYPE_MYSTERY: xml.get_widget('check_search_type_unknown'), 
                    geocaching.GeocacheCoordinate.TYPE_VIRTUAL: xml.get_widget('check_search_type_virtual'), 
                    'all': xml.get_widget('check_search_type_other')}, 
           'name': xml.get_widget('entry_search_name'), 
           'status': xml.get_widget('combo_search_status'), 
           'size': {1: xml.get_widget('check_search_size_1'), 
                    2: xml.get_widget('check_search_size_2'), 
                    3: xml.get_widget('check_search_size_3'), 
                    4: xml.get_widget('check_search_size_4'), 
                    5: xml.get_widget('check_search_size_5')}, 
           'diff': {'selector': xml.get_widget('combo_search_diff_sel'), 
                    'value': xml.get_widget('combo_search_diff')}, 
           'terr': {'selector': xml.get_widget('combo_search_terr_sel'), 
                    'value': xml.get_widget('combo_search_terr')}, 
           'inview': xml.get_widget('check_search_inview')}
        txtRdr = gtk.CellRendererText()
        (ROW_TITLE, ROW_TYPE, ROW_SIZE, ROW_TERRAIN, ROW_DIFF, ROW_ID) = range(6)
        columns = (
         (
          'name', [(txtRdr, gobject.TYPE_STRING)], (ROW_TITLE,), False, True),
         (
          'type', [(txtRdr, gobject.TYPE_STRING)], (ROW_TYPE,), False, True),
         (
          'size', [(txtRdr, gobject.TYPE_STRING)], (ROW_SIZE, ROW_ID), False, True),
         (
          'ter', [(txtRdr, gobject.TYPE_STRING)], (ROW_TERRAIN, ROW_ID), False, True),
         (
          'dif', [(txtRdr, gobject.TYPE_STRING)], (ROW_DIFF, ROW_ID), False, True),
         (
          'ID', [(txtRdr, gobject.TYPE_STRING)], (ROW_ID,), False, True))
        self.cachelist = listview = extListview.ExtListView(columns, sortable=True, useMarkup=True, canShowHideColumns=False)
        self.cachelist_contents = []
        listview.connect('extlistview-button-pressed', self.on_search_cache_clicked)
        xml.get_widget('scrolledwindow_search').add(listview)
        (COL_COORD_NAME, COL_COORD_LATLON, COL_COORD_ID, COL_COORD_COMMENT) = range(4)
        columns = (
         (
          'name', [(txtRdr, gobject.TYPE_STRING)], COL_COORD_NAME, False, True),
         (
          'pos', [(txtRdr, gobject.TYPE_STRING)], COL_COORD_LATLON, False, True),
         (
          'id', [(txtRdr, gobject.TYPE_STRING)], COL_COORD_ID, False, True),
         (
          'comment', [(txtRdr, gobject.TYPE_STRING)], (COL_COORD_COMMENT,), False, True))
        self.coordlist = extListview.ExtListView(columns, sortable=True, useMarkup=False, canShowHideColumns=False)
        self.coordlist.connect('extlistview-button-pressed', self.on_waypoint_clicked)
        xml.get_widget('scrolledwindow_coordlist').add(self.coordlist)
        self.notebook_all.set_current_page(1)
        gobject.timeout_add_seconds(10, self._check_notes_save)

    def _configure_map(self):
        try:
            coord = geo.Coordinate(self.settings['map_position_lat'], self.settings['map_position_lon'])
            zoom = self.settings['map_zoom']
        except KeyError:
            coord = self._get_best_coordinate(geo.Coordinate(50, 10))
            zoom = 6

        self.map = Map(center=coord, zoom=zoom)
        self.geocache_layer = GeocacheLayer(self._get_geocaches_callback, self.show_cache)
        self.marks_layer = MarksLayer()
        self.map.add_layer(self.geocache_layer)
        self.map.add_layer(self.marks_layer)
        self.map.add_layer(OsdLayer())
        self.core.connect('target-changed', self.marks_layer.on_target_changed)
        self.core.connect('good-fix', self.marks_layer.on_good_fix)
        self.core.connect('no-fix', self.marks_layer.on_no_fix)
        self.map.connect('tile-loader-changed', lambda widget, loader: self._update_zoom_buttons())

    def on_marked_label_clicked(self, event=None, widget=None):
        w = xml.get_widget('check_cache_marked')
        w.set_active(not w.get_active())

    def _check_notes_save(self):
        if self.current_cache != None and self.notes_changed:
            self.current_cache.notes = self.cache_elements['notes'].get_text(self.cache_elements['notes'].get_start_iter(), self.cache_elements['notes'].get_end_iter())
            self.core.save_cache_attribute(self.current_cache, 'notes')
            self.notes_changed = False
        if self.current_cache != None and self.fieldnotes_changed:
            self.current_cache.fieldnotes = self.cache_elements['fieldnotes'].get_text(self.cache_elements['fieldnotes'].get_start_iter(), self.cache_elements['fieldnotes'].get_end_iter())
            self.core.save_cache_attribute(self.current_cache, 'fieldnotes')
            self.fieldnotes_changed = False
        return

    def _configure_event_arrow(self, widget, event):
        (x, y, width, height) = widget.get_allocation()
        self.pixmap_arrow = gtk.gdk.Pixmap(widget.window, width, height)
        self.xgc_arrow = widget.window.new_gc()
        if self.north_indicator_layout == None:
            self.north_indicator_layout = widget.create_pango_layout('N')
            self.north_indicator_layout.set_alignment(pango.ALIGN_CENTER)
            self.north_indicator_layout.set_font_description(self.FONT_NORTH_INDICATOR)
        self.drawing_area_arrow_configured = True
        gobject.idle_add(self._draw_arrow)
        return

    def on_window_destroy(self, target, more=None, data=None):
        self.core.on_destroy()
        gtk.main_quit()

    def _get_best_coordinate(self, start=None):
        if start != None:
            c = start
        elif self.gps_data != None and self.gps_data.position != None:
            c = self.gps_data.position
        elif self.core.current_target != None:
            c = self.core.current_target
        else:
            c = geo.Coordinate(0, 0)
        return c

    def display_results_advanced(self, caches):
        label = xml.get_widget('label_too_much_results')
        too_many = len(caches) > self.MAX_NUM_RESULTS
        if too_many:
            text = 'Too many results. Only showing first %d.' % self.MAX_NUM_RESULTS
            label.set_text(text)
            label.show()
            caches = caches[:self.MAX_NUM_RESULTS]
        else:
            label.hide()
        self.cachelist_contents = caches
        rows = []
        for r in caches:
            if r.size == -1:
                s = '?'
            else:
                s = '%d' % r.size
            if r.difficulty == -1:
                d = '?'
            else:
                d = '%.1f' % (r.difficulty / 10)
            if r.terrain == -1:
                t = '?'
            else:
                t = '%.1f' % (r.terrain / 10)
            title = self._format_cache_title(r)
            rows.append((title, r.type, s, t, d, r.name))

        self.cachelist.replaceContent(rows)
        self.notebook_search.set_current_page(1)
        self.map.redraw_layers()

    @staticmethod
    def _format_cache_title(cache):
        m = cache.title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if cache.marked and cache.found:
            return '<span bgcolor="yellow" fgcolor="gray">%s</span>' % m
        else:
            if cache.marked:
                return '<span bgcolor="yellow" fgcolor="black">%s</span>' % m
            if cache.found:
                return '<span fgcolor="gray">%s</span>' % m
            return m

    def _draw_arrow(self):
        outer_circle_size = 3
        circle_border = 10
        indicator_border = 40
        distance_attarget = 50
        distance_near = 150
        disabled_border_size = 30
        signal_width = 15
        error_circle_size = 0.95
        error_circle_width = 7
        if not self.drawing_area_arrow_configured:
            return
        else:
            widget = self.drawing_area_arrow
            (x, y, width, height) = widget.get_allocation()
            disabled = not (self.gps_has_fix and self.gps_target_bearing != None and self.gps_target_distance != None)
            self.pixmap_arrow.draw_rectangle(widget.get_style().bg_gc[gtk.STATE_NORMAL], True, 0, 0, width, height)
            if disabled:
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_DISABLED)
                border = disabled_border_size
                self.pixmap_arrow.draw_line(self.xgc_arrow, border, border, width - border, height - border)
                self.pixmap_arrow.draw_line(self.xgc_arrow, border, height - border, width - border, border)
                self.drawing_area_arrow.queue_draw()
                return False
            if self.COLOR_QUALITY_OUTER != None:
                self.xgc_arrow.line_width = 1
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_QUALITY_OUTER)
                self.pixmap_arrow.draw_rectangle(self.xgc_arrow, True, width - signal_width - 2, 0, signal_width + 2, height)
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_QUALITY_INNER)
                usable_height = height - 1
                target_height = int(round(usable_height * self.gps_data.quality))
                self.pixmap_arrow.draw_rectangle(self.xgc_arrow, True, width - signal_width - 1, usable_height - target_height, signal_width, target_height)
            display_bearing = self.gps_target_bearing - self.gps_data.bearing
            display_distance = self.gps_target_distance
            display_north = math.radians(self.gps_data.bearing)
            try:
                sun_angle = self.astral.get_sun_azimuth_from_fix(self.gps_data)
            except Exception, e:
                logger.exception("Couldn't get sun angle: %s" % e)
                sun_angle = None

            if sun_angle != None:
                display_sun = math.radians((-sun_angle + self.gps_data.bearing) % 360)
            if self.COLOR_ARROW_CROSS != None:
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_CROSS)
                self.pixmap_arrow.draw_line(self.xgc_arrow, width / 2, height, width / 2, 0)
                self.pixmap_arrow.draw_line(self.xgc_arrow, 0, height / 2, width, height / 2)
            self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_CIRCLE)
            self.xgc_arrow.line_width = outer_circle_size
            circle_size = min(height, width) / 2 - circle_border
            indicator_dist = min(height, width) / 2 - indicator_border
            center_x, center_y = width / 2, height / 2
            self.pixmap_arrow.draw_arc(self.xgc_arrow, False, center_x - circle_size, center_y - circle_size, circle_size * 2, circle_size * 2, 0, 23040)
            if display_distance > self.DISTANCE_DISABLE_ARROW:
                self.xgc_arrow.line_width = error_circle_width
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_ERROR)
                self.xgc_arrow.set_dashes(1, (5, 5))
                self.xgc_arrow.line_style = gtk.gdk.LINE_ON_OFF_DASH
                ecc = int(error_circle_size * circle_size)
                err = min(self.gps_data.error_bearing, 181)
                err_start = int((90 - (display_bearing + err)) * 64)
                err_delta = int(err * 2 * 64)
                self.pixmap_arrow.draw_arc(self.xgc_arrow, False, center_x - ecc, center_y - ecc, ecc * 2, ecc * 2, err_start, err_delta)
                self.xgc_arrow.line_style = gtk.gdk.LINE_SOLID
            if display_distance < distance_attarget:
                color = self.COLOR_ARROW_ATTARGET
            elif display_distance < distance_near:
                color = self.COLOR_ARROW_NEAR
            else:
                color = self.COLOR_ARROW_DEFAULT
            self.xgc_arrow.set_rgb_fg_color(color)
            if display_distance != None and display_distance > self.DISTANCE_DISABLE_ARROW:
                arrow_transformed = self._get_arrow_transformed(x, y, width, height, display_bearing)
                self.pixmap_arrow.draw_polygon(self.xgc_arrow, True, arrow_transformed)
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_OUTER_LINE)
                self.xgc_arrow.line_width = self.ARROW_LINE_WIDTH
                self.pixmap_arrow.draw_polygon(self.xgc_arrow, False, arrow_transformed)
                (ni_w, ni_h) = self.north_indicator_layout.get_size()
                position_x = int(width / 2 - math.sin(display_north) * indicator_dist - ni_w / pango.SCALE / 2)
                position_y = int(height / 2 - math.cos(display_north) * indicator_dist - ni_h / pango.SCALE / 2)
                self.xgc_arrow.set_function(gtk.gdk.COPY)
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_NORTH_INDICATOR)
                self.pixmap_arrow.draw_layout(self.xgc_arrow, position_x, position_y, self.north_indicator_layout)
                if sun_angle != None:
                    sun_center_x = int(width / 2 - math.sin(display_sun) * indicator_dist)
                    sun_center_y = int(height / 2 - math.cos(display_sun) * indicator_dist)
                    sun_indicator_layout = widget.create_pango_layout('sun')
                    sun_indicator_layout.set_alignment(pango.ALIGN_CENTER)
                    sun_indicator_layout.set_font_description(self.FONT_SUN_INDICATOR)
                    circle_size = int(sun_indicator_layout.get_size()[0] / pango.SCALE / 2)
                    self.xgc_arrow.set_function(gtk.gdk.COPY)
                    self.xgc_arrow.set_rgb_fg_color(self.COLOR_SUN_INDICATOR)
                    self.pixmap_arrow.draw_arc(self.xgc_arrow, True, sun_center_x - circle_size, sun_center_y - circle_size, circle_size * 2, circle_size * 2, 0, 23040)
                    position_x = int(sun_center_x - sun_indicator_layout.get_size()[0] / pango.SCALE / 2)
                    position_y = int(sun_center_y - sun_indicator_layout.get_size()[1] / pango.SCALE / 2)
                    self.xgc_arrow.set_rgb_fg_color(self.COLOR_SUN_INDICATOR_TEXT)
                    self.pixmap_arrow.draw_layout(self.xgc_arrow, position_x, position_y, sun_indicator_layout)
            else:
                circle_size = int(max(height / 2.5, width / 2.5))
                self.pixmap_arrow.draw_arc(self.xgc_arrow, True, width / 2 - circle_size / 2, height / 2 - circle_size / 2, circle_size, circle_size, 0, 23040)
                self.xgc_arrow.set_rgb_fg_color(self.COLOR_ARROW_OUTER_LINE)
                self.xgc_arrow.line_width = self.ARROW_LINE_WIDTH
                self.pixmap_arrow.draw_arc(self.xgc_arrow, False, width / 2 - circle_size / 2, height / 2 - circle_size / 2, circle_size, circle_size, 0, 23040)
            self.drawing_area_arrow.queue_draw()
            return False

    @staticmethod
    def _get_arrow_transformed(root_x, root_y, width, height, angle):
        multiply = height / (2 * (2 - SimpleGui.ARROW_OFFSET))
        offset_x = width / 2
        offset_y = height / 2
        s = multiply * math.sin(math.radians(angle))
        c = multiply * math.cos(math.radians(angle))
        arrow_transformed = [ (int(x * c + offset_x - y * s) + root_x, int(y * c + offset_y + x * s) + root_y) for (x, y) in SimpleGui.ARROW_SHAPE
                            ]
        return arrow_transformed

    def _expose_event_arrow(self, widget, event):
        (x, y, width, height) = event.area
        widget.window.draw_drawable(self.xgc_arrow, self.pixmap_arrow, x, y, x, y, width, height)
        return False

    def hide_progress(self):
        self.progressbar.hide()

    def _load_images(self):
        if self.current_cache == None:
            self._update_cache_image(reset=True)
            return
        else:
            if len(self.current_cache.get_images()) > 0:
                self.images = self.current_cache.get_images().items()
            else:
                self.images = {}
            self._update_cache_image(reset=True)
            return

    def on_download_clicked(self, widget, data=None):
        self.core.on_download(self.map.get_visible_area())

    def on_download_details_map_clicked(self, some, thing=None):
        logger.debug('Downloading geocaches on map.')
        self.core.on_download_descriptions(self.map.get_visible_area())

    def on_download_details_sync_clicked(self, something):
        self.core.on_download_descriptions(self.map.get_visible_area())

    def on_actions_clicked(self, widget, event):
        xml.get_widget('menu_actions').popup(None, None, None, event.button, event.get_time())
        return

    def on_cache_marked_toggled(self, widget):
        if self.current_cache == None:
            return
        else:
            self._update_mark(self.current_cache, widget.get_active())
            return

    def on_change_coord_clicked(self, something):
        self.set_target(self.show_coordinate_input(self.core.current_target))

    def _get_search_selected_cache(self):
        index = self.cachelist.getFirstSelectedRowIndex()
        if index == None:
            return (None, None)
        else:
            cache = self.cachelist_contents[index]
            return (
             index, cache)

    def on_result_marked_toggled(self, widget):
        (index, cache) = self._get_search_selected_cache()
        if cache == None:
            return
        else:
            self._update_mark(cache, widget.get_active())
            title = self._format_cache_title(cache)
            self.cachelist.setItem(index, 0, title)
            return

    def _update_mark(self, cache, status):
        cache.marked = status
        self.core.save_cache_attribute(cache, 'marked')
        self.map.redraw_layers()

    def on_download_cache_clicked(self, something):
        self.core.on_download_cache(self.current_cache)

    def on_export_cache_clicked(self, something):
        if self.input_export_path.get_value().strip() == '':
            self.show_error('Please input path to export to.')
            return
        self.core.on_export_cache(self.current_cache, self.input_export_path.get_value())

    def _on_good_fix(self, core, gps_data, distance, bearing):
        self.gps_data = gps_data
        self.gps_last_good_fix = gps_data
        self.gps_has_fix = True
        self.gps_target_distance = distance
        self.gps_target_bearing = bearing
        self._draw_arrow()
        self.update_gps_display()

    def on_image_next_clicked(self, something):
        if len(self.images) == 0:
            self._update_cache_image(reset=True)
            return
        self.image_no += 1
        self.image_no %= len(self.images)
        self._update_cache_image()

    def on_image_zoom_clicked(self, something):
        self.image_zoomed = not self.image_zoomed
        self._update_cache_image()

    def _on_fieldnotes_changed(self, caller):
        widget = self.label_fieldnotes
        self._check_notes_save()
        l = self.core.get_new_fieldnotes_count()
        if l > 0:
            widget.set_text('you have created %d fieldnotes' % l)
            self.button_upload_fieldnotes.set_sensitive(True)
        else:
            widget.set_text('you have not created any new fieldnotes')
            self.button_upload_fieldnotes.set_sensitive(False)

    def on_list_marked_clicked(self, widget):
        self.core.on_start_search_advanced(marked=True)

    def _on_no_fix(self, caller, gps_data, status):
        self.gps_data = gps_data
        self.label_bearing.set_text('No Fix')
        self.label_latlon.set_text(status)
        self.gps_has_fix = False
        self.update_gps_display()
        self._draw_arrow()

    def on_notes_changed(self, something, somethingelse=None):
        self.notes_changed = True

    def on_fieldnotes_changed(self, something, somethingelse):
        self.fieldnotes_changed = True

    def on_fieldnotes_log_changed(self, something):
        from time import gmtime
        from time import strftime
        if self.current_cache == None:
            return
        else:
            if self.cache_elements['log_found'].get_active():
                log = geocaching.GeocacheCoordinate.LOG_AS_FOUND
            elif self.cache_elements['log_notfound'].get_active():
                log = geocaching.GeocacheCoordinate.LOG_AS_NOTFOUND
            elif self.cache_elements['log_note'].get_active():
                log = geocaching.GeocacheCoordinate.LOG_AS_NOTE
            else:
                log = geocaching.GeocacheCoordinate.LOG_NO_LOG
            logdate = strftime('%Y-%m-%d', gmtime())
            self.cache_elements['log_date'].set_text('fieldnote date: %s' % logdate)
            self.current_cache.logas = log
            self.current_cache.logdate = logdate
            self.core.save_fieldnote(self.current_cache)
            return

    def on_save_config(self, something):
        if not self.block_changes:
            self._on_save_settings(self.core)

    def on_search_action_center_clicked(self, widget):
        (index, cache) = self._get_search_selected_cache()
        if cache == None:
            return
        else:
            self.set_center(cache)
            self.notebook_all.set_current_page(1)
            return

    def on_search_action_set_target_clicked(self, widget):
        (index, cache) = self._get_search_selected_cache()
        if cache == None:
            return
        else:
            self.current_cache = cache
            self.set_target(cache)
            self.notebook_all.set_current_page(0)
            return

    def on_search_action_view_details_clicked(self, widget):
        (index, cache) = self._get_search_selected_cache()
        if cache == None:
            return
        else:
            self.show_cache(cache)
            return

    def on_search_advanced_clicked(self, something):

        def get_val_from_text(input, use_max):
            if not use_max:
                valmap = {'1..1.5': 1, '2..2.5': 2, '3..3.5': 3, '4..4.5': 4, '5': 5}
                default = 1
            else:
                valmap = {'1..1.5': 1.5, '2..2.5': 2.5, '3..3.5': 3.5, '4..4.5': 4.5, '5': 5}
                default = 5
            if input in valmap:
                return valmap[input]
            else:
                return default

        types = [ a for a in [geocaching.GeocacheCoordinate.TYPE_REGULAR,
         geocaching.GeocacheCoordinate.TYPE_MULTI,
         geocaching.GeocacheCoordinate.TYPE_MYSTERY,
         geocaching.GeocacheCoordinate.TYPE_VIRTUAL] if self.search_elements['type'][a].get_active()
                ]
        if self.search_elements['type']['all'].get_active() or len(types) == 0:
            types = None
        name_search = self.search_elements['name'].get_text()
        status = self.search_elements['status'].get_active_text()
        if status == 'not found':
            found = False
            marked = None
        elif status == 'found':
            found = True
            marked = None
        elif status == 'marked & new':
            found = False
            marked = True
        else:
            found = None
            marked = None
        sizes = [ a for a in [1, 2, 3, 4, 5] if self.search_elements['size'][a].get_active() ]
        if len(sizes) == 0:
            sizes = None
        search = {}
        for i in ['diff', 'terr']:
            sel = self.search_elements[i]['selector'].get_active_text()
            value = self.search_elements[i]['value'].get_active_text()
            if sel == 'min':
                search[i] = (
                 get_val_from_text(value, False), 5)
            elif sel == 'max':
                search[i] = (
                 0, get_val_from_text(value, True))
            elif sel == '=':
                search[i] = (
                 get_val_from_text(value, False), get_val_from_text(value, True))
            else:
                search[i] = None

        if self.search_elements['inview'].get_active():
            location = self.map.get_visible_area()
        else:
            location = None
        if found == None and name_search == None and sizes == None and search['terr'] == None and search['diff'] == None and types == None:
            self.filtermsg.hide()
        else:
            self.filtermsg.show()
        self.core.on_start_search_advanced(found=found, name_search=name_search, size=sizes, terrain=search['terr'], diff=search['diff'], ctype=types, location=location, marked=marked)
        return

    def on_search_cache_clicked(self, listview, event, element):
        if element == None:
            return
        else:
            (index, cache) = self._get_search_selected_cache()
            if cache == None:
                return
            if event.type == gtk.gdk._2BUTTON_PRESS:
                self.show_cache(cache)
                self.set_center(cache)
            else:
                self.check_result_marked.set_active(cache.marked)
            return

    def on_search_reset_clicked(self, something):
        self.filtermsg.hide()
        self.core.on_start_search_advanced()

    def on_set_target_clicked(self, something):
        if self.current_cache == None:
            return
        else:
            self.set_target(self.current_cache)
            self.notebook_all.set_current_page(0)
            return

    def on_set_target_center(self, some, thing=None):
        self.set_target(self.map.get_center())

    def on_show_target_clicked(self, some=None, data=None):
        if self.core.current_target == None:
            return
        else:
            self.set_center(self.core.current_target)
            return

    def on_track_toggled(self, widget, data=None):
        logger.info('Track toggled, new state: ' + repr(widget.get_active()))
        self.marks_layer.set_follow_position(widget.get_active())

    def on_upload_fieldnotes(self, something):
        self.core.on_upload_fieldnotes()

    def on_waypoint_clicked(self, listview, event, element):
        if event.type != gtk.gdk._2BUTTON_PRESS or element == None:
            return
        else:
            if self.current_cache == None:
                return
            if element[0] == 0:
                self.set_target(self.current_cache)
                self.notebook_all.set_current_page(0)
            else:
                wpt = self.current_cache.get_waypoints()[(element[0] - 1)]
                if wpt['lat'] == -1 or wpt['lon'] == -1:
                    return
                self.set_target(geo.Coordinate(wpt['lat'], wpt['lon'], wpt['id']))
                self.notebook_all.set_current_page(0)
            return

    def on_zoomin_clicked(self, widget, data=None):
        self.map.relative_zoom(+1)

    def on_zoomout_clicked(self, widget, data=None):
        self.map.relative_zoom(-1)

    def _update_cache_image(self, reset=False):
        if reset:
            self.image_zoomed = False
            self.image_no = 0
            if len(self.images) == 0:
                self.image_cache.set_from_stock(gtk.STOCK_CANCEL, -1)
                self.image_cache_caption.set_text("There's nothing to see here.")
                return
        try:
            if self.current_cache == None or len(self.images) <= self.image_no:
                self._update_cache_image(True)
                return
                filename = path.join(self.settings['download_output_dir'], self.images[self.image_no][0])
                if not path.exists(filename):
                    self.image_cache_caption.set_text('not found: %s' % filename)
                    self.image_cache.set_from_stock(gtk.STOCK_GO_FORWARD, -1)
                    return
                mw, mh = self.image_zoomed or self.scrolledwindow_image.get_allocation().width - 10, self.scrolledwindow_image.get_allocation().height - 10
                pb = gtk.gdk.pixbuf_new_from_file_at_size(filename, mw, mh)
            else:
                pb = gtk.gdk.pixbuf_new_from_file(filename)
            self.image_cache.set_from_pixbuf(pb)
            caption = self.images[self.image_no][1]
            self.image_cache_caption.set_text('<b>%d</b> %s' % (self.image_no, caption))
            self.image_cache_caption.set_use_markup(True)
        except Exception, e:
            logger.exception('Error loading image: %s' % e)

        return

    @staticmethod
    def replace_image_tag(m):
        if m.group(1) != None and m.group(1).strip() != '':
            return ' [Image: %s] ' % m.group(1).strip()
        else:
            return ' [Image] '
            return

    def set_center(self, coord, noupdate=False, reset_track=True):
        logger.info('Set Center to %s with reset_track = %s' % (coord, reset_track))
        self.map.set_center(coord, not noupdate)

    def _set_track_mode(self, mode):
        self.marks_layer.set_follow_position(mode)
        try:
            self.button_track.set_active(mode)
        except:
            pass

    def _get_track_mode(self):
        return self.marks_layer.get_follow_position()

    def set_progress(self, fraction, text):
        self.progressbar.show()
        self.progressbar.set_text(text)
        self.progressbar.set_fraction(fraction)

    def set_target(self, cache):
        self.core.set_target(cache)

    def _on_target_changed(self, caller, cache, distance, bearing):
        self.gps_target_distance = distance
        self.gps_target_bearing = bearing
        self.label_target.set_text("<span size='large'>%s\n%s</span>" % (cache.get_lat(self.format), cache.get_lon(self.format)))
        self.label_target.set_use_markup(True)

    def show(self):
        self.window.show_all()
        gtk.main()

    def show_cache(self, cache):
        if cache == None:
            return
        else:
            self._check_notes_save()
            self.current_cache = cache
            self.cache_elements['title'].set_text('<b>%s</b> %s' % (cache.name, cache.title))
            self.cache_elements['title'].set_use_markup(True)
            self.cache_elements['type'].set_text('%s' % cache.type)
            if cache.size == -1:
                self.cache_elements['size'].set_text('?')
            else:
                self.cache_elements['size'].set_text('%d/5' % cache.size)
            if cache.terrain == -1:
                self.cache_elements['terrain'].set_text('?')
            else:
                self.cache_elements['terrain'].set_text('%s/5' % cache.get_terrain())
            if cache.difficulty == -1:
                self.cache_elements['difficulty'].set_text('?')
            else:
                self.cache_elements['difficulty'].set_text('%s/5' % cache.get_difficulty())
            text_shortdesc = self._strip_html(cache.shortdesc)
            if cache.status == geocaching.GeocacheCoordinate.STATUS_DISABLED:
                text_shortdesc = 'ATTENTION! This Cache is Disabled!\n--------------\n' + text_shortdesc
            text_longdesc = self._strip_html(re.sub('(?i)<img[^>]+?>', ' [to get all images, re-download description] ', re.sub('\\[\\[img:([^\\]]+)\\]\\]', lambda a: self._replace_image_callback(a, cache), cache.desc)))
            if text_longdesc == '':
                text_longdesc = '(no description available)'
            if not text_shortdesc == '':
                showdesc = text_shortdesc + '\n\n' + text_longdesc
            else:
                showdesc = text_longdesc
            self.cache_elements['desc'].set_text(showdesc)
            self.cache_elements['marked'].set_active(True if cache.marked else False)
            self.notebook_cache.set_current_page(0)
            self.notebook_all.set_current_page(2)
            logs = cache.get_logs()
            if len(logs) > 0:
                text_hints = 'LOGS:\n'
                for l in logs:
                    if l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_FOUND:
                        t = 'FOUND'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_NOTFOUND:
                        t = 'NOT FOUND'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_NOTE:
                        t = 'NOTE'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_MAINTENANCE:
                        t = 'MAINTENANCE'
                    else:
                        t = l['type'].upper()
                    text_hints += '%s by %s at %4d/%d/%d: %s\n\n' % (t, l['finder'], int(l['year']), int(l['month']), int(l['day']), l['text'])

                text_hints += '\n----------------\n'
            else:
                text_hints = 'NO LOGS.\n\n'
            hints = cache.hints.strip()
            if hints == '':
                hints = '(no hints available)'
                showdesc += '\n[no hints]'
            else:
                showdesc += '\n[hints available]'
            text_hints += 'HINTS:\n' + hints
            self.cache_elements['hints'].set_text(text_hints)
            format = lambda n: '%s %s' % (re.sub(' ', '', n.get_lat(geo.Coordinate.FORMAT_DM)), re.sub(' ', '', n.get_lon(geo.Coordinate.FORMAT_DM)))
            rows = [(cache.name, format(cache), '(cache coord)', '')]
            for w in cache.get_waypoints():
                if not (w['lat'] == -1 and w['lon'] == -1):
                    latlon = format(geo.Coordinate(w['lat'], w['lon']))
                else:
                    latlon = '???'
                rows.append((w['name'], latlon, w['id'], self._strip_html(w['comment'])))

            self.coordlist.replaceContent(rows)
            self.button_download_details.set_sensitive(True)
            self.cache_elements['notes'].set_text(cache.notes if cache.notes != None else '')
            self.cache_elements['fieldnotes'].set_text(cache.fieldnotes if cache.fieldnotes != None else '')
            if cache.logas == geocaching.GeocacheCoordinate.LOG_AS_FOUND:
                self.cache_elements['log_found'].set_active(True)
            elif cache.logas == geocaching.GeocacheCoordinate.LOG_AS_NOTFOUND:
                self.cache_elements['log_notfound'].set_active(True)
            elif cache.logas == geocaching.GeocacheCoordinate.LOG_AS_NOTE:
                self.cache_elements['log_note'].set_active(True)
            else:
                self.cache_elements['log_no'].set_active(True)
            if cache.logdate != '':
                self.cache_elements['log_date'].set_text('fieldnote date: %s' % cache.logdate)
            else:
                self.cache_elements['log_date'].set_text('fieldnote date: not set')
            self._load_images()
            self.image_no = 0
            if len(self.images) > 0:
                showdesc += '\n[%d image(s) available]' % len(self.images)
            else:
                showdesc += '\n[no images available]'
            self.cache_elements['desc'].set_text(showdesc)
            return

    def _replace_image_callback(self, match, coordinate):
        if match.group(1) in coordinate.get_images():
            desc = coordinate.get_images()[match.group(1)]
            if desc.strip() != '':
                return ' [image: %s] ' % desc
            return ' [image] '
        else:
            return ' [image not found -- please re-download geocache description] '

    def show_error(self, errormsg):
        gtk.gdk.threads_enter()
        error_dlg = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, '%s' % errormsg)
        error_dlg.connect('response', lambda w, d: error_dlg.destroy())
        error_dlg.run()
        error_dlg.destroy()
        gtk.gdk.threads_leave()

    def show_success(self, message):
        gtk.gdk.threads_enter()
        suc_dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO, message_format=message, buttons=gtk.BUTTONS_OK)
        suc_dlg.run()
        suc_dlg.destroy()
        gtk.gdk.threads_leave()

    def show_coordinate_input(self, start):
        udr = UpdownRows(self.format, start, False)
        dialog = gtk.Dialog('Change Target', None, gtk.DIALOG_MODAL, (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        frame = gtk.Frame('Latitude')
        frame.add(udr.table_lat)
        dialog.vbox.pack_start(frame)
        frame = gtk.Frame('Longitude')
        frame.add(udr.table_lon)
        dialog.vbox.pack_start(frame)
        dialog.show_all()
        dialog.run()
        dialog.destroy()
        c = udr.get_value()
        c.name = 'manual'
        return c

    @staticmethod
    def _strip_html(text):
        return HTMLManipulations.strip_html_visual(text, SimpleGui.replace_image_tag)

    def update_gps_display(self):
        if self.gps_data == None:
            return
        else:
            if self.gps_data.sats == 0:
                label = 'No sats available'
            else:
                label = '%d/%d sats, error: ±%3.1fm' % (self.gps_data.sats, self.gps_data.sats_known, self.gps_data.error)
                if self.gps_data.dgps:
                    label += ' DGPS'
            self.label_quality.set_text(label)
            if self.gps_data.altitude == None or self.gps_data.bearing == None:
                return
            self.label_altitude.set_text('alt %3dm' % self.gps_data.altitude)
            self.label_bearing.set_text('%d°' % self.gps_data.bearing)
            self.label_latlon.set_text("<span size='large'>%s\n%s</span>" % (self.gps_data.position.get_lat(self.format), self.gps_data.position.get_lon(self.format)))
            self.label_latlon.set_use_markup(True)
            if self.core.current_target == None:
                return
            if self.gps_has_fix:
                target_distance = self.gps_target_distance
                label = geo.Coordinate.format_distance(target_distance)
                self.label_dist.set_text("<span size='large'>%s</span>" % label)
                self.label_dist.set_use_markup(True)
            else:
                self.label_dist.set_text("<span size='large'>No Fix</span>")
                self.label_dist.set_use_markup(True)
            return

    def _on_settings_changed_gui(self, settings):
        for x in self.SETTINGS_CHECKBOXES:
            if x in self.settings:
                w = xml.get_widget('check_%s' % x)
                if w == None:
                    continue
                w.set_active(self.settings[x])

        for x in self.SETTINGS_INPUTS:
            if x in self.settings:
                w = xml.get_widget('input_%s' % x)
                if w == None:
                    continue
                w.set_text(str(self.settings[x]))

        return

    @staticmethod
    def shorten_name(s, chars):
        max_pos = chars
        min_pos = chars - 10
        NOT_FOUND = -1
        suffix = '…'
        length = len(s)
        if length <= max_pos:
            return s
        else:
            try:
                end = s.rindex('.', min_pos, max_pos)
            except ValueError:
                end = s.rfind(' ', min_pos, max_pos)
                if end == NOT_FOUND:
                    end = max_pos

            return s[0:end] + suffix

    def _on_settings_changed(self, caller, settings, source):
        logger.debug('Got settings from %s, len() = %d, source = %s' % (caller, len(settings), source))
        self.settings.update(settings)
        self.block_changes = True
        if 'options_show_name' in settings:
            self.geocache_layer.set_show_name(settings['options_show_name'])
        if 'options_map_double_size' in settings:
            self.map.set_double_size(settings['options_map_double_size'])
        if 'map_zoom' in settings:
            if self.map.get_zoom() != settings['map_zoom']:
                self.map.set_zoom(settings['map_zoom'])
        if 'map_position_lat' in settings and 'map_position_lon' in settings:
            self.set_center(geo.Coordinate(settings['map_position_lat'], settings['map_position_lon']), reset_track=False)
        if 'map_follow_position' in settings:
            self._set_track_mode(settings['map_follow_position'])
        if 'last_target_lat' in settings:
            self.set_target(geo.Coordinate(settings['last_target_lat'], settings['last_target_lon']))
        if 'last_selected_geocache' in settings and settings['last_selected_geocache'] not in (None,
                                                                                               ''):
            cache = self.core.get_geocache_by_name(settings['last_selected_geocache'])
            if cache != None:
                self.set_current_cache(cache)
        self._on_settings_changed_gui(settings)
        self.block_changes = False
        return

    def _on_save_settings(self, caller):
        c = self.map.get_center()
        settings = {}
        settings['map_position_lat'] = c.lat
        settings['map_position_lon'] = c.lon
        settings['map_zoom'] = self.map.get_zoom()
        settings['map_follow_position'] = self._get_track_mode()
        if self.current_cache != None:
            settings['last_selected_geocache'] = self.current_cache.name
        for x in self.SETTINGS_CHECKBOXES:
            w = xml.get_widget('check_%s' % x)
            if w != None:
                settings[x] = w.get_active()
            else:
                logger.info("Couldn't find widget: check_%s" % x)

        for x in self.SETTINGS_INPUTS:
            w = xml.get_widget('input_%s' % x)
            if w != None:
                settings[x] = w.get_text()
            else:
                logger.info("Couldn't find widget: input_%s" % x)

        caller.save_settings(settings, self)
        return

    def on_button_check_updates_clicked(self, caller):
        updates = self.core.try_update()
        if updates != None:
            gobject.idle_add(self.show_success, "%d modules upgraded. There's no need to restart AGTL." % updates)
        return False


class Updown():

    def __init__(self, table, position, small):
        self.value = int(0)
        self.label = gtk.Label('<b>0</b>')
        self.label.set_use_markup(True)
        self.button_up = gtk.Button('+')
        self.button_down = gtk.Button('-')
        table.attach(self.button_up, position, position + 1, 0, 1)
        table.attach(self.label, position, position + 1, 1, 2, 0, 0)
        table.attach(self.button_down, position, position + 1, 2, 3)
        self.button_up.connect('clicked', self.value_up)
        self.button_down.connect('clicked', self.value_down)
        if small != None:
            if small:
                font = pango.FontDescription('sans 8')
            else:
                font = pango.FontDescription('sans 12')
            self.label.modify_font(font)
            self.button_up.child.modify_font(font)
            self.button_down.child.modify_font(font)
        return

    def value_up(self, target):
        self.value = int((self.value + 1) % 10)
        self.update()

    def value_down(self, target):
        self.value = int((self.value - 1) % 10)
        self.update()

    def set_value(self, value):
        self.value = int(value)
        self.update()

    def update(self):
        self.label.set_markup('<b>%d</b>' % self.value)


class PlusMinusUpdown():

    def __init__(self, table, position, labels, small=None):
        self.is_neg = False
        self.labels = labels
        self.button = gtk.Button(labels[0])
        table.attach(self.button, position, position + 1, 1, 2, gtk.FILL, gtk.FILL)
        self.button.connect('clicked', self.value_toggle)
        if small != None:
            self.button.child.modify_font(pango.FontDescription('sans 8'))
        return

    def value_toggle(self, target):
        self.is_neg = not self.is_neg
        self.update()

    def set_value(self, value):
        self.is_neg = value < 0
        self.update()

    def get_value(self):
        if self.is_neg:
            return -1
        else:
            return 1

    def update(self):
        if self.is_neg:
            text = self.labels[0]
        else:
            text = self.labels[1]
        self.button.child.set_text(text)


class UpdownRows():

    def __init__(self, format, coord, large_dialog):
        self.format = format
        self.large_dialog = large_dialog
        if coord == None:
            coord = geo.Coordinate(50, 10, 'none')
        if format == geo.Coordinate.FORMAT_DM:
            (init_lat, init_lon) = coord.to_dm_array()
        elif format == geo.Coordinate.FORMAT_D:
            (init_lat, init_lon) = coord.to_d_array()
        (self.table_lat, self.chooser_lat) = self.generate_table(False, init_lat)
        (self.table_lon, self.chooser_lon) = self.generate_table(True, init_lon)
        self.switcher_lat.set_value(coord.lat)
        self.switcher_lon.set_value(coord.lon)
        return

    def get_value(self):
        coord = geo.Coordinate(0, 0)
        lat_values = [ ud.value for ud in self.chooser_lat ]
        lon_values = [ ud.value for ud in self.chooser_lon ]
        if self.format == geo.Coordinate.FORMAT_DM:
            coord.from_dm_array(self.switcher_lat.get_value(), lat_values, self.switcher_lon.get_value(), lon_values)
        elif self.format == geo.Coordinate.FORMAT_D:
            coord.from_d_array(self.switcher_lat.get_value(), lat_values, self.switcher_lon.get_value(), lon_values)
        return coord

    def generate_table(self, is_long, initial_value):
        interrupt = {}
        if self.format == geo.Coordinate.FORMAT_DM and not is_long:
            small = 2
            num = 7
            interrupt[3] = '°'
            interrupt[6] = '.'
        elif self.format == geo.Coordinate.FORMAT_DM and is_long:
            small = 3
            num = 8
            interrupt[4] = '°'
            interrupt[7] = '.'
        elif self.format == geo.Coordinate.FORMAT_D and not is_long:
            small = 2
            num = 7
            interrupt[3] = '.'
        elif self.format == geo.Coordinate.FORMAT_D and is_long:
            small = 3
            num = 8
            interrupt[4] = '.'
        table = gtk.Table(3, num + len(interrupt) + 1, False)
        if is_long:
            self.switcher_lon = PlusMinusUpdown(table, 0, ['W', 'E'], None if self.large_dialog else False)
        else:
            self.switcher_lat = PlusMinusUpdown(table, 0, ['S', 'N'], None if self.large_dialog else False)
        chooser = []
        cn = 0
        for i in xrange(1, num + len(interrupt) + 1):
            if i in interrupt:
                table.attach(gtk.Label(interrupt[i]), i, i + 1, 1, 2, 0, 0)
            else:
                ud = Updown(table, i, cn < small if not self.large_dialog else None)
                if cn < len(initial_value):
                    ud.set_value(initial_value[cn])
                    chooser.append(ud)
                    cn = cn + 1

        return [
         table, chooser]