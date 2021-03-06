# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyivi\ivic\definesivispecan.py
# Compiled at: 2013-08-15 18:15:02
from ivi_defines import *

def add_props(cls):
    cls._new_attr('cache', IVI_ATTR_CACHE, 'ViBoolean', False, False, False)
    cls._new_attr('range_check', IVI_ATTR_RANGE_CHECK, 'ViBoolean', False, False, False)
    cls._new_attr('query_instrument_status', IVI_ATTR_QUERY_INSTRUMENT_STATUS, 'ViBoolean', False, False, False)
    cls._new_attr('record_coercions', IVI_ATTR_RECORD_COERCIONS, 'ViBoolean', False, False, False)
    cls._new_attr('simulate', IVI_ATTR_SIMULATE, 'ViBoolean', False, False, False)
    cls._new_attr('interchange_check', IVI_ATTR_INTERCHANGE_CHECK, 'ViBoolean', False, False, False)
    cls._new_attr('spy', IVI_ATTR_SPY, 'ViBoolean', False, False, False)
    cls._new_attr('use_specific_simulation', IVI_ATTR_USE_SPECIFIC_SIMULATION, 'ViBoolean', False, False, False)
    cls._new_attr('channel_count', IVI_ATTR_CHANNEL_COUNT, 'ViInt32', False, False, True)
    cls._new_attr('group_capabilities', IVI_ATTR_GROUP_CAPABILITIES, 'ViString', False, False, True)
    cls._new_attr('function_capabilities', IVI_ATTR_FUNCTION_CAPABILITIES, 'ViString', False, False, True)
    cls._new_attr('class_driver_prefix', IVI_ATTR_CLASS_DRIVER_PREFIX, 'ViString', False, False, True)
    cls._new_attr('class_driver_vendor', IVI_ATTR_CLASS_DRIVER_VENDOR, 'ViString', False, False, True)
    cls._new_attr('class_driver_description', IVI_ATTR_CLASS_DRIVER_DESCRIPTION, 'ViString', False, False, True)
    cls._new_attr('class_driver_class_spec_major_version', IVI_ATTR_CLASS_DRIVER_CLASS_SPEC_MAJOR_VERSION, 'ViInt32', False, False, True)
    cls._new_attr('class_driver_class_spec_minor_version', IVI_ATTR_CLASS_DRIVER_CLASS_SPEC_MINOR_VERSION, 'ViInt32', False, False, True)
    cls._new_attr('specific_driver_prefix', IVI_ATTR_SPECIFIC_DRIVER_PREFIX, 'ViString', False, False, True)
    cls._new_attr('specific_driver_locator', IVI_ATTR_SPECIFIC_DRIVER_LOCATOR, 'ViString', False, False, True)
    cls._new_attr('io_resource_descriptor', IVI_ATTR_IO_RESOURCE_DESCRIPTOR, 'ViString', False, False, True)
    cls._new_attr('logical_name', IVI_ATTR_LOGICAL_NAME, 'ViString', False, False, True)
    cls._new_attr('specific_driver_vendor', IVI_ATTR_SPECIFIC_DRIVER_VENDOR, 'ViString', False, False, True)
    cls._new_attr('specific_driver_description', IVI_ATTR_SPECIFIC_DRIVER_DESCRIPTION, 'ViString', False, False, True)
    cls._new_attr('specific_driver_class_spec_major_version', IVI_ATTR_SPECIFIC_DRIVER_CLASS_SPEC_MAJOR_VERSION, 'ViInt32', False, False, True)
    cls._new_attr('specific_driver_class_spec_minor_version', IVI_ATTR_SPECIFIC_DRIVER_CLASS_SPEC_MINOR_VERSION, 'ViInt32', False, False, True)
    cls._new_attr('instrument_firmware_revision', IVI_ATTR_INSTRUMENT_FIRMWARE_REVISION, 'ViString', False, False, True)
    cls._new_attr('instrument_manufacturer', IVI_ATTR_INSTRUMENT_MANUFACTURER, 'ViString', False, False, True)
    cls._new_attr('instrument_model', IVI_ATTR_INSTRUMENT_MODEL, 'ViString', False, False, True)
    cls._new_attr('supported_instrument_models', IVI_ATTR_SUPPORTED_INSTRUMENT_MODELS, 'ViString', False, False, True)
    cls._new_attr('class_driver_revision', IVI_ATTR_CLASS_DRIVER_REVISION, 'ViString', False, False, True)
    cls._new_attr('specific_driver_revision', IVI_ATTR_SPECIFIC_DRIVER_REVISION, 'ViString', False, False, True)
    cls._new_attr('driver_setup', IVI_ATTR_DRIVER_SETUP, 'ViString', False, False, False)
    cls._new_attr('amplitude_units', IVI_CLASS_PUBLIC_ATTR_BASE + 1, 'ViInt32', False, False, False)
    cls._new_attr('attenuation', IVI_CLASS_PUBLIC_ATTR_BASE + 2, 'ViReal64', False, False, False)
    cls._new_attr('attenuation_auto', IVI_CLASS_PUBLIC_ATTR_BASE + 3, 'ViBoolean', False, False, False)
    cls._new_attr('detector_type', IVI_CLASS_PUBLIC_ATTR_BASE + 4, 'ViInt32', False, False, False)
    cls._new_attr('detector_type_auto', IVI_CLASS_PUBLIC_ATTR_BASE + 5, 'ViBoolean', False, False, False)
    cls._new_attr('frequency_start', IVI_CLASS_PUBLIC_ATTR_BASE + 6, 'ViReal64', False, False, False)
    cls._new_attr('frequency_stop', IVI_CLASS_PUBLIC_ATTR_BASE + 7, 'ViReal64', False, False, False)
    cls._new_attr('frequency_offset', IVI_CLASS_PUBLIC_ATTR_BASE + 8, 'ViReal64', False, False, False)
    cls._new_attr('input_impedance', IVI_CLASS_PUBLIC_ATTR_BASE + 9, 'ViReal64', False, False, False)
    cls._new_attr('number_of_sweeps', IVI_CLASS_PUBLIC_ATTR_BASE + 10, 'ViInt32', False, False, False)
    cls._new_attr('reference_level', IVI_CLASS_PUBLIC_ATTR_BASE + 11, 'ViReal64', False, False, False)
    cls._new_attr('reference_level_offset', IVI_CLASS_PUBLIC_ATTR_BASE + 12, 'ViReal64', False, False, False)
    cls._new_attr('resolution_bandwidth', IVI_CLASS_PUBLIC_ATTR_BASE + 13, 'ViReal64', False, False, False)
    cls._new_attr('resolution_bandwidth_auto', IVI_CLASS_PUBLIC_ATTR_BASE + 14, 'ViBoolean', False, False, False)
    cls._new_attr('sweep_mode_continuous', IVI_CLASS_PUBLIC_ATTR_BASE + 15, 'ViBoolean', False, False, False)
    cls._new_attr('sweep_time', IVI_CLASS_PUBLIC_ATTR_BASE + 16, 'ViReal64', False, False, False)
    cls._new_attr('sweep_time_auto', IVI_CLASS_PUBLIC_ATTR_BASE + 17, 'ViBoolean', False, False, False)
    cls._new_attr('trace_count', IVI_CLASS_PUBLIC_ATTR_BASE + 18, 'ViInt32', False, False, False)
    cls._new_attr('trace_size', IVI_CLASS_PUBLIC_ATTR_BASE + 19, 'ViInt32', False, True, False)
    cls._new_attr('trace_type', IVI_CLASS_PUBLIC_ATTR_BASE + 20, 'ViInt32', False, True, False)
    cls._new_attr('vertical_scale', IVI_CLASS_PUBLIC_ATTR_BASE + 21, 'ViInt32', False, False, False)
    cls._new_attr('video_bandwidth', IVI_CLASS_PUBLIC_ATTR_BASE + 22, 'ViReal64', False, False, False)
    cls._new_attr('video_bandwidth_auto', IVI_CLASS_PUBLIC_ATTR_BASE + 23, 'ViBoolean', False, False, False)
    cls._new_attr('active_marker', IVI_CLASS_PUBLIC_ATTR_BASE + 201, 'ViString', False, False, False)
    cls._new_attr('marker_amplitude', IVI_CLASS_PUBLIC_ATTR_BASE + 202, 'ViReal64', False, False, False)
    cls._new_attr('marker_count', IVI_CLASS_PUBLIC_ATTR_BASE + 203, 'ViInt32', False, False, False)
    cls._new_attr('marker_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 204, 'ViBoolean', False, False, False)
    cls._new_attr('marker_frequency_counter_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 205, 'ViBoolean', False, False, False)
    cls._new_attr('marker_frequency_counter_resolution', IVI_CLASS_PUBLIC_ATTR_BASE + 206, 'ViReal64', False, False, False)
    cls._new_attr('marker_position', IVI_CLASS_PUBLIC_ATTR_BASE + 207, 'ViReal64', False, False, False)
    cls._new_attr('marker_threshold', IVI_CLASS_PUBLIC_ATTR_BASE + 208, 'ViReal64', False, False, False)
    cls._new_attr('marker_trace', IVI_CLASS_PUBLIC_ATTR_BASE + 209, 'ViString', False, False, False)
    cls._new_attr('peak_excursion', IVI_CLASS_PUBLIC_ATTR_BASE + 210, 'ViReal64', False, False, False)
    cls._new_attr('signal_track_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 211, 'ViBoolean', False, False, False)
    cls._new_attr('trigger_source', IVI_CLASS_PUBLIC_ATTR_BASE + 301, 'ViInt32', False, False, False)
    cls._new_attr('external_trigger_level', IVI_CLASS_PUBLIC_ATTR_BASE + 401, 'ViReal64', False, False, False)
    cls._new_attr('external_trigger_slope', IVI_CLASS_PUBLIC_ATTR_BASE + 402, 'ViInt32', False, False, False)
    cls._new_attr('video_trigger_level', IVI_CLASS_PUBLIC_ATTR_BASE + 501, 'ViReal64', False, False, False)
    cls._new_attr('video_trigger_slope', IVI_CLASS_PUBLIC_ATTR_BASE + 502, 'ViInt32', False, False, False)
    cls._new_attr('number_of_divisions', IVI_CLASS_PUBLIC_ATTR_BASE + 602, 'ViInt32', False, False, False)
    cls._new_attr('units_per_division', IVI_CLASS_PUBLIC_ATTR_BASE + 601, 'ViReal64', False, False, False)
    cls._new_attr('marker_type', IVI_CLASS_PUBLIC_ATTR_BASE + 701, 'ViInt32', False, False, False)
    cls._new_attr('reference_marker_amplitude', IVI_CLASS_PUBLIC_ATTR_BASE + 801, 'ViReal64', False, False, False)
    cls._new_attr('reference_marker_position', IVI_CLASS_PUBLIC_ATTR_BASE + 802, 'ViReal64', False, False, False)
    cls._new_attr('external_mixer_average_conversion_loss', IVI_CLASS_PUBLIC_ATTR_BASE + 901, 'ViReal64', False, False, False)
    cls._new_attr('external_mixer_bias', IVI_CLASS_PUBLIC_ATTR_BASE + 902, 'ViReal64', False, False, False)
    cls._new_attr('external_mixer_bias_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 903, 'ViBoolean', False, False, False)
    cls._new_attr('external_mixer_bias_limit', IVI_CLASS_PUBLIC_ATTR_BASE + 904, 'ViReal64', False, False, False)
    cls._new_attr('external_mixer_conversion_loss_table_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 905, 'ViBoolean', False, False, False)
    cls._new_attr('external_mixer_enabled', IVI_CLASS_PUBLIC_ATTR_BASE + 906, 'ViBoolean', False, False, False)
    cls._new_attr('external_mixer_harmonic', IVI_CLASS_PUBLIC_ATTR_BASE + 907, 'ViInt32', False, False, False)
    cls._new_attr('external_mixer_number_of_ports', IVI_CLASS_PUBLIC_ATTR_BASE + 908, 'ViInt32', False, False, False)