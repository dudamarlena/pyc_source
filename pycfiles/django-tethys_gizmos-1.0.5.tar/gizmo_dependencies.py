# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/gizmo_dependencies.py
# Compiled at: 2015-03-05 14:41:04
from django.conf import settings

def global_dependencies(context):
    """
    Dependencies that are loaded for all tethys gizmos (after gizmo dependencies).
    """
    return ('tethys_gizmos/css/tethys_gizmos.css', 'tethys_gizmos/js/tethys_gizmos.js')


def date_picker(context):
    """
    Dependencies for date_picker gizmo.
    """
    return ('tethys_gizmos/vendor/bootstrap_datepicker/css/datepicker3.css', 'tethys_gizmos/vendor/bootstrap_datepicker/js/bootstrap_datepicker.js')


def select_input(context):
    """
    Dependencies for select2_input gizmo.
    """
    return ('tethys_gizmos/vendor/select2_3.5.1/select2.css', 'tethys_gizmos/vendor/select2_3.5.1/select2.js')


def highcharts_plot_view(context):
    """
    Dependencies for highcharts_plot_view gizmo.
    """
    return ('tethys_gizmos/vendor/highcharts/js/highcharts.js', 'tethys_gizmos/vendor/highcharts/js/highcharts-more.js',
            'tethys_gizmos/vendor/highcharts/js/modules/exporting.js')


def map_view(context):
    """
    Dependencies for map_view gizmo.
    """
    return ('tethys_gizmos/css/tethys_map_view.css', 'tethys_gizmos/js/tethys_map_view.js')


def toggle_switch(context):
    """
    Dependencies for toggle_switch gizmo.
    """
    return ('tethys_gizmos/vendor/bootstrap_switch/dist/css/bootstrap3/bootstrap-switch.min.css',
            'tethys_gizmos/vendor/bootstrap_switch/dist/js/bootstrap-switch.min.js')


def editable_google_map(context):
    """
    Dependencies for editable_google_map gizmo.
    """
    return ('tethys_gizmos/vendor/farbtastic/farbtastic.css', 'tethys_gizmos/vendor/farbtastic/farbtastic.js',
            'tethys_gizmos/js/tethys_editable_map.js')


def google_map_view(context):
    """
    Dependencies for google_map_view gizmo.
    """
    return ('tethys_gizmos/vendor/farbtastic/farbtastic.css', 'tethys_gizmos/vendor/farbtastic/farbtastic.js',
            'tethys_gizmos/js/tethys_google_map_view.js')


def google_map(context):
    """
    Dependencies for google_map gizmo.
    """
    return ('tethys_gizmos/js/tethys_map.js', )


def fetchclimate(context):
    """
    Dependencies for fetchclimate gizmo.
    """
    return ('tethys_gizmos/vendor/farbtastic/farbtastic.css', 'tethys_gizmos/vendor/bootstrap_datepicker/css/datepicker3.css',
            'tethys_gizmos/css/fetchclimate/fetchclimate.css', 'tethys_gizmos/css/fetchclimate/fetchclimate_map.css',
            'tethys_gizmos/css/fetchclimate/fetchclimate_plot.css', 'tethys_gizmos/vendor/bootstrap_datepicker/js/bootstrap_datepicker.js',
            'tethys_gizmos/js/fetchclimate/fetchclimate_main.js', 'tethys_gizmos/js/fetchclimate/fetchclimate_date.js',
            'tethys_gizmos/js/fetchclimate/fetchclimate_map.js', 'tethys_gizmos/vendor/highcharts/js/highcharts.js',
            'tethys_gizmos/vendor/highcharts/js/highcharts-more.js', 'tethys_gizmos/js/fetchclimate/fetchclimate_plot.js',
            'tethys_gizmos/js/fetchclimate/fetchclimate_data.js')